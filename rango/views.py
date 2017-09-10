from django.template import RequestContext
from django.shortcuts import render_to_response, render
from rango.models import Category, Page
from rango.forms import CategoryForm

def add_category(request):
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)         
            return index(request)     
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})
            

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
        
    return render(request, 'rango/category.html', context_dict)

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage':"I am the bold font from the context"}
    
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    
    return render_to_response('rango/index.html', context_dict, context)
    
