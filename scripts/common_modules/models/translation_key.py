from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TranslationKey:
	id: str
	en: str | None = None
	jp: str | None = None
