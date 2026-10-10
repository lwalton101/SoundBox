import math


class Track:
    def __init__(self, id: str | None, position: int, number: int, length: int, artist_credit: str, title: str) -> None:
        self.id: str | None = id 
        self.position = position
        self.number = number
        self.length = length
        self.artist_credit = artist_credit
        self.title = title
        
    def get_formatted_length(self) -> str:
        minutes: int = int(self.length / 1000 // 60)
        seconds = int(self.length / 1000 % 60)
        return f"{minutes}:{seconds:02}"