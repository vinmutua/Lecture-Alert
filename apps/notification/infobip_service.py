import http.client
import json
from django.conf import settings

class InfobipService:
    def __init__(self):
        self.host = "wgx5gy.api.infobip.com"
        self.api_key = "705e2e9f63bbb0257576074beedcd78b-48738de4-8bf4-49d8-8402-d34ed38efdf7"
        self.sender = "447491163443"

    def send_sms(self, phone_number, message):
        try:
            conn = http.client.HTTPSConnection(self.host)
            
            payload = json.dumps({
                "messages": [
                    {
                        "destinations": [{"to": phone_number}],
                        "from": self.sender,
                        "text": message
                    }
                ]
            })
            
            headers = {
                'Authorization': f'App {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            conn.request("POST", "/sms/2/text/advanced", payload, headers)
            response = conn.getresponse()
            data = response.read()
            
            return True, json.loads(data.decode("utf-8"))
            
        except Exception as e:
            return False, str(e)
        finally:
            if conn:
                conn.close()