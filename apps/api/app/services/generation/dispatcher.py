# 負責啟動 generation，不做實際生成

def dispatch_generation(request):
    """
    - 驗證 request
    - 建立 generation_id
    - 丟給 background worker
    """
    pass
