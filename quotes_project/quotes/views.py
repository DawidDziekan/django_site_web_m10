from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from .models import Author, Quote, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from scrapers.scraper import scrape_quote

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_author(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        bio = request.POST['bio']
        author = Author(name=name, bio=bio)
        author.save()
        return redirect('author_list')
    return render(request, 'add_author.html', {'tags': Tag.objects.all()})

@login_required
def add_quote(request):
    if request.method == 'POST':
        text = request.POST['text']
        author_id = request.POST['author']
        author = Author.objects.get(id=author_id)
        quote = Quote(text=text, author=author)
        quote.save()
        tags = request.POST.getlist('tags')
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)
        quote.save()
        return redirect('quote_list')
    authors = Author.objects.all()
    return render(request, 'add_quote.html', {'authors': authors, 'tags': Tag.objects.all()})

@login_required
def scrape_quotes(request):
    if request.method == 'POST':
        render(request, 'scrape_quotes.html')
        scrape_quote()
        return redirect('home')

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors, 'tags': Tag.objects.all()})

def quotes_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = tag.quote_set.all()
    return render(request, 'quotes_by_tag.html', {'quotes': quotes, 'tag': tag})

def quote_list(request):
    
    quotes_list = Quote.objects.all().order_by('author')
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quote_list.html', {'page_obj': page_obj, 'tags': Tag.objects.all()})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author_detail.html', {'author': author, 'tags': Tag.objects.all()})

