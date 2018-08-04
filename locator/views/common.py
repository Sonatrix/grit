from django.shortcuts import render
from locator.models import Product, Category

def contact(request):
	categories = Category.objects.all()[:5]

	return render(request, 'locator/common/contact_us.html', {"categories": categories})
