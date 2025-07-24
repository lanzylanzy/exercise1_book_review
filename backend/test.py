from spider import search_db_subject_url
from spider import search_db_subject_details
from spider import search_db_subject_isbn
from spider import search_db_reviews
from spider import search_db_reviews
from spider import search_gr_info
from spider import search_gr_reviews
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#用名称搜索豆瓣详情页url
#为了省api次数，测试时候先不用谷歌搜索
db_subject_url=search_db_subject_url("小狗钱钱")
print(db_subject_url)

#爬取豆瓣详情页相关信息，包括英文版url
db_book_info, en_url=search_db_subject_details(db_subject_url)
print(db_book_info)
print(en_url)
#爬取豆瓣详情页isbn
en_version_isbn=search_db_subject_isbn(en_url)
print(en_version_isbn)
#爬取豆瓣评论
db_good_reviews,db_bad_reviews=search_db_reviews(db_subject_url)
print(db_good_reviews)
print(db_bad_reviews)
#爬取goodread详情信息
gr_book_info,resourceID=search_gr_info(en_version_isbn)
print(gr_book_info)
print(resourceID)
#爬取goodread评论
gr_good_reviews,gr_bad_reviews=search_gr_reviews(resourceID)
print(gr_good_reviews)
print(gr_bad_reviews)
