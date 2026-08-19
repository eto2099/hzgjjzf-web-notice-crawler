# 信息收集任务提示词 — 执法公告采集

## 任务目标
执行目标站点「执法公告」栏目的公告信息采集，并核对采集结果。

## 环境与准备
- 项目目录：`D:\admin\works\ai\hzgjjzf`，必须在该目录（仓库根目录）下运行，否则日志/输出会写到错误位置。
- Python 虚拟环境：`.venv`（已存在）。用 `.venv\Scripts\python.exe` 执行，不要用系统 python。
- 依赖已装好（含 `brotli`，详情页是 brotli 压缩，缺它详情解析全空）。如需补装：`.venv\Scripts\python.exe -m pip install -r requirements.txt`。
- 采集刻意慢（每次请求随机延迟 3–8s、失败重试带退避）。**禁止移除延迟或调小 MAX_RETRIES**，等待时要有耐心。

## 执行命令
1. **采集最新日期**（当日无公告自动回退到最新公告日期）：
   ```
   .venv\Scripts\python.exe src/main.py
   ```
2. **回补某一天的历史数据**：
   ```
   .venv\Scripts\python.exe src/main.py --date 2026-08-18
   ```
   不传 `--date` 默认采集最新日期；`--date` 只采集指定那一天的公告，且不会覆盖已记录的 `last_date.txt`。

## 运行与验证
- 运行命令的**超时建议 ≥ 10 分钟**（每次采集约 1–3 分钟，视当日公告数量而定）。
- 采集完成后检查：
  - `data/report.csv`（追加模式，utf-8-sig）有新增行，字段含 `title, publish_date, source, notice_object, detail_content, content_html, keywords, description, url, article_id`。
  - `data/<日期>/<article_id>.json` 按日期分目录生成。
  - `data/last_date.txt` 记录本次采集日期。
- 用 UTF-8 正确读取验证中文内容（PowerShell 控制台可能是 GBK 乱码，不代表数据错误，用编辑器或 python 读）。

## 结果汇报
汇总：本次采集的目标日期、采集条数、`data/` 下新增的目录与文件数、`report.csv` 总行数。若失败请报告日志中的报错。

## 注意事项 / 排查提示
- 所有日志为英文（项目约定，禁止新增中文日志）。
- 若详情解析为空、JSON 落到 `data/unknown/`：先确认 `brotli` 已装；再确认详情页 meta/`div#zoom` 结构是否变化。
- 若列表翻页异常（每页始终同一批）：翻页必须走 `paramJson` 参数（JSON 字符串，含 `pageNo`/`pageSize`/`search`），顶层 `pageNo`/`rows` 会被 API 忽略。
- 反爬规则：随机 UA/Referer 已内置，勿改动；若触发风控，可降低频率而非调小延迟。