import requests
import time
import os

from bs4 import BeautifulSoup

def get_blog_articles():
    '''
    saves the text of 5 articles from the codeup website
    '''
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)

    # request the content from the main page
    soup = BeautifulSoup(response.content, 'html.parser')

    # create a dictionary to hold link, title and content of the article
    blog_articles = {
        #'link':[],
        'title':[],
        'content':[]
    }
    for i in range(len(h2)-1):
        # link
        link = h2[i].a['href']
        #blog_articles['link'].append(link)
        # title
        blog_articles['title'].append(h2[i].a.text)
        # request the content from the article using the link
        s = BeautifulSoup(requests.get(link, headers=headers).content, 'html.parser')
        # inside the <div class='entry-content ...> find all paragraphers'
        texts = s.find('div', class_='entry-content').find_all('p')
        # text holds all words from the article
        text = ''
        for t in texts:
            # each article has the same ending *Codeup ..., so I don't grab it
            if not t.text.startswith('*Codeup'):
                text += t.text
            else:
                break
        # add the article's text to the dictionary
        blog_articles['content'].append(text)
    return blog_articles

def get_news_articles():
    url = 'https://inshorts.com/en/read'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = soup.find('ul', class_='category-list').find_all('a')[1:] # first one is All News, I don't grab it
    # dictionary to hold categories names and links
    categories_links = {}
    # main link
    link = 'https://inshorts.com'
    for c in categories:
        # add path to the main link
        categories_links[c.text.strip()] = link + c['href'] 
    # create a dictionary to return
    shorts = {
        'title':[],
        'content':[],
        'category':[]
    }
    # loop through the categories and scrap the news
    for key in categories_links:
        # link
        l = categories_links[key]
        # new soup
        s = BeautifulSoup(requests.get(l).content, 'html.parser')
        # all news cards from the page
        news_cards = s.find_all('div', class_='news-card')
        for news in news_cards:
            # add title
            shorts['title'].append(news.find('a').text.strip())
            # grab the text of the article
            shorts['content'].append(news.find('div', itemprop="articleBody").text)
            # add the category name
            shorts['category'].append(key)
    return shorts