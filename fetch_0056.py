import json
import os
import sys
from datetime import datetime, timezone, timedelta
from playwright.sync_api import sync_playwright

def fetch_0056_data():
    main_url = "https://www.yuantaetfs.com/product/detail/0056/ratio"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # 準備一個變數來裝攔截到的資料
        api_data = None
        
        # 1. 架設監聽器：當瀏覽器收到任何網路回應時，這個函數就會被觸發
        def handle_response(response):
            nonlocal api_data
            # 如果網址包含 StkWeights，且狀態碼是 200，我們就攔截它的內容！
            if "StkWeights" in response.url and response.status == 200:
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"🎯 成功在背景流量中攔截到目標 JSON！")
                        api_data = data
                except:
                    pass

        # 將監聽器綁定到網頁上
        page.on("response", handle_response)

        try:
            print("啟動 Playwright 進入元大 0056 介紹頁...")
            print("📡 網路監聽器已啟動，正在靜靜等待網頁自己下載資料...")
            
            # 2. 進入主網頁，等待所有網路活動靜止
            page.goto(main_url, wait_until="networkidle", timeout=30000)
            
            # 稍微等個 3 秒，確保網頁把資料都消化完
            page.wait_for_timeout(3000) 

            # 3. 檢查有沒有攔截到東西
            if api_data:
                print(f"太棒了！共攔截到 {len(api_data)} 檔成分股資料。")
                
                os.makedirs('data', exist_ok=True)
                tz = timezone(timedelta(hours=8))
                tw_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

                output_file = 'data/0056.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "last_updated": tw_time,
                        "components": api_data
                    }, f, ensure_ascii=False, indent=4)
                    
                print(f"資料成功更新並寫入 {output_file}")
            else:
                print("❌ 錯誤：網頁已載入完成，但在背景流量中沒有抓到 API 資料。")
                sys.exit(1)
                
        except Exception as e:
            print(f"抓取發生錯誤: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fetch_0056_data()