from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.models import Post
from locator.models import Category


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/post_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.published.all()
        context['parent_category'] = Category.published.all().filter(parent=None)
        return context


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, 'blog/post/post_detail.html', {'post': post})
