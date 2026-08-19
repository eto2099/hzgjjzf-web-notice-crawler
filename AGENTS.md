# AGENTS.md

杭州公积金执法公告采集爬虫。注意：这是 **requests 手写爬虫，不是 Scrapy**（"spider/pipeline/middleware" 只是目录命名），不要用 `scrapy` 命令。Python 3.13，虚拟环境 `.venv` 已存在。

## 运行

- 必须在**仓库根目录**执行：`python src/main.py`（或 `.venv\Scripts\python.exe src/main.py`）。支持 `--date YYYY-MM-DD` 指定采集某一天（回补历史），不传则默认采集最新日期（当日无公告回退到最新公告日期）。
  - `config/.env`、日志 `logs/`、输出 `data/` 都是相对 CWD 的路径；从其他目录运行会把产物写到错误位置。
- 依赖：`pip install -r requirements.txt`。无测试、无 lint/CI 配置。

## 架构约定

- 导入风格：`from config.settings import settings`、`from src.spiders.base import ...`。包未安装，靠 `src/main.py` 顶部的 `sys.path` 注入根目录；新增模块沿用此绝对导入，勿用相对导入。
- 配置在 `config/settings.py`（pydantic-settings），可用 `config/.env` 覆盖（该文件当前不存在）。

## 关键行为（与直觉不同处）

- 列表数据走 API：`GET https://gjj.hangzhou.gov.cn/api-gateway/jpaas-publish-server/front/page/build/unit`，带 `API_PARAMS` + `paramJson`（JSON 字符串，含 `pageNo`/`pageSize`/`search`）；返回 JSON 的 `data.html` 用 BeautifulSoup 解析 `<li>`。注意：翻页必须走 `paramJson`，顶层 `pageNo`/`rows` 会被忽略（始终返回首页 14 条）。
- 详情页从 HTML 的 `<meta name="ArticleTitle|PubDate|...">` 和 `div#zoom` 提取。站点结构一旦变化，记录将只剩 `url` 有值、JSON 落到 `data/unknown/`（`publish_date` 为空 → "unknown" 目录），这是解析失败的信号。注意：详情页是 brotli 压缩（`Content-Encoding: br`），必须装 `brotli`，否则 `resp.text` 是乱码、解析结果同样为空（此时是环境问题不是站点改版）。
- 停止条件：遇到更早日期、第一页无数据，或第一个重复/空 URL（`seen_urls` 去重）即停。
- 只采集最新日期：以第一页列表中的最大日期为 `latest_date`，只处理该日期条目，遇到更早日期即停；本次采集日期写入 `data/last_date.txt`，下次运行若最新日期不晚于上次则跳过（增量去重）。当日无公告时自动回退：`latest_date` 直接取列表最新一条的日期（即"前一天/往前推"），并打印 fallback 日志。
- 日志（`logger.*`）一律英文，禁止中文；修改或新增日志时遵循此约定。
- 反爬：每次请求前随机 UA/Referer，延迟 3–8s，失败重试带 2^n 退避。采集**刻意慢**，测试/开发时不要移除延迟或调小 MAX_RETRIES。
- 输出：`data/report.csv`（utf-8-sig，追加模式，仅文件为空时写表头）+ 按日期目录的 `<article_id>.json`。`data/` 和 `logs/` 已 gitignore（保留 `.gitkeep`）。`data/last_date.txt` 记录上次采集日期。
- `DETAIL_FIELDS`（settings.py）决定 CSV 列；改字段时需同步检查 `src/pipelines/storage.py`。
