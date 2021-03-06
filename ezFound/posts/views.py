from django.shortcuts import render
from pkg_resources import require
from django.http import JsonResponse

category = [
    {"id":1,"value":"Wallet"},
    {"id":2,"value":"Cards"},
    {"id":3,"value":"Bags"},
    {"id":4,"value":"Books"},
    {"id":5,"value":"Stationery"},
    {"id":6,"value":"Glasses"},
    {"id":7,"value":"Jewery"},
    {"id":8,"value":"Other"},
    {"id":9,"value":"Other"},
    {"id":10,"value":"Other"},
    {"id":11,"value":"Other"},
    {"id":12,"value":"Other"},
    {"id":13,"value":"Other"},
    {"id":14,"value":"Other"},
    {"id":15,"value":"Other"},
]

status = [
    {"id":1,"value":"Lost"},
    {"id":2,"value":"Found"},
    {"id":3,"value":"Returned"},
    {"id":4,"value":"Other"},
    {"id":5,"value":"Other"},
    {"id":6,"value":"Other"},
    {"id":7,"value":"Other"},
    
]

locations = [
    {"id":1,"value":"Lost"},
    {"id":2,"value":"Found"},
    {"id":3,"value":"Returned"},
    {"id":4,"value":"Other"},
]

noti = [
    {"id":1,"value":"Lost"},
    {"id":2,"value":"Found"},
    {"id":3,"value":"Returned"},
    {"id":4,"value":"Other"},
    {"id":1,"value":"Lost"},
    {"id":2,"value":"Found"},
    {"id":3,"value":"Returned"},
    {"id":4,"value":"Other"},
    {"id":1,"value":"Lost"},
    {"id":2,"value":"Found"},
    {"id":3,"value":"Returned"},
    {"id":4,"value":"Other"},
]

# Create your views here.
def index(request):
    return render(request, 'posts/index.html', context={
        'Category': category,
        'Status': status,
        'Locations': locations,
        'Noti': noti
    })

def uploadTest(request):
    
    if request.method == "POST":
        upload_file = request.FILES['dropzone']
        print(upload_file.name)
        print(upload_file.size)
        print(request.POST.get('new-post-form-status'))
        
    return render(request, 'posts/index.html', context={
        'Category': category,
        'Status': status,
        'Locations': locations,
        'Noti': noti
    })

def post(request, post_id):
    return render(request, 'posts/post.html', context={
        'Category': category,
        'Status': status,
        'Locations': locations,
        'Noti': noti
    })