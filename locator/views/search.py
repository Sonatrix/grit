from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg
from locator.models import Product, Category
from django.views.generic.list import ListView

class SearchView(ListView):
   model = Product
   template_name = 'locator/product/search_results.html'
   paginate_by = 20

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      qs = Product.objects.prefetch_related().all()
      try:
          search_string = self.request.GET['q']
          query = SearchQuery(search_string)
          vector=(
              SearchVector('name',  weight='A') +
              SearchVector('description',  weight='C')
          )
          qs = qs.annotate(
              document=vector, rank=SearchRank(vector, query)
          ).filter(document=query).order_by('-rank').values()
      except KeyError:
          return Product.objects.none()

      context['products'] = qs.order_by('updated_at')
      context["path"] = search_string
      return context