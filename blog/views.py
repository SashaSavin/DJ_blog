from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm
from taggit.models import Tag


def posts_view(request, tag_slug=None):
    post_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts.html', {'page': page, 'posts': posts, 'tag': tag})


def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment.filter(active=True)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return render(request, 'post.html', {'post': post,
                                         'comments': comments,
                                         'form': form })
