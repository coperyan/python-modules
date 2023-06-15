def get_col_char(i):
    """Returns the excel char
    Based on the integer index of a column
    """
    string = ""
    while i > 0:
        i, remainder = divmod(i - 1, 26)
        string = chr(65 + remainder) + string
    return string


def rgb_to_hex(rgb):
    """
    ws.Cells(1, i).Interior.color uses bgr in hex
    """
    bgr = (rgb[2], rgb[1], rgb[0])
    strValue = "%02x%02x%02x" % bgr
    # print(strValue)
    iValue = int(strValue, 16)
    return iValue
