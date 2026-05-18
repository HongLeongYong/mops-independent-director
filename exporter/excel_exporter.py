import os
import shutil
from datetime import datetime
import pandas as pd
from config import BASE_OUTPUT_DIR, LATEST_SUBDIR, HISTORY_SUBDIR, OUTPUT_BASENAME


def export_to_excel(data: dict[str, list[dict]]) -> str | None:
    has_data = any(records for records in data.values())
    if not has_data:
        print("[錯誤] 所有市場別皆無資料，不產生 Excel")
        return None

    frames = []
    for sheet_name, records in data.items():
        if not records:
            print(f"  [警告] {sheet_name} 無資料，略過")
            continue
        df = pd.DataFrame(records)
        df.insert(0, "市場別", sheet_name)
        frames.append(df)
        print(f"  {sheet_name}：{len(df)} 筆")

    if not frames:
        print("[錯誤] 無可合併資料")
        return None

    combined = pd.concat(frames, ignore_index=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_BASENAME}_{timestamp}.xlsx"

    latest_path  = os.path.join(BASE_OUTPUT_DIR, LATEST_SUBDIR,  filename)
    history_path = os.path.join(BASE_OUTPUT_DIR, HISTORY_SUBDIR, filename)

    combined.to_excel(latest_path, index=False, sheet_name="獨立董事彙總表")
    shutil.copy2(latest_path, history_path)

    print(f"\n已儲存：{latest_path}（共 {len(combined)} 筆，{len(combined.columns)} 個欄位）")
    print(f"已備份：{history_path}")
    return latest_path
