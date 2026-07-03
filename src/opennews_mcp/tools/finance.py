"""Finance enhancement tools — company reports and on-chain holdings evidence."""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import make_serializable, require_token


def _clamp(value: int, low: int, high: int) -> int:
    return min(max(low, value), high)


@mcp.tool()
async def search_companies(keyword: str, ctx: Context, limit: int = 20, auto_collect: bool = True) -> dict:
    """Search public company candidates by keyword, ticker, CIK, or fuzzy company name.

    Args:
        keyword: Search keyword, ticker, CIK, or company name (e.g. "IBM", "Apple").
        limit: Maximum company candidates to return (default 20, max 100).
        auto_collect: Whether to trigger backend collection and retry when cache is missing.
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    limit = _clamp(limit, 1, 100)
    try:
        result = await api.search_companies(
            keyword=keyword,
            limit=limit,
            auto_collect=auto_collect,
        )
        return make_serializable(result)
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_company_info(
    company: str,
    ctx: Context,
    auto_collect: bool = True,
    filing_limit: int = 300,
    fact_limit: int = 5000,
    include_all_filings: bool = False,
) -> dict:
    """Resolve a company and return available SEC filings, research reports, transcripts, and financial item indexes.

    Args:
        company: Company name, ticker, or CIK (e.g. "IBM", "AAPL", "0000320193").
        auto_collect: Whether to trigger backend collection and retry when cache is missing.
        filing_limit: Number of filings to scan (default 300, max 1000).
        fact_limit: Number of financial facts to scan (default 5000, max 20000).
        include_all_filings: Whether to return all filing forms instead of common report forms only.
    """
    if (err := require_token()):
        return err
    api = ctx.request_context.lifespan_context.api
    filing_limit = _clamp(filing_limit, 1, 1000)
    fact_limit = _clamp(fact_limit, 1, 20000)
    try:
        result = await api.get_company_info(
            company=company,
            auto_collect=auto_collect,
            filing_limit=filing_limit,
            fact_limit=fact_limit,
            include_all_filings=include_all_filings,
        )
        return make_serializable(result)
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_company_report_text(
    company: str,
    report_name: str,
    ctx: Context,
    accession: str = "",
    form_type: str = "",
    section_key: str = "",
    text_search: str = "",
    auto_collect: bool = True,
    max_section_chars: int = 100000,
    filing_search_limit: int = 300,
    section_limit: int = 1000,
) -> dict:
    """Get SEC filing, research report, or earnings-call transcript text by report name or identifier.

    Args:
        company: Company name, ticker, or CIK.
        report_name: Report name, form, accession, research slug, transcript source key, or quarter hint.
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
    api = ctx.request_context.lifespan_context.api
    max_section_chars = _clamp(max_section_chars, 1, 500000)
    filing_search_limit = _clamp(filing_search_limit, 1, 1000)
    section_limit = _clamp(section_limit, 1, 5000)
    try:
        result = await api.get_company_report_text(
            company=company,
            report_name=report_name,
            accession=accession or None,
            form_type=form_type or None,
            section_key=section_key or None,
            text_search=text_search or None,
            auto_collect=auto_collect,
            max_section_chars=max_section_chars,
            filing_search_limit=filing_search_limit,
            section_limit=section_limit,
        )
        return make_serializable(result)
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


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
