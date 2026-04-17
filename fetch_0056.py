import requests
import json
import os
from datetime import datetime, timezone, timedelta

def fetch_0056_data():
    # 元大投信官網取得 ETF 權重的隱藏 API 端點 (0056 的內部 fundid 通常是 1066)
    url = "https://www.yuantaetfs.com/api/StkWeights?fundid=1066"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        print("開始從元大官網抓取資料...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 建立 data 資料夾存放靜態資料
        os.makedirs('data', exist_ok=True)
        
        # 取得台灣時間 (UTC+8)
        tz = timezone(timedelta(hours=8))
        tw_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

        # 整理並寫入 JSON 檔案
        output_file = 'data/0056.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "last_updated": tw_time,
                "components": data
            }, f, ensure_ascii=False, indent=4)
            
        print(f"資料成功更新並寫入 {output_file}")
        
    except Exception as e:
        print(f"抓取資料時發生錯誤: {e}")

if __name__ == "__main__":
    fetch_0056_data()