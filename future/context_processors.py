
from .models import FutureRelease

def future_release(request):
	try:
		return {'future_release':FutureRelease.objects.get(pk=1)}
	except:
		return {'future_release':None}