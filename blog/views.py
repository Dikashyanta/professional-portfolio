from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post


def blog_list(request):
    post_list = Post.objects.filter(published=True)
    paginator = Paginator(post_list, 6)  # 6 posts per page, matches the 2x3 grid
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    word_count = len(post.content.split())
    read_time = max(1, round(word_count / 200))  # ~200 words per minute
    return render(request, 'blog/blog_detail.html', {'post': post, 'read_time': read_time})