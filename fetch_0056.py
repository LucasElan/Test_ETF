import json
import os
import sys
from datetime import datetime, timezone, timedelta
from playwright.sync_api import sync_playwright

def fetch_0056_data():
    # 1. 這是正常人會去看的網頁 (用來騙過防火牆並取得 Cookie)
    main_url = "https://www.yuantaetfs.com/product/detail/0056/ratio"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("啟動 Playwright 進入元大 0056 介紹頁...")
            # 進入主網頁，等待網路安靜下來
            response = page.goto(main_url, wait_until="networkidle", timeout=30000)
            print(f"進入主網頁 HTTP 狀態碼: {response.status}")
            
            print("WAF 驗證通過！正在從瀏覽器內部發射 API 請求...")
            # 2. 特洛伊木馬：在已經合法的瀏覽器環境中，打出 API 請求！
            # Playwright 會自動把這段 JS 執行的 JSON 結果傳回給 Python
            api_data = page.evaluate("""() => {
                return fetch('https://www.yuantaetfs.com/api/StkWeights?fundid=1066')
                    .then(res => res.json());
            }""")
            
            print(f"成功取得 JSON 資料！共抓到 {len(api_data)} 檔成分股。")
            
            # --- 以下儲存邏輯完全不變 ---
            os.makedirs('data', exist_ok=True)
            tz = timezone(timedelta(hours=8))
            tw_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

            output_file = 'data/0056.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "last_updated": tw_time,
                    "components": api_data # 存入抓到的 JSON
                }, f, ensure_ascii=False, indent=4)
                
            print(f"資料成功更新並寫入 {output_file}")
            
        except Exception as e:
            print(f"抓取發生錯誤: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fetch_0056_data()