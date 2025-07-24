import requests
import random
import parsel
import re
import time
import datetime


#制作用于豆瓣爬虫的headers,无cookies
def create_douban_session() -> requests.Session:
    sess = requests.Session()
    sess.headers.update({
        "User-Agent":random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36 Edg/117.0.2045.31",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
        ]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Referer": random.choice([
            "https://www.douban.com/",
            "https://book.douban.com/",
            "https://www.douban.com/explore/",
            "https://www.douban.com/group/",
        ]), 
        })
    sess.cookies.update({
        "dbcl2": "181853562:Jg3hvQpQ+Ek",   
        "ck": "ejDJ",          
        })
    return sess
#每次搜索创建一个固定session
session=create_douban_session()
#豆瓣通用爬虫，可通过参数灵活提取所需信息
def search_elements_db(url, div_selector=None, verify=False, timeout=7,sleep_range=(0.05, 0.2)):
    try:
        # ✅ 请求前先 sleep
        sleep_time = random.uniform(*sleep_range)
        time.sleep(sleep_time)
        #通过伪装的session获取网页
        resp =session.get(url, timeout=timeout, verify=verify)
        #自检测请求是否成功过，是否2开头，否则进入exception
        resp.raise_for_status()
        #构造html对象，把页面整理成css的格式
        selector = parsel.Selector(resp.text)
        #如果函数设置了了div选择器参数，就只提取选择器的内容
        if div_selector:
            elements = selector.css(div_selector)
            return elements
        else:
            return selector
    
    except Exception as e:
        raise RuntimeError(f"search_elements_db 请求失败，URL={url}，错误信息：{e}")        
#豆瓣评论筛选函数（仅使用于豆瓣评论页数据）
def extract_db_reviews(db_reviews_selector):
    comments=[]
    #遍历页面中的每一条评论，提取内容，分数，日期。并根据分数分为好，中，差三组
    for i, comment_item in enumerate(db_reviews_selector.css('li.comment-item')):
        #打印每一条评论看哪里出错了 print(f"✅ 第{i+1}条评论内容：{comment_item.css('p.comment-content span.short::text').get()}")
        #从原始html文件提取内容，分数，日期
        content = comment_item.css('p.comment-content span.short::text').get()
        rating_class = comment_item.css('span.user-stars::attr(class)').get()
        review_score = int(re.search(r'\d+', rating_class).group()) / 10 if rating_class else None
        date = comment_item.css('a.comment-time::text').get().strip().split(' ')[0]
        #如果是没评分或没评论的则跳过。
        if review_score is None or not content:
            continue
        #评论的格式改一下，不用文本换行\n，而用网页格式<br>
        content = content.replace('\n', '<br>').strip()
        #分成好，中，差三组
        if review_score >= 4:
            comments.append(("good", content, review_score, date))
        elif review_score <= 2:
            comments.append(("bad", content, review_score, date))
        elif review_score == 3:
            comments.append(("neutral", content, review_score, date))

    return comments

#制作用于goodread爬虫的headers
def create_gr_session():
    sess = requests.Session()

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/122.0.0.0"
    ]

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }

    sess.headers.update(headers)
    return sess
#每次搜索创建一个固定session
session_gr=create_gr_session()
#gr通用爬虫
def search_elements_gr(url, div_selector=None, verify=False, timeout=10):
    resp = session_gr.get(url, timeout=timeout, verify=verify)
    resp.raise_for_status()
    selector = parsel.Selector(resp.text)
    if div_selector:
        elements = selector.css(div_selector)
        return elements
    else:
        return selector
#gr评论页爬虫（有固定session，通过非公开api）
def search_review_gr(resourceID,ratingMin,ratingMax):
    url = "https://kxbwmqov6jgg3daaamb744ycu4.appsync-api.us-east-1.amazonaws.com/graphql"
    sess=requests.session()
    sess.headers.update({
        "Content-Type": "application/json",
        "x-api-key": "da2-xpgsdydkbregjhpr6ejzqdhuwy",  # 抓包获得的 key
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.goodreads.com/",
        "Origin": "https://www.goodreads.com"
    }
    )
    query ="""
        query getReviews($filters: BookReviewsFilterInput!, $pagination: PaginationInput) {
        getReviews(filters: $filters, pagination: $pagination) {
            edges {
            node {
                text
                rating
                createdAt
            }
            }
        }
        }
        """

    variables = {
        "filters": {
            "resourceType": "WORK",
            "resourceId": resourceID,
            "ratingMin": ratingMin,
            "ratingMax": ratingMax
        },
        "pagination": {
            "limit": 6
        }
    }

    response = sess.post(url, json={"query": query, "variables": variables})
    response.raise_for_status()
    gr_review_json = response.json()
    
    return gr_review_json
#gr评论筛选函数
def extract_gr_reviews(gr_reviews_json, reviews_type):
    edges=gr_reviews_json["data"]["getReviews"]["edges"]
    reviews = []
    idx=1
    for edge in edges:
        #如果带有超链接，跳过不取
        if "href=" in edge["node"]["text"]:
            continue
        #去掉所有标签，如换行的<br>和斜体，加粗等
        #edge["node"]["text"] = re.sub(r'<[^>]+>', '', edge["node"]["text"]).strip()
        content=edge["node"]["text"]
        review_score=edge["node"]["rating"]
        ts = edge["node"]["createdAt"]
        dt = datetime.datetime.fromtimestamp(ts / 1000)
        date=dt.strftime("%Y-%m-%d")

        reviews.append({
            f"{reviews_type}{idx}": {
                "content": content,
                "review_score": review_score,
                "date": date}
        })
        idx += 1

    if not reviews:
        reviews = [{"notation": "无更多评论"}]
    return reviews
