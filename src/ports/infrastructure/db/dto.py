from dataclasses import dataclass

@dataclass
class UrlCreateDbDTO:
    code: str
    original_url: str
