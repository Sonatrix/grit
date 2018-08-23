from django.shortcuts import render, redirect

def handler404(request):
	return redirect('locator:home')
    #return render(request,'locator/error/404.html',{})

def handler500(request):
	return redirect('locator:home')
    #return render(request,'locator/error/500.html', {})