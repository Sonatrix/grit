from django.shortcuts import render
from locator.models import Product, Category

def contact(request):
	return render(request, 'locator/common/contact_us.html')
