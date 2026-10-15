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
    print(f"[city 統一] 6 個縣市有效筆數: {df_clean['city'].notna().sum()}，缺值: {df_clean['city'].isna().sum()} 筆")

    # 2. gender 統一
    gender_map = {
        "M": "M", "男": "M",
        "F": "F", "女": "F"
    }
    df_clean["gender"] = df_clean["gender"].map(gender_map)
    print(f"[gender 統一] M: {(df_clean['gender'] == 'M').sum()} 筆, F: {(df_clean['gender'] == 'F').sum()} 筆")

    return df_clean


if __name__ == "__main__":
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"找不到原始資料: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    df = remove_duplicates(df)
    df = unify_categories(df)
