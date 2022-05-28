from django.contrib import admin
from . models import Answer, Question, Quizes, Participant, Attempt


class QuizesAdmin(admin.ModelAdmin):
    model = Quizes
    list_display = ['created_by', 'title', 'attempts', 'duration', 'is_published']
    list_filter = ['title']
    search_fields = ['title']
    list_per_page = 20
    list_editable = ['is_published']    
    fieldsets = (
        ('Description', {'fields': ('title', 'reference','slug')}),
        ('Requirements', {'fields': ('skills', 'questions', 'attempts', 'duration',)}),
        ('Instructions', {'fields': ('instruction','is_published')}),    
    )    


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['created_by', 'question', 'marks']
    search_fields = ['question']
    list_per_page = 20    
    exclude = ['reference','slug']
    # readonly_fields = ['created_by', 'answers', 'marks']

class ParticipantAdmin(admin.ModelAdmin):
    model = Participant
    list_display = ['participant', 'quiz', 'score', 'completed']
    search_fields = ['quiz__title']
    list_display_links = None
    list_per_page = 20


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ['created_by', 'answer','is_correct']
    list_display_links = None
    list_per_page = 20


class AttemptAdmin(admin.ModelAdmin):
    model = Attempt
    list_display = ['participant', 'quiz', 'question', 'answer']
    search_fields = ['question__question']
    list_display_links = None
    list_per_page = 20







admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quizes, QuizesAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Attempt, AttemptAdmin)