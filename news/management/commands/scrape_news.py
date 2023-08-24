from django.core.management.base import BaseCommand
from ...services import create_news_item
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from concurrent.futures import ThreadPoolExecutor
import random

def normalize_datetime_to_django_format(dt_str):
    dt = parse(dt_str)
    # Format the datetime object as a string in the desired format
    return dt.strftime('%Y-%m-%d %H:%M:%S%z')

def fetch_feed(url, main_tag, link_tag, title_tag, image_tag, image_attr, category, website, date_tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml-xml')
    entries = []

    for entry in soup.find_all(main_tag):
        title = entry.find(title_tag).text
        link = entry.find(link_tag).text
        date = entry.find(date_tag).text
        published = normalize_datetime_to_django_format(date)
        if image_tag:
            if website == "Psyche":
                description_content = entry.find('description').text
                description_soup = BeautifulSoup(description_content, 'html.parser')
                image_tag_obj = description_soup.find('img')
                image = image_tag_obj['src']
            
            elif "The Athletic" in website:
                image_link = entry.find('link', {'rel': 'enclosure'})
                media_content = entry.find('media:content')  # This line is added to define media_content for "The Athletic".
                
                if media_content and 'url' in media_content.attrs:
                    image = media_content['url']
                elif "liverpool" in url:
                    image = 'https://images.unsplash.com/photo-1518188049456-7a3a9e263ab2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1674&q=80'
                else:
                    image = 'https://images.unsplash.com/photo-1486286701208-1d58e9338013?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80'
                   
            elif "The Guardian" in website:
                media_content = entry.find('media:content')
                if media_content and 'url' in media_content.attrs:
                    image = media_content['url']
                else:
                    image = 'https://images.unsplash.com/photo-1555862124-94036092ab14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1771&q=80'

            elif website == "New York Times Wirecutter":
                description_content = entry.find('description').text
                description_soup = BeautifulSoup(description_content, 'html.parser')
                image_tag_obj = description_soup.find('img')
                if image_tag_obj:
                    image = image_tag_obj['src']
                else:
                    images = ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80","https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"]
                    image = random.choice(images)


            elif "New York Times" in website:
                if 'Opinion' in url or 'Magazine' in url:
                    images = ["https://images.unsplash.com/photo-1506543277633-99deabfcd722?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=750&q=80","https://images.unsplash.com/photo-1548706108-582111196a20?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1782&q=80"]
                    image = random.choice(images)
                
                elif 'Business' in url:
                    images = ["https://images.unsplash.com/photo-1504711434969-e33886168f5c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2940&q=80",
                              "https://images.unsplash.com/photo-1572883454114-1cf0031ede2a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YnVpbGRpbmdzfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
                              "https://images.unsplash.com/photo-1543286386-2e659306cd6c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8ZmluYW5jaWFsfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60",
                              "https://images.unsplash.com/photo-1634542984003-e0fb8e200e91?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGZpbmFuY2lhbHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"]
                    image = random.choice(images)
                    
                elif "Home" in url:
                    images = ["https://images.unsplash.com/photo-1521295121783-8a321d551ad2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80","https://images.unsplash.com/photo-1573812195421-50a396d17893?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fG5ld3N8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=800&q=60"]
                    image = random.choice(images)

                elif "Travel" in url:
                    images = ["https://images.unsplash.com/photo-1488085061387-422e29b40080?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2231&q=80","https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8dHJhdmVsfGVufDB8MHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60","https://images.unsplash.com/photo-1530521954074-e64f6810b32d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRyYXZlbHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1530789253388-582c481c54b0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHRyYXZlbHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRyYXZlbHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fHRyYXZlbHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1504609773096-104ff2c73ba4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjZ8fHRyYXZlbHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1494783367193-149034c05e8f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzJ8fHRyYXZlbHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60"]
                    image = random.choice(images)
                    
                elif "Technology" in url:
                    images = ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80","https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"]
                    image = random.choice(images)

                elif "Style" in url:
                    image = 'https://images.unsplash.com/photo-1501127122-f385ca6ddd9d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=870&q=80'

                else:
                    image ='https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'

            elif website == "Popular Science":
                description_content = entry.find('description').text
                description_soup = BeautifulSoup(description_content, 'html.parser')
                image_tag_obj = description_soup.find('img')
                image = image_tag_obj['src']

            elif website == "Autosport":
                enclosure_tag = entry.find('enclosure')
                if enclosure_tag and 'url' in enclosure_tag.attrs:
                    image = enclosure_tag['url']
                else:
                    image = 'https://images.unsplash.com/photo-1656337449909-141091f4df4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'

            elif website == 'The Race':
                media_content = entry.find('media:content')
                if media_content and 'url' in media_content.attrs:
                    image = media_content['url']
                else:
                    image = 'https://images.unsplash.com/photo-1656337449909-141091f4df4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=774&q=80'

            elif website == 'This is Anfield':
                media_thumbnail = entry.find('media:thumbnail')
                if media_thumbnail and 'url' in media_thumbnail.attrs:
                    image = media_thumbnail['url']
                else:
                    image = 'https://images.unsplash.com/photo-1555862124-94036092ab14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1771&q=80'

            elif website == 'The Verge':
                content_html = entry.find('content').text
                content_soup = BeautifulSoup(content_html, 'html.parser')
                image = content_soup.find('img')['src']
            
            elif 'smithsonian' in url:
                    images = ["https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1772&q=80","https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550745165-9bc0b252726f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8dGVjaHxlbnwwfDB8MHx8fDA%3D&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60","https://images.unsplash.com/photo-1496065187959-7f07b8353c55?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fHRlY2h8ZW58MHwwfDB8fHww&auto=format&fit=crop&w=1400&q=60"]
                    image = random.choice(images)

            elif "dawn" in link:
                media_content = entry.find('media:content')
                if media_content and 'url' in media_content.attrs:
                    image = media_content['url']
                else:
                    image = 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'
           
            else:
                image = entry.find(image_tag, {image_attr: True})
                if not image:
                    image = 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'
        
        else:
            image = 'https://images.unsplash.com/photo-1588414884049-eb55cd4c72b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=776&q=80'
        entries.append([title, link, category, website, published, image])

    return entries

rss_feed_details = [
    ('https://theathletic.com/team/liverpool/?rss=1', 'entry', 'id', 'title', 'link', 'href', 'Liverpool FC','The Athletic','published'),
    ('http://www.thisisanfield.com/feed/', 'item', 'link', 'title', 'enclosure', 'url', 'Liverpool FC','This is Anfield', 'pubDate'),
    ('http://www.theguardian.com/football/rss', 'item', 'link', 'title', 'media:content', 'url', 'Football', 'The Guardian', 'pubDate'),
    ('https://theathletic.com/premier-league/?rss', 'entry', 'id', 'title', 'link', 'href', 'Football','The Athletic', 'published'),
    ('https://theathletic.com/soccer/?rss', 'entry', 'id', 'title', 'link', 'href', 'Football','The Athletic','published'),
    ('https://theathletic.com/champions-league/?rss', 'entry', 'id', 'title', 'link', 'href', 'Football','The Athletic', 'published'),
    ('https://www.autosport.com/rss/feed/f1', 'item', 'link', 'title', 'enclosure', 'url', 'Formula 1', 'Autosport', 'pubDate'),
    ('https://the-race.com/category/formula-1/feed/', 'item', 'link', 'title','media:content', 'url', 'Formula 1', 'The Race', 'pubDate'),
    ('https://aeon.co/feed.rss', 'item', 'link', 'title', None, None, 'Self Dev', "Aeon", 'pubDate'),
    ('https://psyche.co/feed', 'item', 'link', 'title', None,None, 'Self Dev', "Psyche", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Opinion.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Magazine.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Science.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', "New York Times", 'pubDate'),
    ('https://www.popsci.com/rss', 'item', 'link', 'title', 'image', 'url', 'Science & Technology', "Popular Science", 'pubDate'),
    ('http://www.smithsonianmag.com/rss/innovation/', 'item', 'link', 'title', 'enclosure', 'url', 'Science & Technology', "Smithsonian", 'pubDate'),
    ('http://www.smithsonianmag.com/rss/latest_articles/', 'item', 'link', 'title', 'enclosure', 'url', 'Science & Technology', "Smithsonian", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Travel.xml', 'item', 'link', 'title', 'media:content', 'url', 'Travel', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Style.xml', 'item', 'link', 'title', 'media:content', 'url', 'Self Dev', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Technology.xml', 'item', 'link', 'title', 'media:content', 'url', 'Science & Technology', "New York Times", 'pubDate'),
    ('http://www.nytimes.com/services/xml/rss/nyt/Business.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', "New York Times", 'pubDate'),
     ('http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'item', 'link', 'title', 'media:content', 'url', 'Global News', "New York Times", 'pubDate'),
     ('http://feeds.feedburner.com/dawn-news', 'item', 'link', 'title',  'media:content', 'url', 'Pakistan', "Dawn", 'pubDate'),
     ('https://feeds.feedburner.com/dawn-news-world', 'item', 'link', 'title',  'media:content', 'url', 'Global News', "Dawn", 'pubDate'),
    ('https://www.theverge.com/rss/reviews/index.xml', 'entry', 'id', 'title', None, None, 'Science & Technology', 'The Verge', 'published'),
    ('https://www.nytimes.com/wirecutter/rss/', 'item', 'link', 'title', 'description', 'src', 'Science & Technology', "New York Times Wirecutter", 'pubDate')
]

def fetch_feed_with_details(feed_details):
    return fetch_feed(*feed_details)


# ... (the rest of your code)

class Command(BaseCommand):
    help = 'Scrape news from various sources'

    def handle(self, *args, **options):
        all_entries = []

        # Using ThreadPoolExecutor to parallelize the fetch operations
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(fetch_feed_with_details, rss_feed_details))
            
        # Flatten the list of lists
        for result in results:
            all_entries.extend(result)

        print(all_entries)
        
        for entry in all_entries:
            title, link, category, website, published, image = entry
            item = create_news_item(title=title, link=link, category=category, website=website, published=published, image=image)
            if item:
                self.stdout.write(self.style.SUCCESS(f'Successfully added article: {title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Duplicate article found: {title}'))

                self.stdout.write(self.style.SUCCESS('Successfully scraped news'))