import boto3
import re

REGION = "us-east-1"
BUCKET = "fincloud-loan-team14-2026"
FILE = "raw/loan_application_1page.pdf"
TABLE = "LoanApplications"

textract = boto3.client("textract", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)

print("步驟 1：正在使用 Textract 辨識文件...")

response = textract.analyze_document(
    Document={
        "S3Object": {
            "Bucket": BUCKET,
            "Name": FILE
        }
    },
    FeatureTypes=["FORMS"]
)

lines = [
    b["Text"]
    for b in response["Blocks"]
    if b["BlockType"] == "LINE"
]

print("辨識到", len(lines), "行文字")

text = "\n".join(lines)

def extract(label):
    pattern = rf"(?im)^\s*{re.escape(label)}\s*:\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if not match:
        raise ValueError("找不到欄位：" + label)
    return match.group(1).strip()

def number(label):
    value = extract(label).replace(",", "")
    if not re.fullmatch(r"\d+", value):
        raise ValueError("數值格式錯誤：" + label)
    return int(value)

item = {
    "application_id": extract("Application ID"),
    "applicant_name": extract("Applicant Name"),
    "monthly_income": number("Monthly Income"),
    "monthly_expenses": number("Monthly Expenses"),
    "loan_amount": number("Loan Amount"),
    "loan_term": number("Loan Term"),
    "status": "PENDING_REVIEW",
    "source_file": FILE
}

print("步驟 2：正在寫入 DynamoDB...")

table = dynamodb.Table(TABLE)
table.put_item(Item=item)

print("步驟 3：正在驗證資料...")

result = table.get_item(
    Key={"application_id": item["application_id"]},
    ConsistentRead=True
)

assert result.get("Item") == item

print("=== MVP SUCCESS ===")
print("Application ID:", item["application_id"])
print("Applicant:", item["applicant_name"])
print("Monthly Income:", item["monthly_income"])
print("Loan Amount:", item["loan_amount"])
print("Status:", item["status"])
print("DynamoDB verification: PASS")
