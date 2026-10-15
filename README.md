# claims-eda
模擬保險理賠資料EDA分析

## 專案結構
```text
claims-eda/
├── data/
│   ├── raw/           # 原始資料（唯讀，claims_raw.csv）
│   └── clean/         # 清理後資料（由 src/clean.py 產生，claims_clean.csv）
├── notebooks/         # 分析筆記本
├── src/               # 共用邏輯與清理腳本（clean.py）
├── reports/           # 分析圖表與報告產出
├── README.md          # 專案說明、欄位字典與清理決策
└── requirements.txt   # 相依套件清單
```

## 欄位字典 (Data Dictionary)

| 欄位名稱 | 原始型別 | 清理後型別 | 說明與格式 |
| :--- | :--- | :--- | :--- |
| `claim_id` | object | string | 理賠案件唯一識別碼（無重複） |
| `policy_id` | object | string | 保單編號 |
| `age` | int64 / float64 | float64 | 保戶年齡（合法範圍 18–100 歲，不合理者標為缺值） |
| `gender` | object | string | 性別（標準化為 `M` / `F`） |
| `city` | object | string | 投保人居住縣市（標準化為 6 縣市，未填者為缺值） |
| `product` | object | string | 保險商品種類（4 種商品） |
| `income` | float64 | float64 | 年收入（NT$） |
| `premium` | int64 | int64 | 年繳保費（NT$） |
| `claim_date` | object | datetime64[ns] | 理賠申請日（標準格式 `YYYY-MM-DD`，範圍 2026-01-01 至 2026-09-27） |
| `hospital_days` | int64 | int64 | 住院天數 |
| `claim_amount` | object | float64 | 理賠金額（轉為浮點數數值） |
| `ocr_confidence` | float64 | float64 | OCR 文件辨識信心度（0–100） |
| `status` | object | string | 理賠進度狀態（已給付 / 審核中 / 駁回） |

## 清理決策紀錄 (Data Cleaning Decisions)

- **[組員 B] 列數去重**：依 `claim_id` 保留首筆並刪除重複列，移除 30 筆重複，總列數由 1,230 列降至 1,200 列，確保案件唯一性。
- **[組員 B] city 類別統一**：將 11 種寫法（含台/臺異體字與英文 Taipei、Kaohsiung）統一對應為 6 個標準縣市，18 筆未填保留為缺值。
- **[組員 B] gender 標籤統一**：將「男」、「女」統一轉換為「M」、「F」，消除中英文混用。
- **[組員 B] claim_amount 金額轉數值**：去除字串中的「NT$」與逗號「,」，轉為數值型別（float），共 1,156 筆有效金額，44 筆缺值保留。
- **[組員 B] claim_date 日期格式解析**：統一西元與民國 115 年格式為標準 `YYYY-MM-DD` 日期格式，涵蓋區間為 2026-01-01 至 2026-09-27。
- **[組員 B] age 年齡異常值標記**：檢查年齡範圍，將 5 筆不合理極端值（-3、0、7、150、999）標記為缺值（NaN）。
