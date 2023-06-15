from .constants import *
from .helpers import *

import os
from typing import Any
import xlwings as xw
import pandas as pd

if MacOS:
    from appscript import k


class ExcelRange(xw.Range):
    def __init__(self, range_obj: xw.Range):
        super().__init__(impl=range_obj)
        self.range_obj = range_obj

    def SetValue(self, val: Any):
        self.range_obj.value = val

    def PasteDF(self, df: pd.DataFrame, header: bool = False, index: bool = False):
        self.range_obj.options(header=header, index=index).value = df

    def FontSize(self, size: int):
        self.range_obj.font.size = size

    def FontName(self, font_name: str):
        self.range_obj.font.name = font_name

    def Bold(self):
        self.range_obj.font.bold = True

    def Italic(self):
        self.range_obj.font.italic = True

    def Underline(self):
        if WindowsOS:
            self.range_obj.api.Font.Underline = 2
        elif MacOS:
            self.range_obj.api.font_object.underline.set(k.underline_style_single)

    def Border(self, border_type, border_weight, border_style):
        if WindowsOS:
            self.range_obj.api.Borders(border_type).Weight = border_weight
            self.range_obj.api.Borders(border_type).LineStyle = border_style
        elif MacOS:
            self.range_obj.api.get_border(which_border=border_type).weight.set(
                border_weight
            )
            self.range_obj.api.get_border(which_border=border_type).line_style.set(
                border_style
            )

    def VerticalAlign(self, alignment_type):
        self.range_obj.api.VerticalAlignment = alignment_type

    def HorizontalAlign(self, alignment_type):
        self.range_obj.api.HorizontalAlignment = alignment_type


class ExcelSheet(xw.Sheet):
    def __init__(self, sheet_obj: xw.Sheet):
        super().__init__(sheet_obj)
        self.sheet_obj = sheet_obj

    def Range(self, range_str: str) -> ExcelRange:
        return ExcelRange(self.sheet_obj.range(range_str))


class ExcelWorkbook(xw.Book):
    def __init__(self, wb_path: str = None):
        super().__init__(wb_path)
        self.ExcelApp = xw.App(visible=False)

    def Sheet(self, name: str) -> ExcelSheet:
        return ExcelSheet(self.sheets[name])

    def RefreshAll(self):
        self.api.refreshall()
