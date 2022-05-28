from future.models import FutureRelease

     
def get_sms_feature():
    try:
        return FutureRelease.objects.get(pk=1).sms_authenticator
    except:
        pass

def get_transfer_feature():
    try:
        return FutureRelease.objects.get(pk=1).transfer
    except:
        pass

def get_more_team_per_user_feature():
    try:
        return FutureRelease.objects.get(pk=1).more_team_per_user
    except:
        pass


















