def safe_get_list(l, item, default=None):
    try:
        return l[item]
    except Exception:
        return default
