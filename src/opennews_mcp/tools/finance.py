"""Finance enhancement tools — company reports and holdings evidence."""

import re
from dataclasses import dataclass
from typing import Literal

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import make_serializable, require_token


def _clamp(value: int, low: int, high: int) -> int:
    return min(max(low, value), high)


def _comma_list(value: str) -> list[str] | None:
    return [item.strip() for item in value.split(",") if item.strip()] or None


IdentifierType = Literal[
    "ticker",
    "cik",
    "krx_stock_code",
    "dart_corp_code",
    "company_name",
    "auto",
]
Market = Literal["US", "KR", "HK", "JP", "CN", "GLOBAL"]
ResultScope = Literal["issuer", "security"]
ReportType = Literal["SEC", "RESEARCH", "TRANSCRIPT", "DART"]
PoliticianChamber = Literal["house", "senate", "all"]
InstitutionStockSort = Literal["value", "shares", "change", "institution"]

_SELECTOR_NAMES = (
    "company",
    "identifier",
    "canonical_issuer_id",
    "ticker",
    "cik",
    "krx_stock_code",
    "dart_corp_code",
)


@dataclass(frozen=True)
class _CompanySelector:
    company: str | None
    identifier: str | None
    identifier_type: IdentifierType
    market: Market


def _selector_error(status: str, message: str) -> dict[str, object]:
    return {
        "success": False,
        "status": status,
        "error": message,
        "accepted_selectors": list(_SELECTOR_NAMES),
        "examples": [
            {"canonical_issuer_id": "SEC:0002120882"},
            {"cik": "0002120882"},
            {"ticker": "SKHY", "market": "US"},
            {"canonical_issuer_id": "DART:00164779"},
            {"krx_stock_code": "000660"},
        ],
    }


def _resolve_company_selector(
    *,
    company: str = "",
    identifier: str = "",
    canonical_issuer_id: str = "",
    ticker: str = "",
    cik: str = "",
    krx_stock_code: str = "",
    dart_corp_code: str = "",
    identifier_type: IdentifierType = "auto",
    market: Market = "GLOBAL",
) -> tuple[_CompanySelector | None, dict[str, object] | None]:
    values = {
        "company": str(company or "").strip(),
        "identifier": str(identifier or "").strip(),
        "canonical_issuer_id": str(canonical_issuer_id or "").strip(),
        "ticker": str(ticker or "").strip(),
        "cik": str(cik or "").strip(),
        "krx_stock_code": str(krx_stock_code or "").strip(),
        "dart_corp_code": str(dart_corp_code or "").strip(),
    }
    provided = [(name, value) for name, value in values.items() if value]
    if not provided:
        return None, _selector_error(
            "invalid_input",
            "Provide exactly one company selector. Use canonical_issuer_id from a prior "
            "search result, a dedicated identifier field, identifier + identifier_type, "
            "or company for fuzzy name discovery.",
        )
    if len(provided) > 1:
        return None, _selector_error(
            "selector_conflict",
            "Provide exactly one company selector; do not combine a fuzzy company name "
            "with ticker, CIK, DART, KRX, identifier, or canonical_issuer_id.",
        )

    selector_name, value = provided[0]
    resolved_type: IdentifierType = identifier_type
    resolved_market: Market = market

    if selector_name == "canonical_issuer_id":
        sec_match = re.fullmatch(r"SEC:(\d{1,10})", value, flags=re.IGNORECASE)
        dart_match = re.fullmatch(r"DART:(\d{8})", value, flags=re.IGNORECASE)
        if sec_match:
            value = sec_match.group(1).zfill(10)
            expected_type: IdentifierType = "cik"
            expected_market: Market = "US"
        elif dart_match:
            value = dart_match.group(1)
            expected_type = "dart_corp_code"
            expected_market = "KR"
        else:
            return None, _selector_error(
                "invalid_input",
                "canonical_issuer_id must use SEC:<1-10 digit CIK> or "
                "DART:<8 digit corp code>.",
            )
        if identifier_type not in ("auto", expected_type) or market not in (
            "GLOBAL",
            expected_market,
        ):
            return None, _selector_error(
                "selector_conflict",
                "canonical_issuer_id conflicts with identifier_type or market.",
            )
        return _CompanySelector(None, value, expected_type, expected_market), None

    dedicated: dict[str, tuple[IdentifierType, Market | None]] = {
        "ticker": ("ticker", None),
        "cik": ("cik", "US"),
        "krx_stock_code": ("krx_stock_code", "KR"),
        "dart_corp_code": ("dart_corp_code", "KR"),
    }
    if selector_name in dedicated:
        expected_type, expected_market = dedicated[selector_name]
        if identifier_type not in ("auto", expected_type):
            return None, _selector_error(
                "selector_conflict",
                f"{selector_name} conflicts with identifier_type={identifier_type}.",
            )
        if expected_market and market not in ("GLOBAL", expected_market):
            return None, _selector_error(
                "selector_conflict",
                f"{selector_name} conflicts with market={market}.",
            )
        if selector_name == "cik":
            if not re.fullmatch(r"\d{1,10}", value):
                return None, _selector_error("invalid_input", "cik must contain 1-10 digits.")
            value = value.zfill(10)
        elif selector_name == "krx_stock_code" and not re.fullmatch(r"\d{6}", value):
            return None, _selector_error(
                "invalid_input", "krx_stock_code must contain exactly 6 digits."
            )
        elif selector_name == "dart_corp_code" and not re.fullmatch(r"\d{8}", value):
            return None, _selector_error(
                "invalid_input", "dart_corp_code must contain exactly 8 digits."
            )
        resolved_type = expected_type
        if expected_market:
            resolved_market = expected_market
        return _CompanySelector(None, value, resolved_type, resolved_market), None

    if selector_name == "identifier":
        return _CompanySelector(None, value, resolved_type, resolved_market), None
    return _CompanySelector(value, None, resolved_type, resolved_market), None


def _candidate_retry(candidate: object) -> dict[str, object] | None:
    if not isinstance(candidate, dict):
        return None
    canonical = str(candidate.get("canonical_issuer_id") or "").strip()
    cik = str(candidate.get("cik") or "").strip()
    dart = str(candidate.get("dart_corp_code") or candidate.get("corp_code") or "").strip()
    krx = str(candidate.get("krx_stock_code") or candidate.get("stock_code") or "").strip()
    ticker = str(candidate.get("ticker") or "").strip()
    identifier = str(candidate.get("identifier") or "").strip()
    identifier_type = str(candidate.get("identifier_type") or "").strip()
    market = str(candidate.get("market") or "GLOBAL").strip() or "GLOBAL"

    if canonical:
        mcp_selector: dict[str, object] = {"canonical_issuer_id": canonical}
    elif cik:
        mcp_selector = {"cik": cik}
    elif dart:
        mcp_selector = {"dart_corp_code": dart}
    elif krx:
        mcp_selector = {"krx_stock_code": krx}
    elif ticker:
        mcp_selector = {"ticker": ticker, "market": market}
    elif identifier and identifier_type in {
        "ticker",
        "cik",
        "krx_stock_code",
        "dart_corp_code",
    }:
        mcp_selector = {identifier_type: identifier}
        if identifier_type == "ticker":
            mcp_selector["market"] = market
    else:
        return None

    if cik:
        http_selector = {"identifier": cik, "identifier_type": "cik", "market": "US"}
    elif dart:
        http_selector = {
            "identifier": dart,
            "identifier_type": "dart_corp_code",
            "market": "KR",
        }
    elif krx:
        http_selector = {
            "identifier": krx,
            "identifier_type": "krx_stock_code",
            "market": "KR",
        }
    elif ticker:
        http_selector = {"identifier": ticker, "identifier_type": "ticker", "market": market}
    elif identifier and identifier_type:
        http_selector = {
            "identifier": identifier,
            "identifier_type": identifier_type,
            "market": market,
        }
    else:
        return None
    return {
        "issuer_name": candidate.get("issuer_name") or candidate.get("company_name"),
        "canonical_issuer_id": canonical or None,
        "mcp_selector": mcp_selector,
        "http_selector": http_selector,
    }


def _with_resolution_hint(result: object) -> object:
    if not isinstance(result, dict):
        return result
    payload = result.get("data") if isinstance(result.get("data"), dict) else result
    if not isinstance(payload, dict):
        return result
    company = payload.get("company") if isinstance(payload.get("company"), dict) else {}
    status = payload.get("status") or company.get("status")
    if status != "ambiguous_entity":
        return result
    candidates = payload.get("ambiguity_candidates") or company.get("ambiguity_candidates") or []
    retries = [retry for row in candidates if (retry := _candidate_retry(row)) is not None]
    payload["resolution_hint"] = {
        "message": "Choose one candidate, then retry with exactly one MCP selector. "
        "Raw HTTP callers must use identifier + identifier_type + market.",
        "retry_candidates": retries,
    }
    return result


def _upstream_error(error: Exception) -> dict[str, object]:
    return {
        "success": False,
        "status": "upstream_error",
        "error": str(error) or repr(error),
    }


@mcp.tool()
async def search_companies(
    ctx: Context,
    keyword: str = "",
    identifier: str = "",
    canonical_issuer_id: str = "",
    ticker: str = "",
    cik: str = "",
    krx_stock_code: str = "",
    dart_corp_code: str = "",
    identifier_type: IdentifierType = "auto",
    market: Market = "GLOBAL",
    exchange: str = "",
    result_scope: ResultScope = "issuer",
    limit: int = 20,
    auto_collect: bool = True,
) -> dict:
    """Resolve an exact identifier or return explicit company ambiguity candidates.

    Args:
        keyword: Legacy fuzzy company-name query. Do not combine with another selector.
        identifier: Typed identifier used with identifier_type and market.
        canonical_issuer_id: Stable ID returned by search, such as SEC:0002120882 or DART:00164779.
        ticker: Exact ticker convenience selector, such as SKHY.
        cik: Exact SEC CIK convenience selector; 1-10 digits are normalized to 10 digits.
        krx_stock_code: Exact six-digit KRX security code, such as 000660.
        dart_corp_code: Exact eight-digit DART issuer code, such as 00164779.
        identifier_type: ticker, cik, krx_stock_code, dart_corp_code, company_name, or auto.
        market: US, KR, HK, JP, CN, or GLOBAL.
        exchange: Optional exchange constraint.
        result_scope: issuer or security.
        limit: Maximum company candidates to return (default 20, max 100).
        auto_collect: Whether to trigger backend collection and retry when cache is missing.
    """
    if (err := require_token()):
        return err
    selector, selector_error = _resolve_company_selector(
        company=keyword,
        identifier=identifier,
        canonical_issuer_id=canonical_issuer_id,
        ticker=ticker,
        cik=cik,
        krx_stock_code=krx_stock_code,
        dart_corp_code=dart_corp_code,
        identifier_type=identifier_type,
        market=market,
    )
    if selector_error:
        return selector_error
    assert selector is not None
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 100)
    try:
        result = await api.search_companies(
            keyword=selector.company or "",
            identifier=selector.identifier,
            identifier_type=selector.identifier_type,
            market=selector.market,
            exchange=exchange or None,
            result_scope=result_scope,
            limit=limit,
            auto_collect=auto_collect,
        )
        return make_serializable(_with_resolution_hint(result))
    except Exception as e:
        return _upstream_error(e)


@mcp.tool()
async def get_company_info(
    ctx: Context,
    company: str = "",
    identifier: str = "",
    canonical_issuer_id: str = "",
    ticker: str = "",
    cik: str = "",
    krx_stock_code: str = "",
    dart_corp_code: str = "",
    identifier_type: IdentifierType = "auto",
    market: Market = "GLOBAL",
    exchange: str = "",
    result_scope: ResultScope = "issuer",
    auto_collect: bool = True,
    filing_limit: int = 300,
    fact_limit: int = 5000,
    include_all_filings: bool = False,
) -> dict:
    """Resolve one exact issuer and return its report and financial-item catalog.

    Args:
        company: Legacy name/ticker/CIK input. Prefer an exact selector after search.
        identifier: Typed identifier used with identifier_type and market.
        canonical_issuer_id: Stable ID returned by search, such as SEC:0002120882 or DART:00164779.
        ticker: Exact ticker convenience selector.
        cik: Exact SEC CIK convenience selector.
        krx_stock_code: Exact six-digit KRX security code.
        dart_corp_code: Exact eight-digit DART issuer code.
        identifier_type: ticker, cik, krx_stock_code, dart_corp_code, company_name, or auto.
        market: US, KR, HK, JP, CN, or GLOBAL.
        exchange: Optional exchange constraint.
        result_scope: issuer or security.
        auto_collect: Whether to trigger backend collection and retry when cache is missing.
        filing_limit: Number of filings to scan (default 300, max 1000).
        fact_limit: Number of financial facts to scan (default 5000, max 20000).
        include_all_filings: Whether to return all filing forms instead of common report forms only.
    """
    if (err := require_token()):
        return err
    selector, selector_error = _resolve_company_selector(
        company=company,
        identifier=identifier,
        canonical_issuer_id=canonical_issuer_id,
        ticker=ticker,
        cik=cik,
        krx_stock_code=krx_stock_code,
        dart_corp_code=dart_corp_code,
        identifier_type=identifier_type,
        market=market,
    )
    if selector_error:
        return selector_error
    assert selector is not None
    api = ctx.request_context.lifespan_context.api
    filing_limit = _clamp(filing_limit, 1, 1000)
    fact_limit = _clamp(fact_limit, 1, 20000)
    try:
        result = await api.get_company_info(
            company=selector.company or "",
            identifier=selector.identifier,
            identifier_type=selector.identifier_type,
            market=selector.market,
            exchange=exchange or None,
            result_scope=result_scope,
            auto_collect=auto_collect,
            filing_limit=filing_limit,
            fact_limit=fact_limit,
            include_all_filings=include_all_filings,
        )
        return make_serializable(_with_resolution_hint(result))
    except Exception as e:
        return _upstream_error(e)


@mcp.tool()
async def get_company_report_text(
    ctx: Context,
    company: str = "",
    identifier: str = "",
    canonical_issuer_id: str = "",
    ticker: str = "",
    cik: str = "",
    krx_stock_code: str = "",
    dart_corp_code: str = "",
    identifier_type: IdentifierType = "auto",
    market: Market = "GLOBAL",
    exchange: str = "",
    report_name: str = "",
    report_id: str = "",
    report_type: ReportType | None = None,
    accession: str = "",
    form_type: str = "",
    section_key: str = "",
    text_search: str = "",
    auto_collect: bool = True,
    max_section_chars: int = 100000,
    filing_search_limit: int = 300,
    section_limit: int = 1000,
) -> dict:
    """Read one issuer-bound report using an exact company selector and stable report ID.

    Args:
        company: Legacy name/ticker/CIK input. Prefer an exact selector after search.
        identifier: Typed identifier used with identifier_type and market.
        canonical_issuer_id: Stable ID returned by search, such as SEC:0002120882 or DART:00164779.
        ticker: Exact ticker convenience selector.
        cik: Exact SEC CIK convenience selector.
        krx_stock_code: Exact six-digit KRX security code.
        dart_corp_code: Exact eight-digit DART issuer code.
        identifier_type: ticker, cik, krx_stock_code, dart_corp_code, company_name, or auto.
        market: US, KR, HK, JP, CN, or GLOBAL.
        exchange: Optional exchange constraint.
        report_name: Optional legacy display/form lookup.
        report_id: Stable SEC accession, research slug, transcript source key, or DART rcept_no.
        report_type: SEC, RESEARCH, TRANSCRIPT, or DART.
        accession: Optional SEC accession, research-report identifier, or transcript identifier.
        form_type: Optional SEC form type such as "10-K", "10-Q", or "8-K".
        section_key: Optional section key to fetch a specific section.
        text_search: Optional keyword to search within report text.
        auto_collect: Whether to trigger backend collection and retry when cache is missing.
        max_section_chars: Maximum characters per section (default 100000).
        filing_search_limit: Candidate filing search limit (default 300).
        section_limit: Maximum returned sections (default 1000).
    """
    if (err := require_token()):
        return err
    selector, selector_error = _resolve_company_selector(
        company=company,
        identifier=identifier,
        canonical_issuer_id=canonical_issuer_id,
        ticker=ticker,
        cik=cik,
        krx_stock_code=krx_stock_code,
        dart_corp_code=dart_corp_code,
        identifier_type=identifier_type,
        market=market,
    )
    if selector_error:
        return selector_error
    assert selector is not None
    api = ctx.request_context.lifespan_context.api
    max_section_chars = _clamp(max_section_chars, 1, 500000)
    filing_search_limit = _clamp(filing_search_limit, 1, 1000)
    section_limit = _clamp(section_limit, 1, 5000)
    try:
        result = await api.get_company_report_text(
            company=selector.company or "",
            identifier=selector.identifier,
            identifier_type=selector.identifier_type,
            market=selector.market,
            exchange=exchange or None,
            report_name=report_name,
            report_id=report_id or None,
            report_type=report_type,
            accession=accession or None,
            form_type=form_type or None,
            section_key=section_key or None,
            text_search=text_search or None,
            auto_collect=auto_collect,
            max_section_chars=max_section_chars,
            filing_search_limit=filing_search_limit,
            section_limit=section_limit,
        )
        return make_serializable(_with_resolution_hint(result))
    except Exception as e:
        return _upstream_error(e)


@mcp.tool()
async def get_key_market_events(
    ctx: Context,
    start_date: str = "",
    end_date: str = "",
    categories: str = "",
    countries: str = "",
    event_types: str = "",
    tickers: str = "",
    sector: str = "",
    importance: str = "",
    include_estimated: bool = True,
    text_search: str = "",
    auto_collect: bool = True,
    force_collect: bool = False,
    lookahead_days: int = 0,
    earnings_batch_size: int = 0,
    limit: int = 100,
) -> dict:
    """Query important macro and focus-company earnings event dates.

    Returns Fed/BOJ policy dates, US CPI/PPI/nonfarm payroll releases, and
    configured focus-company earnings events. Rows marked estimated_schedule
    should be confirmed against official calendars before alerting or trading.

    Args:
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        categories: Optional comma-separated categories, such as "central_bank,earnings".
        countries: Optional comma-separated countries or regions, such as "US,JP".
        event_types: Optional comma-separated event types, such as "fomc_rate_decision,company_earnings".
        tickers: Optional comma-separated company tickers, such as "ARM,NVDA".
        sector: Optional sector filter.
        importance: Optional importance filter, such as "high".
        include_estimated: Whether to include estimated fallback schedule rows.
        text_search: Optional keyword filter.
        auto_collect: Whether to trigger backend key-events collection on cache miss.
        force_collect: Whether to force collection before reading cache.
        lookahead_days: Optional collection lookahead window; 0 means backend default.
        earnings_batch_size: Optional earnings collection batch size; 0 means backend default.
        limit: Maximum event rows to return (default 100, max 500).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 500)
    try:
        result = await api.get_key_market_events(
            start_date=start_date or None,
            end_date=end_date or None,
            categories=_comma_list(categories),
            countries=_comma_list(countries),
            event_types=_comma_list(event_types),
            tickers=_comma_list(tickers),
            sector=sector or None,
            importance=importance or None,
            include_estimated=include_estimated,
            text_search=text_search or None,
            auto_collect=auto_collect,
            force_collect=force_collect,
            lookahead_days=lookahead_days if lookahead_days > 0 else None,
            earnings_batch_size=earnings_batch_size if earnings_batch_size > 0 else None,
            limit=limit,
        )
        return make_serializable(result)
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_politician_stock_activity(
    ctx: Context,
    chamber: PoliticianChamber = "house",
    source_year: int = 0,
    doc_id: str = "",
    ticker: str = "",
    politician: str = "",
    state_district: str = "",
    transaction_codes: str = "",
    owner_codes: str = "",
    start_date: str = "",
    end_date: str = "",
    min_amount: float = -1,
    max_amount: float = -1,
    auto_collect: bool = False,
    force_collect: bool = False,
    collect_max_pdfs: int = 0,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Query official U.S. House PTR stock transaction disclosures.

    Returns public transaction disclosure evidence and amount buckets. It is not
    current holdings, exact trade value, cost basis, profit, or investment advice.

    Args:
        chamber: Disclosure chamber. Only house is currently supported; senate/all return a boundary message.
        source_year: Optional House disclosure year; 0 means backend default.
        doc_id: Optional House PTR PDF document ID.
        ticker: Optional stock ticker filter.
        politician: Optional filer name filter.
        state_district: Optional district filter, such as CA12.
        transaction_codes: Optional comma-separated codes: P, S, E.
        owner_codes: Optional comma-separated owner codes: SP, DC, JT.
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.
        min_amount: Optional disclosed amount bucket lower bound; negative means unset.
        max_amount: Optional disclosed amount bucket upper bound; negative means unset.
        auto_collect: Whether to trigger bounded House PTR collection when cache is missing.
        force_collect: Whether to force collection.
        collect_max_pdfs: Optional PDF collection cap; 0 means backend default.
        limit: Maximum returned transaction rows (default 100, max 500).
        offset: Pagination offset.
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 500)
    try:
        result = await api.get_politician_stock_activity(
            chamber=chamber,
            source_year=source_year if source_year > 0 else None,
            doc_id=doc_id or None,
            ticker=ticker or None,
            politician=politician or None,
            state_district=state_district or None,
            transaction_codes=_comma_list(transaction_codes),
            owner_codes=_comma_list(owner_codes),
            start_date=start_date or None,
            end_date=end_date or None,
            min_amount=min_amount if min_amount >= 0 else None,
            max_amount=max_amount if max_amount >= 0 else None,
            auto_collect=auto_collect,
            force_collect=force_collect,
            collect_max_pdfs=(
                _clamp(collect_max_pdfs, 1, 250) if collect_max_pdfs > 0 else None
            ),
            limit=limit,
            offset=max(0, int(offset)),
        )
        return make_serializable(result)
    except Exception as e:
        return _upstream_error(e)


@mcp.tool()
async def get_institution_stock_holdings(
    ctx: Context,
    institution: str = "",
    as_of: str = "",
    changed_only: bool = False,
    include_options: bool = False,
    include_exited: bool = False,
    sort_by: InstitutionStockSort = "value",
    auto_collect: bool = True,
    force_collect: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Query SEC Form 13F institution stock holding disclosures.

    Returns one manager's latest quarter-end 13F evidence from the staged manager
    universe. It is delayed filing evidence, not real-time ownership or complete
    economic exposure. Use list_institution_managers first when the manager CIK
    or exact staged manager name is unknown.

    Args:
        institution: Required staged manager name or exact SEC manager CIK.
        as_of: Optional report-period cutoff in YYYY-MM-DD format.
        changed_only: Whether to exclude unchanged positions.
        include_options: Whether to include put/call option rows.
        include_exited: Whether to include exited positions.
        sort_by: value, shares, change, or institution.
        auto_collect: Whether Finance Enhance should check and refresh the resolved
            manager within its SEC refresh TTL.
        force_collect: Compatibility flag; the backend still honors its SEC refresh TTL.
        limit: Maximum returned holding rows (default 100, max 500).
        offset: Pagination offset.
    """
    if (err := require_token()):
        return err
    if not institution.strip():
        return {
            "success": False,
            "status": "invalid_input",
            "error": "institution is required. Use list_institution_managers to find a manager CIK.",
        }
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 500)
    try:
        result = await api.get_institution_stock_holdings(
            institution=institution,
            as_of=as_of or None,
            changed_only=changed_only,
            include_options=include_options,
            include_exited=include_exited,
            sort_by=sort_by,
            auto_collect=auto_collect,
            force_collect=force_collect,
            limit=limit,
            offset=max(0, int(offset)),
        )
        return make_serializable(result)
    except Exception as e:
        return _upstream_error(e)


@mcp.tool()
async def list_institution_managers(
    ctx: Context,
    search: str = "",
    as_of: str = "",
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """List staged SEC Form 13F managers without returning holdings.

    Use this first when a user gives a fuzzy institution name. The response
    includes manager CIKs and filing coverage metadata; pass one returned
    manager CIK or exact name to get_institution_stock_holdings for positions.

    Args:
        search: Optional institution name or exact SEC manager CIK filter.
        as_of: Optional filing/report-period cutoff in YYYY-MM-DD format.
        limit: Maximum returned manager rows (default 100, max 500).
        offset: Pagination offset.
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 500)
    try:
        result = await api.list_institution_managers(
            search=search or None,
            as_of=as_of or None,
            limit=limit,
            offset=max(0, int(offset)),
        )
        return make_serializable(result)
    except Exception as e:
        return _upstream_error(e)


@mcp.tool()
async def get_crypto_holdings(
    ctx: Context,
    institution: str = "",
    address: str = "",
    chain: str = "",
    token_symbol: str = "",
    token_address: str = "",
    as_of: str = "",
    auto_collect: bool = True,
    force_collect: bool = False,
    collect_max_rows: int = 0,
    limit: int = 100,
) -> dict:
    """Query visible on-chain holdings evidence for an institution or wallet address.

    Returns Blockscout address-balance evidence. This is not proof of economic ownership,
    beneficial ownership, investment advice, or a trading signal.

    Args:
        institution: Optional institution name for watchlist matching or result labeling.
        address: Optional wallet address. If address is provided without chain, backend defaults to ethereum.
        chain: Optional chain name.
        token_symbol: Optional token symbol filter, such as "ETH" or "USDC".
        token_address: Optional token contract address filter.
        as_of: Optional date or snapshot-time filter.
        auto_collect: Whether to collect address balances when cache is missing.
        force_collect: Whether to force a fresh address-balance collection.
        collect_max_rows: Optional collection row cap; 0 means backend default.
        limit: Maximum holdings rows to return (default 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 1000)
    collect_rows = _clamp(collect_max_rows, 1, 10000) if collect_max_rows > 0 else None
    try:
        result = await api.get_crypto_holdings(
            institution=institution or None,
            address=address or None,
            chain=chain or None,
            token_symbol=token_symbol or None,
            token_address=token_address or None,
            as_of=as_of or None,
            auto_collect=auto_collect,
            force_collect=force_collect,
            collect_max_rows=collect_rows,
            limit=limit,
        )
        return make_serializable(result)
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_crypto_holding_changes(
    ctx: Context,
    institution: str = "",
    address: str = "",
    chain: str = "",
    token_symbol: str = "",
    token_address: str = "",
    change_types: str = "",
    start_date: str = "",
    end_date: str = "",
    include_unchanged: bool = False,
    auto_collect: bool = False,
    force_collect: bool = False,
    collect_max_rows: int = 0,
    limit: int = 100,
) -> dict:
    """Query on-chain holdings changes between adjacent wallet snapshots.

    Args:
        institution: Optional institution name.
        address: Optional wallet address. At least two snapshots are needed for changed records.
        chain: Optional chain name.
        token_symbol: Optional token symbol filter.
        token_address: Optional token contract address filter.
        change_types: Optional comma-separated filters, such as "increase,decrease".
        start_date: Optional start date filter.
        end_date: Optional end date filter.
        include_unchanged: Whether to include unchanged rows.
        auto_collect: Whether to collect address balances when cache is missing.
            Defaults to false because address-only change queries can fail in the backend
            auto-collection path; collect holdings first when a fresh snapshot is needed.
        force_collect: Whether to force a fresh address-balance collection.
        collect_max_rows: Optional collection row cap; 0 means backend default.
        limit: Maximum change rows to return (default 100).
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 1000)
    collect_rows = _clamp(collect_max_rows, 1, 10000) if collect_max_rows > 0 else None
    change_type_list = [item.strip() for item in change_types.split(",") if item.strip()] or None
    try:
        result = await api.get_crypto_holding_changes(
            institution=institution or None,
            address=address or None,
            chain=chain or None,
            token_symbol=token_symbol or None,
            token_address=token_address or None,
            change_types=change_type_list,
            start_date=start_date or None,
            end_date=end_date or None,
            include_unchanged=include_unchanged,
            auto_collect=auto_collect,
            force_collect=force_collect,
            collect_max_rows=collect_rows,
            limit=limit,
        )
        return make_serializable(result)
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
