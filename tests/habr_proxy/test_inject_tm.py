import re

from habr_proxy.inject_tm import bs4_, iter_
from tests.helpers import read_fixture, html_uniform


def nullify_hrefs(text):
    return re.sub(r'href="\S+?"', 'href="..."', text, flags=re.M)


def _prepare_fixture(name):
    text = read_fixture(name).strip()
    # подменяем URL-ы из строки: в этом тесте они только мешаются
    text = nullify_hrefs(text)
    return text


INPUT_PAGE = _prepare_fixture('page_in.html')
EXPECTED_PAGE = _prepare_fixture('page_out.html')


def test_inject_tm_html__bs4():
    result_page = bs4_.inject_tm_html(INPUT_PAGE)
    assert html_uniform(EXPECTED_PAGE) == html_uniform(result_page)


def test_inject_tm_html__iter():
    result_page = iter_.inject_tm_html(INPUT_PAGE)
    assert EXPECTED_PAGE == result_page
