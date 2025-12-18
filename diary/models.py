"""
Models for DayScript - Personal Diary Application
Handles diary entries with tags for organization
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Tag(models.Model):
    """
    Tag model for categorizing diary entries
    Allows users to organize entries by topics
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models. DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class DiaryEntry(models. Model):
    """
    Main diary entry model
    Stores user's personal diary entries with title, content, date, and tags
    """
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('neutral', '😐 Neutral'),
        ('excited', '🎉 Excited'),
        ('anxious', '😰 Anxious'),
        ('grateful', '🙏 Grateful'),
        ('angry', '😠 Angry'),
        ('peaceful', '😌 Peaceful'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diary_entries'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        default='neutral'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='entries'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Diary Entry'
        verbose_name_plural = 'Diary Entries'

    def __str__(self):
        return f"{self. title} - {self.user.username}"

    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})

    def get_mood_display_emoji(self):
        """Return just the emoji for the mood"""
        mood_emojis = {
            'happy': '😊',
            'sad': '😢',
            'neutral': '😐',
            'excited': '🎉',
            'anxious': '😰',
            'grateful': '🙏',
            'angry': '😠',
            'peaceful':  '😌',
        }
        return mood_emojis.get(self. mood, '😐')

    def content_preview(self):
        """Return first 100 characters of content"""
        if len(self.content) > 100:
            return self. content[:100] + '...'
        return self.content