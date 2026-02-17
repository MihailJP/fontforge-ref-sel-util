import fontforge


def selectedGlyphs(font: fontforge.font, allGlyphs: bool = False):
    """
    Returns selected glyphs

    :param font: Fontforge font object
    :type font: fontforge.font
    :param allGlyphs: If ``True``, always returns all glyphs. \
    If ``False``, returns selected glyphs if any. \
    If no glyphs are selected, returns all glyphs.
    :type allGlyphs: bool
    """
    if any(font.selection):
        return font.selection.byGlyphs
    else:
        return font.glyphs()
