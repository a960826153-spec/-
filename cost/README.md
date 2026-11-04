# 第 14 組數位申貸 AWS 成本試算

## 一、估算目的

本專題使用 AWS Pricing Calculator，評估數位申貸文件處理系統的雲端資源費用。

估算區域為 us-east-1（美國東部維吉尼亞北部）。

## 二、每月使用量假設

- 申貸文件：1,000 份單頁 PDF
- Amazon S3：1 GB 儲存、1,000 次上傳、1,000 次讀取
- Amazon Textract：1,000 頁 Forms 分析
- Amazon DynamoDB：1 GB 儲存、1,000 次寫入、5,000 次讀取

## 三、成本試算結果

| AWS 服務 | 每月費用 |
|---|---:|
| Amazon S3 | US$0.03 |
| Amazon Textract | US$50.00 |
| Amazon DynamoDB | US$0.25 |
| **總計** | **US$50.28** |

- 每月成本：US$50.28
- 一年成本：US$603.36
- 三年成本：US$1,810.08
- 預付成本：US$0.00

## 四、AWS Pricing Calculator 連結

https://calculator.aws/#/estimate?id=48288f1051fa9464aaa020334f22bb4b47da91a1

## 五、估算限制

本次為每月 1,000 份文件的規劃情境，並非 AWS Learner Lab 的實際帳單。

三年成本假設服務價格與每月使用量不變，尚未包含未實作的 Lambda、完整稽核功能及其他額外費用。
