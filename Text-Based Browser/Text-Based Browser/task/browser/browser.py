import os
import argparse
import _collections
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def create_directory():
    indata = argparse.ArgumentParser()
    indata.add_argument("directory")
    args = indata.parse_args()
    directory = args.directory
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def create_file(url, directory, text):
    filename = url[url.index('/')+1:url.index('.')]
    with open(f'{directory}/{filename}.txt', 'w', encoding="utf-8") as file:
        file.write(text)


def parse_website(url):
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    web_contents = soup.find_all(tag for tag in tags)
    links = soup.find_all('a')
    web_text = list()

    for content in web_contents:
        content_text = content.get_text().replace('\n', ' ')
        if content_text != '':
            web_text.append(content_text)

    for link in links:
        link_text = link.get_text()
        if link_text in web_text:
            web_text[web_text.index(link_text)] = Fore.BLUE + link_text + Style.RESET_ALL

    text = '\n'.join(web_text)

    return text


file_directory = create_directory()
history = _collections.deque()

website = ''
while website != 'exit':
    website = input('> ')
    if website == 'exit':
        break
    else:
        if website == 'back':
            try:
                history.pop()
                website = history.pop()
            except Exception:
                continue

        if '.' not in website:
            try:
                open(f'{file_directory}/{website}.txt', encoding='utf-8')
            except Exception:
                print('Error: Incorrect URL')
            else:
                with open(f'{file_directory}/{website}.txt', encoding='utf-8') as content_file:
                    print(content_file.read())
                    history.append(website)
        else:
            if 'https://' not in website:
                website = 'https://' + website
            try:
                site_content = parse_website(website)
            except Exception:
                print('Error: Incorrect URL')
            else:
                create_file(website, file_directory, site_content)
                print(site_content)
                history.append(website)
