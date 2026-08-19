# hzgjjzf

hz住房公积金管理中心 — 执法公告信息采集爬虫。

## 目标站点

https://gjj.hangzhou.gov.cn/col/col1229287674/index.html

采集「执法公告」栏目下的公告列表及详情，包括标题、发布日期、来源、正文内容等字段。

## 项目结构

```
hzgjjzf/
├── src/
│   ├── spiders/
│   │   ├── base.py              # 爬虫基类（请求、重试、延迟）
│   │   └── hzgjj_spider.py      # hz公积金执法公告爬虫
│   ├── parsers/
│   │   ├── list_parser.py       # 列表页解析器
│   │   └── detail_parser.py     # 详情页解析器
│   ├── pipelines/
│   │   └── storage.py           # 数据存储（CSV + JSON）
│   ├── middleware/
│   │   └── anti_anti_spider.py  # 反爬策略（随机UA、Referer、请求头）
│   └── main.py                  # 入口
├── config/
│   └── settings.py              # 全局配置
├── data/                        # 采集数据输出
├── logs/                        # 运行日志
├── requirements.txt
└── .gitignore
```

## 技术要点

| 项目 | 说明 |
|------|------|
| 数据源 | JCMS 动态加载，通过 `/api-gateway/jpaas-publish-server/front/page/build/unit` 接口获取列表 JSON |
| 翻页策略 | 按页遍历（14条/页），只采集列表最新日期的那批公告，遇到更早日期即停 |
| 反爬措施 | 随机 User-Agent、随机 Referer、请求间隔 3-8s、重试机制 |
| 去重逻辑 | 基于 URL 的 `seen_urls` 集合去重 + 基于 `data/last_date.txt` 的日期增量去重 |
| 输出格式 | CSV 汇总（`report.csv`）+ 按日期/ID 分文件的 JSON 详情 |

## 快速开始

```bash
pip install -r requirements.txt
python src/main.py            # 采集最新日期（当日无公告则回退到最新公告日期）
python src/main.py --date 2026-08-18   # 指定采集某一天（回补历史）
```

## 配置

编辑 `config/settings.py` 或创建 `config/.env` 文件覆盖默认值：

```ini
REQUEST_DELAY_MIN=3.0
REQUEST_DELAY_MAX=8.0
PROXY_ENABLED=false
LOG_LEVEL=INFO
```

## 输出示例

```
data/
├── report.csv
├── last_date.txt
├── 2026-08-18/
│   ├── art_825f56331cd24a49944a1421bb3e8900.json
│   └── ...
└── 2026-08-17/
    └── ...
```

## 免责声明

- 本项目仅用于合法、合规的信息采集与研究学习，不提供任何采集数据成品。
- 采集的数据可能包含企业及个人姓名、金额等个人信息，请使用者遵守适用法律（如《个人信息保护法》）及数据来源网站的 robots.txt、服务条款。本项目不承担因使用者违规采集、存储或传播数据而产生的任何责任。
- 本项目的采集行为刻意保持低频、慢速，请勿移除延迟或调大并发，以免对目标站点造成影响。
- 若数据来源网站或其运营方要求停止采集，应立即停止使用本项目。

## 许可

MIT，详见 [LICENSE](LICENSE)。