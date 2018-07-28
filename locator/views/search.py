from django.contrib.postgres.search import SearchVector
from locator.models import Product
from django.views.generic.list import ListView

class SearchView(ListView):
   model = Product
   template_name = 'locator/product/search_results.html'
   context_object_name = 'products'
   paginate_by = 5

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.config_kwargs = {}
       search_settings = getattr(settings, 'SEARCH_SETTINGS', {})
       if 'config' in search_settings:
           self.config_kwargs['config'] = search_settings['config']

   def get_queryset(self):
       qs = Product.objects.filter(visible=True)

       try:
           search_string = self.request.GET['q']
           qs = qs.annotate(
               search=(
                   SearchVector('name', **self.config_kwargs) +
                   SearchVector('description', **self.config_kwargs) +
                   SearchVector('brand', **self.config_kwargs)
               ),
           ).filter(search=SearchQuery(search_string, **self.config_kwargs))
       except KeyError:
           return Product.objects.none()

       return qs.order_by('updated_at')


       # https://emptyhammock.com/blog/Postgres-full-text-search-with-Django.html