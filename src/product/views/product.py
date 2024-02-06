from django.views import generic

from django.shortcuts import render
from django.views import View
from product.models import Product, ProductVariant, ProductVariantPrice, Variant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ListProductView(View):
    template_name = 'your_template_name.html'

    def get(self, request, *args, **kwargs):
        # Fetch data using select_related and prefetch_related for optimization
        products_data = Product.objects.select_related('productvariant').prefetch_related('productvariant__productvariantprice').values(
            'title',
            'description',
            'productvariant__variant__title',
            'productvariant__productvariantprice__price',
            'productvariant__productvariantprice__stock'
        ).distinct()

        # Convert the queryset to a list for better manipulation in the template
        products_list = list(products_data)

        # Render the template with the data
        return render(request, self.template_name, {'products_list': products_list})