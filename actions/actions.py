# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

PARAM = {'access_key': '', 'query': '', 'units': 'f'}
URL = "http://api.weatherstack.com/current"
PARAM['access_key'] = 'fb6c53c837ca70cd933868e7f5a869ed'

def get_weather(city):
    PARAM['query'] = city 
    
    r = requests.get(url=URL, params=PARAM)
    return r.json()


class ActionWeather(Action):
    def name(self):
        return "action_weather"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ent = tracker.latest_message['entities'][0]['value']
        data = get_weather(ent)
        city = data['location']['name']
        condition = data['current']['weather_descriptions'][0]
        temperature = data['current']['temperature']
        temperature = (temperature - 32) * (5/9)
        humidity = data['current']['humidity']
        wind_mph = data['current']['wind_speed']
        
        response = f"""
        At {city.title()}: \n
        Weather description: {condition}.\n
        Temperature: {temperature} degree celsius \n
        Humidity: {humidity}\n
        Wind Speed: {wind_mph} mph
        """
        
        dispatcher.utter_message(text=response)

        return []
