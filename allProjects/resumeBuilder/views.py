from django.shortcuts import render

# Create your views here.
def index(request):
    title = 'Resume Builder'
    return render(request, 'resumeBuilder/index.html',{'title':title})

def showResume(request):
    title = 'My Resume'
    return render(request, 'resumeBuilder/showResume.html',{'title':title})

def editResume(request):
    title = 'Edit My Resume'
    return render(request, 'resumeBuilder/editResume.html',{'title':title})