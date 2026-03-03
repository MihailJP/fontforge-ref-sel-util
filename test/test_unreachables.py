import pytest
from pathlib import Path
import fontforge
import fontforge_refsel
from fontforge_refsel.unreachables import (
    _glyphIsEncodedOrDefault,
    _referredGlyphs,
    _gsubGlyphs,
    _ligatureGlyphs,
)


@pytest.fixture
def testFont():
    path = Path(__file__).parent / 'assets' / 'Inconsolata-LGC.sfd'
    font = fontforge.open(str(path))
    yield font
    font.close()


@pytest.fixture
def testFont2():
    path = Path(__file__).parent / 'assets' / 'OldStandard-Regular.sfd'
    font = fontforge.open(str(path))
    yield font
    font.close()


@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('A', True),
    ('.notdef', True),
    ('zero.longslash', True),
    ('zero.noslash', False),
])
def test_glyphIsEncodedOrDefault(testFont, glyphname, expected):
    assert _glyphIsEncodedOrDefault(testFont[glyphname]) == expected


@pytest.mark.parametrize(('testFunc', 'glyphname', 'expected'), [
    (_referredGlyphs, 'circumflex.cap', True),
    (_referredGlyphs, 'acute.cap', True),
    (_referredGlyphs, 'd.narrow', True),
    (_referredGlyphs, 'ze.bg', False),
    (_referredGlyphs, 'iu.bg', False),
    (_gsubGlyphs, 'd.narrow', False),
    (_gsubGlyphs, 'ze.bg', True),
    (_gsubGlyphs, 'iu.bg', True),
    (_gsubGlyphs, 'dollar.var1', True),
    (_gsubGlyphs, 'dollar.var2', True),
])
def test_glyphSet(testFunc, testFont, glyphname, expected):
    assert (
        glyphname in testFunc(
            testFont,
            set((
                glyph.glyphname for glyph in testFont.glyphs() if _glyphIsEncodedOrDefault(glyph)
            ))
        )
    ) == expected


@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('f_f_j', True),
    ('f_j', True),
    ('eogonek', True),
    ('afii10194_acutecomb', True),
    ('uni0313_gravecomb.grek', True),
    ('afii10147.csl', False),
    ('afii10194.low', False),
])
def test_ligatureGlyphs(testFont2, glyphname, expected):
    assert (
        glyphname in _ligatureGlyphs(
            testFont2,
            set((
                glyph.glyphname for glyph in testFont2.glyphs() if _glyphIsEncodedOrDefault(glyph)
            ))
        )
    ) == expected


DISABLE_TEST = (
    'A',
    'f',
    'zero',
    'iogonek',
    'afii10147',
    'afii10194',
    'afii10072',
)


UNLINK_TEST = (
    'zero.dnom',
    'afii10194_acutecomb',
    'uni04C2',
)


@pytest.mark.parametrize(('selResult', 'disable', 'unlink'), [
    (0, None, None),
    (1, DISABLE_TEST, None),
    (2, DISABLE_TEST, UNLINK_TEST),
])
@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('A', (False, False, False)),
    ('B', (False, False, False)),
    ('C', (False, False, False)),
    ('afii10072', (False, False, True)),
    ('zero.dnom', (False, False, False)),
    ('iogonek.dotless', (False, True, True)),
    ('afii10147.csl', (False, True, True)),
    ('afii10194.low', (False, True, True)),
    ('afii10194_acutecomb', (False, True, True)),
    ('f_j', (False, True, True)),
    ('f_f_j', (False, False, False)),
])
def test_unusedGlyphs(testFont2, glyphname, expected, selResult, disable, unlink):
    if disable:
        for glyph in disable:
            testFont2[glyph].unicode = -1
            testFont2[glyph].altuni = None
    if unlink:
        testFont2.selection.select(*unlink)
        testFont2.unlinkReferences()
    assert (glyphname in fontforge_refsel.unusedGlyphs(testFont2)) == expected[selResult]


@pytest.mark.parametrize(('selResult', 'moreless', 'selection'), [
    (0, 0, None),
    (1, 1, ('A', 'B', 'C', 'caron.cap')),
    (2, -1, None),
])
@pytest.mark.parametrize(('glyphname', 'expected'), [
    ('A', (False, True, True)),
    ('B', (False, True, True)),
    ('C', (False, True, True)),
    ('D', (False, False, True)),
    ('E', (False, False, True)),
    ('caron.cap', (True, True, False)),
    ('invertedbreve', (True, True, False)),
])
def test_selectUnusedGlyphs(
    testFont, glyphname, expected, selResult, moreless, selection
):
    fontforge_refsel.decomposeNestedRefs(testFont, True)
    if selection:
        testFont.selection.select(*selection)
    elif moreless < 0:
        testFont.selection.all()
    fontforge_refsel.selectUnusedGlyphs(testFont, moreless)
    assert testFont.selection[glyphname] == expected[selResult]
