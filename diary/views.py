from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import UserRegisterForm, DiaryEntryForm
from .models import DiaryEntry, Tag


# ============== Authentication Views ==============
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to DayScript, {user.username}! Your account has been created.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'diary/register.html', {'form': form})


# ============== Home/Dashboard View ==============
class HomeView(ListView):
    model = DiaryEntry
    template_name = 'diary/home.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return DiaryEntry.objects.none()

        qs = DiaryEntry.objects.filter(user=self.request.user)

        # Search text
        query = self.request.GET.get('query', '').strip()
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))

        # Tag filter
        tag_id = self.request.GET.get('tag', '').strip()
        if tag_id:
            qs = qs.filter(tags__id=tag_id)

        # Mood filter
        mood = self.request.GET.get('mood', '').strip()
        if mood:
            qs = qs.filter(mood=mood)

        # Date range
        date_from = self.request.GET.get('date_from', '').strip()
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)

        date_to = self.request.GET.get('date_to', '').strip()
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        # Sorting
        sort = self.request.GET.get('sort', '').strip()
        order = self.request.GET.get('order', 'desc').strip() or 'desc'
        sort_map = {
            'title': 'title',
            'date': 'created_at',
            'mood': 'mood',
        }
        if sort in sort_map:
            field = sort_map[sort]
            if order == 'asc':
                qs = qs.order_by(field)
            else:
                qs = qs.order_by(f'-{field}')
        else:
            qs = qs.order_by('-created_at')

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            entries_qs = DiaryEntry.objects.filter(user=user)
            ctx['total_entries'] = entries_qs.count()
            ctx['total_tags'] = Tag.objects.filter(entries__user=user).distinct().count()
            ctx['entries_last_30'] = entries_qs.filter(
                created_at__date__gte=timezone.now().date() - timedelta(days=30)
            ).count()
            ctx['recent_count'] = entries_qs[:5].count()
            ctx['user_tags'] = Tag.objects.filter(entries__user=user).distinct()
        else:
            ctx['total_entries'] = 0
            ctx['total_tags'] = 0
            ctx['entries_last_30'] = 0
            ctx['recent_count'] = 0
            ctx['user_tags'] = Tag.objects.none()
        return ctx


# ============== CRUD Views ==============
class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DiaryEntry
    template_name = 'diary/entry_detail.html'
    context_object_name = 'entry'

    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your diary entry has been created!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Entry'
        context['button_text'] = 'Save Entry'
        return context


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user

    def form_valid(self, form):
        messages.success(self.request, 'Your diary entry has been updated!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Entry'
        context['button_text'] = 'Update Entry'
        return context


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DiaryEntry
    template_name = 'diary/entry_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'entry'

    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.user

    def form_valid(self, form):
        messages.success(self.request, 'Your diary entry has been deleted.')
        return super().form_valid(form)


# ============== Profile View ==============
@login_required
def profile(request):
    user = request.user
    entries = DiaryEntry.objects.filter(user=user)

    total_entries = entries.count()
    mood_stats = {}
    for mood, label in DiaryEntry.MOOD_CHOICES:
        count = entries.filter(mood=mood).count()
        if count > 0:
            mood_stats[label] = count

    user_tags = Tag.objects.filter(entries__user=user).distinct()
    recent_entries = entries[:5]

    context = {
        'total_entries': total_entries,
        'mood_stats': mood_stats,
        'user_tags': user_tags,
        'recent_entries': recent_entries,
    }
    return render(request, 'diary/profile.html', context)
def about(request):
    return render(request, 'diary/about.html')