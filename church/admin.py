from django.contrib import admin
from django.forms import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Register your models here.

from django.db.utils import ProgrammingError

from church.models import SiteSettings, Advantage, Pastor, Image, Sermon, Category, Tag, Event, SocialNet, Donate, Post, \
    Gallery, MenuTop


class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main page options'), {
            'fields': ('title', 'site_url','top_biblia_citation')
        }),
        (_('Hero section'), {
            'fields': ('hero_section_image', 'hero_section_title', 'hero_scripture_quote'),
        }),
        (_('Upcoming Event'), {
            'fields': ('upcoming_event_enable',),
        }),
        (_('About section'), {
            'fields': ('about_section_enable','about_section_image', 'about_section_title', 'about_section_content'),
        }),
        (_('Advantage section'), {
            'fields': ('advantage_section_enable','advantage_max_count'),
        }),
        (_('Sermon'), {
            'fields': ('sermon_section_enable',),
        }),
        (_('Events'), {
            'fields': ('event_section_enable','event_max_count'),
        }),
        (_('Donate'), {
            'fields': ('donate_section_enable',),
        }),
        (_('News'), {
            'fields': ('news_section_enable','news_post_max_count',),
        }),
        (_('Subscribe'), {
            'fields': ('subscribe_section_enable',),
        }),
        (_('Contact'), {
            'fields': ('contact_section_content','google_map_url',),
        }),
        (_('Social Network'), {
            'fields': ('social_net_link',),
        }),

    )

    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            SiteSettings.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False

class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "get_photo")
    fields = ('title','file','get_photo','created_at' ,'deleted')

    def get_photo(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title','slug')

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title','slug')

class AdvantageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title','slug','class_name','content')

class PastorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("fullname",)}
    fields = ('fullname','slug','title_pastor','biography','get_photo','photo')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo.file:
            return mark_safe(f'<img src="{obj.photo.file.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"

class SermonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "category", "pin" , "created_at", "get_photo" , "deleted")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_filter = ("category", "tags")
    fields = ('title','slug','pastor','content','data_sermon','web_url_sermon','file_sermon','pin','get_photo','photo','category','tags','created_at','deleted')
    readonly_fields = ('created_at','get_photo',)

    def get_photo(self, obj):
        if obj.photo.file:
            return mark_safe(f'<img src="{obj.photo.file.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "created_at", "get_photo" , "deleted")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    fields = ('title','slug','author','content','datatime_event','place_event','get_photo','photo','views','created_at','deleted')
    readonly_fields = ('created_at','get_photo','views')

    def get_photo(self, obj):
        if obj.photo.file:
            return mark_safe(f'<img src="{obj.photo.file.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"

class SocialNetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"title": ("social_net",)}
    fields = ("title",'social_net','url')
    list_display = ("id", "title")
    list_display_links = ("id", "title")

class DonateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "category", "created_at", "get_photo" , "deleted")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_filter = ("category",)
    fields = ('title','slug','author','content','donate_sum','enddate_donate','get_photo','photo','category','created_at','deleted')
    readonly_fields = ('created_at','get_photo',)
    def get_photo(self, obj):
        if obj.photo.file:
            return mark_safe(f'<img src="{obj.photo.file.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title", "slug", "created_at", "get_photo" , "deleted")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    fields = ('title','slug','author','content','category','tags','get_photo','photo','gallery','views','created_at','deleted')
    readonly_fields = ('created_at','get_photo','views')

    def get_photo(self, obj):
        if obj.photo.file:
            return mark_safe(f'<img src="{obj.photo.file.url}" width="50">')
        return "-"

    get_photo.short_description = "Фото"

class GalleryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    fields = ('title','slug','image','created_at')
    readonly_fields = ('created_at',)

class MenuTopAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    save_as = True
    save_on_top = True


admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Advantage, AdvantageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, CategoryAdmin)
admin.site.register(Pastor, PastorAdmin)
admin.site.register(Sermon, SermonAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(SocialNet, SocialNetAdmin)
admin.site.register(Donate, DonateAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(MenuTop, MenuTopAdmin)

admin.site.site_title = 'Управление страницами сайта Church'
admin.site.site_header = 'Управление страницами сайта Church'