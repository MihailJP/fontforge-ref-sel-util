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
    ('A', False),
    ('B', False),
    ('C', False),
    ('D', False),
    ('E', False),
    ('ocircumflex', False),
    ('ccaron', True),
    ('scaron', True),
])
def test_nestedRefs(testFont, glyphname, expected):
    assert fontforge_refsel.glyphHasNestedRefs(testFont[glyphname]) == expected


@pytest.mark.parametrize(('selResult', 'moreless', 'selection'), [
    (0, 0, None),
    (1, 1, ('A', 'B', 'C', 'ccaron')),
    (2, -1, None),
])
@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('A', (False, True, True)),
    ('B', (False, True, True)),
    ('C', (False, True, True)),
    ('D', (False, False, True)),
    ('E', (False, False, True)),
    ('ocircumflex', (False, False, True)),
    ('ccaron', (True, True, False)),
    ('scaron', (True, True, False)),
])
def test_selectGlyphsWithNestedRefs(
    testFont, glyphname, expected, selResult, moreless, selection
):
    if selection:
        testFont.selection.select(*selection)
    elif moreless < 0:
        testFont.selection.all()
    fontforge_refsel.selectGlyphsWithNestedRefs(testFont, moreless)
    assert testFont.selection[glyphname] == expected[selResult]


@pytest.mark.parametrize(('selResult', 'allGlyphs', 'selection'), [
    (0, True, None),
    (0, True, ('A', 'B', 'C', 'ccaron')),
    (0, False, None),
    (1, False, ('A', 'B', 'C', 'ccaron')),
])
@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('A', (False, False)),
    ('B', (False, False)),
    ('C', (False, False)),
    ('D', (False, False)),
    ('E', (False, False)),
    ('ocircumflex', (False, False)),
    ('ccaron', (True, True)),
    ('scaron', (True, False)),
])
def test_decomposeNestedRefs(
    testFont, glyphname, expected, selResult, allGlyphs, selection
):
    if selection:
        testFont.selection.select(*selection)
    else:
        testFont.selection.none()
    fontforge_refsel.decomposeNestedRefs(testFont, allGlyphs)
    assert testFont[glyphname].changed == expected[selResult]
    assert not (expected[selResult] and fontforge_refsel.glyphHasNestedRefs(testFont[glyphname]))


def test_decomposeNestedRefs_mixed(testFont):
    testFont['dasiavaria'].unlinkRef('dasia')
    fontforge_refsel.decomposeNestedRefs(testFont, True)
    assert len(testFont['etaiotasubaspergrave'].references) == 3
    assert len(testFont['etaiotasubaspergrave'].layers[1]) == 1
