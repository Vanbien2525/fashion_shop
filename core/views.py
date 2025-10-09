from django.shortcuts import render

def home(request):
    return render(request, 'core/base.html')

def contact(request):
    return render(request, 'core/contact.html')
