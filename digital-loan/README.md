# 金融上雲實務 — 第 14 組數位申貸專題

## 1. 專題介紹

本專題以數位申貸流程為研究主題，透過 AWS 雲端服務建立申貸文件自動化處理原型，減少人工輸入資料的工作。

**Product Goal：** 建立一套能自動擷取申貸文件資料並建立案件紀錄的雲端原型，提升申貸資料處理效率。

## 2. AWS 系統架構

目前 MVP 流程：

1. Amazon S3：儲存模擬申貸 PDF。
2. Amazon Textract：辨識申貸文件中的欄位與文字。
3. Python / AWS CloudShell：解析欄位、建立案件資料。
4. Amazon DynamoDB：儲存申貸案件及審核狀態。

目前採用手動執行 Python 程式的批次流程，尚未實作上傳事件自動觸發。

## 3. AWS 環境資訊

- Region：us-east-1
- S3 Bucket：fincloud-loan-team14-2026
- S3 Object：raw/loan_application_1page.pdf
- DynamoDB Table：LoanApplications
- Partition Key：application_id（String）
- Python 套件：boto3

## 4. MVP 測試結果

已使用模擬申貸文件進行測試。

- Application ID：LOAN001
- Applicant Name：Test User A
- Monthly Income：50000
- Loan Amount：300000
- Loan Term：36
- Application Status：PENDING_REVIEW

測試結果：

- S3 文件上傳成功
- Textract API 成功辨識 22 行文字
- DynamoDB 寫入成功
- DynamoDB 讀回資料驗證 PASS

以上為單筆測試結果，不代表已完成正式環境部署或大量文件測試。

## 5. 重現步驟

1. 準備具備 S3、Textract、DynamoDB 所需權限的 AWS 環境。
2. 選擇 us-east-1。
3. 建立私有且加密的 S3 Bucket，並上傳測試文件至 raw/。
4. 建立 DynamoDB 資料表 LoanApplications，主鍵為 application_id（String）。
5. 安裝 requirements.txt 中的 Python 套件。
6. 依實際環境修改 app.py 中的 Bucket、文件路徑及資料表名稱。
7. 使用具有適當 AWS 權限的環境執行：

   `python3 app.py`

8. 確認出現 MVP SUCCESS 與 DynamoDB verification: PASS。
9. 在 DynamoDB Explore items 查詢 LOAN001。

測試文件與程式僅供教學環境使用，不包含真實申貸資料。

## 6. Scrum 團隊資訊

- Product Owner：待填
- Scrum Master：待填
- 開發組員：待填
- Product Backlog 看板：待填
- Sprint 1–2 Retro 紀錄：待補
- 專案決策紀錄：待補
- 10/29 業師回饋與調整：待補

## 7. 資料安全

- 僅使用虛構申貸資料
- S3 採私人存取與儲存加密
- 不將 AWS 金鑰、密碼或其他憑證上傳 GitHub
- DynamoDB 案件狀態為待人工審核
- 正式環境仍須補齊最小權限、稽核、個資保護及人工覆核機制

## 8. AI 使用聲明

本專題使用生成式 AI 輔助 AWS 操作流程規劃、Python 程式撰寫與文件整理。組員實際在 AWS Learner Lab 執行程式，並以 CloudShell 和 DynamoDB 查詢結果驗證 MVP。

AI 產出內容仍由組員檢查與確認，實際實作結果以 AWS 測試紀錄為準。
