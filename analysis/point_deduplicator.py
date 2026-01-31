def dedupe_points(points):
    """
    Removes duplicate injection points based on:
    (method, url, parameter)
    """

    seen = set()
    unique = []

    for p in points:
        key = (p.method, p.url, p.target_param)
        if key not in seen:
            seen.add(key)
            unique.append(p)

    return unique