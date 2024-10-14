from datetime import datetime


class Transaction:
    SELL: int = 1
    SUPPLY: int = 2

    def __init__(self, type: int, copies: int):
        self.type: int = type
        self.copies: int = copies
        self.date: datetime = datetime.now()


class Disc:
    def __init__(self, sid: str, title: str, artist: str, sale_price: float, purchase_price: float, quantity: int):
        self.sid: str = sid
        self.title: str = title
        self.artist: str = artist
        self.sale_price: float = sale_price
        self.purchase_price: float = purchase_price
        self.quantity: int = quantity
        self.transactions: list[Transaction] = []
        self.song_list: list[str] = []

    def add_song(self, song: str):
        self.song_list.append(song)

    def sell(self, copies: int) -> bool:
        if copies > self.quantity:
            return False
        else:
            self.quantity -= copies
            new_transaction = Transaction(Transaction.SELL, copies)
            self.transactions.append(new_transaction)
            return True

    def supply(self, copies: int):
        self.quantity += copies
        new_transaction = Transaction(Transaction.SUPPLY, copies)
        self.transactions.append(new_transaction)

    def copies_sold(self) -> int:
        total_copies_sold = sum(t.copies for t in self.transactions if t.type == Transaction.SELL)
        return total_copies_sold

    def __str__(self) -> str:
        return (f"SID: {self.sid}\n"
                f"Title: {self.title}\n"
                f"Artist: {self.artist}\n"
                f"Song List: {', '.join(self.song_list)}")


class MusicStore:
    def __init__(self):
        self.discs: dict[str, Disc] = {}

    def add_disc(self, sid: str, title: str, artist: str, sale_price: float, purchase_price: float, quantity: int):
        if sid not in self.discs:
            new_disc = Disc(sid, title, artist, sale_price, purchase_price, quantity)
            self.discs[sid] = new_disc

    def search_by_sid(self, sid: str) -> Disc | None:
        return self.discs.get(sid, None)

    def search_by_artist(self, artist: str) -> list[Disc]:
        return [disc for disc in self.discs.values() if disc.artist == artist]

    def sell_disc(self, sid: str, copies: int) -> bool:
        disc = self.search_by_sid(sid)
        if disc is None:
            return False

        return disc.sell(copies)

    def supply_disc(self, sid: str, copies: int) -> bool:
        disc = self.search_by_sid(sid)
        if disc is None:
            return False

        disc.supply(copies)
        return True

    def worst_selling_disc(self) -> Disc | None:
        if not self.discs:
            return None
        worst_selling_disc = None
        worst_sales = float('inf')
        for disc in self.discs.values():
            sales = disc.copies_sold()
            if sales < worst_sales:
                worst_sales = sales
                worst_selling_disc = disc

        return worst_selling_disc