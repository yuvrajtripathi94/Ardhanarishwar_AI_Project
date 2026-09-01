from datetime import timedelta

# Maps a selected country to a default UI language and its timezone offset
# from UTC (in hours). Language codes must match src/i18n.py's TRANSLATIONS
# keys — countries whose primary language isn't supported yet fall back to
# English until that language is added to i18n.py.
COUNTRIES = {
    "India":                {"lang": "hi", "offset_hours": 5.5,  "tz_label": "IST"},
    "United States":        {"lang": "en", "offset_hours": -5,   "tz_label": "EST"},
    "United Kingdom":       {"lang": "en", "offset_hours": 0,    "tz_label": "GMT"},
    "United Arab Emirates": {"lang": "en", "offset_hours": 4,    "tz_label": "GST"},
    "Canada":               {"lang": "en", "offset_hours": -5,   "tz_label": "EST"},
    "Australia":            {"lang": "en", "offset_hours": 10,   "tz_label": "AEST"},
    "Germany":              {"lang": "en", "offset_hours": 1,    "tz_label": "CET"},
    "Singapore":            {"lang": "en", "offset_hours": 8,    "tz_label": "SGT"},
    "Nepal":                {"lang": "hi", "offset_hours": 5.75, "tz_label": "NPT"},
    "Bangladesh":           {"lang": "en", "offset_hours": 6,    "tz_label": "BST"},
    "South Africa":         {"lang": "en", "offset_hours": 2,    "tz_label": "SAST"},
    "Japan":                {"lang": "en", "offset_hours": 9,    "tz_label": "JST"},
    "Other / Global (UTC)": {"lang": "en", "offset_hours": 0,    "tz_label": "UTC"},
}

DEFAULT_COUNTRY = "India"


def to_local_time_str(utc_iso_string, country):
    """Converts a stored UTC ISO timestamp string to the selected country's
    local time for display, e.g. '2026-09-01 13:16 IST'."""
    if not utc_iso_string:
        return ""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(utc_iso_string)
        info = COUNTRIES.get(country, COUNTRIES[DEFAULT_COUNTRY])
        local_dt = dt + timedelta(hours=info["offset_hours"])
        return f"{local_dt.strftime('%Y-%m-%d %H:%M')} {info['tz_label']}"
    except Exception:
        return utc_iso_string[:16].replace("T", " ")
