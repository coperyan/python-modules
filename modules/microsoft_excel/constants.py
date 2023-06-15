import platform

WindowsOS = True if platform.platform() == "Windows" else False
MacOS = True if "macOS" in platform.platform() else False

if MacOS:
    from appscript import k


class CustomNumberFormats:
    Percentage = """0.0%"""
    Accounting = """_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)"""
    MonthDate = """[$-en-US]mmm-d"""
    Currency = """$#,##0"""
    Number = "#,##0"


class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class CustomCellFormats:
    ManualEntry = DotDict({"FontColor": 9851952, "FillColor": 13434879})
    Good = DotDict({"FontColor": 24832, "FillColor": 13561798})
    Neutral = DotDict({"FontColor": 26012, "FillColor": 10284031})
    Bad = DotDict({"FontColor": 393372, "FillColor": 13551615})


class BorderTypes:
    if WindowsOS:
        Left = 7
        Top = 8
        Bottom = 9
        Right = 10
    elif MacOS:
        Left = k.border_left
        Top = k.border_top
        Bottom = k.border_bottom
        Right = k.border_right


class BorderWeights:
    Hairline = 1
    Thin = 2
    Medium = -4138
    Thick = 4


class BorderStyles:
    if WindowsOS:
        Continuous = 1
        Dash = -4115
        DashDot = 4
        DashDotDot = 5
        Dot = -4142
        Double = -4119
        LineStyleNone = -4118
        SlantDashDot = 13
    elif MacOS:
        Continuous = k.continuous


class VerticalAlignment:
    Bottom = 4107
    Center = -4108
    Distributed = 4117
    Justify = -4130
    Top = -4160


class HorizontalAlignment:
    Center = -4108
    CenterAcrossSelection = 7
    Distributed = -4117
    Fill = 5
    General = 1
    Justify = -4130
    Left = -4131
    Right = -4152
