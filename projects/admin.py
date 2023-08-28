from django.contrib import admin
from .models import Project #ProjectLanguageRequired, 


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'salary', 'duration', 'reopen_count', 'status']                 
    list_filter = ['published',]
    list_editable = ['reopen_count', 'status']
    search_fields = ['title']
    readonly_fields = [
        'merchant', 'category', 'preview', 'salary','rating',
        'service_level', 'skill', 'created_by', 'reference', 'identifier',
        'description','sample_link', 'duration','duration_time', 
        'reopen_count', 'completion_time'
    ]
    actions = ['Feature_on_home', 'Unfeature_from_home']
    fieldsets = (
        ('Introduction', {'fields': ('merchant', 'identifier', 'category', 'preview', 'salary',)}),
        ('Specialties', {'fields': ('service_level', 'skill','rating','reopen_count', )}),
        ('Details', {'fields': (
            'description','sample_link','duration','duration_time', 'completion_time',
        )}),
        ('Project Creator', {'fields': ('reference','created_by',)}),   
    )

    # def get_queryset(self, request):
    #     qs = super(ProjectAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs.all()
        
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
# admin.site.register(Project, ProjectAdmin)

