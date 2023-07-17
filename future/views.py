from django.shortcuts import render, get_object_or_404
from .models import Plugin
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from django.contrib.auth.decorators import login_required


@login_required
def plugin_list(request):
    plugins = Plugin.objects.all()
    context = {
        'plugins':plugins,
        'base_currency': get_base_currency_code()
    }
    return render(request, 'future/plugin.html', context)


@login_required
def plugin_detail(request, plugin_slug):
    plugin = get_object_or_404(Plugin, slug=plugin_slug, status=True)
    context = {
        'plugin':plugin,
        'base_currency': get_base_currency_symbol()
    }
    return render(request, 'future/plugin_detail.html', context)