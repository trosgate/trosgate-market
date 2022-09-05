import json 

from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from . models import NewStats
# Register your models here.


class NewStatsAdmin(admin.ModelAdmin):
    model = NewStats
    list_display = ['description','win', 'mac', 'iph', 'android','oth']
    list_display_links = ['description']   

    def changelist_view(self, request, extra_context=None):

        stat_data = (
            NewStats.objects.annotate().values("win","mac","iph","android","oth")
        )

        # data = NewStats.objects.all()
        # newdata = serializers.serialize('json', list(data), fields=("win","mac","iph","android","oth"))
        # print(newdata)

        as_json = json.dumps(list(stat_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"stat_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(NewStats, NewStatsAdmin)
