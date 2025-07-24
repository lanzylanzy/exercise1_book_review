from django.http import JsonResponse
from backend.service import pack_db_info, pack_gr_info
import threading
from collections import OrderedDict

#临时缓存
gr_cache = {}
gr_lock = threading.Lock()
MAX_CACHE_SIZE = 10

#提取豆瓣详情信息
def db_info_view(request):
    #关键词
    query = request.GET.get("q")
    if not query:
        return JsonResponse({"success": False, "error": "缺少参数 q"}, status=400)
    db_result = pack_db_info(query)


    isbn = db_result.get("en_version_isbn")

    # 如果有 ISBN，就后台开线程开始抓 GR 数据
    if isbn:
        def run_gr_task():
            try:
                gr_result = pack_gr_info(isbn)
            #有isbn，但抓不到，就返回service里的“Goodreads 未收录该书”错误
            except Exception as e:
                gr_result = {"success": False, "error": str(e)}
            #将通过isbn提取的gr内容存入缓存
            gr_cache[isbn] = gr_result
            with gr_lock:
             # 如果已存在则先删掉再加，避免顺序错乱
                if isbn in gr_cache:
                    del gr_cache[isbn]
            gr_cache[isbn] = gr_result

        # 超过最大缓存长度就删掉最旧的一条
        if len(gr_cache) > MAX_CACHE_SIZE:
            gr_cache.popitem(last=False)  # FIFO 删除最早添加的
        #这行代码表示，开始同步提取gr内容，也就是运行上面那个函数。同时不影响原本函数的返回
        threading.Thread(target=run_gr_task).start()

    return JsonResponse({
        "success": True,
        "db": db_result,
        #如果有isbn，显示正在提取，如果没有，显示none。
        "gr": {"status": "loading"} if isbn else None
    }, json_dumps_params={'ensure_ascii': False})

def gr_info_view(request):
    isbn = request.GET.get("isbn")
    if not isbn:
        return JsonResponse({"success": False, "error": "缺少参数 isbn"}, status=400)
    #把缓存里提取的数据导出
    gr_result = gr_cache.get(isbn)
    
    if gr_result is None:
    # 没提取完
        return JsonResponse({"gr": None, "status": "loading"})
    elif not gr_result.get("success"):
    # 提取失败
        return JsonResponse({"gr": None, "status": "failed", "error": gr_result.get("error")})
    else:
    # 提取成功
        return JsonResponse({"gr": gr_result},json_dumps_params={'ensure_ascii': False})