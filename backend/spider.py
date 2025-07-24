import requests
import re
from parsel import Selector

from backend.utils import (search_elements_db,
                           extract_db_reviews,
                           extract_db_reviews,
                           search_elements_gr,
                           extract_gr_reviews,
                           search_review_gr)

# 用于通过书名在google引擎搜索的 API Key 和 CSE ID
API_KEY = "AIzaSyCge0r4L3k2_9rY67wKwB1pT-yWWqbsF8Q"
CSE_ID = "81569e7d7abc249b8"

#用书名在谷歌搜索，提取结果中豆瓣书籍详情页的url
def search_db_subject_url(query, num=1):
    #谷歌搜索固定url，和搜索需要的关键词
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CSE_ID,
        "num": num
    }
    #提取搜索结果，若失败则报错对应代码
    response = requests.get(url, params=params)
    if response.status_code != 200:
         raise ValueError(f"请求失败: {response.status_code} - {response.text}")
    #从搜索结果的josn中，提取页面链接
    data = response.json()
    items = data.get("items") 
    #如果搜索不到任何页面，则报错
    if not items:
         raise ValueError("找不到相关书籍，建议完善关键词，如输入作者、出版年份等") 
    #从所有的页面连接中，提取书籍主页面链接的代码
    link = data["items"][0].get("link")
    subject_link= re.search(r"https://book\.douban\.com/subject/\d+/", link)
    #增加一个无法提取的报错
    if subject_link:
        return subject_link.group(0)
    else:
        raise ValueError("搜索结果中未能提取到豆瓣书籍页面链接") 



#【豆瓣数据清洗】
#-从详情页提取book_info(包括本书info，英文版详情页的url)
def search_db_subject_details(db_url):
    selector = search_elements_db(db_url)
    #【提取该书籍的基本信息】没有则返回none
    db_book_info={
        "title":(selector.xpath('//title/text()').get() or '').strip() or None,
        "img_url": selector.css('img::attr(src)').get() or None,
        "author":(re.sub(r'^作者[::]?\s*', '', selector.xpath('normalize-space(string(//span[span[@class="pl" and normalize-space(text())="作者"]]))').get() or '')).strip() or None,
        "published_date": (selector.xpath('normalize-space(//span[@class="pl" and contains(text(),"出版年")]/following-sibling::text())').get() or '').strip() or None,
        "intr" :'\n'.join(p.strip() for p in Selector(text=(selector.css('span.all.hidden div.intro').get() or selector.css('div.intro').get() or '')).css('p::text').getall() if p.strip()) or None,
        "score":(selector.css('strong.rating_num::text').get() or '').strip() or None,
        "rating":(selector.css('span[property="v:votes"]::text').get() or '').strip() or None,
        }

    #创建一个判断是否为英文名字的函数
    def is_english(text):
        if not text:
            return False
        eng_count = sum(1 for c in text if c.isascii() and c.isalpha())
        return eng_count / len(text) > 0.5  # 50%以上是英文字母
    
    #【提取英文版书籍的url】若没有英文版，则返回""
    en_version_url = False
    other_versions = selector.css('li.mb8.pl')
    #遍历所有其他版本，直到找到英文版
    for index,li in  enumerate(other_versions):
        a_tag_list= li.css('div.meta a')
        if not a_tag_list:
            continue  # 防止找不到a
        a_tag = a_tag_list[0]  # 取第一个a标签
        title_text = a_tag.xpath('text()').get(default='').strip()
        title_text = re.sub(r'\s*[（(]\d{4}[）)]$', '', title_text).strip()
        if is_english(title_text):            
            en_version_url = a_tag.xpath('@href').get(default='').strip()# 是英文，提取链接
            break  # 找到第一个英文版就停止

    return  db_book_info,en_version_url
#【豆瓣数据清洗】 
#-从详情页提取isbn（用于英文版提取）
def search_db_subject_isbn(db_url):
    selector = search_elements_db(db_url)    
    isbn = selector.xpath('//span[text()="ISBN:"]/following-sibling::text()[1]').get(default='').strip()
    return isbn
#【豆瓣爬虫+数据清洗】 
#-爬取多个从多个评论页，从评论页提取好评和差评
def search_db_reviews(db_subject_url,max_review=6):
     #从详情页url中提取本书id
    subject_id = db_subject_url.split('/')[4]
    #创建装好，中，差评的容器
    good_reviews = []  
    bad_reviews = []
    neutral_reviews = []

    #遍历评论前4页，将提取到的评论放到对应的容器里，并随时检查是否到达max_review
    for page in range(4):
        start_num=page*20
        reviews_url=f"https://book.douban.com/subject/{subject_id}/comments/?start={start_num}&limit=20&status=P&sort=score"
        db_reviews_selector=search_elements_db(reviews_url)
        page_comments=extract_db_reviews(db_reviews_selector)
        #如果这页已经没有评论了，直接停止，继续翻页
        if not page_comments:
            break 
        #把提取的comment分类到对应dict
        for tag, content, score, date in page_comments:
            if tag == "good" and len(good_reviews) < max_review:
                i = len(good_reviews)
                good_reviews.append({
                    f"db_good_review{i}": {
                        "content": content,
                        "review_score": score,
                        "date": date
                    }
                })
            elif tag == "bad" and len(bad_reviews) < max_review:
                i = len(bad_reviews)
                bad_reviews.append({
                    f"db_bad_review{i}": {
                        "content": content,
                        "review_score": score,
                        "date": date
                    }
                })
            elif tag == "neutral":
                neutral_reviews.append({
                    "content": content,
                    "review_score": score,
                    "date": date
                })
        # 如果好评和差评数量都够了，提前终止
        if len(good_reviews) >= max_review and len(bad_reviews) >= max_review:
            break
    #如果差评数量没够，用中评补上
    for review in neutral_reviews:
        if len(bad_reviews) < max_review:
            i = len(bad_reviews)
            bad_reviews.append({
                f"db_bad_review{i}": review
            })
        else:
            break
    #若未找到任何评论
    if not good_reviews:
        good_reviews = [{"notation": "无更多评论"}]
    if not bad_reviews:
        bad_reviews = [{"notation": "无更多评论"}]

    return good_reviews, bad_reviews



#【goodread数据清洗】
#-从详情页提取book_info
def search_gr_info(isbn):
        isbn_url = f"https://www.goodreads.com/search?q={isbn}"
        selector=search_elements_gr(isbn_url) 
        gr_book_info={
            "title":selector.xpath('normalize-space(//h1[@data-testid="bookTitle"]/text())').get(),
            "img_url": selector.xpath("//img[@class='ResponsiveImage']/@src").get(),
            "author":selector.xpath("normalize-space(//a[contains(@class,'ContributorLink')]/span[@data-testid='name']/text())").get(default=''),
            "published_date":selector.xpath("normalize-space(substring-after(//p[@data-testid='publicationInfo']/text(), 'published '))").get(default=''),
            #intr的换行问题还未处理
            "intr" :selector.xpath("string(//span[@class='Formatted'])").get().replace("<br>", "\n").replace("&nbsp;", " ").strip(),
            "score":selector.xpath("normalize-space(//div[contains(@class,'RatingStatistics__rating')]/text())").get() or "暂无评分",
            "rating":selector.xpath("normalize-space((//div[contains(@class,'RatingStatistics__meta')]""//span[@data-testid='ratingsCount']/text())[1])").get(default='') or "暂无评论人数",
        }
        #提取书籍resourceID
        gr_details_text=selector.get()
        resourceID = re.search(r'kca://work/amzn1\.gr\.work\.v1\.[a-zA-Z0-9_-]+', gr_details_text)
        resourceID=resourceID.group(0)
        return gr_book_info,resourceID
#【goodread数据清洗】
#-从评论页提取book_info
def search_gr_reviews(resourceID):    
    gr_good_reviews_json=search_review_gr(resourceID,4,5)   
    gr_good_reviews=extract_gr_reviews(gr_good_reviews_json, "gr_good_review")
    gr_bad_reviews_json=search_review_gr(resourceID,1,2)
    gr_bad_reviews=extract_gr_reviews(gr_bad_reviews_json, "gr_bad_review")       
    return gr_good_reviews,gr_bad_reviews