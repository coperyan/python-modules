from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lng1, lat2, lng2):
    """ """
    R = 3959.87433
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c
