from pathlib import Path

import fontforge
import pytest

from fontforge_refsel.searchRefs import whatRefers


@pytest.fixture
def testFont():
    path = Path(__file__).parent / 'assets' / 'Inconsolata-LGC.sfd'
    font = fontforge.open(str(path))
    yield font
    font.close()


@pytest.mark.parametrize(('glyphname', 'indirect', 'expected'), [
    ('ampersand', False, []),
    ('zhe', False, ['zhebreve', 'zhedieresiscyrillic']),
    ('A', False, [
        'Aring', 'Agrave', 'Aacute', 'Acircumflex', 'Atilde', 'Adieresis',
        'Aogonek', 'Abreve', 'Alpha', 'Acyril', 'Amacron', 'Aringacute',
        'universal', 'Adotbelow', 'Ahookabove', 'Acaron', 'Abrevecyrillic',
        'Adieresiscyrillic', 'Adblgrave', 'Ainvertedbreve', 'Adieresismacron',
        'uni0226', 'Adotmacron', 'Aringbelow', 'Aacute.pinyin',
        'Adieresis.alt',
    ]),
    ('A', True, [
        'Aring', 'Agrave', 'Aacute', 'Acircumflex', 'Atilde', 'Adieresis',
        'Aogonek', 'Abreve', 'Alpha', 'Alphatonos', 'Acyril', 'Amacron',
        'Aringacute', 'angstrom', 'universal', 'Adotbelow', 'Ahookabove',
        'Acircumflexacute', 'Acircumflexgrave', 'Acircumflexhookabove',
        'Acircumflextilde', 'Acircumflexdotbelow', 'Abreveacute',
        'Abrevegrave', 'Abrevehookabove', 'Abrevetilde', 'Abrevedotbelow',
        'Acaron', 'Abrevecyrillic', 'Adieresiscyrillic', 'Adblgrave',
        'Ainvertedbreve', 'Adieresismacron', 'uni0226', 'Adotmacron',
        'Aringbelow', 'Aacute.pinyin', 'Adieresis.alt', 'Alphalenis',
        'Alphaasper', 'Alphabreve', 'Alphamacron', 'Alphagrave', 'Alphaacute',
    ]),
])
def test_whatRefers(testFont, glyphname, indirect, expected):
    assert whatRefers(testFont[glyphname], indirect) == expected
