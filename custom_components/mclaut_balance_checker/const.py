from datetime import timedelta

DOMAIN = "mclaut_balance_checker"
UPDATE_INTERVAL = timedelta(minutes=50)

USERNAME = "username"
PASSWORD = "password"
CITY_ID = "city_id"
CITY_NAME = "city_name"

SENSORS = [
    {
        "key": "daily_cost",
        "api_key": "dailyCost",
        "name": "Daily Cost",
        "unit": "₴",
        "icon": "mdi:cash-multiple",
    },
    {
        "key": "account_number",
        "api_key": "accountNumber",
        "name": "Account Number",
        "unit": None,
        "icon": "mdi:access-point",
    },
    {
        "key": "internet_speed",
        "api_key": "internetSpeed",
        "name": "Connection Speed",
        "unit": "MBit/s",
        "icon": "mdi:speedometer",
    },
    {
        "key": "balance",
        "api_key": "balance",
        "name": "Balance",
        "unit": "₴",
        "icon": "mdi:wallet",
    },
    {
        "key": "ip_address",
        "api_key": "ipAddress",
        "name": "IP Address",
        "unit": None,
        "icon": "mdi:ip",
    },
    {
        "key": "days_of_internet",
        "api_key": "daysOfInternet",
        "name": "Days of Internet",
        "unit": None,
        "icon": "mdi:counter",
    },
]
