from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from locator.models import Product, Category


def contact(request):
	categories = Category.objects.all()
	
	return render(request, 'locator/common/contact_us.html', {"categories": categories})
