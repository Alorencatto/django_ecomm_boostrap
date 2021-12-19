from django.db import connection, transaction
from django.shortcuts import render, get_object_or_404

# Create your views here.
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


def test_manual_transaction():
    """
    Demonstração de uma transaction manula

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
    test_manual_transaction()

    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        "products": products,
        "product_count": product_count,
        "style": {
            "card_size": "4"
        }
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        "single_product": single_product
    }
    return render(request, "store/product_detail.html", context)
