from healthcard.reader import HealthCardReader
import json
import urllib.parse

from kivy.core.window import Window
from kivy import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import *
import webbrowser
from smartcard.Exceptions import CardConnectionException



class KartendatenApp(App):

    def build(self):

        Config.set('graphics', 'resizable', False)

        self.window = FloatLayout()
        Window.size = (350, 150)



        with self.window.canvas.before:
            Color(255, 255, 255, 1)
            Rectangle(pos=(0, 0), size=(350, 150))


        self.window.cols = 1
        self.window.rows = 1
        self.window.size_hint = (1, 1)



        return self.window



def kartenscanner(*args):

    try:
        reader = HealthCardReader()
        krankenkassenkarte = reader.get_health_card()
        print("test")
    except CardConnectionException:

        return "Keine Karte gefunden"

    print(reader, "test")


    krankenkasse_json = json.loads(krankenkassenkarte.to_json())
    print(krankenkasse_json)

    krankenkasse_nachname = krankenkasse_json["patient"]["last_name"]
    krankenkasse_vorname = krankenkasse_json["patient"]["first_name"]
    krankenkasse_strasse = krankenkasse_json["patient"]["residential_address"]["street"] + " " + krankenkasse_json["patient"]["residential_address"]["street_number"]
    krankenkasse_ort_plz = krankenkasse_json["patient"]["residential_address"]["zip_code"] + " " + krankenkasse_json["patient"]["residential_address"]["city"]
    krankenkasse_versicherungsname = krankenkasse_json["insurance"]["insurance_name"]
    krankenkasse_geburtsdatum = krankenkasse_json["patient"]["birthdate"]
    krankenkasse_geschlecht = krankenkasse_json["patient"]['gender']

    krankenkasse_dict = {
        "nachname": krankenkasse_nachname,
        "vorname": krankenkasse_vorname,
        "strasse": krankenkasse_strasse,
        "ort_plz": krankenkasse_ort_plz,
        "versicherungsname": krankenkasse_versicherungsname,
        "geburtsdatum": krankenkasse_geburtsdatum,
        "geschlecht": krankenkasse_geschlecht
    }

    url = "https://localhost:8000/register/" + urllib.parse.urlencode(krankenkasse_dict)

    print(krankenkasse_nachname)
    print(krankenkasse_vorname)
    print(krankenkasse_strasse)
    print(krankenkasse_ort_plz)
    print(krankenkasse_versicherungsname)
    print(krankenkasse_geburtsdatum)
    print(krankenkasse_geschlecht)

    return url

if __name__ == "__main__":
    app = KartendatenApp()
    app.run()
    webbrowser.open(url)
