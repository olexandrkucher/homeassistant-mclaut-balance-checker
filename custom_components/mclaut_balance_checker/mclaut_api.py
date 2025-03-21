import logging
import re

from custom_components.mclaut_balance_checker.http_client import AsyncHttpClient

_LOGGER = logging.getLogger(__name__)


class City:
    def __init__(self, city_id: int, city_name: str, human_readable_city_name: str):
        self.city_id = city_id
        self.city_name = city_name
        self.human_readable_city_name = human_readable_city_name

    @staticmethod
    def from_dict(data: dict) -> "City":
        return City(
            city_id=data["city_id"],
            city_name=data["city_name"],
            human_readable_city_name=data["human_readable_city_name"]
        )


class McLautCredentials:
    def __init__(self, username: str, password: str, city_id: int, city_name: str):
        self.username = username
        self.password = password
        self.city_id = city_id
        self.city_name = city_name


class McLautApi:
    def __init__(self, credentials: McLautCredentials, client: AsyncHttpClient):
        self.cookies = None
        self.client = client
        self.credentials = credentials

    async def login(self):
        if await self._is_logged():
            _LOGGER.info('Existing integration session has been found, no need to login')
        else:
            response = await self.client.do_post('https://bill.mclaut.com/index.php', self._prepare_login_data(), self.cookies)
            response_json = response.json()
            if response_json['resultCode'] == 0:
                raise Exception(f"Login failed: {response_json['resultCode']}")
            else:
                self.cookies = response.cookies

    async def load_all_data(self):
        if not await self._is_logged():
            await self.login()
            _LOGGER.info('Integration has been logged in before loading data')

        general_data = await self._load_general_data(self.credentials.city_name)
        balance_data = await self._load_balance_data(self.credentials.city_name)
        return {
            'staticData': {
                'dailyCost': balance_data['dailyCost'],
                'accountNumber': general_data['accountNumber'],
                'internetSpeed': general_data['internetSpeed']
            },
            'dynamicData': {
                'balance': general_data['balance'],
                'ipAddress': general_data['ipAddress'],
                'daysOfInternet': round(general_data['balance'] / balance_data['dailyCost']) - 2
            }
        }

    async def _is_logged(self):
        response = await self.client.do_post(f"https://bill.mclaut.com/client/{self.credentials.city_name}", {}, self.cookies)
        return self.credentials.username in response.text

    async def _load_general_data(self, city):
        response = await self.client.do_post(f"https://bill.mclaut.com/client/{city}", {}, self.cookies)
        return self._parse_general_data(response.text)

    def _parse_general_data(self, text):
        internet_speed_regex = re.compile(r'<div[^>]*>\s*тариф:\s*</div>\s*<div[^>]*>\D*(\d+)[^<]*</div>',
                                          re.IGNORECASE)
        account_number_regex = re.compile(r'<div[^>]*>\s*рахунок:\s*</div>\s*<div[^>]*>\D*(\d+)[^<]*</div>',
                                          re.IGNORECASE)
        ip_address_regex = re.compile(
            r'<div[^>]*>\s*ip-адреса:\s*</div>\s*<div[^>]*>\s*<span[^>]*>\D*(\d+\.\d+\.\d+\.\d+)[^<]*</span>\s*</div>',
            re.IGNORECASE)
        balance_regex = re.compile(
            r'<div[^>]*>\s*баланс\s*</div>\s*<div[^>]*>\s*<span[^>]*>[^>]*</span>\D*([\d .]+)[^<]*</div>',
            re.IGNORECASE)
        return {
            'balance': self._parse_number(balance_regex, text),
            'ipAddress': self._parse_string(ip_address_regex, text),
            'accountNumber': self._parse_string(account_number_regex, text),
            'internetSpeed': self._parse_number(internet_speed_regex, text)
        }

    async def _load_balance_data(self, city):
        response = await self.client.do_post(f"https://bill.mclaut.com/client/{city}/balance", {}, self.cookies)
        return self._parse_balance_data(response.text)

    def _parse_balance_data(self, text):
        balance_regex = re.compile(r'<div[^>]*>\s*на рахунку:\s*</div>\s*<div[^>]*>\s*([^< ]*)\D*([\d .]+)[^<]*</div>',
                                   re.IGNORECASE)
        daily_cost_regex = re.compile(r'<div[^>]*>\s*останнє зняття:\s*</div>\s*<div[^>]*>\D*([\d .]+)[^<]*</div>',
                                      re.IGNORECASE)
        return {
            'balance': self._parse_number(balance_regex, text),
            'dailyCost': self._parse_number(daily_cost_regex, text)
        }

    def _prepare_login_data(self):
        return {
            'login': f'"{self.credentials.username}"',
            'pass': f'"{self.credentials.password}"',
            'city': f'"{self.credentials.city_id}"',
            'query': 'ajax',
            'app': 'client',
            'module': 'auth',
            'socketId': 0,
            'action': 'logIn',
            'lang': 'ua'
        }

    @staticmethod
    def _parse_number(regexp, text):
        result = regexp.search(text)
        if result and result.group(1):
            return float(re.sub(r'[^\d.]', '', result.group(1)))
        else:
            return float('nan')

    @staticmethod
    def _parse_string(regexp, text):
        result = regexp.search(text)
        if result and result.group(1):
            return result.group(1).strip()
        else:
            return 'N/A'
