from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import *
from webapp.models import *
from django.views.generic import View, TemplateView, RedirectView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        context = {
            'tasks': tasks
        }
        return render(request, 'index.html', context)


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['task_pk'])
        return context


def add_view(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
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
        form = AddTaskForm()
    context = {
        'form': form
    }
    return render(request, 'add.html', context)
