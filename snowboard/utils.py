import requests

def geocode_address_yandex(address, api_key):
    try:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={address}&results=1"
        response = requests.get(url)
        data = response.json()

        if 'response' in data and 'GeoObjectCollection' in data['response']:
            features = data['response']['GeoObjectCollection']['featureMember']
            if not features:
                print(f"Ошибка геокодирования: Нет данных для адреса '{address}'.")
                return None, None

            geo_object = features[0]['GeoObject']
            coords = geo_object['Point']['pos'].split()
            full_address = geo_object['metaDataProperty']['GeocoderMetaData']['text']

            # Проверяем, что полный адрес соответствует ожидаемому
            if address.lower() not in full_address.lower():
                print(f"Предупреждение: Адрес '{address}' не совпадает с найденным адресом '{full_address}'.")
                return None, None

            print(f"Геокодирование адреса '{address}' успешно. Полный адрес: {full_address}. Координаты: {coords}")
            return coords[1], coords[0]  # [latitude, longitude]
        else:
            print(f"Ошибка геокодирования: Нет данных для адреса '{address}'. Ответ API:", data)
            return None, None
    except Exception as e:
        print(f"Ошибка геокодирования: {e} для адреса '{address}'")
        return None, None


def reverse_geocode_yandex(lat, lon, api_key):
    try:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&format=json&geocode={lon},{lat}"
        response = requests.get(url)
        data = response.json()

        if 'response' in data and 'GeoObjectCollection' in data['response']:
            geo_object = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            full_address = geo_object['metaDataProperty']['GeocoderMetaData']['text']
            print(f"Обратное геокодирование координат [{lat}, {lon}] дало адрес: {full_address}")
            return full_address
        else:
            print(f"Ошибка обратного геокодирования для координат [{lat}, {lon}]. Ответ API:", data)
            return None
    except Exception as e:
        print(f"Ошибка обратного геокодирования: {e} для координат [{lat}, {lon}]")
        return None


