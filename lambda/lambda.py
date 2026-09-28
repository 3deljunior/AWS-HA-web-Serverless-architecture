import os
import base64
import urllib.parse
import boto3

s3 = boto3.client("s3")

DEST_BUCKET = "task1-filtered-copy-893877416641-eu-central-1-an"

def lambda_handler(event, context):
    records = event.get("Records", [])
    if not records:
        return {"statusCode": 400, "body": "No records found"}

    processed = []
    for record in records:
        src_bucket = record["s3"]["bucket"]["name"]
        src_key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        obj = s3.get_object(Bucket=src_bucket, Key=src_key)
        raw_bytes = obj["Body"].read()
        content_type = obj.get("ContentType", "image/png")

        b64_img = base64.b64encode(raw_bytes).decode("ascii")
        data_uri = f"data:{content_type};base64,{b64_img}"

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%">
  <filter id="visual-change">
    <feColorMatrix type="matrix" values="-1 0 0 0 1
                                         0 -1 0 0 1
                                         0 0 -1 0 1
                                         0 0 0 1 0"/>
  </filter>
  <image href="{data_uri}" width="100%" height="100%" filter="url(#visual-change)"/>
</svg>"""

        base_name = os.path.splitext(os.path.basename(src_key))[0]
        dest_key = f"processed-{base_name}.svg"

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=dest_key,
            Body=svg_content.encode("utf-8"),
            ContentType="image/svg+xml"
        )
        processed.append(dest_key)

    return {
        "statusCode": 200,
        "body": f"Done! Created visually transformed file: {processed}"
    }