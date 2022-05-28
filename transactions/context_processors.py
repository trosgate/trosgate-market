from .hiringbox import HiringBox

def hiring_box(request):
    return {'hiring_box': HiringBox(request)}


