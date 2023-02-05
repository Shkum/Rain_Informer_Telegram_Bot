from pyowm import OWM


class Weather:
    owm = OWM('6447d90ffd2f57c8d4fadf48e2127c0') # UPDATE OWM KEY
    exit_thread_flag = False

    def __init__(self, location='Odessa'):
        self.loc = location

    def check_weather(self):
        mgr = self.owm.weather_manager()
        try:
            observation = mgr.weather_at_place(self.loc)
            w = observation.weather
        except:
            w = None
        if w:
            return ['Weather: ' + w.detailed_status, ['Rain: ', w.rain]]  # remove for rain only informing  TEST MESSAGE

            # if not w.rain.keys:  # informing only in case of rain
            #     return 'Rain: ' + w.rain + '\nWeather: ' + w.detailed_status
        else:
            return 'City not found or connection error...'

    def set_location(self, location):
        self.loc = location

    def get_location(self):
        return self.loc
