from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class ShiPanRequest(BaseModel):
    year: int = Field(..., ge=1920, le=2100, description="起課年份")
    month: int = Field(..., ge=1, le=12, description="起課月份")
    day: int = Field(..., ge=1, le=31, description="起課日期")
    hour: int = Field(..., ge=0, le=23, description="起課小時")
    minute: int = Field(..., ge=0, le=59, description="起課分鐘")
    second: int = Field(0, ge=0, le=59, description="起課秒數")
    
    # 專屬參數
    gender: int = Field(0, description="0: 男, 1: 女")
    birth_year: int = Field(..., ge=1920, le=2100, description="求測者出生年 (本命)")
    is_daytime: bool = Field(True, description="是否為晝占 (影響貴人順逆)")
    is_mingpan: bool = Field(False, description="是否為命局 (False為事占)")
    query_matter: str = Field("", description="占測之事 (捕捉意念)")

class ShiPanResponse(BaseModel):
    status: str
    message: str
    html_content: Optional[str] = None 

# ==========================================================
# 強型別 JSON-First 回傳模型
# ==========================================================

class FourPillars(BaseModel):
    year: str = Field(..., description="年柱干支")
    month: str = Field(..., description="月柱干支")
    day: str = Field(..., description="日柱干支")
    hour: str = Field(..., description="時柱干支")

class SolarTerms(BaseModel):
    current: str = Field(..., description="當前節氣與交接時間")
    next: str = Field(..., description="下一中氣與交接時間")

class BasicInfo(BaseModel):
    time: str = Field(..., description="西元起課標準時間")
    four_pillars: FourPillars = Field(..., description="四柱八字資訊")
    solar_terms: SolarTerms = Field(..., description="曆法節氣數據")
    yue_jiang: str = Field(..., description="當前月將")
    zhan_shi: str = Field(..., description="起課占時")
    day_night: str = Field(..., description="晝夜占判定結果")
    kong_wang: List[str] = Field(..., description="旬落空亡之地支清單")

class ChuanState(BaseModel):
    liu_qin: str = Field(..., description="六親 (財/官/父/兄/子)")
    dun_gan: str = Field(..., description="天盤遁干")
    di_zhi: str = Field(..., description="傳遞地支")
    tian_jiang: str = Field(..., description="所乘十二天將")
    is_kong_wang: bool = Field(..., description="該傳地支是否落入空亡")

class SanChuanData(BaseModel):
    chu: ChuanState = Field(..., description="初傳 (發用)")
    zhong: ChuanState = Field(..., description="中傳")
    mo: ChuanState = Field(..., description="末傳")

class KeState(BaseModel):
    ke_shang: str = Field(..., description="課上神 (天盤)")
    ke_xia: str = Field(..., description="課下神 (地盤)")
    tian_jiang: str = Field(..., description="所乘天將")

class SiKeData(BaseModel):
    ke1: KeState = Field(..., description="第一課 (日干陽神)")
    ke2: KeState = Field(..., description="第二課 (日干陰神)")
    ke3: KeState = Field(..., description="第三課 (日支陽神)")
    ke4: KeState = Field(..., description="第四課 (日支陰神)")

class TianDiPanState(BaseModel):
    tian_pan: str = Field(..., description="天盤落宮地支")
    tian_jiang: str = Field(..., description="天盤地支所乘之天將")

class ShiPanJsonData(BaseModel):
    basic_info: BasicInfo = Field(..., description="基本曆法與空亡資訊")
    san_chuan: SanChuanData = Field(..., description="三傳事態軌跡數據")
    si_ke: SiKeData = Field(..., description="四課主客現狀數據")
    tian_di_pan: Dict[str, TianDiPanState] = Field(..., description="完整天地盤與十二神佈局 (地盤十二宮映射)")
    格局: List[str] = Field(..., description="觸發之大六壬卦體格局清單")

class ShiPanJsonResponse(BaseModel):
    status: str
    message: str
    data: Optional[ShiPanJsonData] = None