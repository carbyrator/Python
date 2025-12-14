import requests


def get_currencies(currency_codes, url=None):
    """
    Получает курсы валют с сайта ЦБ
    """
    if url is None:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"

    # 1. Проверка соединения
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except:
        raise ConnectionError("Сайт не доступен")

    # 2. Проверка JSON
    try:
        data = response.json()
    except:
        raise ValueError("Пришел не JSON")

    # 3. Проверка ключа Valute
    if "Valute" not in data:
        raise KeyError("Нет ключа Valute")

    result = {}
    for code in currency_codes:
        # 4. Проверка есть ли валюта
        if code not in data["Valute"]:
            raise KeyError(f"Нет валюты {code}")

        # 5. Получаем значение
        value = data["Valute"][code]["Value"]

        # 6. Проверяем тип значения
        if not isinstance(value, (int, float)):
            try:
                value = float(value)
            except:
                raise TypeError(f"Курс {code} не число")

        result[code] = value

    return result
