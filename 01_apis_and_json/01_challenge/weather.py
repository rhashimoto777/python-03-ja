import requests
API_key = "71a673e4a77aa9bdc2e8a53467d75a82"


def search_city(city):
    # Call API
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_key}&limit=5"
    response = requests.get(url)

    # Extract one city data from API result
    if response.status_code == 200:
        data = response.json()
        if len(data) == 1:
            return data[0]
        elif len(data) == 0:
            print("No city matched!")
            return None
        else:
            for i, city in enumerate(data):
                print(f"{i+1}. {city['name']},{city['country']}")
            idx = input("Multiple matches found, which city did you mean?\n>")
            for i in range(10):
                try:
                    return data[int(idx)]
                except:
                    idx = input("Invalid input. Could you input again? \n>")
                    continue
            return print(f"Return to top menu...")
    else:
        print(f"Error : {response.status_code}")
        return None


def weather_forecast(lat, lon):
    # Call API
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}"
    response = requests.get(url)

    # Extract specific data to utilize
    if response.status_code == 200:
        data = response.json()["list"]
        result = []
        for i, forcast_3h in enumerate(data):
            max_display_num = 5
            if "12:00:00" in forcast_3h["dt_txt"]:
                forecast_1day = {}
                forecast_1day["date"] = forcast_3h["dt_txt"][:10]
                forecast_1day["weather"] = forcast_3h["weather"][0]["main"]
                forecast_1day["temp"] = int(forcast_3h["main"]["temp"] -273.15)
                result.append(forecast_1day)
                if len(result) < max_display_num:
                    continue
                else:
                    break
            else:
                continue
        return result
    else:
        print(f"Error : {response.status_code}")
        return None

def main():
    while True:
        city_name = input("City?\n>")
        if city_name != "":
            city_data = search_city(city_name)
            if city_data != None:
                forcast_data = weather_forecast(city_data["lat"], city_data["lon"])
                if forcast_data != None:
                    for i in forcast_data:
                        print(f'{i["date"]}: {i["weather"]} ({i["temp"]}°C)')
                    continue
                else:
                    continue
            else:
                continue
        else:
            continue

if __name__ == "__main__":
    main()
