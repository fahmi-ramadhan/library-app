import json
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse, JsonResponse
from main.forms import ItemForm
from django.urls import reverse
from main.models import Item
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime

@login_required(login_url='/login')
def show_main(request):
    books = Item.objects.filter(user=request.user)

    context = {
        'app_name': 'Library Management System',
        'name': request.user.username,
        'class': 'PBP A',
        'books': books,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def add_book(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(request, "add_book.html", context)

def remove_book(request, book_id):
    if request.method == 'POST' and 'Remove' in request.POST:
        book = Item.objects.get(id=book_id)
        book.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def add_book_amount(request, book_id):
    if request.method == 'POST' and 'Increment' in request.POST:
        book = Item.objects.get(id=book_id)
        book.amount += 1
        book.save()
    return HttpResponseRedirect(reverse('main:show_main'))

def dec_book_amount(request, book_id):
    if request.method == 'POST' and 'Decrement' in request.POST:
        book = Item.objects.get(id=book_id)
        book.amount -= 1
        if book.amount < 0:
            book.amount = 0
        book.save()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type="application/xml")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_item_json(request):
    books = Item.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', books))

@csrf_exempt
def add_item_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        author = request.POST.get("author")
        category = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_book = Item(name=name, author=author, category=category, amount=amount, description=description, user=user)
        new_book.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def delete_item_ajax(request, book_id):
    if request.method == 'DELETE':
        book = Item.objects.get(pk=book_id, user=request.user)
        book.delete()
        return HttpResponse(b"OK", status=200)

    return HttpResponseNotFound()

@csrf_exempt
def add_book_amount_ajax(request, book_id):
    if request.method == 'POST':
        book = Item.objects.get(pk=book_id, user=request.user)
        book.amount += 1
        book.save()
        return HttpResponse(b"OK", status=200)
    
    return HttpResponseNotFound()

@csrf_exempt
def dec_book_amount_ajax(request, book_id):
    if request.method == 'POST':
        book = Item.objects.get(pk=book_id, user=request.user)
        book.amount -= 1
        if book.amount < 0:
            book.amount = 0
        book.save()
        return HttpResponse(b"OK", status=200)
    
    return HttpResponseNotFound()

@csrf_exempt
def create_item_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_item = Item.objects.create(
            user = request.user,
            name = data["name"],
            author = data["author"],
            category = data["category"],
            amount = int(data["amount"]),
            description = data["description"]
        )

        new_item.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)