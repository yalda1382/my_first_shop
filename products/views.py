from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator

def home(request):
    search = request.GET.get('search', '')
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    qs = Product.objects.all()
    if search:
        qs = qs.filter(name__icontains=search)
    if category_id:
        qs = qs.filter(category_id=category_id)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'search': search,
    }
    return render(request, 'home.html', context)