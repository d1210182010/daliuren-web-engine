import sys
import os

from opencc import OpenCC
from app.repo_core.common import GetLi, GetShiChen, DiZHiList
from app.repo_core.shipan.shipan import ShiPan, MinGPan

def _get_engine_object(req_data):
    li_data = GetLi(
        req_data.year, req_data.month, req_data.day, 
        req_data.hour, req_data.minute, req_data.second
    )
    yuejiang_obj = li_data[4] 
    yuejiang_str = DiZHiList[yuejiang_obj.num - 1]
    zhanshi_obj = GetShiChen(req_data.hour)
    zhanshi_str = DiZHiList[zhanshi_obj.num - 1]
    
    if req_data.is_mingpan:
        return MinGPan(
            req_data.year, req_data.month, req_data.day, 
            req_data.hour, req_data.minute, req_data.second, 
            yuejiang_str, zhanshi_str, req_data.is_daytime,
            req_data.query_matter, req_data.gender, req_data.birth_year
        )
    else:
        return ShiPan(
            req_data.year, req_data.month, req_data.day, 
            req_data.hour, req_data.minute, req_data.second, 
            yuejiang_str, zhanshi_str, req_data.is_daytime,
            req_data.query_matter, req_data.gender, req_data.birth_year
        )

def generate_shipan(req_data) -> str:
    sq = _get_engine_object(req_data)
    cc = OpenCC('s2t')
    html_content = cc.convert(sq.toHml)
    html_content = html_content.replace('後', '后')
    html_content = html_content.replace('佔', '占')
    html_content = html_content.replace('醜', '丑')
    return html_content

def generate_shipan_json(req_data) -> dict:
    sp = _get_engine_object(req_data)
    cc = OpenCC('s2t')
    
    def clean_str(s):
        if not s:
            return ""
        res = cc.convert(str(s))
        res = res.replace('後', '后')
        res = res.replace('佔', '占')
        res = res.replace('醜', '丑')
        return res

    kw_list = [clean_str(k) for k in sp.空亡]

    # 動態萃取完整天地盤與十二神佈局
    tian_di_pan_data = {}
    for dz in ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]:
        from ganzhiwuxin.ganzhiwuxin import 支
        dz_obj = 支(dz)
        tp_branch = sp.tp[dz_obj]
        tian_di_pan_data[dz] = {
            "tian_pan": clean_str(tp_branch),
            "tian_jiang": clean_str(sp.tianJiang[tp_branch])
        }

    return {
        "basic_info": {
            "time": f"{sp.year}-{sp.month:02d}-{sp.day:02d} {sp.hour:02d}:{sp.minutes:02d}:{sp.second:02d}",
            "four_pillars": {
                "year": clean_str(sp.四柱與節氣[0] if hasattr(sp, '四柱與節氣') else sp.四柱停靠 if False else sp.四柱与节气[0]),
                "month": clean_str(sp.四柱与节气[1]),
                "day": clean_str(sp.四柱与节气[2]),
                "hour": clean_str(sp.四柱with_term if False else sp.四柱隔 if False else sp.四柱与节气[3])
            },
            "solar_terms": {
                "current": clean_str(sp.四柱与节气[5]),
                "next": clean_str(sp.四柱与节气[6])
            },
            "yue_jiang": clean_str(sp.yueJiang),
            "zhan_shi": clean_str(sp.zhanShi),
            "day_night": "晝占" if sp.昼占 else "夜占",
            "kong_wang": kw_list
        },
        "san_chuan": {
            "chu": {
                "liu_qin": clean_str(sp.sc.六亲[0]),
                "dun_gan": clean_str(sp.sc.遁干[0]),
                "di_zhi": clean_str(sp.sc.初),
                "tian_jiang": clean_str(sp.tianJiang[sp.sc.初]),
                "is_kong_wang": clean_str(sp.sc.初) in kw_list
            },
            "zhong": {
                "liu_qin": clean_str(sp.sc.六亲[1]),
                "dun_gan": clean_str(sp.sc.遁干[1]),
                "di_zhi": clean_str(sp.sc.中),
                "tian_jiang": clean_str(sp.tianJiang[sp.sc.中]),
                "is_kong_wang": clean_str(sp.sc.中) in kw_list
            },
            "mo": {
                "liu_qin": clean_str(sp.sc.六亲[2]),
                "dun_gan": clean_str(sp.sc.遁干[2]),
                "di_zhi": clean_str(sp.sc.末),
                "tian_jiang": clean_str(sp.tianJiang[sp.sc.末]),
                "is_kong_wang": clean_str(sp.sc.末) in kw_list
            }
        },
        "si_ke": {
            "ke1": { "ke_shang": clean_str(sp.sk.干阳神), "ke_xia": clean_str(sp.sk.干), "tian_jiang": clean_str(sp.tianJiang[sp.sk.干阳神]) },
            "ke2": { "ke_shang": clean_str(sp.sk.干陰神 if hasattr(sp.sk, '干陰神') else sp.sk.干阴神), "ke_xia": clean_str(sp.sk.干阳神), "tian_jiang": clean_str(sp.tianJiang[sp.sk.干阴神]) },
            "ke3": { "ke_shang": clean_str(sp.sk.支阳神), "ke_xia": clean_str(sp.sk.支), "tian_jiang": clean_str(sp.tianJiang[sp.sk.支阳神]) },
            "ke4": { "ke_shang": clean_str(sp.sk.支阴神), "ke_xia": clean_str(sp.sk.支阳神), "tian_jiang": clean_str(sp.tianJiang[sp.sk.支阴神]) }
        },
        "tian_di_pan": tian_di_pan_data,
        "格局": [clean_str(g) for g in sp.格局]
    }