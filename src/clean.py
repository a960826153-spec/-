"""
clean.py - 模擬保險理賠資料清理腳本
組員 B: 型別與一致性 (去重、city 與 gender 統一、金額轉數值、日期解析)
組員 A: 缺值處理 (income 分群填補、新增 income_missing 旗標)
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
    print(f"[去重] 原始列數: {initial_count}，移除重複: {removed_count} 筆，剩餘列數: {len(df_clean)}")
    return df_clean


if __name__ == "__main__":
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"找不到原始資料: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    df = remove_duplicates(df)
