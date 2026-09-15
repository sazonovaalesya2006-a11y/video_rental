from enum import Enum
from datetime import date, timedelta


class CassetteStatus(Enum):
    AVAILABLE = "Свободна"
    RENTED = "Выдана"


class RentalStatus(Enum):
    ACTIVE = "Активен"
    RETURNED = "Возвращён"


class Film:
    """Фильм — хранит информацию о фильме."""

    def __init__(self, title, genre, year, director, duration, age_limit, description=""):
        self._title = title
        self._genre = genre
        self._year = year
        self._director = director
        self._duration = duration
        self._age_limit = age_limit
        self._description = description

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def genre(self):
        return self._genre

    @property
    def year(self):
        return self._year

    @property
    def director(self):
        return self._director

    @property
    def duration(self):
        return self._duration

    @property
    def age_limit(self):
        return self._age_limit

    @property
    def description(self):
        return self._description

    def __str__(self):
        return (f"«{self._title}» ({self._year}), жанр: {self._genre}, "
                f"режиссёр: {self._director}, {self._duration} мин., {self._age_limit}")


class Videocassette:
    """Видеокассета — привязана к одному фильму, имеет статус."""

    def __init__(self, cassette_id, film):
        self._id = cassette_id
        self._film = film
        self._status = CassetteStatus.AVAILABLE

    @property
    def id(self):
        return self._id

    @property
    def film(self):
        return self._film

    @property
    def status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def is_available(self):
        return self._status == CassetteStatus.AVAILABLE

    def __str__(self):
        return f"Кассета №{self._id} — {self._film.title} [{self._status.value}]"


class Client:
    """Клиент пункта проката."""

    def __init__(self, surname, name, patronymic, contact):
        self._surname = surname
        self._name = name
        self._patronymic = patronymic
        self._contact = contact

    @property
    def surname(self):
        return self._surname

    @property
    def name(self):
        return self._name

    @property
    def patronymic(self):
        return self._patronymic

    @property
    def contact(self):
        return self._contact

    @property
    def full_name(self):
        return f"{self._surname} {self._name} {self._patronymic}"

    def __str__(self):
        return f"{self.full_name} (контакт: {self._contact})"


class Rental:
    """Операция проката одной видеокассеты одному клиенту."""

    COST_PER_CASSETTE = 200.0    # руб. за одну кассету
    RENTAL_DAYS = 7              # календарных дней
    FINE_PER_DAY = 20.0          # руб. за каждый день просрочки

    def __init__(self, client, cassette, start_date):
        self._client = client
        self._cassette = cassette
        self._start_date = start_date
        self._due_date = start_date + timedelta(days=self.RENTAL_DAYS)
        self._return_date = None
        self._cost = self.calculate_cost()
        self._fine = 0.0
        self._status = RentalStatus.ACTIVE

    @property
    def client(self):
        return self._client

    @property
    def cassette(self):
        return self._cassette

    @property
    def start_date(self):
        return self._start_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def return_date(self):
        return self._return_date

    @property
    def cost(self):
        return self._cost

    @property
    def fine(self):
        return self._fine

    @property
    def status(self):
        return self._status

    def calculate_cost(self):
        """Стоимость проката = 200 руб. за одну кассету."""
        return self.COST_PER_CASSETTE

    def calculate_fine(self, today):
        """Штраф = 20 руб. за каждый день просрочки."""
        if today <= self._due_date:
            return 0.0
        overdue_days = (today - self._due_date).days
        return overdue_days * self.FINE_PER_DAY

    def is_overdue(self, today):
        return today > self._due_date

    def close(self, today):
        """Закрыть прокат (оформить возврат)."""
        self._return_date = today
        self._fine = self.calculate_fine(today)
        self._status = RentalStatus.RETURNED

    def __str__(self):
        info = (f"Прокат: клиент «{self._client.full_name}», "
                f"кассета №{self._cassette.id} ({self._cassette.film.title})\n"
                f"  Дата выдачи: {self._start_date}, плановая дата возврата: {self._due_date}\n"
                f"  Стоимость: {self._cost:.2f} руб.")
        if self._status == RentalStatus.RETURNED:
            info += (f"\n  Фактическая дата возврата: {self._return_date}, "
                     f"штраф: {self._fine:.2f} руб.")
        return info