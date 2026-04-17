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

        try:
            print("啟動 Playwright 進入元大 0056 介紹頁...")
            # 1. 進入主網頁，等待網路安靜
            page.goto(main_url, wait_until="networkidle", timeout=30000)
            
            print("網頁載入完成，正在模擬人類眼睛掃描畫面上的表格...")
            # 2. 故意等 3 秒，確保前端框架把表格完全畫出來
            page.wait_for_timeout(3000) 

            # 3. 視覺暴力破解法：直接從網頁的 HTML 元素中抓字
            # 我們寫一段 JavaScript 丟進網頁裡執行，讓它幫我們找表格
            api_data = page.evaluate("""() => {
                let results = [];
                // 抓取網頁中所有的表格橫列 (tr)
                let rows = document.querySelectorAll("tr");
                
                rows.forEach(row => {
                    // 抓取每一列裡面的所有格子 (td)
                    let cols = row.querySelectorAll("td");
                    
                    // 正常的成分股表格至少會有：代號、名稱、權重 這三欄
                    if(cols.length >= 3) {
                        let id = cols[0].innerText.trim();
                        let name = cols[1].innerText.trim();
                        // 把權重欄位的 % 號去掉，方便之後處理
                        let weightStr = cols[2].innerText.trim().replace('%', '').trim();
                        
                        // 關鍵過濾條件：確定第一欄是股票代號 (數字)，且第三欄是權重 (可轉成數字)
                        if(/^[0-9]+$/.test(id) && !isNaN(parseFloat(weightStr))) {
                            results.push({
                                "stkCd": id,      // 對應你前端 index.html 寫的變數
                                "stkNm": name,
                                "weights": weightStr
                            });
                        }
                    }
                });
                return results;
            }""")
            
            # 4. 檢查是否有成功刮到資料
            if api_data and len(api_data) > 0:
                print(f"太棒了！直接從畫面上成功刮下 {len(api_data)} 檔成分股資料。")
                
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
                print("❌ 錯誤：在網頁畫面上找不到符合格式的表格資料。網站排版可能不符合預期。")
                sys.exit(1)
                
        except Exception as e:
            print(f"抓取發生錯誤: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    fetch_0056_data()