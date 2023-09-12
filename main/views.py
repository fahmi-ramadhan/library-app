from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Operating System Concepts',
        'author': 'Abraham Silberschatz, Peter B. Galvin, and Greg Gagne',
        'category': 'Computer Science',
        'amount': '10',
        'description': 'Operating System Concepts is a book written by Abraham Silberschatz, Peter B. Galvin, and Greg Gagne. It is an informative guide to operating systems with an overview of all the major aspects. The book deals with topics like process, operating systems and their functioning, and design. It also looks at special-purpose systems, storage management, security, distributed systems and memory.'
    }

    return render(request, "main.html", context)
