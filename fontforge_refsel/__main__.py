import fontforge
import psMat
from numbers import Real


def _selectedGlyphs(font: fontforge.font, allGlyphs: bool = False):
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


def glyphHasNestedRefs(glyph: fontforge.glyph) -> bool:
	"""
	Checks if glyph has nested references
	
	:param glyph: Fontforge glyph object
	:type glyph: fontforge.glyph
	:return: ``True`` if at least one reference is nested
	:rtype: bool
	"""
	font = glyph.font
	for glyph in font.glyphs():
		for ref in glyph.references:
			(srcglyph, _, _) = ref
			if len(font[srcglyph].references) > 0:
				return True
	return False


def selectGlyphsWithNestedRefs(font: fontforge.font, moreless: Real = 0):
	"""
	Selects glyphs with nested references

	:param font: Fontforge font object
	:type font: fontforge.font
	:param moreless: If positive, selects relevant glyphs in addition to the current selection. \
	If negative, deselects such glyphs. If zero, forgets current selection and then selects.
	:type moreless: numbers.Real
	"""
	glyphsWithNestedRefs = set()
	for glyph in font.glyphs():
		if glyphHasNestedRefs(glyph):
			glyphsWithNestedRefs.add(glyph.glyphname)
	if moreless == 0:
		font.selection.none()
	for glyph in glyphsWithNestedRefs:
		font.selection.select(('more',) if moreless >= 0 else ('less',), glyph)


def decomposeNestedRefs(font: fontforge.font, allGlyphs: bool = False):
	"""
	Decomposes nested references into simple ones

	Nested references are known to cause problems in some environments.
	This function decomposes such refs into single-level ones.

	:param font: Fontforge font object
	:type font: fontforge.font
	:param allGlyphs: Ignores current selection and processes all glyphs
	:type allGlyphs: bool
	"""
	while True:
		nestedRefsFound = False
		for glyph in _selectedGlyphs(font, allGlyphs):
			decomposedRef = []
			for ref in glyph.references:
				(srcglyph, matrix, _) = ref
				if len(font[srcglyph].references) > 0:
					for srcref in font[srcglyph].references:
						decomposedRef += [(srcref[0], psMat.compose(srcref[1], matrix), False)]
					for layerNum in range(min(glyph.layer_cnt, font[srcglyph].layer_cnt)):
						#  in case there are both contours and references
						layer = font[srcglyph].layers[layerNum].dup()
						layer.transform(matrix)
						glyph.layers[layerNum] += layer
					nestedRefsFound = True
				else:
					decomposedRef += [ref]
			if glyph.references != tuple(decomposedRef):
				glyph.references = tuple(decomposedRef)
		if not nestedRefsFound:
			break


def _selectGlyphsWithNestedRefsMenu(u, font):
	selectGlyphsWithNestedRefs(font)


def _decomposeNestedRefsMenu(u, font):
	decomposeNestedRefs(font)


def fontforge_plugin_init(**kw):
	fontforge.registerMenuItem(
		callback=_selectGlyphsWithNestedRefsMenu,
		enable=lambda x, y: True,
		context="Font",
		name="Select glyphs with nested references"
	)
	fontforge.registerMenuItem(
		callback=_decomposeNestedRefsMenu,
		enable=lambda x, y: True,
		context="Font",
		name="Decompose nested references"
	)
