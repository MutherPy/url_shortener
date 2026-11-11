from dataclasses import dataclass

@dataclass
class UrlCreateDomainDTO:
    original_url: str

@dataclass
class UrlCreatedDomainDTO:
    code: str
    short_url: str
