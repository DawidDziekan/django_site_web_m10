from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from .models import Author, Quote, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from scrapers.spiders.authors_spider import AuthorsSpider
from scrapers.spiders.quotes_spider import QuotesSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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
    if request.method == 'POST':
        name = request.POST['name']
        bio = request.POST['bio']
        author = Author(name=name, bio=bio)
        author.save()
        return redirect('author_list')
    return render(request, 'add_author.html')

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
        process = CrawlerProcess(settings=get_project_settings())
        process.crawl(AuthorsSpider)
        process.crawl(QuotesSpider)
        process.start()
        
        return redirect('home')
    return render(request, 'scrape.html')

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})

def top_tags(request):
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, 'top_tags.html', {'tags': tags})

def quotes_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = tag.quote_set.all()
    return render(request, 'quotes_by_tag.html', {'quotes': quotes, 'tag': tag})

def quote_list(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quote_list.html', {'page_obj': page_obj})