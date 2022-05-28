from django.contrib import admin
from .models import (ProjectLanguageRequired, Project)


        
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rating', 'amount', 'dura_converter', 'created_by', 'published', 'status']                 
    list_filter = ['published',]
    list_editable = ['amount','published', 'dura_converter', 'status']
    search_fields = ['title']    
    # readonly_fields = ['created_by','reference']
    actions = ['Feature_on_home', 'Unfeature_from_home']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Introduction', {'fields': ('title','slug', 'category', 'preview', 'amount','rating',)}),
        ('Specialties', {'fields': ('service_level', 'project_skill',)}),
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

admin.site.register(ProjectLanguageRequired)
admin.site.register(Project, ProjectAdmin)

