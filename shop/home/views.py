from django.shortcuts import render
from django.http import HttpResponse

denomi = [2000,500,200,100,50,20,10,5,2,1]
def index(request):
    context = {
        'denomi':denomi
    }
    return render(request,'home/home.html',context)#HttpResponse("Hi! Nithin")