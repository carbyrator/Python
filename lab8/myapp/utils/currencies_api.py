import xml.etree.ElementTree as ET
from urllib.request import urlopen
from typing import List, Dict


def get_currencies(currency_codes: List[str] = None) -> Dict[str, Dict]:
    """
    Получает курсы валют с сайта ЦБ РФ.

    Этот метод парсит XML-данные с сайта Центробанка России и возвращает курсы валют в виде словаря.
    Если переданы коды валют через параметр `currency_codes`, то возвращаются только эти валюты.

    Аргументы:
        currency_codes (List[str]): Список кодов валют, для которых нужно получить курсы.
                                     Если не передан, возвращаются все доступные валюты.

    Возвращает:
        Dict[str, Dict]: Словарь, где ключом является код валюты (char_code),
                         а значением — информация о валюте, включая её ID, код, имя, курс и номинал.

    Исключения:
        Exception: В случае ошибки при запросе или парсинге данных, будет возвращено
                   значение из тестовых данных.
    """
    try:
        url = "http://www.cbr.ru/scripts/XML_daily.asp"
        with urlopen(url) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        currencies = {}

        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            num_code = valute.find('NumCode').text
            name = valute.find('Name').text
            nominal = int(valute.find('Nominal').text)
            value = float(valute.find('Value').text.replace(',', '.'))
            valute_id = valute.attrib['ID']

            # Если указаны конкретные коды валют или если не указаны - берем все
            if currency_codes is None or char_code in currency_codes:
                currencies[char_code] = {
                    'id': valute_id,
                    'num_code': num_code,
                    'char_code': char_code,
                    'name': name,
                    'value': value,
                    'nominal': nominal
                }

        return currencies

    except Exception as e:
        print(f"Ошибка при получении курсов валют: {e}")
        # Возвращаем тестовые данные в случае ошибки
        return get_test_currencies(currency_codes)


def get_test_currencies(currency_codes: List[str] = None) -> Dict[str, Dict]:
    """
    Тестовые данные для разработки.

    Этот метод возвращает заранее определённые тестовые данные о валютах, которые могут использоваться
    для тестирования и разработки.
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
