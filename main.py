from kivymd.app import MDApp

from kivy_garden.mapview import MapView,MapMarker
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
class Map(MapView):
    pass
class GpsHelper():
    hh = False
    def run(self):
        self.app = MDApp.get_running_app()
        self.app.gps_blinker.blink()
        if platform == "android":
            from android.permissions import Permission,request_permissions
            def callback(permission,results):
                if all([res for res in results]):
                    print("okk!!")
                else:
                    print("not got all")
            request_permissions([Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION],callback)

        if platform == "android":
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position,
                          on_status=self.on_auth_status)
            gps.start(minTime=1000,minDistance=0)

    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs["lat"]
        my_lon = kwargs["lon"]


        print("GPS POSITION", my_lat, my_lon)

        self.app.gps_blinker.lat = my_lat
        self.app.gps_blinker.lon = my_lon
        if not self.hh:
            self.app.map.center_on(my_lat,my_lon)
            self.hh = True
    def on_auth_status(self, general_status, status_message):
        if general_status == "provider-enabled":
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dailouge = MDDialog(title="GPS OFF", text="Enable The Fucking GPS!")
        dailouge.size_hint = [0.8, 0.8]
        dailouge.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        dailouge.open()


class GpsBlinker(MapMarker):
    def blink(self):
        animation = Animation(opacity=0,blink_size=50)
        animation.bind(on_complete=self.reset)
        animation.start(self)




    def reset(self,*args):
        self.opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()




class MainApp(MDApp):
    def build(self):
        self.gps_helper = GpsHelper()
        self.map = Map()
        self.gps_blinker = self.map.ids.blinker
        return self.map

    def on_start(self):
        self.gps_helper.run()

MainApp().run()
