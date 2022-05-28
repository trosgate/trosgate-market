from django.conf import settings
from django.contrib import messages
import requests
import base64

zoom_client_id = settings.ZOON_CLIENT_ID
zoom_secret_key = settings.ZOOM_SECRET_KEY


def base64_encode(content):
    content_bytes = content.encode('ascii')
    base64_bytes = base64.b64encode(content_bytes)
    base64_content = base64_bytes.decode('ascii')
    return base64_content


def zoom_callback(function):
    def wrap(request, *args, **kwargs):
        request.zoom_callback_url = None
        if request.method == 'POST':    
            # secret_key = request.GET["code"]
        
            headers = {
                "Authorization": "Basic" + base64_encode('zoom_client_id:zoom_secret_key')
            }
            zoom_redirect = requests.post(f"https://zoom.us/oauth/authorize?response_type=code&client_id=YP9WPWBhQZiT7TC6GFekgQ&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fproject%2Fschedule-interview%2Fcallback", headers=headers)

            print(zoom_redirect.text)
            
            result = request.session["zoom_access_token"] = zoom_redirect.json()["access_token"]
            if result:
                request.zoom_callback_url = True
            else:
                request.zoom_callback_url = False
                messages.error(request, 'Invalid connection. Please contact Admin.')
        return function(request, *args, **kwargs)
    return wrap

     