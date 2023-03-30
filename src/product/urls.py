from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'product': True,
        'products': True,
        'variants': True,
        'product_variants': True,
        'product_image': True,
        'product_variant_price': True
    }), name='list.product'),
    path('table/', TemplateView.as_view(template_name='products/table.html', extra_context={
        'product': True
    }), name='table.product'),
]
