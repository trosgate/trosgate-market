from django.contrib import admin
from .models import Message, Room



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['merchant','guest','agent', 'reference', 'status']
    

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['merchant','sender','created_by', 'created_at',]
    
#     def get_urls(self):
#         urls = super().get_urls()
#         pattern = [
#             path('<int:id>/welcome-to-team/', self.admin_site.admin_view(self.preview_email_composed), name='preview-mail'),
#         ]
#         return pattern + urls

#     def preview_action(self, obj):
#         return format_html(
#             '<a class="button" href="{}" target=_blank>Preview</a>',
#             reverse('admin:preview-mail', args=[obj.pk]),
#         )
    
#     preview_action.allow_tags = True
#     preview_action.short_description = 'Template'

#     def preview_email_composed(self, request, **kwargs):
#         mail =  Notification.objects.get(id=kwargs['id'])
#         context = self.admin_site.each_context(request)
#         context['opts'] = self.model._meta
#         context['mail'] = mail
#         return TemplateResponse(request, 'notification/new_credit_email.html', context)


# admin.site.register(Notification, NotificationAdmin)

# admin.site.register(.........)