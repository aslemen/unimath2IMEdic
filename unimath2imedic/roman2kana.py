import importlib.resources
import csv

import jaconv

# https://support.microsoft.com/ja-jp/topic/%E3%83%AD%E3%83%BC%E3%83%9E%E5%AD%97%E5%85%A5%E5%8A%9B%E3%81%AE%E3%81%A4%E3%81%A5%E3%82%8A%E4%B8%80%E8%A6%A7%E8%A1%A8%E3%82%92%E7%A2%BA%E8%AA%8D%E3%81%97%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86-bcc0ad7e-2781-cc9a-e524-7de506d8fdae
_DICT_MSIME = None

# https://cylomw.hatenablog.com/entry/2016/12/06/131418
def roman2kana_msime(roman: str) -> str:
    global _DICT_MSIME

    if not _DICT_MSIME:
        with importlib.resources.open_text("unimath2imedic", "table_MSIME.csv") as f_table:
            r = csv.reader(f_table)
            _DICT_MSIME = dict(r)
            import sys

    len_roman = len(roman)
    window_begin = 0
    window_end = 1
    res = ""

    while window_end <= len_roman:
        flag = False
        for i in range(window_begin, window_end):
            window_split_former, window_split_latter = (
                roman[window_begin:i],
                roman[i:window_end],
            )
            if window_split_latter_kana := _DICT_MSIME.get(window_split_latter, None):
                # try to detect double consonant
                window_split_former_last = window_split_former[-1:]
                if (
                    window_split_former_last # non-empty
                    and window_split_latter.startswith(window_split_former_last)
                ):
                    res = f"{res}{jaconv.h2z(window_split_former[:-1], ascii = True, digit = True)}っ{window_split_latter_kana}"
                else:
                    res = f"{res}{jaconv.h2z(window_split_former, ascii = True, digit = True)}{window_split_latter_kana}"

                flag = True
                break
        
        if flag:
            # kana conv successful
            window_begin = window_end
            window_end += 1
        else:
            # nothign found
            # widen the window
            window_end += 1

    res += jaconv.h2z(
        roman[window_begin:window_end],
        ascii = True, digit = True
    )

    return res