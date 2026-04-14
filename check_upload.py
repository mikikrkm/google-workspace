import urllib.request
import urllib.error
import json

API_URL = "https://av45ti0j66.execute-api.ap-northeast-1.amazonaws.com/getUploadUrl"

print("=== S3アップロードAPI確認 ===\n")

# ① 署名URL取得テスト
print("① getUploadUrl APIを呼び出し中...")
try:
    data = json.dumps({"fileName": "test.png", "fileType": "image/png"}).encode()
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    res = urllib.request.urlopen(req, timeout=10)
    body = res.read().decode()
    result = json.loads(body)
    print(f"  ✅ ステータス: {res.status}")
    print(f"  ✅ 署名URL取得成功")

    signed_url = result.get("url", "")
    if signed_url:
        print(f"  ✅ URL先頭: {signed_url[:80]}...")
    else:
        print("  ❌ URLが返ってきていません")
        print(f"  レスポンス内容: {result}")

except urllib.error.HTTPError as e:
    print(f"  ❌ HTTPエラー: {e.code} {e.reason}")
    print(f"  レスポンス: {e.read().decode()}")
except urllib.error.URLError as e:
    print(f"  ❌ 接続エラー: {e.reason}")
except Exception as e:
    print(f"  ❌ 予期しないエラー: {e}")

print("\n=== 確認完了 ===")
