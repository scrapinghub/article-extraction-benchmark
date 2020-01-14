import pytest

from evaluate import string_shingle_matching, _ngrams, _tokenize


def test_tokenize():
    assert _tokenize('a b,cd:e(foo,bar) ') == \
           ['a', 'b', 'cd', 'e', 'foo', 'bar']


@pytest.mark.parametrize(
    ['text', 'n', 'expected'],
    [('!', 4, []),
     ('a,b c ', 5, [('a', 'b', 'c')]),
     ('aa 11 c 22', 3, [('aa', '11', 'c'), ('11', 'c', '22')]),
     ('a b c a b c', 3, [('a', 'b', 'c'), ('b', 'c', 'a'),
                         ('c', 'a', 'b'), ('a', 'b', 'c')]),
     ])
def test_ngrams(text, n, expected):
    assert _ngrams(text, n) == expected


@pytest.mark.parametrize(
    ['true', 'pred', 'tp_fp_fn'],
    [('a b c', 'a b c', (1, 0, 0)),
     ('a b c d', 'a b c', (0.5, 0, 0.5)),
     ('a b c', 'a b c d', (0.5, 0.5, 0)),
     ('', '', (0, 0, 0)),
     ('a', '', (0, 0, 1)),
     ('', 'a', (0, 1, 0)),
     ('a b c a b c', 'a b c', (0.25, 0, 0.75)),
     ('a b c', 'a b c a b c', (0.25, 0.75, 0)),
     ])
def test_string_shingle_matching(true, pred, tp_fp_fn):
    assert string_shingle_matching(true, pred, ngram_n=3) == tp_fp_fn
