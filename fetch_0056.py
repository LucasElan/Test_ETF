import requests
import json
import os
import sys
from datetime import datetime, timezone, timedelta

def fetch_0056_data():
    url = "https://www.yuantaetfs.com/api/StkWeights?fundid=1066"
    # 增加更多 Header 偽裝成正常瀏覽器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.yuantaetfs.com/product/detail/0056/ratio",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        print("開始從元大官網抓取資料...")
        response = requests.get(url, headers=headers, timeout=10)
        
        # 印出狀態碼，這對除錯非常重要
        print(f"伺服器回傳 HTTP 狀態碼: {response.status_code}")
        
        # 如果不是 200 OK，這行會直接觸發例外錯誤
        response.raise_for_status()
        
        data = response.json()
        
        os.makedirs('data', exist_ok=True)
        tz = timezone(timedelta(hours=8))
        tw_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

        output_file = 'data/0056.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "last_updated": tw_time,
                "components": data
            }, f, ensure_ascii=False, indent=4)
            
        print(f"資料成功更新並寫入 {output_file}")
        
    except Exception as e:
        print(f"抓取資料時發生錯誤: {e}")
        # 強制讓 Python 以錯誤代碼退出，這樣 GitHub Actions 才會標示為紅色的失敗
        sys.exit(1) 

if __name__ == "__main__":
    fetch_0056_data()