from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, SearchForm


def home(request):
    """Display list of published posts with pagination"""
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    """Display single post with comments"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check if user can view the post
    if post.status == 'draft' and (not request.user.is_authenticated or 
                                   (request.user != post.author and not request.user.is_staff)):
        messages.error(request, 'This post is not available.')
        return redirect('blog:home')
    
    comments = post.approved_comments
    comment_form = CommentForm()
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:post_detail', slug=slug)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'title': post.title
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """Display posts by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'title': f'Category: {category.name}'
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """Display posts by tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tag': tag,
        'title': f'Tag: {tag.name}'
    }
    return render(request, 'blog/tag_posts.html', context)


def search(request):
    """Search posts by title and content"""
    form = SearchForm(request.GET)
    posts = []
    query = ''
    
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                status='published'
            ).distinct()
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'query': query,
        'title': f'Search: {query}' if query else 'Search'
    }
    return render(request, 'blog/search.html', context)


@login_required
def dashboard(request):
    """Author dashboard for managing posts"""
    if not request.user.profile.is_author:
        messages.error(request, 'You need author privileges to access the dashboard.')
        return redirect('blog:home')
    
    posts = Post.objects.filter(author=request.user)
    
    context = {
        'posts': posts,
        'title': 'Dashboard'
    }
    return render(request, 'blog/dashboard.html', context)


@login_required
def create_post(request):
    """Create a new post"""
    if not request.user.profile.is_author:
        messages.error(request, 'You need author privileges to create posts.')
        return redirect('blog:home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('blog:dashboard')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create Post'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def edit_post(request, slug):
    """Edit an existing post"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check permissions
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('blog:dashboard')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:dashboard')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': f'Edit: {post.title}'
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def delete_post(request, slug):
    """Delete a post"""
    post = get_object_or_404(Post, slug=slug)
    
    # Check permissions
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('blog:dashboard')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:dashboard')
    
    context = {
        'post': post,
        'title': f'Delete: {post.title}'
    }
    return render(request, 'blog/post_confirm_delete.html', context)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Only comment owner or admin can delete
    if comment.user != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('blog:post_detail', slug=comment.post.slug)
    
    post_slug = comment.post.slug
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('blog:post_detail', slug=post_slug)
