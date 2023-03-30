from django.views import generic

from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator, EmptyPage


class CreateProductView(generic.TemplateView):
    model = Product
    paginate_by = 10
    template_name = 'products/create.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 1
        current_page = context['page_obj'].number
        start_page = max(current_page - page_numbers_range, 1)
        end_page = min(current_page + page_numbers_range, paginator.num_pages)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        context['page_numbers'] = range(start_page, end_page + 1)
        return context
    
    @csrf_exempt
    def create_product(request):
        if request.method=="POST":
            product_name = request.POST.get("product_name")
            product_sku = request.POST.get("product_sku")
            product_description = request.POST.get("product_description")
            product_variants = json.loads(request.POST.get("product_variants"))
            product_media = request.FILES.getlist("product_media")

        # Create the product
        product = Product(name=product_name, sku=product_sku, description=product_description)
        product.save()
        
        # Create the product variants
        for variant in product_variants:
            variant_title = variant["title"]
            variant_price = variant["price"]
            variant_stock = variant["stock"]
            product_variant = ProductVariant(product=product, title=variant_title, price=variant_price, stock=variant_stock)
            product_variant.save()

        # return JsonResponse({ "success": True })

        variants = [
            { "id": 1, "title": "Color" },
            { "id": 2, "title": "Size" },
            { "id": 3, "title": "Style" }
        ]

        return render(request, "products/create.html", {"variants": variants})
    
    def product_variant(request):
        product_variants = ProductVariant.objects.all()
        return render(request, 'products/list.html', {'product_variants': product_variants})
    
    def product_image(request):
        product_images = ProductImage.objects.all()
        return render(request, 'products/list.html', {'product_image': product_images})
    
    def product_variant_price(request):
        product_variant_prices = ProductVariantPrice.objects.all()
        return render(request, 'products/list.html', {'product_variant_price': product_variant_prices})
    
    def product(request):
        products = Product.objects.all()
        paginator = Paginator(products, 10)
        page_number = request.GET.get('list')
        try:
            items = paginator.get_page(page_number)
        except EmptyPage:
            items = paginator.get_page(1)
        return render(request, 'products/list.html', {'product': products, 'items': items, 'paginator': paginator })
    
    def product_filter(request):
        # Get all products
        products = Product.objects.all()

        # Apply filters
        product_title = request.GET.get('product_title')
        product_variant = request.GET.get('product_variant')
        min_price = request.GET.get('price_from')
        max_price = request.GET.get('price_to')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if product_title:
            products = products.filter(name__icontains=product_title)

        if product_variant:
            products = products.filter(variant__icontains=product_variant)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        if start_date:
            products = products.filter(date_created__gte=start_date)

        if end_date:
            products = products.filter(date_created__lte=end_date)

        context = {
            'products': products
        }

        return render(request, 'products/list.html', context)

