import requests
from bs4 import BeautifulSoup
from quotes.models import Quote, Tag, Author

def scrape_quote():
    start_url = 'http://quotes.toscrape.com/'
    saved_authors = []

    while start_url:
        response = requests.get(start_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        
        for quote in soup.select('div.quote'):
            text = quote.select_one('span.text').get_text()
            author_name = quote.select_one('span small.author').get_text()

            try:
                author, created = Author.objects.get_or_create(name=author_name)
            except Author.MultipleObjectsReturned:
                author = Author.objects.filter(name=author_name).first()

            
            if not Quote.objects.filter(text=text, author=author).exists():
                tags_text = [tag.get_text() for tag in quote.select('div.tags a.tag')]
                tags = []
                for tag_text in tags_text:
                    tag, created = Tag.objects.get_or_create(name=tag_text)
                    tags.append(tag)

                quote_instance = Quote.objects.create(
                    text=text,
                    author=author
                )
                quote_instance.tags.set(tags)
                quote_instance.save()

        quotes = soup.select('div.quote')
        for quote in quotes:
            author_name = quote.select_one('span small.author').get_text()
            if author_name not in saved_authors:
                saved_authors.append(author_name)
                author_url = quote.select_one('span a')['href']
                full_author_url = requests.compat.urljoin(start_url, author_url)
                scrape_author_info(full_author_url)

        next_page = soup.select_one('li.next a')
        if next_page:
            start_url = requests.compat.urljoin(start_url, next_page['href'])
        else:
            start_url = None

def scrape_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.select_one('h3.author-title').get_text().strip()
    born_date = soup.select_one('span.author-born-date').get_text().strip()
    born_location = soup.select_one('span.author-born-location').get_text().strip()
    bio = soup.select_one('div.author-description').get_text().strip()

    author, created = Author.objects.get_or_create(
        name=name,
        defaults={
            'born_date': born_date,
            'born_location': born_location,
            'bio': bio
        }
    )

    if not created:
        author.born_date = born_date
        author.born_location = born_location
        author.bio = bio
        author.save()

