import requests
import re # 匯入正規表示式模組
from typing import List, Dict

YAHOO_SEARCH_URLS = [
	"https://query2.finance.yahoo.com/v1/finance/search",
	"https://query1.finance.yahoo.com/v1/finance/search",
]

DEFAULT_HEADERS = {
	"User-Agent": (
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) "
		"Chrome/124.0.0.0 Safari/537.36"
	),
	"Accept": "application/json, text/plain, */*",
	"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
	"Origin": "https://finance.yahoo.com",
    "Referer": "https://finance.yahoo.com/",
	"Connection": "keep-alive",
}


def search_yahoo_stocks(query: str, limit: int = 10) -> List[Dict[str, str]]:
	"""
	呼叫 Yahoo Finance 搜尋API 取得台股股票建議清單。
	- 使用 query2 為主、query1 為備援
	- 送出常見 Header 以避免被擋
	- 多策略查詢並過濾為台股
	"""
	if not query:
		return []

	search_queries = [query, f"{query} TW", f"{query} 台股"]
	all_results: List[Dict[str, str]] = []

	for url in YAHOO_SEARCH_URLS:
		for term in search_queries:
			params = {
				"q": term,
				"quotesCount": max(20, limit * 2),
				"newsCount": 0,
				"lang": "zh-TW",
				"region": "TW",
			}
			try:
				resp = requests.get(url, params=params, headers=DEFAULT_HEADERS, timeout=8)
				status = resp.status_code
				if status != 200:
					print(f"Yahoo 搜尋非200回應 (url={url}, term={term}, status={status})")
					continue
				
				data = resp.json() or {}
				quotes = data.get("quotes", [])
				
				for q in quotes:
					symbol = q.get("symbol") or ""
					if not symbol:
						continue

					if is_taiwan_stock(symbol, q):
						code = symbol.split(".")[0]
						# *** 修改點：優先使用 longname，因為它通常是完整的中文名稱 ***
						name = q.get("longname") or q.get("shortname") or code
						
						if not any(r["code"] == code for r in all_results):
							all_results.append({"code": code, "name": name})

			except requests.exceptions.RequestException as e:
				print(f"Yahoo 搜尋請求失敗 (url={url}, term={term}): {e}")
				continue
			except Exception as e:
				print(f"Yahoo 搜尋發生未知錯誤 (url={url}, term={term}): {e}")
				continue
		
		if all_results:
			break

	seen = set()
	unique_results: List[Dict[str, str]] = []
	for item in all_results:
		key = (item["code"], item["name"])
		if key in seen:
			continue
		seen.add(key)
		unique_results.append(item)

	return unique_results[:limit]


def is_taiwan_stock(symbol: str, quote_data: dict) -> bool:
	"""判斷是否為台股股票（增加中文名稱檢查）"""
	# 1) 後綴判斷 (最準確)
	if symbol.endswith((".TW", ".TWO")):
		return True
	# 2) 交易所判斷
	exchange = (quote_data.get("exchange") or "").upper()
	if exchange in ("TWSE", "TPEX", "TAI"):
		return True
		
	name = quote_data.get("longname") or quote_data.get("shortname") or ""
	# 3) *** 新增：名稱包含中文字元，能有效過濾掉純英文名稱的結果 ***
	if re.search(r'[\u4e00-\u9fff]', name):
		return True

	# 4) 代碼形狀判斷 (作為備用)
	code = symbol.split(".")[0]
	if code.isdigit() and len(code) >= 4:
		return True
		
	return False