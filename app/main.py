from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ShiPanRequest, ShiPanResponse, ShiPanJsonResponse
from app.services.daliuren_engine import generate_shipan, generate_shipan_json

app = FastAPI(title="大六壬 Web排盤介面 API", version="2.2.1")

# 設定 CORS，讓前端網頁可以跨網域呼叫 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.get("/privacy.html", include_in_schema=False)
async def privacy_page():
    return FileResponse("privacy.html")

@app.get("/tutorial.html", include_in_schema=False)
async def tutorial_page():
    return FileResponse("tutorial.html")

@app.get("/knowledge.html", include_in_schema=False)
async def knowledge_page():
    return FileResponse("knowledge.html")

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