from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.http import urlencode

from webapp.forms import *
from webapp.models import *
from django.views.generic import View, TemplateView, RedirectView, ListView


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = "tasks"
    model = Task

    paginate_by = 10
    paginate_orphans = 1

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
        context['task'] = get_object_or_404(Task, pk=kwargs['task_pk'])
        return context


def add_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                summary = form.cleaned_data.get("summary")
                description = form.cleaned_data.get("description")
                status = form.cleaned_data.get("status")
                type = form.cleaned_data.get("type")
                Task.objects.create(summary=summary, description=description, status=status, type=type)
                return redirect('index')
            except:
                form.add_error(None, 'Ошибка добавления задачи')

    else:
        form = TaskForm()
    context = {
        'form': form
    }
    return render(request, 'add.html', context)


def edit_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                task.summary = form.cleaned_data.get("summary")
                task.description = form.cleaned_data.get("description")
                task.status = form.cleaned_data.get("status")
                task.type = form.cleaned_data.get("type")
                task.save()
                return redirect('task_view', pk=task.pk)
            except:
                form.add_error(None, 'Ошибка редактирования задачи')

    else:
        form = TaskForm()
    context = {
        'form': form
    }
    return render(request, 'edit.html', context)


def delete_view(request, pk):
    tasks = get_object_or_404(Task, pk=pk)
    if request.method == "GET":
        return render(request, 'delete.html', context={'tasks': tasks})
    elif request.method == "POST":
        tasks.delete()
        return redirect('index')
