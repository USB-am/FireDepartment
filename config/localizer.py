TRANSLATION_WORDS = {
	'title': 'заголовок',
}


def LOCALIZE(text: str) -> str:
	words = text.lower().split()

	localized_text = ' '.join(
		[TRANSLATION_WORDS.get(word, word) for word in words]
	)

	return localized_text