from bs4 import BeautifulSoup


def parse_table(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="hasBorder") or soup.find("table")
    if table is None:
        return []

    headers = _extract_headers(table)
    if not headers:
        return []

    rows = _extract_data_rows(table, len(headers))
    return [dict(zip(headers, row)) for row in rows]


def _extract_headers(table) -> list[str]:
    """
    處理多列 header（tblHead），展開 colspan/rowspan，
    colspan 子欄位格式：父標題-子標題
    """
    header_rows = table.find_all("tr", class_="tblHead")
    if not header_rows:
        return []

    col_count = _count_columns(header_rows)
    # grid[col_idx] = (label, remaining_rowspan)
    grid: dict[int, tuple[str, int]] = {}
    result_rows: list[list[str]] = []

    for tr in header_rows:
        row = [""] * col_count
        # 填入上一列 rowspan 延續的值
        for col_idx, (label, remaining) in list(grid.items()):
            row[col_idx] = label
            if remaining > 1:
                grid[col_idx] = (label, remaining - 1)
            else:
                del grid[col_idx]

        cells = tr.find_all("td")
        fill_idx = 0
        for cell in cells:
            # 找到下一個空格
            while fill_idx < col_count and row[fill_idx] != "":
                fill_idx += 1

            text = cell.get_text(separator="\n", strip=True)
            rowspan = int(cell.get("rowspan", 1))
            colspan = int(cell.get("colspan", 1))

            for c in range(colspan):
                if fill_idx + c < col_count:
                    row[fill_idx + c] = text
                    if rowspan > 1:
                        grid[fill_idx + c] = (text, rowspan - 1)

            fill_idx += colspan

        result_rows.append(row)

    # 合併多列 header：若第二列有值則用「父-子」，否則直接用第一列
    if len(result_rows) == 1:
        return result_rows[0]

    final_headers = []
    for col_idx in range(col_count):
        top = result_rows[0][col_idx]
        sub = result_rows[1][col_idx] if len(result_rows) > 1 else ""
        if sub and sub != top:
            final_headers.append(f"{top}-{sub}")
        else:
            final_headers.append(top)

    return final_headers


def _count_columns(header_rows) -> int:
    total = 0
    for cell in header_rows[0].find_all("td"):
        total += int(cell.get("colspan", 1))
    return total


def _extract_data_rows(table, col_count: int) -> list[list]:
    """
    展開資料列的 rowspan，跳過 tblHead 列。
    """
    grid: dict[tuple, str] = {}
    result = []
    row_idx = 0

    for tr in table.find_all("tr"):
        if "tblHead" in (tr.get("class") or []):
            continue

        cells = tr.find_all("td")
        if not cells:
            continue

        row_data: list[str] = []
        cell_iter = iter(cells)

        for col_pos in range(col_count):
            if (row_idx, col_pos) in grid:
                val, remaining = grid[(row_idx, col_pos)]
                row_data.append(val)
                if remaining > 1:
                    grid[(row_idx + 1, col_pos)] = (val, remaining - 1)
                del grid[(row_idx, col_pos)]
            else:
                try:
                    cell = next(cell_iter)
                    text = cell.get_text(separator="\n", strip=True)
                    rowspan = int(cell.get("rowspan", 1))
                    colspan = int(cell.get("colspan", 1))
                    for c in range(colspan):
                        row_data.append(text)
                        if rowspan > 1:
                            grid[(row_idx + 1, col_pos + c)] = (text, rowspan - 1)
                except StopIteration:
                    row_data.append("")

        result.append(row_data[:col_count])
        row_idx += 1

    return result
