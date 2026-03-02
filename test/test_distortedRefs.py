import pytest
from pathlib import Path
import fontforge
import fontforge_refsel


@pytest.fixture
def testFont():
    path = Path(__file__).parent / 'assets' / 'Inconsolata-LGC.sfd'
    font = fontforge.open(str(path))
    yield font
    font.close()


@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('exclam', False),
    ('question', False),
    ('colon', False),
    ('exclamdown', True),
    ('questiondown', True),
])
def test_distortedRefs(testFont, glyphname, expected):
    assert fontforge_refsel.glyphHasDistortedRefs(testFont[glyphname]) == expected


@pytest.mark.parametrize(('selResult', 'moreless', 'selection'), [
    (0, 0, None),
    (1, 1, ('A', 'B', 'C', 'exclamdown')),
    (2, -1, None),
])
@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('A', (False, True, True)),
    ('B', (False, True, True)),
    ('C', (False, True, True)),
    ('exclam', (False, False, True)),
    ('question', (False, False, True)),
    ('colon', (False, False, True)),
    ('exclamdown', (True, True, False)),
    ('questiondown', (True, True, False)),
])
def test_selectGlyphsWithDistortedRefs(
    testFont, glyphname, expected, selResult, moreless, selection
):
    if selection:
        testFont.selection.select(*selection)
    elif moreless < 0:
        testFont.selection.all()
    fontforge_refsel.selectGlyphsWithDistortedRefs(testFont, moreless)
    assert testFont.selection[glyphname] == expected[selResult]
