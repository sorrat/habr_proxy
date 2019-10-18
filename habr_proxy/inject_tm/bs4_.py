import html5_parser
from bs4 import Comment

from .common import inject_tm


def inject_tm_html(html_text):
    soup = parse_html(html_text)
    text_elems = soup.find_all(text=True)

    for elem in text_elems:
        if is_valid_text_elem(elem):
            elem.string.replace_with(inject_tm(elem.string))

    return str(soup)


# -- helpers

def is_valid_text_elem(elem):
    return (
        not isinstance(elem.string, Comment)
        and elem.string
        and elem.string.strip()
        and elem.parent.name not in ('script', 'style')
    )


def parse_html(text):
    opts = {
        'treebuilder': 'soup',
        'namespace_elements': False,
        'keep_doctype': True,
        'sanitize_names': False,
    }
    return html5_parser.parse(text, **opts)
