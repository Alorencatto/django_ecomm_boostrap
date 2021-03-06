from django.shortcuts import render

from store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        "products": products,
        "mainHeader": "Popular products",
        "style": {
            "card_size": "3"
        }
    }
    return render(request, 'home.html', context)
