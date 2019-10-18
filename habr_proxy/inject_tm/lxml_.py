import lxml.html
import html5_parser

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
    opts = {
        'treebuilder': 'lxml',
        'namespace_elements': False,
        'keep_doctype': True,
        'sanitize_names': False,
        'return_root': True,
    }
    return html5_parser.parse(text, **opts)


def to_html_string(tree):
    opts = {
        'encoding': 'unicode',
        'doctype': '<!DOCTYPE html>',
    }
    return lxml.html.tostring(tree, **opts)
