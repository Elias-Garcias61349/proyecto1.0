from django.shortcuts import render
from .models import Task
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def tasks(request):
    profile = request.user.profile_set.first()
    tasks_list = Task.objects.filter(profile=profile).order_by('nombre')

    # Filtro de búsqueda
    search_query = request.GET.get('filter', '')
    if search_query:
        tasks_list = tasks_list.filter(
            Q(nombre__icontains=search_query) | Q(descripcion__icontains=search_query)
        )

    # Paginación
    page_number = request.GET.get('page_tasks')
    paginator = Paginator(tasks_list, 3)  # 3 tareas por página
    tasks = paginator.get_page(page_number)

    context = {
        'tasks': tasks,  
        'filter': search_query
    }

    return render(request, 'task.html', context)
