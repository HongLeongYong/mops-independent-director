import os
import shutil
from datetime import datetime
import pandas as pd
from config import BASE_OUTPUT_DIR, LATEST_SUBDIR, HISTORY_SUBDIR, RELATION_FILE, COMPANY_NAME

# 關係種類 CSV 欄位位置（0-based）
_COL_B = 1   # 關係類別（第一群）
_COL_T = 19  # 關係類別（第三群）
_COL_W = 22  # 姓名（第三群）

_TYPE_A = {
    "本公司關係企業之負責人(利害關係人)",
    "本公司關係企業之大股東(利害關係人)",
    "本公司特定利害關係人(利害關係人)",
    "本公司子公司之負責人(利害關係人)",
}

_SPOUSE = "配偶(利害關係人)"

_TYPE_B_B = {
    "本公司特定利害關係人(利害關係人)",
    "本公司之關係企業(利害關係人)",
    "本公司之子公司(利害關係人)",
    "本公司大股東(利害關係人)",
}

_SUSPICIOUS = f"疑似為{COMPANY_NAME}利害關係人，需再進行確認"


def run_annotate(compare_file: str) -> None:
    if not RELATION_FILE:
        print("[標註] config.py 未設定 RELATION_FILE，跳過標註")
        return
    if not os.path.exists(RELATION_FILE):
        print(f"[標註] 找不到關係種類檔案：{RELATION_FILE}，跳過標註")
        return

    print(f"[標註] 比對檔：{os.path.basename(compare_file)}")
    print(f"[標註] 關係種類：{RELATION_FILE}")

    df_cmp = pd.read_excel(compare_file, dtype=str).fillna("")
    df_rel = pd.read_csv(RELATION_FILE, dtype=str, header=0, encoding="utf-16", sep="\t").fillna("")

    rows = []
    for _, cmp_row in df_cmp.iterrows():
        name = cmp_row.iloc[3]  # D欄：姓名
        matches = df_rel[df_rel.iloc[:, _COL_W] == name]

        if matches.empty:
            new_row = cmp_row.to_dict()
            new_row["姓名比對結果"] = f"非{COMPANY_NAME}利害關係人"
            new_row["系統關係類別一"] = ""
            new_row["系統關係類別二"] = ""
            new_row["比對結果"] = ""
            new_row["備註"] = ""
            rows.append(new_row)
        else:
            for _, rel_row in matches.iterrows():
                t_val = rel_row.iloc[_COL_T]
                b_val = rel_row.iloc[_COL_B]
                new_row = cmp_row.to_dict()
                new_row["姓名比對結果"] = f"與{COMPANY_NAME}利害關係人同名同姓"

                if t_val in _TYPE_A:
                    new_row["系統關係類別一"] = t_val
                    new_row["系統關係類別二"] = ""
                    new_row["比對結果"] = _SUSPICIOUS
                elif t_val == _SPOUSE and b_val in _TYPE_B_B:
                    new_row["系統關係類別一"] = t_val
                    new_row["系統關係類別二"] = b_val
                    new_row["比對結果"] = _SUSPICIOUS
                else:
                    new_row["系統關係類別一"] = ""
                    new_row["系統關係類別二"] = ""
                    new_row["比對結果"] = "非建檔範圍"

                new_row["備註"] = ""
                rows.append(new_row)

    df_result = pd.DataFrame(rows).fillna("").drop_duplicates()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename    = f"annotated_compare_result_{timestamp}.xlsx"
    latest_dir  = os.path.join(BASE_OUTPUT_DIR, LATEST_SUBDIR)
    history_dir = os.path.join(BASE_OUTPUT_DIR, HISTORY_SUBDIR)
    out_latest  = os.path.join(latest_dir,  filename)
    out_history = os.path.join(history_dir, filename)

    df_result.to_excel(out_latest, index=False, sheet_name="標註結果")
    shutil.copy2(out_latest, out_history)
    print(f"[標註] 已儲存：{out_latest}（共 {len(df_result)} 筆）")
    print(f"[標註] 已備份：{out_history}")
