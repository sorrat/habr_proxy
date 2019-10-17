import re
import html


TM = html.unescape('&trade;')
LETTER = r'[^\W\d_]'


def inject_tm(string: str):
    """
    Добавление значка ™ (trademark) после каждого слова из шести букв
    """
    if not string: return string
    return re.sub(
        r'\b(%s{6})\b' % LETTER,
        r'\g<1>%s' % TM,
        string,
        re.M | re.S | re.U
    )
