"""
Admin configuration for DayScript
Enables management of diary entries and tags via Django admin
"""

from django.contrib import admin
from .models import DiaryEntry, Tag


@admin. register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag model
    """
    list_display = ['name', 'created_at', 'entry_count']
    search_fields = ['name']
    ordering = ['name']

    def entry_count(self, obj):
        return obj. entries.count()
    entry_count. short_description = 'Number of Entries'


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for DiaryEntry model
    """
    list_display = ['title', 'user', 'mood', 'created_at', 'updated_at']
    list_filter = ['mood', 'created_at', 'user', 'tags']
    search_fields = ['title', 'content', 'user__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'title', 'content', 'mood')
        }),
        ('Organization', {
            'fields': ('tags',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes':  ('collapse',)
        }),
    )