from django.contrib import admin
from .models import Blog, HelpDesk, AutoTyPist, Announcement, Ticket

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = [ 'identifier', 'title', 'created_by', 'number_of_likes','type', 'published', 'ordering',]
    list_display_links = ['identifier']
    exclude = ['likes', 'number_of_likes']
    list_editable = ['type','published','ordering']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Introduction', {'fields': ('title', 'slug', 'ordering',)}),
        ('Classification', {'fields': ('type', 'category', 'tags',)}),
        ('Description', {'fields': ('description',)}),
        ('State', {'fields': ('identifier','created_by', 'published',)}),
        ('Media', {'fields': ('thumbnail',)}),
    )  
    radio_fields = {'published': admin.HORIZONTAL}


class HelpDeskAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'published']
    list_display_links = ['title']
    list_editable = ['published']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Introduction', {'fields': ('title', 'preview', 'slug','published',)}),
        ('Content Option #1', {'fields': ('option_one', 'option_one_description', 'option_one_backlink',)}),
        ('Content Option #2', {'fields': ('option_two', 'option_two_description', 'option_two_backlink',)}),
        ('Content Option #3', {'fields': ('option_three', 'option_three_description', 'option_three_backlink',)}),
        ('Content Option #4', {'fields': ('option_four', 'option_four_description', 'option_four_backlink',)}),
        ('Content Option #5', {'fields': ('option_five', 'option_five_description', 'option_five_backlink',)}),
        ('Content Option #6', {'fields': ('option_six', 'option_six_description', 'option_six_backlink',)}),
        ('Content Option #7', {'fields': ('option_seven', 'option_seven_description', 'option_seven_backlink',)}),
        ('Content Option #8', {'fields': ('option_eight', 'option_eight_description', 'option_eight_backlink',)}),
        ('Content Option #9', {'fields': ('option_nine', 'option_nine_description', 'option_nine_backlink',)}),
    )
    radio_fields = {'published': admin.HORIZONTAL}


class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'modified_at', 'reference', 'states']
    list_display_links = ['title']
    list_editable = ['states']
    readonly_fields = ['modified_at','reference', 'query_type_reference', 'created_by', 'assisted_by','created_at', 'team']

    fieldsets = (
        ('Introduction', {'fields': ('title', 'reference','states',)}),
        ('Detail', {'fields': ('query_type', 'query_type_reference', 'content',)}),
        ('Other Info', {'fields': ('created_by', 'assisted_by','created_at', 'modified_at', 'team',)}),
    )
    radio_fields = {'states': admin.HORIZONTAL}


class AutoTyPistAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'ordering']
    list_display_links = None
    list_editable = ['title', 'is_active', 'ordering']


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['content', 'backlink', 'default']
    list_display_links = ['content']
    list_editable = ['backlink', 'default']
    radio_fields = {'default': admin.HORIZONTAL}


    
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(HelpDesk, HelpDeskAdmin)
admin.site.register(AutoTyPist, AutoTyPistAdmin)
admin.site.register(Ticket, TicketAdmin)