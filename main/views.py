from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.forms import ItemForm
from django.urls import reverse
from main.models import Item

def show_main(request):
    books = Item.objects.all()

    context = {
        'app_name': 'Library Management System',
        'student_name': 'Fahmi Ramadhan',
        'class': 'PBP A',
        'books': books, 
    }

    return render(request, "main.html", context)

def add_book(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(request, "add_book.html", context)