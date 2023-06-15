import xmltodict
from functools import reduce


def xml_to_dict(xml: str, xml_path: list = None, **kwargs) -> dict:
    if xml_path:
        return reduce(dict.get, xml_path, xmltodict.parse(xml, **kwargs))
    else:
        return xmltodict.parse(xml, kwargs)
