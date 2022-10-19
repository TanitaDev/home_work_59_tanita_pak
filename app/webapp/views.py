from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.http import urlencode
from django.urls import reverse, reverse_lazy

from webapp.forms import *
from webapp.models import *
from django.views.generic import View, ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "tasks"
    model = Task

    paginate_by = 10
    paginate_orphans = 1

    queryset = Task.objects.all().filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context


class TaskCreate(CreateView):
    template_name = "add.html"
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('index')


class TaskUpdate(UpdateView):
    template_name = "edit.html"
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.object.pk})


class TaskDelete(DeleteView):
    template_name = "delete.html"
    model = Task
    success_url = reverse_lazy('index')


class ProjectView(ListView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = "tasks"
    template_name = "projects.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context
