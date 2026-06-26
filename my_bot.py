import time
import requests

TG_TOKEN = '8686193027:AAE8eJCfdr3uMItSjXTa8Jiyr76CLg4OM3o'
TG_CHAT_ID = '7023602154'

def send(msg):
    try:
        # 增加 timeout 設定防止卡死
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                      json={"chat_id": TG_CHAT_ID, "text": msg}, timeout=15)
    except Exception as e:
        print(f"發送失敗: {e}")

print("🤖 雲端監控系統已啟動...")

last_id = 0
while True:
    try:
        # 使用更穩定的 API 請求方式
        url = f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates?offset={last_id+1}&timeout=15"
        res = requests.get(url, timeout=20).json()
        
        if res.get('result'):
            for update in res['result']:
                last_id = update['update_id']
                text = update['message'].get('text', '').lower()
                
                if "/sell " in text or "/buy " in text:
                    coin = text.split()[-1].upper()
                    # 這裡將取得資料的過程分離出來，避免網路波動中斷
                    send(f"📥 正在查詢 {coin} 行情...")
                    
                    # 確保 API 請求格式正確
                    ticker_url = f"https://open-api.bingx.com/openApi/swap/v2/quote/ticker?symbol={coin}-USDT"
                    ticker = requests.get(ticker_url, timeout=15).json()
                    
                    if ticker.get('code') == 0 and ticker.get('data'):
                        price = float(ticker['data'][0]['lastPrice'])
                        send(f"✅ {coin} 目前價格: {price:.4f}\n系統計算中...")
                    else:
                        send(f"❌ 網路異常或代碼錯誤，請檢查 {coin} 是否正確。")
        time.sleep(2)
    except Exception as e:
        print(f"運行中錯誤: {e}")
        time.sleep(10)
