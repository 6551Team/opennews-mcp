from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from opennews_mcp.tools.news import get_high_score_news


class _FakeNewsAPI:
    def __init__(self, data):
        self.data = data
        self.request = None

    async def search_news(self, **kwargs):
        self.request = kwargs
        return {"data": self.data, "total": len(self.data)}


class GetHighScoreNewsTests(IsolatedAsyncioTestCase):
    async def test_sorts_by_documented_nested_ai_rating_score(self):
        api = _FakeNewsAPI([
            {"id": "lower", "aiRating": {"score": 72}},
            {"id": "higher", "aiRating": {"score": 95}},
        ])
        ctx = SimpleNamespace(
            request_context=SimpleNamespace(
                lifespan_context=SimpleNamespace(api=api),
            ),
        )

        with patch("opennews_mcp.tools.news.require_token", return_value=None):
            result = await get_high_score_news(ctx, min_score=70, limit=10)

        self.assertEqual([item["id"] for item in result["data"]], ["higher", "lower"])
        self.assertEqual(api.request, {"score": 70, "limit": 10, "page": 1})
