import lxml.html
import html5lib

from .common import inject_tm


def inject_tm_html(text) -> str:
    tree = parse_html(text)
    text_elems = tree.xpath('.//text()')
    for elem in text_elems:
        parent = elem.getparent()
        if elem.strip() and parent.tag not in ['style', 'script']:
            if elem.is_text: parent.text = inject_tm(elem)
            if elem.is_tail: parent.tail = inject_tm(elem)
    return to_html_string(tree)


# -- helpers

def parse_html(text):
    # html5lib корректно парсит html-entity
    opts = {'treebuilder': 'lxml', 'namespaceHTMLElements': False}
    return html5lib.parse(text, **opts)


def to_html_string(tree):
    opts = {
        'encoding': 'unicode',
        'doctype': '<!DOCTYPE html>',
    }
    return lxml.html.tostring(tree, **opts)
