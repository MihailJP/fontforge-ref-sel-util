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


@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('ampersand', []),
    ('zhe', ['zhebreve', 'zhedieresiscyrillic']),
])
def test_whatRefers(testFont, glyphname, expected):
    assert whatRefers(testFont[glyphname]) == expected
