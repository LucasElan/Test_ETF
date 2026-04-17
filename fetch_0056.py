import json
import os
import sys
from datetime import datetime, timezone, timedelta
import cloudscraper # 引入新的秘密武器

def fetch_0056_data():
    url = "https://www.yuantaetfs.com/api/StkWeights?fundid=1066"
    
    try:
        print("開始從元大官網抓取資料 (使用 Cloudscraper 模式)...")
        
        # 建立一個模擬真實 Chrome 瀏覽器的 scraper
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        response = scraper.get(url, timeout=15)
        print(f"伺服器回傳 HTTP 狀態碼: {response.status_code}")
        
        # 把伺服器回傳的真實內容印出前 100 個字，方便除錯
        print(f"伺服器回傳內容前 100 字: {response.text[:100]}")
        
        response.raise_for_status()
        
        # 嘗試解析 JSON
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
        
    except json.JSONDecodeError:
        print("錯誤：伺服器回傳的不是有效的 JSON 格式。這通常代表我們還是被防火牆擋下，回傳了驗證網頁。")
        sys.exit(1)
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_0056_data()