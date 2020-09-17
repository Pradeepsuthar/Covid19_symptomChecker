from django.shortcuts import render

# Create your views here.
def index(request):
    title = 'PicArt App'
    return render(request, 'PicArt/index.html',{'title':title})