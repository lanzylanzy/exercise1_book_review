```md
## 项目简介

个人开发的全栈书评聚合网站，通过汇总中英文图书社区的评分、评分人数和评论，帮助用户更快判断一本书是否值得阅读。
落地的主要难点其实是部署平台和ip，为了能同时访问豆瓣和goodread，中间需要转接很多次。
由于免费服务和代理资源限制，不适合高并发或大规模访问，且大陆使用时可能需要魔法。由于使用免费服务器，第一次启动可能需要较久时间。

## 主要功能

- 聚合豆瓣与goodreads图书社区的数据
- 分别显示正面和负面评论
- 除评分外，将评分人数作为重要参考指标
- 支持同一本书在不同平台之间快速对比

## 技术栈

React、Tailwind CSS、Django、Requests、lxml、Parsel、Brave Search API、Goodreads GraphQL API、MarsProxies、 netlify、Render

## 数据流程

用户浏览器发送请求 → netlify前端 → Render后端 → 调用Brave浏览器的搜索API，获取对应书籍的豆瓣详情页url →通过 MarsProxies 香港代理 IP 转发请求（海外服务器无法直接访问豆瓣）→ 爬取豆瓣信息，同时查询本书外文版isbn → 获取goodread信息 → 整理为JSON  → netlify前端展示
