from django.http import JsonResponse
from backend.service import pack_db_info, pack_gr_info
import threading
from collections import OrderedDict

#临时缓存
gr_cache = OrderedDict()
gr_lock = threading.Lock()
MAX_CACHE_SIZE = 10



    
#提取豆瓣详情信息
def db_info_view(request):
    db_result = {
    "success": False,
    "db_book_info": None,
    "en_version_url": None,
    "db_good_reviews": None,
    "db_bad_reviews": None,
    "error": None
    }
    gr_result ={
    "success": None,
    "status":False,
    "gr_book_isbn": None,
    "gr_book_info": None,
    "gr_good_reviews": None,
    "gr_bad_reviews": None,
    "error": None
    }
    #提取关键词
    query = request.GET.get("q")
    #无关键词，报错
    if not query:
        db_result["sucess"]="请输入关键词"
        db_result["error"] = "请输入关键词"
        return JsonResponse({
            "db_result": db_result,
            "gr_result": gr_result
        }, status=200, json_dumps_params={'ensure_ascii': False})
    
    #开始通过谷歌爬取豆瓣信息（如果搜所无结果，在service.py中已打包完报错机制）
    db_result= pack_db_info(query)
    #如果没有en_url，在service.py中已打包完报错机制，isbn会等于false
    en_url = db_result["en_version_url"]
    if not en_url:
        gr_result["success"]= False
        gr_result["error"]="未找到对应的英文版本"
    # 如果有英文版url，就后台开线程开始抓 GR 数据
    else:
        def run_gr_task():
            try:
                result = pack_gr_info(en_url)
            #有url，但抓不到，就返回service里的“Goodreads 未收录该书”错误
            except Exception as e:
                result = {"success": False, "error": str(e)}
            with gr_lock:
             # 如果已存在则先删掉再加，避免顺序错乱
                if en_url in gr_cache:
                    del gr_cache[en_url]
                gr_cache[en_url] = result

        # 超过最大缓存长度就删掉最旧的一条
        if len(gr_cache) > MAX_CACHE_SIZE:
            gr_cache.popitem(last=False)  # FIFO 删除最早添加的
        #这行代码表示，开始同步提取gr内容，也就是运行上面那个函数。同时不影响原本函数的返回
        threading.Thread(target=run_gr_task).start()

    return JsonResponse({
        "db_result": db_result,
        "gr_result": gr_result
    }, json_dumps_params={'ensure_ascii': False})

def gr_info_view(request):
    en_url = request.GET.get("en_url")
    #把缓存里提取的数据导出
    gr_result = gr_cache.get(en_url)
    
    if  gr_result is None or gr_result.get("success") is None:
    # 没提取完
        return JsonResponse({
            "gr_result": {
                "success": None,
                "status": "loading",
                "gr_book_isbn": None,
                "gr_book_info": None,
                "gr_good_reviews": None,
                "gr_bad_reviews": None,
                "error": None
            }
        })
    #确认失败
    elif gr_result.get("success") is False:
        return JsonResponse({"gr_result": gr_result}, status=404)

    else:
    # 提取成功
        return JsonResponse({"gr_result":gr_result},json_dumps_params={'ensure_ascii': False})
    
    #python manage.py runserver
