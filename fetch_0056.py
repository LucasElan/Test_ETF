import json
import os
import sys
from datetime import datetime, timezone, timedelta
from playwright.sync_api import sync_playwright

def fetch_0056_data():
    url = "https://www.yuantaetfs.com/api/StkWeights?fundid=1066"
    
    # 啟動 Playwright
    with sync_playwright() as p:
        # 開啟隱形的 Chromium 瀏覽器
        browser = p.chromium.launch(headless=True)
        # 偽裝成一般的 Windows Chrome
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("啟動隱形瀏覽器 (Playwright) 嘗試破解 WAF JS 挑戰...")
            
            # 指揮瀏覽器前往網址，並等待網路安靜下來 (確保 JS 挑戰執行完並重新載入)
            response = page.goto(url, wait_until="networkidle", timeout=20000)
            print(f"最終 HTTP 狀態碼: {response.status}")
            
            # 直接抓取瀏覽器畫面上顯示的文字內容
            content = page.inner_text("body")
            print(f"伺服器回傳內容前 100 字: {content[:100]}")
            
            # 嘗試將文字解析為 JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                print("解析失敗！伺服器畫面上的文字不是有效的 JSON。WAF 可能啟動了更嚴格的圖形驗證碼。")
                sys.exit(1)
            
            # --- 以下儲存邏輯不變 ---
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
            print(f"瀏覽器操作發生錯誤: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fetch_0056_data()