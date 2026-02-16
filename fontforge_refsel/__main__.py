import fontforge
from . import nestedRefs


def _selectGlyphsWithNestedRefsMenu(u, font):
	nestedRefs.selectGlyphsWithNestedRefs(font)


def _decomposeNestedRefsMenu(u, font):
	nestedRefs.decomposeNestedRefs(font)


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
