import re

from bs4 import BeautifulSoup, Comment
from .common import inject_tm


def inject_tm_html(html_text):
    # html5lib корректно парсит html-entity
    soup = BeautifulSoup(html_text, 'html5lib')
    text_elems = soup.find_all(text=True)

    for elem in text_elems:
        if is_valid_text_elem(elem):
            elem.string.replace_with(inject_tm(elem.string))

    return to_html_string(soup)


# -- helpers

def is_valid_text_elem(elem):
    return (
        not isinstance(elem.string, Comment)
        and elem.string
        and elem.string.strip()
        and elem.parent.name not in ('script', 'style')
    )


def parse_html(html_text):
    return BeautifulSoup(html_text, 'lxml')


def to_html_string(soup):
    html_text = str(soup)
    # Исправление сериализации `doctype`:
    # по неизвестной причине bs4 делает это неправильно.
    html_text = re.sub(r'^html', '<!DOCTYPE html>', html_text)
    return html_text
