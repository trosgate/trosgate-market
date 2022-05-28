from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': request.user.receivernotifications.filter(is_read=False)}
    else:
        return {'notifications': []}