from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import ToDoList ,Item
from .forms import CreateNewList

def index(response,id):
    ls = ToDoList.objects.get(id = id)
    
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get( "c"  + str(Item.id)) == "clicked":
                    item.complete = True
            else:
                item.complete = False
            item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text = txt,complete = False)
            else:
                print("Invalid")

        
    return render(response,"strix/list.html", {"ls":ls})
    

def home(response):
    return render(response,"strix/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name = n)
            t.save()
            response.user.ToDoList.add(t)  # adds the to do list to the current logged in user
            
            return HttpResponseRedirect("/%i" %t.id)

    else:
        form = CreateNewList()
    
    return render(response,'strix/create.html',{"form":form})

def view(response):
    return render(response,"strix/view.html",)