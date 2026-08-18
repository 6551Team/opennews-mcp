"""HTTP/WebSocket client for the 6551 news platform API."""

import asyncio
import json
import logging
import time
from typing import Any, Optional

import httpx

from opennews_mcp.config import API_BASE_URL, API_TOKEN, WSS_URL

logger = logging.getLogger(__name__)

MAX_RETRIES = 2


class FreeNewsAPIClient:
    """Async HTTP client for free (no-auth) 6551 news API endpoints."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))
        return self._client

    async def _reset_client(self):
        """Force close and recreate the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        self._client = None

    async def close(self):
        await self._reset_client()

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Execute an HTTP request with automatic retry on connection errors."""
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                client = await self._get_client()
                resp = await client.request(method, url, **kwargs)
                resp.raise_for_status()
                return resp
            except (httpx.ConnectError, httpx.RemoteProtocolError) as e:
                last_exc = e
                logger.warning(
                    "Connection error (attempt %d/%d): %s",
                    attempt + 1, MAX_RETRIES + 1, repr(e),
                )
                await self._reset_client()
            except httpx.HTTPStatusError:
                raise
        raise last_exc  # type: ignore[misc]

    async def get_free_categories(self) -> dict:
        """GET /open/free_categories — 获取所有新闻分类"""
        resp = await self._request("GET", f"{self.base_url}/open/free_categories")
        return resp.json()

    async def get_free_hot(
        self,
        category: str,
        subcategory: str = "",
    ) -> dict:
        """GET /open/free_hot — 获取热点新闻和推文"""
        params: dict = {"category": category}
        if subcategory:
            params["subcategory"] = subcategory
        resp = await self._request("GET", f"{self.base_url}/open/free_hot", params=params)
        return resp.json()


class NewsAPIClient:
    """Async HTTP client for the 6551 news REST API."""

    def __init__(self, base_url: str = API_BASE_URL, token: str = API_TOKEN):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._client: Optional[httpx.AsyncClient] = None

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers=self._headers(),
            )
        return self._client

    async def _reset_client(self):
        """Force close and recreate the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        self._client = None

    async def close(self):
        await self._reset_client()

    # ---------- internal request with retry ----------

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Execute an HTTP request with automatic retry on connection errors."""
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                client = await self._get_client()
                resp = await client.request(method, url, **kwargs)
                resp.raise_for_status()
                return resp
            except (httpx.ConnectError, httpx.RemoteProtocolError) as e:
                last_exc = e
                logger.warning(
                    "Connection error (attempt %d/%d): %s",
                    attempt + 1, MAX_RETRIES + 1, repr(e),
                )
                await self._reset_client()
            except httpx.HTTPStatusError:
                raise
        raise last_exc  # type: ignore[misc]

    # ---------- REST endpoints ----------

    async def get_engine_tree(self) -> dict:
        """GET /open/news_type — 获取所有新闻源分类"""
        resp = await self._request("GET", f"{self.base_url}/open/news_type")
        return resp.json()

    async def search_news(
        self,
        coins: Optional[list[str]] = None,
        query: Optional[str] = None,
        engine_types: Optional[dict[str, list[str]]] = None,
        has_coin: bool = False,
        score: Optional[int] = None,
        limit: int = 20,
        page: int = 1,
    ) -> dict:
        """POST /open/news_search — 搜索新闻文章"""
        body: dict[str, Any] = {"limit": limit, "page": page}
        if coins:
            body["coins"] = coins
        if query:
            body["q"] = query
        if engine_types:
            body["engineTypes"] = engine_types
        if has_coin:
            body["hasCoin"] = has_coin
        if score is not None:
            body["score"] = score

        resp = await self._request("POST", f"{self.base_url}/open/news_search", json=body)
        return resp.json()

    async def get_strategy_list(self, limit: int = 20, page: int = 1) -> dict:
        """GET /open/strategy_list — get user strategy list."""
        params: dict[str, Any] = {"limit": limit, "page": page}
        resp = await self._request("GET", f"{self.base_url}/open/strategy_list", params=params)
        return resp.json()

    async def get_strategy_hits(self, strategy_id: int, limit: int = 20, page: int = 1) -> dict:
        """GET /open/strategy_hits — get triggered events for a user strategy."""
        params: dict[str, Any] = {
            "strategyId": strategy_id,
            "limit": limit,
            "page": page,
        }
        resp = await self._request("GET", f"{self.base_url}/open/strategy_hits", params=params)
        return resp.json()

    async def search_companies(
        self,
        keyword: str = "",
        identifier: Optional[str] = None,
        identifier_type: str = "auto",
        market: str = "GLOBAL",
        exchange: Optional[str] = None,
        result_scope: str = "issuer",
        limit: int = 20,
        auto_collect: bool = True,
    ) -> dict:
        """POST /open/finance-enhance/company-search — search public company candidates."""
        body: dict[str, Any] = {
            "identifier_type": identifier_type,
            "market": market,
            "result_scope": result_scope,
            "limit": limit,
            "auto_collect": auto_collect,
        }
        optional_fields = {
            "keyword": keyword,
            "identifier": identifier,
            "exchange": exchange,
        }
        body.update({key: value for key, value in optional_fields.items() if value})
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/company-search",
            json=body,
        )
        return resp.json()

    async def get_company_info(
        self,
        company: str = "",
        identifier: Optional[str] = None,
        identifier_type: str = "auto",
        market: str = "GLOBAL",
        exchange: Optional[str] = None,
        result_scope: str = "issuer",
        auto_collect: bool = True,
        filing_limit: int = 300,
        fact_limit: int = 5000,
        include_all_filings: bool = False,
    ) -> dict:
        """POST /open/finance-enhance/company-info — get company metadata and report indexes."""
        body: dict[str, Any] = {
            "identifier_type": identifier_type,
            "market": market,
            "result_scope": result_scope,
            "auto_collect": auto_collect,
            "filing_limit": filing_limit,
            "fact_limit": fact_limit,
            "include_all_filings": include_all_filings,
        }
        optional_fields = {
            "company": company,
            "identifier": identifier,
            "exchange": exchange,
        }
        body.update({key: value for key, value in optional_fields.items() if value})
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/company-info",
            json=body,
        )
        return resp.json()

    async def get_company_report_text(
        self,
        company: str = "",
        identifier: Optional[str] = None,
        identifier_type: str = "auto",
        market: str = "GLOBAL",
        exchange: Optional[str] = None,
        report_name: str = "",
        report_id: Optional[str] = None,
        report_type: Optional[str] = None,
        accession: Optional[str] = None,
        form_type: Optional[str] = None,
        section_key: Optional[str] = None,
        text_search: Optional[str] = None,
        auto_collect: bool = True,
        max_section_chars: int = 100000,
        filing_search_limit: int = 300,
        section_limit: int = 1000,
    ) -> dict:
        """POST /open/finance-enhance/company-report-text — get filing/report/transcript text."""
        body: dict[str, Any] = {
            "identifier_type": identifier_type,
            "market": market,
            "auto_collect": auto_collect,
            "max_section_chars": max_section_chars,
            "filing_search_limit": filing_search_limit,
            "section_limit": section_limit,
        }
        optional_fields = {
            "company": company,
            "identifier": identifier,
            "exchange": exchange,
            "report_name": report_name,
            "report_id": report_id,
            "report_type": report_type,
            "accession": accession,
            "form_type": form_type,
            "section_key": section_key,
            "text_search": text_search,
        }
        body.update({key: value for key, value in optional_fields.items() if value})
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/company-report-text",
            json=body,
        )
        return resp.json()

    async def get_key_market_events(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        categories: Optional[list[str]] = None,
        countries: Optional[list[str]] = None,
        event_types: Optional[list[str]] = None,
        tickers: Optional[list[str]] = None,
        sector: Optional[str] = None,
        importance: Optional[str] = None,
        include_estimated: bool = True,
        text_search: Optional[str] = None,
        auto_collect: bool = True,
        force_collect: bool = False,
        lookahead_days: Optional[int] = None,
        earnings_batch_size: Optional[int] = None,
        limit: int = 100,
    ) -> dict:
        """POST /open/finance-enhance/key-market-events — get macro and focus-company events."""
        body: dict[str, Any] = {
            "include_estimated": include_estimated,
            "auto_collect": auto_collect,
            "force_collect": force_collect,
            "limit": limit,
        }
        optional_fields = {
            "start_date": start_date,
            "end_date": end_date,
            "categories": categories,
            "countries": countries,
            "event_types": event_types,
            "tickers": tickers,
            "sector": sector,
            "importance": importance,
            "text_search": text_search,
            "lookahead_days": lookahead_days,
            "earnings_batch_size": earnings_batch_size,
        }
        body.update({
            key: value for key, value in optional_fields.items()
            if value is not None and value != "" and value != []
        })
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/key-market-events",
            json=body,
        )
        return resp.json()

    async def get_politician_stock_activity(
        self,
        chamber: str = "house",
        source_year: Optional[int] = None,
        doc_id: Optional[str] = None,
        ticker: Optional[str] = None,
        politician: Optional[str] = None,
        state_district: Optional[str] = None,
        transaction_codes: Optional[list[str]] = None,
        owner_codes: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        auto_collect: bool = False,
        force_collect: bool = False,
        collect_max_pdfs: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """POST /open/finance-enhance/politician-stock-activity — get House PTR disclosures."""
        body: dict[str, Any] = {
            "chamber": chamber,
            "auto_collect": auto_collect,
            "force_collect": force_collect,
            "limit": limit,
            "offset": offset,
        }
        optional_fields = {
            "source_year": source_year,
            "doc_id": doc_id,
            "ticker": ticker,
            "politician": politician,
            "state_district": state_district,
            "transaction_codes": transaction_codes,
            "owner_codes": owner_codes,
            "start_date": start_date,
            "end_date": end_date,
            "min_amount": min_amount,
            "max_amount": max_amount,
            "collect_max_pdfs": collect_max_pdfs,
        }
        body.update({
            key: value for key, value in optional_fields.items()
            if value is not None and value != "" and value != []
        })
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/politician-stock-activity",
            json=body,
        )
        return resp.json()

    async def get_institution_stock_holdings(
        self,
        institution: str,
        as_of: Optional[str] = None,
        changed_only: bool = False,
        include_options: bool = False,
        include_exited: bool = False,
        sort_by: str = "value",
        auto_collect: bool = True,
        force_collect: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """POST /open/finance-enhance/institution-stock-holdings — get SEC 13F evidence."""
        body: dict[str, Any] = {
            "changed_only": changed_only,
            "include_options": include_options,
            "include_exited": include_exited,
            "sort_by": sort_by,
            "auto_collect": auto_collect,
            "force_collect": force_collect,
            "limit": limit,
            "offset": offset,
        }
        optional_fields = {
            "institution": institution,
            "as_of": as_of,
        }
        body.update({
            key: value for key, value in optional_fields.items()
            if value is not None and value != ""
        })
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/institution-stock-holdings",
            json=body,
        )
        return resp.json()

    async def list_institution_managers(
        self,
        search: Optional[str] = None,
        as_of: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """POST /open/finance-enhance/institution-managers — list SEC 13F managers."""
        body: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }
        optional_fields = {
            "search": search,
            "as_of": as_of,
        }
        body.update({
            key: value for key, value in optional_fields.items()
            if value is not None and value != ""
        })
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/institution-managers",
            json=body,
        )
        return resp.json()

    async def get_crypto_holdings(
        self,
        institution: Optional[str] = None,
        address: Optional[str] = None,
        chain: Optional[str] = None,
        token_symbol: Optional[str] = None,
        token_address: Optional[str] = None,
        as_of: Optional[str] = None,
        auto_collect: bool = True,
        force_collect: bool = False,
        collect_max_rows: Optional[int] = None,
        limit: int = 100,
    ) -> dict:
        """POST /open/finance-enhance/crypto-holdings — get on-chain holdings evidence."""
        body: dict[str, Any] = {
            "auto_collect": auto_collect,
            "force_collect": force_collect,
            "limit": limit,
        }
        optional_fields = {
            "institution": institution,
            "address": address,
            "chain": chain,
            "token_symbol": token_symbol,
            "token_address": token_address,
            "as_of": as_of,
            "collect_max_rows": collect_max_rows,
        }
        body.update({
            key: value for key, value in optional_fields.items()
            if value is not None and value != ""
        })
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/crypto-holdings",
            json=body,
        )
        return resp.json()

    async def get_crypto_holding_changes(
        self,
        institution: Optional[str] = None,
        address: Optional[str] = None,
        chain: Optional[str] = None,
        token_symbol: Optional[str] = None,
        token_address: Optional[str] = None,
        change_types: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        include_unchanged: bool = False,
        auto_collect: bool = False,
        force_collect: bool = False,
        collect_max_rows: Optional[int] = None,
        limit: int = 100,
    ) -> dict:
        """POST /open/finance-enhance/crypto-holding-changes — get holdings changes."""
        body: dict[str, Any] = {
            "include_unchanged": include_unchanged,
            "auto_collect": auto_collect,
            "force_collect": force_collect,
            "limit": limit,
        }
        optional_fields = {
            "institution": institution,
            "address": address,
            "chain": chain,
            "token_symbol": token_symbol,
            "token_address": token_address,
            "change_types": change_types,
            "start_date": start_date,
            "end_date": end_date,
            "collect_max_rows": collect_max_rows,
        }
        body.update({
            key: value for key, value in optional_fields.items()
            if value is not None and value != "" and value != []
        })
        resp = await self._request(
            "POST",
            f"{self.base_url}/open/finance-enhance/crypto-holding-changes",
            json=body,
        )
        return resp.json()



class NewsWSClient:
    """WebSocket client for real-time news subscription."""

    def __init__(self, wss_url: str = WSS_URL, token: str = API_TOKEN):
        self.wss_url = f"{wss_url}?token={token}"
        self._ws = None
        self._request_id = 0

    def _next_id(self) -> str:
        self._request_id += 1
        return f"req_{self._request_id}_{int(time.time())}"

    async def connect(self):
        import websockets
        self._ws = await websockets.connect(self.wss_url)

    async def close(self):
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def subscribe_latest(
        self,
        engine_types: Optional[dict[str, list[str]]] = None,
        coins: Optional[list[str]] = None,
        has_coin: bool = False,
    ) -> dict:
        """订阅新闻推送，支持过滤器"""
        if not self._ws:
            await self.connect()
        req_id = self._next_id()
        params: dict[str, Any] = {}
        if engine_types:
            params["engineTypes"] = engine_types
        if coins:
            params["coins"] = coins
        if has_coin:
            params["hasCoin"] = has_coin
        msg = {"method": "news.subscribe", "id": req_id, "params": params}
        await self._ws.send(json.dumps(msg))
        resp = await self._ws.recv()
        return json.loads(resp)

    async def receive_news(self, timeout: float = 10.0) -> Optional[dict]:
        if not self._ws:
            return None
        try:
            msg = await asyncio.wait_for(self._ws.recv(), timeout=timeout)
            return json.loads(msg)
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            logger.warning("WebSocket receive error: %s", repr(e))
            return None
