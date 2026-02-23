import fontforge
from numbers import Real


__all__ = ["unusedGlyphs", "selectUnusedGlyphs"]


def _glyphIsNotEncoded(glyph: fontforge.glyph) -> bool:
    return (glyph.unicode == -1) and (glyph.altuni is None)


def _referredGlyphs(font: fontforge.font) -> frozenset[str]:
    referred = set()
    for glyph in font.glyphs():
        for (ref, _, _) in glyph.references:
            referred.add(ref)
    return frozenset(referred)


def _gsubGlyphs(font: fontforge.font) -> frozenset[str]:
    referred = set()
    for glyph in font.glyphs():
        for (_, lookupType, *lookupData) in glyph.getPosSub('*'):
            if lookupType in ('Substitution', 'AltSubs', 'MultSubs', 'Ligature'):
                for ref in lookupData:
                    referred.add(ref)
                if lookupType == 'Ligature':
                    referred.add(glyph.glyphname)
    return frozenset(referred)


def unusedGlyphs(font: fontforge.font) -> frozenset[str]:
    """
    Returns names of unused glyphs

    Returns names of glyphs which neither has Unicode encodings nor is
    referenced from another glyph or a GSUB table.
    Such glyphs can be dropped to reduce the file size.

    :param font: Fontforge font object
    :type font: fontforge.font
    :return: Names of unused glyphs
    :rtype: frozenset[str]
    """
    unused = set([glyph.glyphname for glyph in filter(_glyphIsNotEncoded, font.glyphs())])
    unused -= _referredGlyphs(font)
    unused -= _gsubGlyphs(font)
    unused -= {'.notdef'}
    return frozenset(unused)


def selectUnusedGlyphs(font: fontforge.font, moreless: Real = 0):
    """
    Selects unused glyphs

    :param font: Fontforge font object
    :type font: fontforge.font
    :param moreless: If positive, selects relevant glyphs in addition to the current selection. \
    If negative, deselects such glyphs. If zero, forgets current selection and then selects.
    :type moreless: numbers.Real
    """
    if moreless == 0:
        font.selection.none()
    for glyph in unusedGlyphs(font):
        font.selection.select(('more',) if moreless >= 0 else ('less',), glyph)
