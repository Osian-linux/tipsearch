import requests
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Input, Button, Static

class IPSearchApp(App):
    CSS_PATH = "tipsearch.css"

    def compose(self) -> ComposeResult:
        with Container(id="container"):
            yield Input(placeholder="Enter IP Address", type="text", max_length=15, id="ip_input")
            yield Button("Search", id="search_button")
        with Container(id="result_container"):
            yield Static("Result: ", id="result")

    def get_router_location(self, ip_address):
        try:
            response = requests.get(f'http://ip-api.com/json/{ip_address}')
            data = response.json()

            if 'lat' in data and 'lon' in data:
                return {
                    'ip': data.get('query'),
                    'hostname': data.get('as'),
                    'city': data.get('city'),
                    'region': data.get('regionName'),
                    'country': data.get('country'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'isp': data.get('isp'),
                    'zip': data.get('zip'),
                }
            else:
                return None 
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def on_button_pressed(self, event):
        ip_input = self.query_one("#ip_input", Input)
        result = self.query_one("#result", Static)
        ip_address = ip_input.value
        ip_info = self.get_router_location(ip_address)
        if ip_info:
            result.update(f"IP: {ip_info['ip']}\nHostname/ASN: {ip_info['hostname']}\nCity: {ip_info['city']}\nRegion: {ip_info['region']}\nCountry: {ip_info['country']}\nLatitude: {ip_info['latitude']}\nLongitude: {ip_info['longitude']}\nISP: {ip_info['isp']}\nZip: {ip_info['zip']}")
        else:
            result.update("Failed to retrieve location information.")


if __name__ == "__main__":
    IPSearchApp().run()