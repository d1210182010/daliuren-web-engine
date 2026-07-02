from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.models.schemas import ShiPanRequest, ShiPanResponse, ShiPanJsonResponse
from app.services.daliuren_engine import generate_shipan, generate_shipan_json

app = FastAPI(title="大六壬 Web排盤介面 API", version="2.2.1")

# GZip 壓縮：HTML/JSON 回應體積約可減少 70%
app.add_middleware(GZipMiddleware, minimum_size=1024)

# 設定 CORS，開放外部呼叫 API（本站前端為同源，不受此影響）
# 注意：allow_origins=["*"] 依規範不可與 allow_credentials=True 並用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML 頁面：no-cache 讓瀏覽器每次重新驗證（有 ETag，未變動時回 304），
# 避免 deploy 更新後使用者仍看到舊頁面
def _page(filename: str) -> FileResponse:
    return FileResponse(filename, headers={"Cache-Control": "no-cache"})

@app.get("/")
async def serve_frontend():
    return _page("index.html")

@app.get("/privacy.html", include_in_schema=False)
async def privacy_page():
    return _page("privacy.html")

@app.get("/tutorial.html", include_in_schema=False)
async def tutorial_page():
    return _page("tutorial.html")

@app.get("/knowledge.html", include_in_schema=False)
async def knowledge_page():
    return _page("knowledge.html")

@app.get("/favicon.svg", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.svg", media_type="image/svg+xml",
                        headers={"Cache-Control": "public, max-age=604800"})

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("robots.txt", media_type="text/plain",
                        headers={"Cache-Control": "public, max-age=86400"})

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse("sitemap.xml", media_type="application/xml",
                        headers={"Cache-Control": "public, max-age=86400"})

@app.post("/api/v1/shipan/generate", response_model=ShiPanResponse)
async def create_shipan(request: ShiPanRequest):
    try:
        # 呼叫六壬 HTML 渲染引擎
        html_result = generate_shipan(request)
        
        return ShiPanResponse(
            status="success",
            message="六壬盤起課成功",
            html_content=html_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"起課失敗: {str(e)}")

@app.post("/api/v1/shipan/json", response_model=ShiPanJsonResponse)
async def create_shipan_json(request: ShiPanRequest):
    """
    正式回應挑戰者：提供強型別、結構化、JSON-First 的大六壬純數據提取端點
    """
    try:
        # 呼叫六壬數據萃取引擎
        json_result = generate_shipan_json(request)
        
        return ShiPanJsonResponse(
            status="success",
            message="六壬純數據結構序列化成功",
            data=json_result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON結構提取失敗: {str(e)}")

# 啟動伺服器指令： uvicorn app.main:app --reload