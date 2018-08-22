from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.aggregates import StringAgg
from locator.models import Product, Category
from django.views.generic.list import ListView
from locator.filters import ProductFilter
from django.shortcuts import render

# class SearchView(ListView):
#    model = Product
#    template_name = 'locator/product/search_results.html'
#    paginate_by = 20

#    def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       qs = Product.objects.prefetch_related().all()
#       try:
#           search_string = self.request.GET['q']
#           query = SearchQuery(search_string)
#           vector=(
#               SearchVector('name',  weight='A') +
#               SearchVector('description',  weight='C')
#           )
#           qs = qs.annotate(
#               document=vector, rank=SearchRank(vector, query)
#           ).filter(document=query).order_by('-rank').prefetch_related().values()
#       except KeyError:
#           return Product.objects.none()

#       context['products'] = qs.order_by('updated_at')
#       context["path"] = search_string
#       return context

def search(request):
    product_list = Product.objects.prefetch_related().all().order_by("?")
    product_filter = ProductFilter(request.GET, queryset=product_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_filter.qs, 10)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'locator/product/search_results.html', {'filter': product_filter, 'products':numbers})
