from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ShiPanRequest, ShiPanResponse
from app.services.daliuren_engine import generate_shipan

app = FastAPI(title="大六壬Web排盤介面 API", version="2.2.1")

# 設定 CORS，讓前端網頁可以跨網域呼叫 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 實務上請設定為前端的網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.post("/api/v1/shipan/generate", response_model=ShiPanResponse)
async def create_shipan(request: ShiPanRequest):
    try:
        # 呼叫六壬核心引擎
        html_result = generate_shipan(request)
        
        return ShiPanResponse(
            status="success",
            message="六壬盤起課成功",
            html_content=html_result
        )
    except Exception as e:
        # 這裡的 HTTPException 現在已經被正確引入，可以正常發揮作用了
        raise HTTPException(status_code=500, detail=f"起課失敗: {str(e)}")

# 啟動伺服器指令 (開發測試用)： uvicorn app.main:app --reload