## Overview

A self initiated full stack web application to evaluate whether a book is worth reading by aggregating ratings, reader counts, and reviews across platforms.
由于用了vercle和react的云服务部署，在国内需要使用魔法打开。项目最麻烦的其实在于，用国内部署就无法打开goodread，用国外部署又无法打开豆瓣，目前的方案是依然用国外免费服务器部署，但是爬豆瓣的时候用了香港的ip池做转接，全程免费，只是不能大量使用。

## Features
- Aggregates data from Chinese and English book communities  
- Automatically classifies reviews into positive and negative; Douban currently lacks this feature and primarily orders reviews by time, making it difficult to identify critical feedback for highly rated books  
- Highlights reader count as a key metric alongside ratings  
- Enables fast cross-platform comparison for decision making  

## Tech Stack
React, Tailwind CSS, Django, Web scraping & browser-based APIs

## dataflow
User Browser → Vercel Frontend → Render Backend → Brave Search API →  MarsProxies Proxy Pool → Hong Kong Proxy IP → Douban / Goodreads Detail & Review Pages → Render Parsing → JSON  → response Frontend
## Notes
Uses free APIs and proxies; performance may be slower due to anti-scraping restrictions
Prototype project, continuously improving data stability
