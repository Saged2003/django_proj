from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from .forms import TaskForm, CategoryForm, SearchForm
from django.contrib import messages

def index(request):
    tasks = Task.objects.all()
    search_form = SearchForm(request.GET or None)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        status = search_form.cleaned_data.get('status')
        
        if query:
            tasks = tasks.filter(title__icontains=query)
        if status:
            tasks = tasks.filter(status=status)

    return render(request, 'index.html', {'tasks': tasks, 'search_form': search_form})

def detailed_task(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'detail.html', {'task': task})

def todo_by_status(request, st):
    tasks = Task.objects.filter(status=st)
    return render(request, 'index.html', {'tasks': tasks})

def Todo_list_Category(request, id):
    tasks = Task.objects.filter(category_id=id)
    return render(request, 'index.html', {'tasks': tasks})

def Createtodo(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task successfully created.')
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'create.html', {'form': form})

def createCategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category successfully created.')
            return redirect('/')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

def update_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task successfully updated.')
            return redirect('/')
    else:
        form = TaskForm(instance=task)
    return render(request, 'update.html', {'form': form})

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        messages.success(request, 'Task successfully deleted.')
        return redirect('/')
    return render(request, 'delete.html', {'task': task})
