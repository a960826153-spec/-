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


if __name__ == "__main__":
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"找不到原始資料: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    df = add_missing_flags(df)
