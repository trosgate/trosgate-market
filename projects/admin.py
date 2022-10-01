from django.contrib import admin
from .models import Project #ProjectLanguageRequired, 

       
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'dura_converter', 'published', 'status']                 
    list_filter = ['published',]
    list_editable = ['published', 'status']
    search_fields = ['title']
    readonly_fields = [
        'category', 'preview', 'amount','rating',
        'service_level', 'project_skill','reference','created_by',
        'description','sample_link','dura_converter','duration','reopen_count', 'completion_time'
    ]
    actions = ['Feature_on_home', 'Unfeature_from_home']
    fieldsets = (
        ('Introduction', {'fields': ('category', 'preview', 'amount',)}),
        ('Specialties', {'fields': ('service_level', 'project_skill','rating','reopen_count', )}),
        ('Details', {'fields': ('description','sample_link','dura_converter','duration', 'completion_time',)}),
        ('Project Creator', {'fields': ('reference','created_by',)}),   
    )

    def Feature_on_home(self, request, queryset):
        queryset.update(published = True)

    def Unfeature_from_home(self, request, queryset):
        queryset.update(published = False)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

# admin.site.register(ProjectLanguageRequired)
admin.site.register(Project, ProjectAdmin)

