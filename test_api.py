import urllib.request
import urllib.parse
import json

# テスト1: /をエンコードしない方式
key = "VI管理/やさしえ/PHO_000001.jpeg"
encoded = "/".join(urllib.parse.quote(seg, safe="") for seg in key.split("/"))
url = "https://ry8yzf95ea.execute-api.ap-northeast-1.amazonaws.com/miki-assets-test_3/getSignedUrl?key=" + encoded
print("=== テスト1: /をエンコードしない ===")
print("REQUEST URL:", url)
try:
    r = urllib.request.urlopen(url, timeout=10)
    body = r.read().decode("utf-8")
    print("RESPONSE:", body)
    data = json.loads(body)
    print("URL:", data.get("url", "なし"))
except Exception as e:
    print("ERROR:", e)

print()

# テスト2: /もエンコードする方式（元のコード）
encoded2 = urllib.parse.quote(key, safe="")
url2 = "https://ry8yzf95ea.execute-api.ap-northeast-1.amazonaws.com/miki-assets-test_3/getSignedUrl?key=" + encoded2
print("=== テスト2: /もエンコード ===")
print("REQUEST URL:", url2)
try:
    r2 = urllib.request.urlopen(url2, timeout=10)
    body2 = r2.read().decode("utf-8")
    print("RESPONSE:", body2)
    data2 = json.loads(body2)
    print("URL:", data2.get("url", "なし"))
except Exception as e:
    print("ERROR:", e)
