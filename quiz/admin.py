from django.contrib import admin
from . models import Quizes, Participant


@admin.register(Quizes)
class QuizesAdmin(admin.ModelAdmin):
    model = Quizes
    list_display = ['title', 'created_by', 'attempts', 'duration', 'is_published']
    list_filter = ['is_published']
    search_fields = ['title']
    list_per_page = 20
    readonly_fields = [
        'title', 'reference','slug','skills', 'questions', 
        'attempts', 'duration','instruction','is_published'
    ]       
    fieldsets = (
        ('Description', {'fields': ('title', 'reference','slug',)}),
        ('Requirements', {'fields': ('skills', 'attempts', 'duration',)}),
        ('Instructions', {'fields': ('instruction','is_published',)}),    
    )    

    def has_add_permission(self, request):
        return False
        
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    model = Participant
    list_display = ['participant', 'quiz', 'score', 'completed']
    search_fields = ['quiz__title']
    list_display_links = None
    list_per_page = 30

    def has_add_permission(self, request):
        return False
        
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False