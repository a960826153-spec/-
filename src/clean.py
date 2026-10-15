import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 讀取原始資料
df = pd.read_csv("data/raw/claims_raw.csv", encoding="utf-8-sig")

# 2. 先移除重複列 (為了讓計算結果與簡報的 80 筆離群值完全一致)
df = df.drop_duplicates(subset=['claim_id'])

# 3. 清理 claim_amount 欄位：加上 r 解決 SyntaxWarning
df['claim_amount'] = df['claim_amount'].astype(str).str.replace(r'NT\$', '', regex=True).str.replace(',', '')
df['claim_amount'] = pd.to_numeric(df['claim_amount'], errors='coerce')

# 4. 計算 IQR 與找出離群值上界
Q1 = df['claim_amount'].quantile(0.25)
Q3 = df['claim_amount'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

# 5. 篩選並印出超過上界的離群值數量
outliers = df[df['claim_amount'] > upper_bound]
print(f"IQR 上界為: {upper_bound:.0f}")
print(f"超過 IQR 上界的離群值共: {len(outliers)} 筆")

# 6. 處理金額長尾：新增取 log10 後的欄位以便觀察分布
df['amount_log10'] = np.log10(df['claim_amount'].dropna())

# 7. 繪製 log10 後的分布圖
df['amount_log10'].plot(kind='hist', bins=20, title="Claim Amount (log10) Distribution", color='teal', edgecolor='white')
plt.xlabel("log10(Claim Amount)")
plt.ylabel("Frequency")
plt.show()