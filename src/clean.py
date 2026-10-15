"""
clean.py - 模擬保險理賠資料清理管線
整合任務：
- 組員 B: 型別與一致性 (去重、city 與 gender 統一、金額轉數值、日期解析、年齡異常值處理)
- 組員 A: 缺值處理 (新增 income_missing 缺值旗標、income 依險種中位數分群填補)
產出：
- data/clean/claims_clean.csv
"""

import os
import re
import numpy as np
import pandas as pd

RAW_DATA_PATH = os.path.join("data", "raw", "claims_raw.csv")
CLEAN_DATA_PATH = os.path.join("data", "clean", "claims_clean.csv")


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    組員 B 任務 1: 去重
    以 claim_id 為基準去除重複列，保留第一次出現的紀錄。
    影響筆數: 1,230 列 -> 1,200 列 (移除 30 筆重複)
    """
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=["claim_id"], keep="first").copy()
    removed_count = initial_count - len(df_clean)
    print(f"[1. 去重] 原始列數: {initial_count}，移除重複: {removed_count} 筆，剩餘列數: {len(df_clean)}")
    return df_clean


def unify_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    組員 B 任務 2: city 與 gender 統一
    - city: 11 種寫法（含台/臺繁簡異體與英文 Taipei、Kaohsiung）統一對應為 6 個標準縣市，
            缺失者（18 筆）保留為 np.nan
    - gender: 統一為 'M' 與 'F'（'男' -> 'M', '女' -> 'F'）
    """
    df_clean = df.copy()

    # 1. city 統一
    city_map = {
        "台北市": "台北市", "臺北市": "台北市", "Taipei": "台北市",
        "新北市": "新北市",
        "台中市": "台中市", "臺中市": "台中市",
        "台南市": "台南市", "臺南市": "台南市",
        "高雄市": "高雄市", "Kaohsiung": "高雄市",
        "桃園市": "桃園市"
    }
    df_clean["city"] = df_clean["city"].map(city_map)
    valid_cities = df_clean["city"].notna().sum()
    missing_cities = df_clean["city"].isna().sum()
    unique_cities = df_clean["city"].dropna().nunique()
    print(f"[2. city 統一] 統一為 {unique_cities} 個縣市，有效筆數: {valid_cities}，缺值: {missing_cities} 筆")

    # 2. gender 統一
    gender_map = {
        "M": "M", "男": "M",
        "F": "F", "女": "F"
    }
    df_clean["gender"] = df_clean["gender"].map(gender_map)
    m_count = (df_clean["gender"] == "M").sum()
    f_count = (df_clean["gender"] == "F").sum()
    print(f"[3. gender 統一] 性別標籤統一為 M/F: M={m_count} 筆, F={f_count} 筆")

    return df_clean


def convert_types_and_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    組員 B 任務 3: 金額轉數值、日期解析、年齡不合理值標為缺值
    - claim_amount: 去除 'NT$' 與逗號 ','，轉為 float，1,156 筆有效數值，44 筆缺值
    - claim_date: 統一為 YYYY-MM-DD（民國 115 年轉 2026 年），範圍 2026-01-01 至 2026-09-27
    - age: 5 筆不合理值 (< 18 或 > 100，如 -3, 0, 7, 150, 999) 標為缺值 np.nan
    """
    df_clean = df.copy()

    # 1. claim_amount 轉數值
    def parse_amount(val):
        if pd.isna(val):
            return np.nan
        s = str(val).replace("NT$", "").replace(",", "").strip()
        if not s:
            return np.nan
        try:
            return float(s)
        except ValueError:
            return np.nan

    df_clean["claim_amount"] = df_clean["claim_amount"].apply(parse_amount)
    valid_amt = df_clean["claim_amount"].notna().sum()
    missing_amt = df_clean["claim_amount"].isna().sum()
    print(f"[4. 金額轉數值] claim_amount 轉數值完成，有效值: {valid_amt} 筆，缺值: {missing_amt} 筆")

    # 2. claim_date 日期解析
    def parse_date(val):
        if pd.isna(val):
            return np.nan
        s = str(val).replace("民國", "").strip()
        parts = s.replace("/", "-").split("-")
        if len(parts) == 3:
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            if y < 1900:
                y += 1911
            return f"{y:04d}-{m:02d}-{d:02d}"
        return s

    df_clean["claim_date"] = pd.to_datetime(df_clean["claim_date"].apply(parse_date))
    d_min = df_clean["claim_date"].min().strftime("%Y-%m-%d")
    d_max = df_clean["claim_date"].max().strftime("%Y-%m-%d")
    print(f"[5. 日期解析] claim_date 解析完成，日期範圍: {d_min} 至 {d_max}")

    # 3. age 不合理值處理
    unreasonable_mask = (df_clean["age"] < 18) | (df_clean["age"] > 100)
    unreasonable_count = unreasonable_mask.sum()
    df_clean.loc[unreasonable_mask, "age"] = np.nan
    print(f"[6. 年齡合理性] age 不合理值標為缺值: {unreasonable_count} 筆，剩餘有效年齡: {df_clean['age'].notna().sum()} 筆")

    return df_clean


def add_missing_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    組員 A 任務 1: 新增 income_missing 旗標
    保留「缺失本身有資訊」的訊號（與 ocr_confidence 低有關，屬於 MAR 缺失模式）。
    影響筆數: 158 筆缺值標記為 1，其餘為 0。
    """
    df_clean = df.copy()
    df_clean["income_missing"] = df_clean["income"].isna().astype(int)
    missing_count = df_clean["income_missing"].sum()
    print(f"[7. 缺值旗標] 新增 income_missing 旗標完成，缺值標記筆數: {missing_count} 筆")
    return df_clean


def impute_missing_income(df: pd.DataFrame) -> pd.DataFrame:
    """
    組員 A 任務 2: income 分群填補
    依險種（product）計算 income 的分群中位數進行填補。
    影響：
    - 填補前平均收入: 約 65.2 萬元 (652,474 元)
    - 填補後平均收入: 約 64.3 萬元 (642,871 元)
    - income 缺值數量歸零 (填補 158 筆)
    """
    df_clean = df.copy()
    mean_before = df_clean["income"].mean()
    missing_count = df_clean["income"].isna().sum()

    product_medians = df_clean.groupby("product")["income"].median()
    print("[8. 分群填補] 各險種 income 中位數:")
    for prod, med in product_medians.items():
        print(f"    - {prod}: NT$ {med:,.0f}")

    df_clean["income"] = df_clean["income"].fillna(df_clean["product"].map(product_medians))
    mean_after = df_clean["income"].mean()
    print(f"[8. 分群填補] 填補完成: 填補 {missing_count} 筆缺值，剩餘缺值: {df_clean['income'].isna().sum()} 筆")
    print(f"[8. 分群填補] 平均收入由 NT$ {mean_before:,.1f} 調整為 NT$ {mean_after:,.1f} (約 65.2 萬 -> 64.3 萬)")
    return df_clean


def verify_cleaned_data(df: pd.DataFrame) -> None:
    """
    對照 Slide 37 驗收標準與答案
    """
    print("\n" + "=" * 50)
    print("【Lab 1 驗收標準對答案 (Slide 37)】")
    print(f"1. 總列數: {len(df)} 列 (標準: 1,200 列，無重複 claim_id: {df['claim_id'].nunique() == 1200})")
    print(f"2. city 縣市數: {df['city'].dropna().nunique()} 個縣市，缺值: {df['city'].isna().sum()} 筆 (標準: 6 縣市，18 筆缺值)")
    print(f"3. claim_amount 數值型別: {pd.api.types.is_numeric_dtype(df['claim_amount'])}，有效值: {df['claim_amount'].notna().sum()} 筆 (標準: 數值，1,156 筆有值)")
    print(f"4. claim_date 日期範圍: {df['claim_date'].min().strftime('%Y-%m-%d')} 至 {df['claim_date'].max().strftime('%Y-%m-%d')} (標準: 2026-01-01 至 2026-09-27)")
    print(f"5. age 不合理缺值數: {df['age'].isna().sum()} 筆 (標準: 5 筆標為缺值)")
    print(f"6. income_missing 旗標總數: {df['income_missing'].sum()} 筆 (標準: 158 筆缺值標記)")
    print(f"7. income 填補後平均: NT$ {df['income'].mean():,.1f} (標準: 約 64.3 萬元)")
    print("=" * 50 + "\n")


def clean_claims_pipeline(raw_path: str = RAW_DATA_PATH, output_path: str = CLEAN_DATA_PATH) -> pd.DataFrame:
    """
    完整清理管線執行流程
    """
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"找不到原始資料: {raw_path}")

    print(f"開始載入原始資料: {raw_path}")
    df = pd.read_csv(raw_path)

    # 組員 B 任務
    df = remove_duplicates(df)
    df = unify_categories(df)
    df = convert_types_and_formats(df)

    # 組員 A 任務
    df = add_missing_flags(df)
    df = impute_missing_income(df)

    # 驗收標準比對
    verify_cleaned_data(df)

    # 輸出清理後資料
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"清理完成！已產出乾淨資料集至: {output_path}")

    return df


if __name__ == "__main__":
    clean_claims_pipeline()
