from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post

def post_list(request):
	post_list = Post.published.all()
	paginator = Paginator(post_list, 3) # 3 posts on each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer deliver first page
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blog/post/post_list.html',{'page': page, 'posts': posts})

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, 
		status='published', 
		publish__year=year,
        publish__month=month,
        publish__day=day
		)

	return render(request, 'blog/post/post_detail.html', {'post': post})

