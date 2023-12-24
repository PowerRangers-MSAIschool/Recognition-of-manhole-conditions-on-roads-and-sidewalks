from django.shortcuts import render

# Create your views here.
def home_main(request):
    return render(request, 'home_main.html')

def move_page1(request):
    return render(request, 'video_test.html')

def move_page2(request):
    return render(request, 'video_test.html')

def move_page3(request):
    return render(request, 'video_test.html')

def move_page4(request):
    return render(request, 'video_test.html')