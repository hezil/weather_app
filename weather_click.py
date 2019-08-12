import click
import requests
import sys

@click.command()
@click.option('--city', default = "tel aviv", show_default=True, help="wellcome to forecast station!! insert city name. "
                                                   "multi string city name should be srounded with: \"\" ")
@click.option('--forecast', default = 0, show_default=True,
              help="Forecast availble for next 4 days, please insert 0-4")
@click.option('-c', 'i_convention', flag_value='c',
              default=True, help="insert \"-c\" to persent in celsius")
@click.option('-f', 'i_convention', flag_value='f', help="insert \"-f\" to persent in fahrenheit")

def cli(city, forecast, i_convention):
    api_address = 'http://api.openweathermap.org/data/2.5/forecast?appid=70e488eb4c2c4de0ccadc1095cec8b9c&q='
    url = api_address + str(city)
    json_data = requests.get(url).json()

    if json_data == {'cod': '404', 'message': 'city not found'}:
        raise ValueError("city not found")
        quit()

    if forecast > 4 or forecast < 0:
        raise ValueError("The forecast for the next days can be in range on 0-4")
        quit()

    current_day = 0
    start_day = 0
    current_inc = 0
    full_day_temp = []

    for day in range(start_day, forecast + 1):
        while json_data['list'][current_day]['dt_txt'][: -9] == json_data['list'][current_inc]['dt_txt'][: -9]:
            current_inc += 1
            temp_kelvin = json_data['list'][current_inc]['main']['temp']
            full_day_temp.append(temp_kelvin)
        weather = json_data['list'][current_inc]['weather'][0]['description']
        convention = temp_convention(i_convention)
        temp_min = min(full_day_temp)
        temp_min = temp_converter(temp_min, convention)
        temp_max = max(full_day_temp)
        temp_max = temp_converter(temp_max, convention)
        date = json_data['list'][current_day]['dt_txt'][:-9]
        current_day = len(full_day_temp)
        current_inc = current_day

        if day == 0:
            print(
                f'The weather today in {city} is {weather} with temperatures trailing from {temp_min}-{temp_max} {convention}.')
        else:
            print(f'{date} {weather} with temperatures trailing from {temp_min}-{temp_max} {convention}.')

def temp_convention(i_convention):
    if i_convention.upper() == "C":
        o_convention = "celsius"
        return o_convention
    elif i_convention.upper() == "F":
        o_convention = "fahrenheit"
        return o_convention

def temp_converter(temp_kelvin, convention):
    if convention == "celsius":
        result = int(temp_kelvin - 273.15)
        return result
    elif convention == "fahrenheit":
        result = int(round((temp_kelvin - 273.15) * 1.8))
        return result
