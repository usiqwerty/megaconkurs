class ConcursPlace:
    number: int
    snils: str
    bvi: bool
    prior: int
    attestat: bool
    ball: int
    subjects: dict
    def __init__(self, snils=None, number=None, bvi=None, prior=None, attestat=None, ball=None):
        self.number=number
        self.snils=snils
        self.bvi = bvi
        self.prior=prior
        self.attestat=attestat
        self.ball=ball

        self.subjects=dict()
    def __repr__(self):
        return f"{self.number}: {self.snils} ({self.ball}) p{self.prior} {'БВИ' if self.bvi else ''} {'ОРИГ' if self.attestat else ''}"


class FakeResponse:
    text: str
    def __init__(self, text):
        self.text=text