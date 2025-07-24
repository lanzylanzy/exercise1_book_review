from backend.spider import (search_db_subject_url,
                            search_db_subject_details,
                            search_db_subject_isbn,
                            search_db_reviews,
                            search_gr_info,
                            search_gr_reviews)
from pprint import pprint



#打包豆瓣信息，增加错误返回以免程序崩溃
def pack_db_info(keyword):
    #所有数据打包
    db_result = {
        "success": False,
        "db_book_info": None,
        "en_version_url": None,
        "en_version_isbn": None,
        "db_good_reviews": None,
        "db_bad_reviews": None,
        "error": None
    }
    #用try结构，程序在出错时终止并抛出错误信息
    #谷歌搜索豆瓣的url
    try:
        db_subject_url = search_db_subject_url(keyword)
    #若搜不到结果，直接报错结束程序
    except Exception as e:
        db_result["error"] = str(e)
        return db_result
    
    #豆瓣详情页爬取书籍信息，英文版书籍url
    db_book_info, en_url = search_db_subject_details(db_subject_url)
    db_result["db_book_info"] = db_book_info
    db_result["en_version_url"] = en_url
    #en_url默认返回false，只有在提取到时才继续爬isbn
    if en_url:
        en_version_isbn = search_db_subject_isbn(db_result["en_version_url"])
        db_result["en_version_isbn"] = en_version_isbn
    
    #提取评论
    db_good_reviews, db_bad_reviews = search_db_reviews(db_subject_url)
    db_result["db_good_reviews"]=db_good_reviews
    db_result["db_bad_reviews"]=db_bad_reviews
    #全部结束后result成功
    db_result["success"] = True
    return db_result

#打包Goodreads信息，增加错误返回以免程序崩溃
def pack_gr_info(en_version_isbn):
    #所有数据打包
    gr_result = {
        "success": False,
        "gr_book_info": None,
        "gr_good_reviews": None,
        "gr_bad_reviews": None,
        "error": None
    }
    #没有isbn，直接报错终止
    if not en_version_isbn:
        gr_result["error"] = "未找到对应的英文版本，无法提取 Goodreads 数据"
        return gr_result
    
    #提取书籍详情信息
    try:
        gr_book_info, resourceID = search_gr_info(en_version_isbn)
        gr_result["gr_book_info"]=gr_book_info
        #有isbn但没提取到，报错并终止
        if not gr_book_info or not resourceID:
            raise ValueError("Goodreads 未收录该书")
    #没提取到直接报错
    except Exception as e:
            gr_result["error"] = str(e)
            return gr_result
    #提取评论详细信息
    gr_good_reviews, gr_bad_reviews = search_gr_reviews(resourceID)
    gr_result["gr_good_reviews"]=gr_good_reviews
    gr_result["gr_bad_reviews"]=gr_bad_reviews
    #全部结束后result成功
    gr_result["success"]=True
    
    return gr_result


#db_result=pack_db_info("机器人学中的状态估计")
#en_version_isbn=db_result["en_version_isbn"]
#gr_result=pack_gr_info(en_version_isbn)
#pprint(db_result)
#pprint(gr_result)