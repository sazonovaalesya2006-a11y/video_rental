from datetime import date
from models import Film, Videocassette, Client, Rental, CassetteStatus, RentalStatus


class RentalService:
    """Сервис — центральная бизнес-логика системы проката."""

    MAX_CASSETTES_PER_CLIENT = 3

    def __init__(self):
        self._films = []
        self._cassettes = []
        self._clients = []
        self._rentals = []

    # ---------- Фильмы ----------
    def add_film(self, film):
        self._films.append(film)

    def find_film(self, title):
        for f in self._films:
            if f.title.lower() == title.lower():
                return f
        return None

    def remove_film(self, film):
        if film in self._films:
            self._films.remove(film)

    def get_all_films(self):
        return list(self._films)

    # ---------- Кассеты ----------
    def register_cassette(self, cassette):
        self._cassettes.append(cassette)

    def find_cassette(self, cassette_id):
        for c in self._cassettes:
            if c.id == cassette_id:
                return c
        return None

    def get_available_cassettes(self):
        return [c for c in self._cassettes if c.is_available()]

    def get_all_cassettes(self):
        return list(self._cassettes)

    # ---------- Клиенты ----------
    def register_client(self, client):
        self._clients.append(client)

    def find_client(self, full_name):
        for c in self._clients:
            if c.full_name.lower() == full_name.lower():
                return c
        return None

    def get_all_clients(self):
        return list(self._clients)

    # ---------- Прокат ----------
    def get_client_active_rentals(self, client):
        return [r for r in self._rentals
                if r.client is client and r.status == RentalStatus.ACTIVE]

    def create_rental(self, client, cassette, today=None):
        """Оформить прокат. Возвращает (успех: bool, сообщение: str)."""
        if today is None:
            today = date.today()

        if not cassette.is_available():
            return False, f"Кассета №{cassette.id} уже выдана."

        active = self.get_client_active_rentals(client)
        if len(active) >= self.MAX_CASSETTES_PER_CLIENT:
            return False, (f"Превышен лимит: у клиента уже "
                           f"{len(active)} кассет(ы) в прокате "
                           f"(максимум {self.MAX_CASSETTES_PER_CLIENT}).")

        rental = Rental(client, cassette, today)
        cassette.set_status(CassetteStatus.RENTED)
        self._rentals.append(rental)
        return True, (f"Прокат оформлен. Кассета №{cassette.id} выдана клиенту "
                      f"«{client.full_name}» до {rental.due_date}. "
                      f"Стоимость: {rental.cost:.2f} руб.")

    def return_cassette(self, rental, today=None):
        """Оформить возврат. Возвращает (успех: bool, сообщение: str)."""
        if today is None:
            today = date.today()

        if rental.status == RentalStatus.RETURNED:
            return False, "Этот прокат уже закрыт."

        rental.close(today)
        rental.cassette.set_status(CassetteStatus.AVAILABLE)

        message = (f"Возврат оформлен. Кассета №{rental.cassette.id} возвращена "
                   f"{today}. ")
        if rental.fine > 0:
            overdue_days = (today - rental.due_date).days
            message += (f"Просрочка {overdue_days} дн. "
                        f"Штраф: {rental.fine:.2f} руб.")
        else:
            message += "Возврат в срок, штраф не начислен."
        return True, message

    def get_active_rentals(self):
        return [r for r in self._rentals if r.status == RentalStatus.ACTIVE]

    def get_all_rentals(self):
        return list(self._rentals)