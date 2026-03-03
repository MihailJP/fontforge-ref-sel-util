import fontforge
from numbers import Real
from copy import deepcopy


__all__ = ["unusedGlyphs", "selectUnusedGlyphs"]


def _glyphIsEncodedOrDefault(glyph: fontforge.glyph) -> bool:
    return any([
        glyph.unicode >= 0,
        glyph.altuni is not None,
        glyph.glyphname == '.notdef',
    ])


def _referredGlyphs(font: fontforge.font, referFrom: set[str]) -> set[str]:
    referred = set()
    for glyph in referFrom:
        for (ref, _, _) in font[glyph].references:
            referred.add(ref)
    return referred


def _gsubGlyphs(font: fontforge.font, referFrom: set[str]) -> set[str]:
    referred = set()
    for glyph in referFrom:
        for (_, lookupType, *lookupData) in font[glyph].getPosSub('*'):
            if lookupType in ('Substitution', 'AltSubs', 'MultSubs'):
                for ref in lookupData:
                    referred.add(ref)
    return referred


def _ligatureGlyphs(font: fontforge.font, referFrom: set[str]) -> set[str]:
    referred = set()
    for glyph in font:
        for (_, lookupType, *lookupData) in font[glyph].getPosSub('*'):
            if lookupType == 'Ligature':
                if all([(g in referFrom) for g in lookupData]):
                    referred.add(glyph)
    return referred


def unusedGlyphs(font: fontforge.font) -> set[str]:
    """
    Returns names of unused glyphs

    Returns names of glyphs which neither has Unicode encodings nor is
    referenced from another glyph or a GSUB table.
    Such glyphs can be dropped to reduce the file size.

    **CAVEAT** This function may crash if Python < 3.12

    :param font: Fontforge font object
    :type font: fontforge.font
    :return: Names of unused glyphs
    :rtype: set[str]
    """
    used = set([glyph.glyphname for glyph in filter(_glyphIsEncodedOrDefault, font.glyphs())])
    delta = deepcopy(used)
    while delta:
        newDelta = set()
        newDelta |= _referredGlyphs(font, delta)
        newDelta |= _gsubGlyphs(font, delta)
        newDelta |= _ligatureGlyphs(font, used)
        used |= newDelta
        delta = newDelta - used
    unused = set(font) - used
    return unused


def selectUnusedGlyphs(font: fontforge.font, moreless: Real = 0):
    """
    Selects unused glyphs

    **CAVEAT** This function may crash if Python < 3.12

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
