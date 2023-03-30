from django.views import generic

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
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
        return render(request, 'products/list.html', {'product': products})
