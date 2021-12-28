from django.core.paginator import Paginator
from django.db import connection, transaction
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from carts.models import CartItem
# Create your views here.
from carts.views import _cart_id
from category.models import Category
from store.models import Product


# Funciona!
@transaction.atomic()
def test_transaction():
    # Fazendo uma query só para teste de uma transação
    cursor = connection.cursor()
    cursor.execute("select * from category_category")
    row = cursor.fetchall()

    try:
        cursor.execute("""
        insert into category_category (category_name, slug, description, cat_image)
        VALUES('Augusto','augusto','Descrição de teste','dasda')
        """)

        cursor.execute("""
           insert into category_category (category_name, slug, description, cat_image)
            VALUES('Gabi','xulezinho','Descrição de teste','dasda')
            """)
    except Exception as e:
        print(e)

    print(row)


# Funciona!
def test_manual_transaction():
    """
    Demonstração de uma transaction manual

    Sem que precisar usar o rollback, lançar execpetion dentro do bloco de 'transaction.atomic'
    """
    cursor = connection.cursor()
    with transaction.atomic():
        try:
            cursor.execute("""
                            insert into category_category (category_name, slug, description, cat_image)
                            VALUES('Augusto','augusto','Descrição de teste','dasda')
                            """)

            cursor.execute("select * from category_category where id = 1")
            row = cursor.fetchall()

            if len(row) <= 0:
                raise Exception("Fiz o rollback")
        except Exception as e:
            transaction.set_rollback(True)
            print(e)


def store(request, category_slug=None):
    # test_transaction()
    # test_manual_transaction()

    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products": paged_products,
        "product_count": product_count,
        "style": {
            "card_size": "4"
        }
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        # Checa se o produto selecionado está no carrinho
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e

    context = {
        "single_product": single_product,
        "in_cart": in_cart
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)