import fontforge
from numbers import Real
from copy import deepcopy


__all__ = ["unusedGlyphs", "selectUnusedGlyphs"]


def _glyphIsEncodedOrDefault(glyph: fontforge.glyph) -> bool:
    return (
        (glyph.unicode >= 0) or
        (glyph.altuni is not None) or
        (glyph.glyphname == '.notdef')
    )


def _referredGlyphs(font: fontforge.font, referFrom: set[str]) -> frozenset[str]:
    referred = set()
    for glyph in referFrom:
        for (ref, _, _) in font[glyph].references:
            referred.add(ref)
    return frozenset(referred)


def _gsubGlyphs(font: fontforge.font, referFrom: set[str]) -> frozenset[str]:
    referred = set()
    for glyph in referFrom:
        for (_, lookupType, *lookupData) in font[glyph].getPosSub('*'):
            if lookupType in ('Substitution', 'AltSubs', 'MultSubs', 'Ligature'):
                for ref in lookupData:
                    referred.add(ref)
                if lookupType == 'Ligature':
                    referred.add(glyph)
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
    used = set([glyph.glyphname for glyph in filter(_glyphIsEncodedOrDefault, font.glyphs())])
    delta = deepcopy(used)
    while delta:
        newDelta = set()
        newDelta |= _referredGlyphs(font, delta)
        newDelta |= _gsubGlyphs(font, delta)
        used |= newDelta
        delta = newDelta - used
    unused = set(font) - used
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
