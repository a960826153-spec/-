# 第 14 組數位申貸 AWS MVP 重現步驟

## 1. 專題目的

本專題使用 AWS 雲端服務，建立申貸 PDF 文件辨識及案件建檔原型。

已驗證流程：

Amazon S3 → Amazon Textract → Python → Amazon DynamoDB

本次為教學用途，使用完全虛構的模擬申貸資料。

## 2. 執行環境

- AWS Region：us-east-1
- AWS 環境：Learner Lab
- 執行工具：AWS CloudShell
- 程式語言：Python 3
- 主要套件：boto3
- S3 Bucket：fincloud-loan-team14-2026
- S3 文件：raw/loan_application_1page.pdf
- DynamoDB Table：LoanApplications
- 測試案件：LOAN001

## 3. 執行前準備

執行者必須具有授權的 AWS 存取權限。

執行前應確認：

1. S3 Bucket 已存在。
2. 測試 PDF 已上傳至 S3。
3. DynamoDB 的 LoanApplications 資料表已存在，並以 application_id 為主鍵。
4. AWS 身分具有 S3 讀取、Textract 文件分析及 DynamoDB 讀寫權限。

目前程式使用既有 AWS 資源，不會自動建立整套雲端環境。

## 4. 重現步驟

取得 GitHub Repository 的授權存取權後，在 AWS CloudShell 執行：

```bash
git clone https://github.com/a960826153-spec/-.git team14-repo
cd team14-repo/digital-loan
python3 -m pip install -r requirements.txt
export AWS_DEFAULT_REGION=us-east-1
aws s3 ls s3://fincloud-loan-team14-2026/raw/loan_application_1page.pdf
python3 app.py
```

注意：Private Repository 的下載須有適當 GitHub 權限。若無法直接 clone，可透過已授權方式取得程式檔案。

## 5. 原始測試結果

已完成一次模擬申貸 PDF 端到端處理。

原始成功結果：

```text
辨識到 22 行文字
MVP SUCCESS
Application ID: LOAN001
Applicant: Test User A
Monthly Income: 50000
Loan Amount: 300000
Status: PENDING_REVIEW
DynamoDB verification: PASS
```

上述為已取得的測試結果。實際重新執行時，應重新檢查當次執行結果。

## 6. 成功驗證截圖

- screenshots/01_s3_upload.png
- screenshots/02_textract_success.png
- screenshots/03_dynamodb_result.png

## 7. MVP 限制

目前已完成單筆申貸文件的手動端到端流程。

尚未完成：
- S3 事件觸發
- AWS Lambda 自動執行
- 文件信心分數自動分流
- 人工覆核介面
- 完整金融正式環境治理

本次 MVP 不包含實際授信或自動核貸功能。

## 8. 重現驗證狀態

原始 AWS MVP：已成功驗證。

從 GitHub main 於全新工作目錄重現：待再次確認。

從全新 AWS 帳戶建立所有資源：尚未驗證。
