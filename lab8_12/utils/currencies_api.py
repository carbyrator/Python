"""Получение актуальных курсов валют ЦБ РФ и тестовые данные на случай сбоя."""

import os
import ssl
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from typing import List, Dict

TIMEOUT = 10  # seconds


def _open_url(req: Request):
    """
    Открывает URL с учётом проблем сертификатов:
    - пытается использовать системные сертификаты или certifi, если установлен;
    - при переменной окружения ALLOW_INSECURE_CBR=1 пробует небезопасный контекст.
    """
    context = ssl.create_default_context()
    try:
        import certifi

        context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass

    try:
        return urlopen(req, timeout=TIMEOUT, context=context)
    except Exception as first_err:
        if os.environ.get("ALLOW_INSECURE_CBR") == "1":
            insecure = ssl._create_unverified_context()
            return urlopen(req, timeout=TIMEOUT, context=insecure)
        raise first_err


def get_currencies(currency_codes: List[str] = None) -> Dict[str, Dict]:
    """
    Получает курсы валют с сайта ЦБ РФ по актуальному API.

    Args:
        currency_codes: Список символьных кодов (USD, EUR и т.д.) для фильтрации.

    Returns:
        Словарь, где ключом является символьный код, а значением — данные валюты.

    Notes:
        При ошибках сети возвращаются тестовые данные, чтобы приложение продолжало работать.
    """
    try:
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (CurrencyMonitor)"})
        with _open_url(req) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        currencies = {}

        allowed = {code.upper() for code in currency_codes} if currency_codes else None

        for valute in root.findall("Valute"):
            char_code = valute.find("CharCode").text
            num_code = valute.find("NumCode").text
            name = valute.find("Name").text
            nominal = int(valute.find("Nominal").text)
            value = float(valute.find("Value").text.replace(",", "."))
            valute_id = valute.attrib["ID"]

            if allowed is None or char_code in allowed:
                currencies[char_code] = {
                    "id": valute_id,
                    "num_code": num_code,
                    "char_code": char_code,
                    "name": name,
                    "value": value,
                    "nominal": nominal,
                }

        return currencies

    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        # Возвращаем тестовые данные в случае ошибки
        return get_test_currencies(currency_codes)


def get_test_currencies(currency_codes: List[str] = None) -> Dict[str, Dict]:
    """
    Тестовые данные для разработки.

    Возвращает заранее определённые курсы, чтобы приложение было работоспособным без сети.
    """
    test_currencies = {
        'USD': {'id': 'R01235', 'num_code': '840', 'char_code': 'USD',
                'name': 'Доллар США', 'value': 90.5, 'nominal': 1},
        'EUR': {'id': 'R01239', 'num_code': '978', 'char_code': 'EUR',
                'name': 'Евро', 'value': 98.7, 'nominal': 1},
        'GBP': {'id': 'R01035', 'num_code': '826', 'char_code': 'GBP',
                'name': 'Фунт стерлингов', 'value': 115.3, 'nominal': 1},
        'JPY': {'id': 'R01820', 'num_code': '392', 'char_code': 'JPY',
                'name': 'Японских иен', 'value': 0.61, 'nominal': 100},
        'CNY': {'id': 'R01375', 'num_code': '156', 'char_code': 'CNY',
                'name': 'Китайский юань', 'value': 12.5, 'nominal': 10},
        'CHF': {'id': 'R01775', 'num_code': '756', 'char_code': 'CHF',
                'name': 'Швейцарский франк', 'value': 103.2, 'nominal': 1},
        'CAD': {'id': 'R01350', 'num_code': '124', 'char_code': 'CAD',
                'name': 'Канадский доллар', 'value': 67.8, 'nominal': 1},
        'AUD': {'id': 'R01010', 'num_code': '036', 'char_code': 'AUD',
                'name': 'Австралийский доллар', 'value': 60.1, 'nominal': 1},
        'TRY': {'id': 'R01700', 'num_code': '949', 'char_code': 'TRY',
                'name': 'Турецкая лира', 'value': 2.8, 'nominal': 10},
        'BRL': {'id': 'R01115', 'num_code': '986', 'char_code': 'BRL',
                'name': 'Бразильский реал', 'value': 17.9, 'nominal': 10},
        'INR': {'id': 'R01270', 'num_code': '356', 'char_code': 'INR',
                'name': 'Индийских рупий', 'value': 1.09, 'nominal': 100},
        'KRW': {'id': 'R01815', 'num_code': '410', 'char_code': 'KRW',
                'name': 'Вон Республики Корея', 'value': 0.068, 'nominal': 1000},
    }

    if currency_codes is None:
        return test_currencies

    return {code: data for code, data in test_currencies.items() if code in currency_codes}
