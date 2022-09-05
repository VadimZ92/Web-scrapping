import requests
import bs4
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

base_url = "https://habr.com"
url = "https://habr.com/ru/all/"
header = Headers(
    browser="chrome",
    os="win",
    headers=True
).generate()
response = requests.get(url, headers=header)
text = response.text
soup = bs4.BeautifulSoup(text, features="html.parser")
articles = soup.find_all("article")
## список для отсекания повторений
article_list = []
for article in articles:
    articles_list = article.find_all(class_="tm-article-snippet")
    href = article.find(class_="tm-article-snippet__readmore").attrs['href']
    link = base_url + href
    response = requests.get(link, headers=header)
    text = response.text
    soup = bs4.BeautifulSoup(text, features="html.parser")
    articles = soup.find_all("main")
    for article in articles:
        articles_list = article.find_all(class_="tm-article-presenter__content tm-article-presenter__content_narrow")
        articles_list = [articl.text.split() for articl in articles_list]
        for art in articles_list[0]:
            if art.lower() in KEYWORDS:
                title = article.find("h1").find("span").text
                if title not in article_list:
                    article_list.append(title)
                    data = article.find(class_="tm-article-snippet__datetime-published").find("time").text
                    print(f"<{data}> - <{title}> - <{link}>")
if article_list == []:
    print("Статей с ключевыми словами не нашлось")