import os
import glob
import shutil
from datetime import datetime
import pandas as pd
from config import BASE_OUTPUT_DIR, LATEST_SUBDIR, HISTORY_SUBDIR, OUTPUT_BASENAME

KEY_COLS = ["市場別", "公司名稱", "姓名"]
CMP_COLS = [
    "目前兼任其他公司董監事之情形-公司名稱",
    "目前兼任其他公司董監事之情形-職稱",
]
INFO_COL = "公司代號"


def find_previous_in_latest() -> str | None:
    """在「最新檔案」資料夾找上一次的爬蟲結果，應在爬蟲前呼叫。"""
    latest_dir = os.path.join(BASE_OUTPUT_DIR, LATEST_SUBDIR)
    pattern = os.path.join(latest_dir, f"{OUTPUT_BASENAME}_*.xlsx")
    candidates = sorted(glob.glob(pattern))
    if not candidates:
        return None
    # 多份時依檔名排序取最新的（異常防護）
    return candidates[-1]


def run_compare(new_file: str, prev_file: str | None) -> None:
    if prev_file is None:
        print("[比對] 找不到上一版 Excel，跳過比對")
        return

    print(f"[比對] 新版：{os.path.basename(new_file)}")
    print(f"[比對] 舊版：{os.path.basename(prev_file)}")

    df_new = pd.read_excel(new_file, dtype=str).fillna("")
    df_old = pd.read_excel(prev_file, dtype=str).fillna("")

    agg_new = _aggregate(df_new)
    agg_old = _aggregate(df_old)

    merged = agg_old.merge(agg_new, on=KEY_COLS, how="outer", suffixes=("_舊", "_新"), indicator=True)

    rows = []
    for _, row in merged.iterrows():
        flag = row["_merge"]
        if flag == "left_only":
            rows.append(_build_row("刪除", row, side="舊"))
        elif flag == "right_only":
            rows.append(_build_row("新增", row, side="新"))
        else:
            changed = any(row[f"{c}_舊"] != row[f"{c}_新"] for c in CMP_COLS)
            if changed:
                rows.append(_build_row("變更", row, side="both"))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    compare_filename = f"compare_result_{timestamp}.xlsx"
    latest_dir  = os.path.join(BASE_OUTPUT_DIR, LATEST_SUBDIR)
    history_dir = os.path.join(BASE_OUTPUT_DIR, HISTORY_SUBDIR)

    if not rows:
        print("[比對] 無異動")
        compare_latest_path = None
    else:
        df_result = pd.DataFrame(rows).fillna("")
        compare_latest_path  = os.path.join(latest_dir,  compare_filename)
        compare_history_path = os.path.join(history_dir, compare_filename)
        df_result.to_excel(compare_latest_path, index=False, sheet_name="比對結果")
        shutil.copy2(compare_latest_path, compare_history_path)
        print(f"[比對] 已儲存：{compare_latest_path}（共 {len(df_result)} 筆異動）")
        print(f"[比對] 已備份：{compare_history_path}")

    _cleanup_latest(latest_dir, keep_crawl=new_file, keep_compare=compare_latest_path)


def _cleanup_latest(latest_dir: str, keep_crawl: str, keep_compare: str | None) -> None:
    """刪除「最新檔案」裡除了本次結果之外的舊檔。"""
    keep = {os.path.abspath(keep_crawl)}
    if keep_compare:
        keep.add(os.path.abspath(keep_compare))

    for f in glob.glob(os.path.join(latest_dir, "*.xlsx")):
        if os.path.abspath(f) not in keep:
            os.remove(f)
            print(f"[清理] 已刪除舊檔：{os.path.basename(f)}")


def _aggregate(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in KEY_COLS + CMP_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Excel 缺少欄位：{missing}")

    def agg_cmp(series):
        return "\n".join(sorted(series.dropna().astype(str).unique()))

    agg = df.groupby(KEY_COLS, as_index=False)[CMP_COLS].agg(agg_cmp)

    if INFO_COL in df.columns:
        code_map = df.groupby(KEY_COLS)[INFO_COL].first().reset_index()
        agg = agg.merge(code_map, on=KEY_COLS, how="left")
    else:
        agg[INFO_COL] = ""

    return agg


def _build_row(change_type: str, row: pd.Series, side: str) -> dict:
    result = {"異動類型": change_type}
    for k in KEY_COLS:
        result[k] = row[k]

    new_val = row.get(f"{INFO_COL}_新", "")
    old_val = row.get(f"{INFO_COL}_舊", "")
    if side == "舊":
        result[INFO_COL] = old_val if pd.notna(old_val) else ""
    else:
        result[INFO_COL] = new_val if pd.notna(new_val) else old_val if pd.notna(old_val) else ""

    for c in CMP_COLS:
        if side == "舊":
            result[f"舊_{c}"] = row[f"{c}_舊"] if f"{c}_舊" in row.index else row[c]
            result[f"新_{c}"] = "—"
        elif side == "新":
            result[f"舊_{c}"] = "—"
            result[f"新_{c}"] = row[f"{c}_新"] if f"{c}_新" in row.index else row[c]
        else:
            result[f"舊_{c}"] = row[f"{c}_舊"]
            result[f"新_{c}"] = row[f"{c}_新"]

    return result
