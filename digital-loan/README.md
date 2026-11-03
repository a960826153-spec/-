# 金融上雲實務｜第 14 組數位申貸專題

## 1. 專題介紹

### 專題名稱
國泰金控－數位申貸文件自動化處理系統

### 問題與動機
傳統申貸流程需要人工閱讀申請書、輸入申請人資料及建立案件紀錄，不僅耗費時間，也可能因人工輸入而產生錯誤。

本專題運用 AWS 雲端服務，建立數位申貸文件自動化處理原型，透過文件儲存、文字辨識及資料庫管理，減少人工輸入作業。

### Product Goal
建立一套能夠自動擷取申貸文件資料、建立案件紀錄並追蹤處理狀態的雲端原型，提升申貸資料處理效率與準確性。

### 期中 MVP 目標
完成申貸流程的第一階段：

**上傳申貸 PDF → AWS Textract 辨識 → Python 整理資料 → DynamoDB 建立案件紀錄**

目前版本以 Python 手動啟動處理流程，尚未實作網站介面或上傳事件自動觸發。

---

## 2. AWS 系統架構

本專題使用以下 AWS 服務：

| AWS 服務 | 功能 |
|---|---|
| Amazon S3 | 儲存模擬申貸 PDF 文件 |
| Amazon Textract | 辨識申請書中的文字與欄位 |
| AWS CloudShell | 執行 Python 處理程式 |
| Amazon DynamoDB | 儲存申貸案件資料與案件狀態 |

### 資料處理流程

1. 使用者將模擬申貸申請書上傳至 Amazon S3。
2. Python 程式透過 boto3 呼叫 Amazon Textract。
3. Textract 分析 PDF 並回傳文件辨識結果。
4. Python 從辨識文字中擷取申請編號、姓名、月收入、月支出、申貸金額及貸款期限。
5. 將整理後的資料寫入 DynamoDB。
6. 案件狀態設定為 `PENDING_REVIEW`。
7. 從 DynamoDB 重新讀取案件資料，驗證儲存結果。

### 系統目前範圍

已完成：
- S3 文件儲存
- Textract API 文件辨識
- Python 欄位整理
- DynamoDB 案件建立
- 案件資料讀回驗證

尚未完成：
- 前端申貸網站
- S3 事件自動觸發
- 正式貸款審核與授信模型
- 完整的資料治理與稽核系統
- 正式環境部署

---

## 3. AWS 環境設定

### 基本資訊

| 項目 | 設定 |
|---|---|
| AWS Region | us-east-1 |
| S3 Bucket | fincloud-loan-team14-2026 |
| S3 Object Key | raw/loan_application_1page.pdf |
| DynamoDB Table | LoanApplications |
| Partition Key | application_id |
| Partition Key Type | String |
| 程式語言 | Python 3 |
| AWS SDK | boto3 |

以上為第 14 組已測試成功的教學環境設定。不同 AWS 帳號須使用自己建立的 Bucket 與資料表。

### S3 設定

申貸文件存放於：

`s3://fincloud-loan-team14-2026/raw/loan_application_1page.pdf`

儲存空間應保持非公開存取，並啟用伺服器端加密。

### DynamoDB 設定

資料表名稱：`LoanApplications`

主鍵：
- 名稱：`application_id`
- 型別：String

測試案件狀態：`PENDING_REVIEW`

此狀態代表案件等待人工審核，不表示貸款已獲核准。

---

## 4. 專案檔案結構

本次數位申貸專案放在 GitHub 的 `digital-loan/` 資料夾中，與原本上課使用的保險理賠 EDA 範例分開管理。

```text
digital-loan/
├── README.md
├── app.py
├── requirements.txt
└── loan_application_1page.pdf
```

### 檔案用途

| 檔案 | 說明 |
|---|---|
| README.md | 專題介紹、架構與重現步驟 |
| app.py | 執行 Textract 辨識及 DynamoDB 寫入 |
| requirements.txt | Python 套件清單 |
| loan_application_1page.pdf | 虛構申貸資料測試文件 |

---

## 5. MVP 重現步驟

### 步驟一：準備 AWS 環境

使用 AWS Learner Lab 或具備必要權限的 AWS 帳號。

選擇 Region：

`us-east-1`

執行環境須具備以下操作權限：

- S3 物件上傳與讀取
- Textract AnalyzeDocument
- DynamoDB 建立資料表、寫入及讀取資料

### 步驟二：建立 S3 Bucket

1. 開啟 Amazon S3。
2. 建立新的 Bucket。
3. 保持 Block all public access 啟用。
4. 啟用伺服器端加密。
5. 建立 `raw/` 資料夾。
6. 將 `loan_application_1page.pdf` 上傳至 `raw/`。

注意：S3 Bucket 名稱必須全域唯一。如果使用不同名稱，請同步修改 `app.py` 的 `BUCKET` 設定。

### 步驟三：建立 DynamoDB

1. 開啟 Amazon DynamoDB。
2. 建立資料表 `LoanApplications`。
3. Partition key 設為 `application_id`。
4. 資料型別選擇 String。
5. 確認資料表狀態為 Active。

### 步驟四：準備 Python 執行環境

在 AWS CloudShell 或其他已設定 AWS 憑證的環境下載本專案。

進入專案資料夾後，安裝必要套件：

```bash
python3 -m pip install -r requirements.txt
```

使用已授權的 AWS 身分執行，不要將 Access Key 或 Secret Key 寫入程式或上傳到 GitHub。

### 步驟五：確認程式設定

開啟 `app.py`，確認以下設定與實際環境一致：

```python
REGION = "us-east-1"
BUCKET = "fincloud-loan-team14-2026"
FILE = "raw/loan_application_1page.pdf"
TABLE = "LoanApplications"
```

若使用不同 AWS 帳號，請修改為該環境建立的資源名稱。

### 步驟六：執行 MVP

在專案資料夾執行：

```bash
python3 app.py
```

程式會完成：

1. 從 S3 讀取 PDF。
2. 呼叫 Textract API。
3. 整理申貸欄位。
4. 寫入 DynamoDB。
5. 讀回資料並驗證結果。

### 步驟七：確認執行成功

成功時會出現類似結果：

```text
=== MVP SUCCESS ===
Application ID: LOAN001
Applicant: Test User A
Monthly Income: 50000
Loan Amount: 300000
Status: PENDING_REVIEW
DynamoDB verification: PASS
```

### 步驟八：驗證 DynamoDB

1. 進入 DynamoDB。
2. 選擇 Explore items。
3. 選擇 LoanApplications。
4. 執行 Scan 或以申請編號查詢。
5. 確認 `LOAN001` 已寫入。

若能查詢到正確資料，代表案件建立成功。

---

## 6. MVP 實際測試結果

### 測試日期
2026 年 11 月 3 日

### 測試環境
AWS Learner Lab，Region：us-east-1

### 測試文件
`loan_application_1page.pdf`

所有資料均為虛構測試資料，不含真實個資。

### 實際測試資料

| 欄位 | 測試結果 |
|---|---|
| Application ID | LOAN001 |
| Applicant Name | Test User A |
| Monthly Income | 50000 |
| Monthly Expenses | 20000 |
| Loan Amount | 300000 |
| Loan Term | 36 |
| Application Status | PENDING_REVIEW |

### 執行結果

- Amazon S3：文件上傳成功
- Amazon Textract：成功辨識 22 行文字
- Python：成功整理主要申貸欄位
- Amazon DynamoDB：資料寫入成功
- DynamoDB 讀回驗證：PASS

### MVP 驗證結論

本專題已完成單筆模擬申貸文件的端到端處理流程，證明 S3、Textract、Python 與 DynamoDB 可以整合運作。

目前測試僅驗證單筆文件的基本功能，尚未進行大量文件、不同格式或正式申貸情境的完整測試。

---

## 7. 資料安全、法遵與風險

### 個人資料保護

本專題目前僅使用完全虛構的模擬申貸資料，不使用真實姓名、身分證號、銀行帳號或客戶財務資料。

### AWS 安全設計

- S3 儲存空間應限制公開存取。
- 儲存資料應啟用加密。
- 程式不保存 AWS 金鑰。
- AWS 存取應採最小權限原則。
- 申貸案件不由系統直接核准。
- 高風險或辨識不確定的案件應交由人工覆核。

### 主要風險

| 風險 | 可能影響 | 因應方式 |
|---|---|---|
| Textract 辨識錯誤 | 申貸資料不正確 | 欄位檢查與人工覆核 |
| 文件格式不支援 | 無法執行辨識 | 限制格式並提供錯誤處理 |
| AWS 權限不足 | 程式無法執行 | 確認 LabRole 服務權限 |
| 資料存取外洩 | 影響資訊安全 | 私有儲存、加密、最小權限 |
| AWS 額度或成本超出 | 影響實作與運行 | 限制測試次數及監控資源使用 |

### 後續法遵規劃

正式金融環境仍需評估金管會委外相關規定、資料落地位置、保存期限、稽核軌跡、權限管理、跨境資料傳輸及服務退場機制。

上述內容為設計規劃，不代表目前所有法遵與安全功能均已完成實作。

---

## 8. Scrum 專案管理

### 團隊角色

| 角色 | 負責人 |
|---|---|
| Product Owner | 待組員確認 |
| Scrum Master | 待組員確認 |
| AWS MVP 開發 | 待填 |
| 資料分析 | 待填 |
| 文件與簡報整理 | 待填 |

### Product Backlog

由團隊 GitHub Issues 或專案看板管理，預計包含至少 8 則 User Story，並記錄優先級、驗收條件、估點與負責人。

看板連結：待補

### Sprint 計畫

| Sprint | 目標 |
|---|---|
| Sprint 1 | 問題定義、選題、需求與資料規劃 |
| Sprint 2 | AWS MVP、文件辨識、案件資料儲存與期中提案 |
| Sprint 3 | 依期中回饋改進流程與資料品質 |
| Sprint 4 | 擴充功能、驗證與安全設計 |
| Sprint 5 | 完成整合測試、展示與期末成果 |

以上為專題目標規劃，實際 Sprint 紀錄、完成項目及回顧內容應以團隊看板與 GitHub 紀錄為準。

### Sprint 2 Increment

已驗證完成：

- 模擬申貸文件上傳至 S3
- Textract API 文件辨識
- Python 欄位整理
- DynamoDB 案件建立
- 資料讀回驗證

### 待補 Scrum 紀錄

- Sprint 1–2 Burndown Chart
- Sprint 1–2 Retro 紀錄
- 10/29 業師回饋與 Backlog 調整
- Pull Request 與程式碼審查紀錄
- Sprint 3–5 詳細工作規劃

---

## 9. AI 使用聲明

本專題使用生成式 AI 工具（ChatGPT）輔助：

1. 規劃 AWS MVP 實作步驟。
2. 協助撰寫及整理 Python 程式。
3. 協助排查 AWS Textract 測試問題。
4. 整理 AWS 操作與程式重現步驟。
5. 協助撰寫 GitHub README 文件。

本專題的 AWS 操作、程式執行、測試結果檢查與資料庫驗證，由組員在 AWS Learner Lab 實際完成。

AI 產出內容經人工確認後使用，不將 AI 產生的內容直接視為未經驗證的實作成果。

---

## 10. 後續改進方向

本次 MVP 已完成數位申貸流程的第一段，未來可延伸：

1. 使用 AWS Lambda 自動觸發申貸文件處理。
2. 建立申貸文件上傳介面。
3. 增加文件資料格式與完整性檢查。
4. 加入申貸案件查詢與狀態追蹤。
5. 建立人工覆核及錯誤處理機制。
6. 強化最小權限、稽核與資料保護。
7. 加入更多模擬資料測試，評估辨識準確率與處理時間。

---

## 11. 專題成果總結

本專題透過 Amazon S3、Amazon Textract、Python 與 Amazon DynamoDB，成功完成數位申貸文件自動辨識與案件紀錄建立的最小可行原型。

2026 年 11 月 3 日的實際測試結果顯示，單筆模擬申貸文件可以透過 AWS 服務完成資料擷取、整理、儲存及驗證。

此成果可作為後續數位申貸自動化系統開發的基礎，未來將持續改善資料品質、系統可靠性、法遵與使用者操作流程。
