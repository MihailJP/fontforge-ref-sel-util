import fontforge
import psMat
from numbers import Real

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
		for ref in glyph.references:
			(srcglyph, matrix, _) = ref
			if len(font[srcglyph].references) > 0:
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
		for glyph in (font.glyphs() if allGlyphs else font.selection.byGlyphs):
			decomposedRef = []
			for ref in glyph.references:
				(srcglyph, matrix, _) = ref
				if len(font[srcglyph].references) > 0:
					for srcref in font[srcglyph].references:
						decomposedRef += [(srcref[0], psMat.compose(srcref[1], matrix), False)]
					nestedRefsFound = True
				else:
					decomposedRef += [ref]
			glyph.references = tuple(decomposedRef)
		if not nestedRefsFound:
			break


def selectGlyphsWithNestedRefsMenu(u, font):
	selectGlyphsWithNestedRefs(font)


def decomposeNestedRefsMenu(u, font):
	decomposeNestedRefs(font)


def fontforge_plugin_init(**kw):
	fontforge.registerMenuItem(
		callback=selectGlyphsWithNestedRefsMenu,
		enable=lambda x, y: True,
		context="Font",
		name="Select glyphs with nested references"
	)
	fontforge.registerMenuItem(
		callback=decomposeNestedRefsMenu,
		enable=lambda x, y: True,
		context="Font",
		name="Decompose nested references"
	)
