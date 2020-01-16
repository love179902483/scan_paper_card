from django.shortcuts import render
# Create your views here.



from django.http import HttpResponse

def index(request):
    
    context = {}
    context["hello"] = "hello world@!!!!!"

    return render(request, 'hello.html', context)


def test(request):

    testData = {}
    testData['memeda'] = 'memeda!'
    testData['id'] = 'id'
    return render(request, 'base.html',testData)