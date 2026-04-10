<p align="center">
  <b>OpenNews MCP Server</b><br>
  84+ リアルタイムデータソース · 6 エンジンカテゴリ · AI 評価 · トレーディングシグナル
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="./README_ZH.md">中文</a> | <a href="./README_JA.md">日本語</a> | <a href="./README_KO.md">한국어</a>
</p>

---

## クイックインストール

> **まず、[https://6551.io/mcp](https://6551.io/mcp) で API Token を取得してください。**

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=<your-token> \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> `/path/to/opennews-mcp` をローカルのプロジェクトパスに、`<your-token>` を API Token に置き換えてください。

### OpenClaw

```bash
export OPENNEWS_TOKEN="<your-token>"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

---

## AI にレビュー＆インストールしてもらう

この MCP が安全かどうか不安ですか？以下のプロンプトを AI アシスタントに送信すれば、ソースコードをレビューしてからインストールしてくれます：

> **以下のプロンプトをコピーして AI アシスタントに送信してください（`<project-path>` と `<your-token>` を実際の値に置き換え）：**

```text
opennews-mcp という MCP サーバーをレビューしてインストールしてください。プロジェクトはローカルの <project-path> にあります。

手順：
1. 以下のファイルのセキュリティを確認：
   - src/opennews_mcp/api_client.py — ai.6551.io のみに接続し、他のアドレスにデータを送信していないことを確認
   - src/opennews_mcp/config.py — トークンがローカルの config.json または環境変数からのみ読み取られ、ハードコードや漏洩がないことを確認
   - src/opennews_mcp/tools/*.py — すべてのツールが API クエリのみを実行し、ファイル書き込み、コマンド実行、その他の危険な操作がないことを確認
   - pyproject.toml — 依存関係が mcp、httpx、websockets のみで、不審なパッケージがないことを確認
2. レビュー結論を教えてください：安全 / リスクあり / 問題あり、具体的な理由とともに
3. 安全であれば、インストールを実行（Token は https://6551.io/mcp から取得）：
   claude mcp add opennews -e OPENNEWS_TOKEN=<your-token> -- uv --directory <project-path> run opennews-mcp
```

---

## データソース — 6カテゴリ 84+ ソース

| カテゴリ | 数量 | 主なソース |
|---------|------|-----------|
| **News** | 53 | Bloomberg、Reuters、Financial Times、CNBC、CNN、BBC、Fox Business、CoinDesk、Cointelegraph、The Block、Blockworks、Decrypt、DlNews、A16Z、TechCrunch、Wired、Politico、Business Insider、Twitter/X、Telegram、Weibo、Truth Social、U.S. Treasury、ECB、TASS、Handelsblatt、Welt、Ambrey、Morgan Stanley、PR Newswire、Coinbase、Phoenixnews など |
| **Listing** | 9 | Binance、Coinbase、OKX、Bybit、Upbit、Bithumb、Robinhood、Hyperliquid、Aster |
| **OnChain** | 3 | Hyperliquid Whale Trade、Hyperliquid Large Position、KOL Trade |
| **Meme** | 1 | Twitter ミームコインソーシャルセンチメント |
| **Market** | 6 | Price Change、Funding Rate、Funding Rate Difference、Large Liquidation、Market Trends、OI Change |
| **Prediction** | 12 | CORRELATION_LOGICAL、SMART_MONEY_TRADE、PRICE_SPIKE、CLUSTER_ENTRY、WHALE_POSITION、NEW_WALLET_TRADE、INSIDER_PATTERN、CORRELATION_NARRATIVE、CORRELATION_HEDGE、CORRELATION_ENTITY_GEO、CORRELATION_CAUSAL、SETTLEMENT_ARBITRAGE |

すべての記事は **AI 分析済み** — 影響度スコア（0-100）、トレーディングシグナル（long/short/neutral）、中英バイリンガル要約付き。

<details>
<summary><b>News — 53 ソース</b>（engineType: "news"）— プレミアム金融・暗号メディア、政府機関、ソーシャルプラットフォーム</summary>

| ソースコード | 説明 |
|-------------|------|
| Bloomberg | ブルームバーグ — トップクラスの金融ニュース |
| Reuters | ロイター — グローバル通信社 |
| Financial Times | フィナンシャル・タイムズ — プレミアムビジネスニュース |
| CNBC | CNBC — 金融テレビ |
| CNN | CNN — 米国ニュースネットワーク |
| BBC | BBC — 英国放送協会 |
| Fox Business | Fox Business — 米国金融ニュース |
| CoinDesk | CoinDesk — 大手暗号メディア |
| Cointelegraph | Cointelegraph — 暗号メディア |
| The Block | The Block — 暗号データ＆ジャーナリズム |
| Blockworks | Blockworks — 暗号ネイティブメディア |
| Decrypt | Decrypt — 暗号＆Web3メディア |
| DlNews | DL News — 暗号調査報道 |
| A16Z | a16z（Andreessen Horowitz）— 大手暗号VC |
| TechCrunch | TechCrunch — テック＆スタートアップニュース |
| Wired | Wired — テックジャーナリズム |
| Politico | Politico — 米欧政治ニュース |
| Business Insider | Business Insider |
| Twitter/X | Twitter/X 暗号インフルエンサーの投稿 |
| X / Twitter Profile | Twitter/X プロフィール変更（名前・自己紹介更新） |
| Telegram | Telegram チャンネル |
| Weibo | Weibo（微博）— 中国ソーシャルメディア |
| Truth Social | Truth Social — トランプのソーシャルプラットフォーム |
| U.S. Treasury | 米国財務省 — 公式声明 |
| U.S. Trade Representative | USTR — 通商政策発表 |
| ECB | 欧州中央銀行 — 公式コミュニケーション |
| TASS | TASS — ロシア国営通信社 |
| Interfax | Interfax — ロシア通信社 |
| Handelsblatt | Handelsblatt — ドイツビジネス新聞 |
| Hadelsblatt | Hadelsblatt — ドイツビジネス |
| Welt | Welt — ドイツ新聞 |
| Telegraph | テレグラフ — 英国ニュース |
| MS NOW | モルガン・スタンレー NOW — 機関投資家リサーチ |
| Ambrey | Ambrey — 海事＆地政学インテリジェンス |
| PR Newswire | PR Newswire — プレスリリース |
| Coinbase | Coinbase アナウンス＆ブログ |
| Binance | Binance アナウンス＆ブログ |
| Phoenixnews | フェニックスニュース |
| jin10 | 金十データ — 中国金融速報 |
| The Big Whale | The Big Whale — 欧州暗号メディア |
| The Verge | The Verge — テックメディア |
| Techinasia | Tech in Asia — アジアテックニュース |
| Medium | Medium ブログ |
| Chainwire | Chainwire — 暗号プレスリリース |
| Token Relations | トークン関係＆パートナーシップ |
| Crypto Narratives | 暗号ナラティブトラッキング |
| Crypto in America | 米国暗号業界カバレッジ |
| 6551News | 6551 プラットフォームオリジナル分析 |
| BWEnews | BWE ニュースワイヤー |
| AGGRNEWS | アグリゲートニュースフィード |
| dbnews | DB ニュース |
| Tree | Tree ニュース |
| Velo | Velo データインテリジェンス |

</details>

<details>
<summary><b>Listing — 9 ソース</b>（engineType: "listing"）— 主要取引所のトークン上場アナウンス</summary>

| ソースコード | 説明 |
|-------------|------|
| Binance | Binance 新トークン上場 |
| Coinbase | Coinbase 新トークン上場 |
| OKX | OKX 新トークン上場 |
| Bybit | Bybit 新トークン上場 |
| Upbit | Upbit（韓国取引所）上場 |
| Bithumb | Bithumb（韓国取引所）上場 |
| Robinhood | Robinhood 暗号上場 |
| Hyperliquid | Hyperliquid パーペチュアル上場 |
| Aster | Aster 取引所上場 |

</details>

<details>
<summary><b>OnChain — 3 ソース</b>（engineType: "onchain"）— ホエール＆KOLのオンチェーン活動</summary>

| ソースコード | 説明 |
|-------------|------|
| Hyperliquid Whale Trade | Hyperliquid ホエール取引アラート |
| Hyperliquid Large Position | Hyperliquid 大口ポジション変動 |
| KOL Trade | KOL（キーオピニオンリーダー）オンチェーン取引 |

</details>

<details>
<summary><b>Meme — 1 ソース</b>（engineType: "meme"）— ミームコインソーシャルセンチメントトラッキング</summary>

| ソースコード | 説明 |
|-------------|------|
| Twitter | Twitter/X ミームコイン議論＆バイラル投稿 |

</details>

<details>
<summary><b>Market — 6 ソース</b>（engineType: "market"）— マーケット異常検出＆クオンツシグナル</summary>

| ソースコード | 説明 |
|-------------|------|
| Price Change | 大幅な価格変動（急騰/急落） |
| Funding Rate | ファンディングレート異常（パーペチュアル先物） |
| Funding Rate Difference | 取引所間ファンディングレート乖離 |
| Large Liquidation | 大口清算イベント |
| Market Trends | 全体的な市場トレンド変化 |
| OI Change | 建玉の大幅変動 |

</details>

<details>
<summary><b>Prediction — 12 ソース</b>（engineType: "prediction"）— AI予測＆相関シグナル</summary>

| ソースコード | 説明 |
|-------------|------|
| CORRELATION_LOGICAL | 論理的相関分析 |
| SMART_MONEY_TRADE | スマートマネー取引追跡 |
| PRICE_SPIKE | 価格急変検出 |
| CLUSTER_ENTRY | クラスターエントリーシグナル |
| WHALE_POSITION | ホエールポジション監視 |
| NEW_WALLET_TRADE | 新規ウォレット取引検出 |
| INSIDER_PATTERN | インサイダーパターン認識 |
| CORRELATION_NARRATIVE | ナラティブ相関分析 |
| CORRELATION_HEDGE | ヘッジ相関分析 |
| CORRELATION_ENTITY_GEO | 地政学エンティティ相関 |
| CORRELATION_CAUSAL | 因果相関分析 |
| SETTLEMENT_ARBITRAGE | 決済アービトラージシグナル |

</details>

---

## 何ができる？

接続後、AI アシスタントに話しかけるだけ：

| あなたが言う | 実行される操作 |
|-------------|---------------|
| 「最新の暗号通貨ニュース」 | 最新記事を取得 |
| 「SEC 規制のニュースを検索」 | 全文キーワード検索 |
| 「BTC 関連ニュース」 | 通貨でフィルタ |
| 「Bloomberg の記事」 | ソースでフィルタ |
| 「オンチェーンイベント」 | エンジンタイプでフィルタ（onchain） |
| 「AI スコア 80 以上の重要ニュース」 | 高スコアフィルタ |
| 「強気シグナル」 | トレーディングシグナルでフィルタ（long） |
| 「リアルタイムニュースを購読」 | WebSocket リアルタイム更新 |

---

## 利用可能なツール

| カテゴリ | ツール | 説明 |
|---------|--------|------|
| ディスカバリー | `get_news_sources` | 完全エンジンツリー — 6カテゴリ 84+ ソースとメタデータ |
| | `list_news_types` | フィルタ用ソースコードのフラットリスト |
| 検索 | `get_latest_news` | 84+ ソースから最新記事を取得 |
| | `search_news` | 全ソース横断キーワード検索 |
| | `search_news_by_coin` | 通貨別（BTC, ETH, SOL...）全ソース横断 |
| | `get_news_by_source` | 特定ソース指定（例：engine_type="news", news_type="Bloomberg"） |
| | `get_news_by_engine` | カテゴリ別：news, listing, onchain, meme, market, prediction |
| | `search_news_advanced` | 複合フィルタ：通貨 + キーワード + エンジンタイプ |
| AI | `get_high_score_news` | 高 AI 影響度スコア記事（0-100 スケール） |
| | `get_news_by_signal` | AI トレーディングシグナル別：long / short / neutral |
| リアルタイム | `subscribe_latest_news` | WebSocket ライブフィード、通貨・エンジンタイプフィルタ対応 |

> 詳細な使用ガイドとサンプルについては、[ナレッジガイド](../knowledge/guide.md) をご覧ください。

---

## 設定

### API Token を取得

[https://6551.io/mcp](https://6551.io/mcp) で API Token を取得してください。

環境変数を設定：

```bash
# macOS / Linux
export OPENNEWS_TOKEN="<your-token>"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "<your-token>"
```

| 変数 | 必須 | 説明 |
|------|------|------|
| `OPENNEWS_TOKEN` | **はい** | 6551 API Bearer トークン（https://6551.io/mcp から取得） |
| `OPENNEWS_API_BASE` | いいえ | REST API URL のオーバーライド |
| `OPENNEWS_WSS_URL` | いいえ | WebSocket URL のオーバーライド |
| `OPENNEWS_MAX_ROWS` | いいえ | リクエストあたりの最大結果数（デフォルト: 100） |

プロジェクトルートの `config.json` もサポート（環境変数が優先）：

```json
{
  "api_base_url": "https://ai.6551.io",
  "wss_url": "wss://ai.6551.io/open/news_wss",
  "api_token": "<your-token>",
  "max_rows": 100
}
```

---

## WebSocket リアルタイム購読

**エンドポイント**: `wss://ai.6551.io/open/news_wss?token=YOUR_TOKEN`

リアルタイムの暗号通貨ニュース更新を購読します。

### ニュースを購読

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "news.subscribe",
  "params": {
    "engineTypes": {
      "news": ["Bloomberg", "CoinDesk"],
      "onchain": []
    },
    "coins": ["BTC", "ETH"],
    "hasCoin": true
  }
}
```

**レスポンス**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true,
    "filters": {
      "engineTypes": {...},
      "coins": [...],
      "hasCoin": true
    }
  }
}
```

**フィルタパラメータ**（すべてオプション）：
- `engineTypes`: エンジンタイプからニュースタイプコードへのマッピングオブジェクト
  - キー：エンジンタイプ（例：`"news"`, `"onchain"`, `"listing"`, `"meme"`, `"market"`, `"prediction"`）
  - 値：ニュースタイプコードの配列（例：`["Bloomberg", "CoinDesk"]`）
  - 空配列 `[]` はそのエンジン下のすべてのニュースタイプを意味します
  - `list_news_types` ツールで利用可能なコードを取得できます
- `coins`: 通貨シンボルの配列（例：`["BTC", "ETH"]`）
  - 指定した通貨でニュースをフィルタ
  - 空配列 `[]` または省略で全通貨を受信
- `hasCoin`: ブール値、true の場合は通貨タグ付きニュースのみ受信

### 購読解除

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "news.unsubscribe"
}
```

### サーバープッシュ - ニュース更新

フィルタに一致する新しいニュースがあると、サーバーがプッシュ：

```json
{
  "jsonrpc": "2.0",
  "method": "news.update",
  "params": {
    "id": "unique-article-id",
    "text": "記事のタイトルまたは内容",
    "newsType": "Bloomberg",
    "engineType": "news",
    "link": "https://...",
    "coins": [
      {
        "symbol": "BTC",
        "market_type": "spot",
        "match": "title"
      }
    ],
    "ts": 1708473600000
  }
}
```

### サーバープッシュ - AI ニュース更新

AI 分析付きニュース（購読している場合）：

```json
{
  "jsonrpc": "2.0",
  "method": "news.ai_update",
  "params": {
    "id": "unique-article-id",
    "text": "記事のタイトル",
    "newsType": "Bloomberg",
    "engineType": "news",
    "link": "https://...",
    "coins": [...],
    "aiRating": {
      "score": 85,
      "grade": "A",
      "signal": "long",
      "status": "done",
      "summary": "中国語の要約",
      "enSummary": "English summary"
    },
    "ts": 1708473600000
  }
}
```

---

## データ構造

各記事：

```json
{
  "id": "unique-article-id",
  "text": "タイトル / 内容",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "中国語の要約",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI フィールド | 説明 |
|-------------|------|
| `score` | 0-100 影響度スコア |
| `signal` | `long`（強気）/ `short`（弱気）/ `neutral` |
| `status` | `done` = AI 分析完了 |

---

<details>
<summary><b>その他のクライアント — 手動インストール</b>（クリックで展開）</summary>

> 以下のすべての設定で `/path/to/opennews-mcp` をローカルの実際のプロジェクトパスに、`<your-token>` を [https://6551.io/mcp](https://6551.io/mcp) から取得した Token に置き換えてください。

### Claude Desktop

設定ファイルを編集（macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`、Windows: `%APPDATA%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` または Settings > MCP Servers：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Windsurf

`~/.codeium/windsurf/mcp_config.json`：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Cline

VS Code サイドバー > Cline > MCP Servers > Configure、`cline_mcp_settings.json` を編集：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Continue.dev

`~/.continue/config.yaml`：

```yaml
mcpServers:
  - name: opennews
    command: uv
    args:
      - --directory
      - /path/to/opennews-mcp
      - run
      - opennews-mcp
    env:
      OPENNEWS_TOKEN: <your-token>
```

### Cherry Studio

設定 > MCP サーバー > 追加 > タイプ stdio：Command `uv`、Args `--directory /path/to/opennews-mcp run opennews-mcp`、Env `OPENNEWS_TOKEN`。

### Zed Editor

`~/.config/zed/settings.json`：

```json
{
  "context_servers": {
    "opennews": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
        "env": {
          "OPENNEWS_TOKEN": "<your-token>"
        }
      }
    }
  }
}
```

### 任意の stdio MCP クライアント

```bash
OPENNEWS_TOKEN=<your-token> \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## 互換性

| クライアント | インストール方法 | ステータス |
|-------------|-----------------|-----------|
| **Claude Code** | `claude mcp add` | ワンクリック |
| **OpenClaw** | Skill ディレクトリコピー | ワンクリック |
| Claude Desktop | JSON 設定 | 対応 |
| Cursor | JSON 設定 | 対応 |
| Windsurf | JSON 設定 | 対応 |
| Cline | JSON 設定 | 対応 |
| Continue.dev | YAML / JSON | 対応 |
| Cherry Studio | GUI | 対応 |
| Zed | JSON 設定 | 対応 |

---

## 関連プロジェクト

- [twitter-mcp](https://github.com/6551-io/twitter-mcp) - Twitter/X データ MCP サーバー

---

## 開発

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector テスト
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### プロジェクト構造

```
├── README.md
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # 組み込みナレッジ
├── pyproject.toml
├── config.json
└── src/opennews_mcp/
    ├── server.py              # エントリポイント
    ├── app.py                 # FastMCP インスタンス
    ├── config.py              # 設定ローダー
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # ツール
```

## ライセンス

MIT
