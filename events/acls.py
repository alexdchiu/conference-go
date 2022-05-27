from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

import requests, json

def get_photo (city, state):
  headers = {"Authorization": PEXELS_API_KEY}
  params = {
      "per_page": 1,
      "query": f"{city} {state}",
  }
  url = "https://api.pexels.com/v1/search"
  res = requests.get(url, params = params, headers = headers)
  # data = res.json()
  # photos = data["photos"]
  # photo = photos[0]["src"]["medium"]
  # d = {
  #   "picture_url": photo
  # }
  # return d
  content = json.loads(res.content)
  try:
    return {
      "picture_url": content["photos"][0]["src"]["original"]
    }
  except:
    return {
      "picture_url": None
    }
    


def get_weather_data(city, state):
  direct_url = "http://api.openweathermap.org/geo/1.0/direct"
  direct_params = {
    "q": f"{city},{state},us",
    "limit": 5,
    "appid": OPEN_WEATHER_API_KEY
  }
  direct_res = requests.get(direct_url,params=direct_params)
  direct_content = json.loads(direct_res.content)
  try:
    lat = direct_content[0]["lat"]
    lon = direct_content[0]["lon"]
  except:
    return None
  url = "https://api.openweathermap.org/data/2.5/weather"
  params = {
    "lat": lat,
    "lon": lon,
    "appid": "f085a3f146ad572b14e20c3aa4060f4d",
    "units": "imperial"
}
  res = requests.get(url, params=params)
  data = res.json()
  description = data["weather"][0]["description"]
  temperature = data["main"]["temp"]
  try:
    return {
      "temperature": temperature,
      "description": description,
    }
  except:
    return None