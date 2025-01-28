from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, NewsArticle, Epaper, AdditionalImage
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'facebook', 'twitter', 'linkedin')
    search_fields = ('name', 'email')

admin.site.register(Publisher, PublisherAdmin)

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_published', 'trending', 'published_by')
    list_filter = ('category', 'trending', 'date_published')
    search_fields = ('title', 'content')
    ordering = ('-date_published',)
    list_editable = ('trending',)
    date_hierarchy = 'date_published'
    inlines = [AdditionalImageInline]

admin.site.register(NewsArticle, NewsArticleAdmin)

class EpaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'pdf', 'date_uploaded')
    search_fields = ('title',)
    ordering = ('-date_uploaded',)

admin.site.register(Epaper, EpaperAdmin)

# Customize the admin panel appearance
admin.site.site_header = 'Bomet Newswire Admin Panel'
admin.site.site_title = 'Bomet Newswire Admin'
admin.site.index_title = 'Welcome to Bomet Newswire Administration'
