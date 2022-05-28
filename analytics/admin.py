import json 

from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from . models import NewStats, ProjectStatus
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


class ProjectStatusAdmin(admin.ModelAdmin):
    model = ProjectStatus
    list_display = ['description','active_count', 'review_count', 'ongoing_count', 'archived_count']
    list_display_links = ['description']   

    def changelist_view(self, request, extra_context=None):
        status_data = (
            ProjectStatus.objects.annotate().values('active','review', 'ongoing', 'archived')
        )

        as_json = json.dumps(list(status_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"status_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(NewStats, NewStatsAdmin)
admin.site.register(ProjectStatus, ProjectStatusAdmin)