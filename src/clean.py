"""
clean.py - 模擬保險理賠資料清理腳本
組員 A: 缺值處理 (income 分群填補、新增 income_missing 旗標)
"""

import os
import numpy as np
import pandas as pd

RAW_DATA_PATH = os.path.join("data", "raw", "claims_raw.csv")
CLEAN_DATA_PATH = os.path.join("data", "clean", "claims_clean.csv")


def add_missing_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    組員 A 任務 1: 新增 income_missing 旗標
    保留「缺失本身有資訊」的訊號（與 ocr_confidence 低有關，屬於 MAR 缺失模式）。
    影響筆數: 158 筆缺值標記為 1，其餘為 0。
    """
    df_clean = df.copy()
    df_clean["income_missing"] = df_clean["income"].isna().astype(int)
    missing_count = df_clean["income_missing"].sum()
    print(f"[缺值旗標] 新增 income_missing 旗標完成，缺值標記筆數: {missing_count} 筆")
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
    print(f"[分群填補] 各險種 income 中位數:\n{product_medians}")

    df_clean["income"] = df_clean["income"].fillna(df_clean["product"].map(product_medians))
    mean_after = df_clean["income"].mean()
    print(f"[分群填補] 填補完成: 填補 {missing_count} 筆缺值")
    print(f"[分群填補] 平均收入由 {mean_before:.1f} 元 調整為 {mean_after:.1f} 元 (約 65.2 萬 -> 64.3 萬)")
    return df_clean


if __name__ == "__main__":
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"找不到原始資料: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    df = add_missing_flags(df)
    df = impute_missing_income(df)
