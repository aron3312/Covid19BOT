from math import sin, cos, sqrt, atan2, radians

R = 6373.0


def cal_distance(site1, site2):
    """
    input:
    site1 -> (lon, lat)
    site2 -> (lon, lat)

    output:
    distance -> <Float>km
    """
    dlon = radians(site2[0]) - radians(site1[0])
    dlat = radians(site2[1]) - radians(site1[1])

    a = sin(dlat / 2) ** 2 + cos(radians(site1[1])) * cos(radians(site2[1])) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance