from collections import defaultdict

from html.parser import HTMLParser

from .common import inject_tm


def inject_tm_html(html_text):
    parser = MyHTMLParser()
    parser.feed(html_text)

    text_by_row = defaultdict(list)
    for (row, col), text in parser.points:
        for i, line in enumerate(text.splitlines()):
            text_by_row[row + i].append((col if i == 0 else 0, line))

    replacements_by_row = defaultdict(list)
    for row, points in text_by_row.items():
        for col, text in points:
            text_new = inject_tm(text)
            if text != text_new:
                replacements_by_row[row].append((col, text, text_new))

    html_lines = html_text.splitlines()
    for row, replacements in replacements_by_row.items():
        orig_line = line = html_lines[row]
        for col, text_old, text_new in replacements:
            # добавляется образовавщийся сдвиг
            col_fixed = col + len(line) - len(orig_line)
            line = replace_substring(line, text_old, text_new, col_fixed)
        html_lines[row] = line
    return '\n'.join(html_lines)


# -- helpers

def replace_substring(string, current, new, start_pos):
    part_before = string[:start_pos]
    part_after = string[start_pos + len(current):]
    return part_before + new + part_after


class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = []
        self.points = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def handle_endtag(self, tag):
        self.tags.pop()

    def handle_data(self, text):
        current_tag = self.tags[-1] if self.tags else None

        if current_tag not in ['script', 'style']:
            row, col = self.getpos()
            self.points.append([(row - 1, col), text])  # text start
