import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const client = new S3Client({ region: "ap-northeast-1" });

// 拡張子からContent-Typeを判定
function getContentType(key) {
  const ext = key.split(".").pop().toLowerCase();
  const map = {
    pdf:  "application/pdf",
    jpg:  "image/jpeg",
    jpeg: "image/jpeg",
    png:  "image/png",
    gif:  "image/gif",
    webp: "image/webp",
    svg:  "image/svg+xml",
    html: "text/html",
    htm:  "text/html",
    zip:  "application/zip",
  };
  return map[ext] || "application/octet-stream";
}

export const handler = async (event) => {
  console.log("EVENT:", JSON.stringify(event));

  // クエリパラメータ "key" を取得（両方式に対応）
  const key =
    event.queryStringParameters?.key ||
    decodeURIComponent(event.rawQueryString?.split("=").slice(1).join("=") || "");

  if (!key) {
    return {
      statusCode: 400,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
      },
      body: JSON.stringify({ error: "key is required" }),
    };
  }

  console.log("KEY:", key);

  const contentType = getContentType(key);

  // ファイル名をキーの末尾から取得
  const filename = key.split("/").pop();

  const command = new GetObjectCommand({
    Bucket: "miki-assets-test",
    Key: key,
    ResponseContentDisposition: `attachment; filename*=UTF-8''${encodeURIComponent(filename)}`,
    ResponseContentType: contentType,
  });

  const url = await getSignedUrl(client, command, { expiresIn: 3600 });

  console.log("SIGNED URL:", url);

  return {
    statusCode: 200,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "*",
    },
    body: JSON.stringify({ url }),
  };
};
