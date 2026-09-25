"""Фабрика тестовых данных (паттерн Object Mother)."""
from datetime import date
from models import Film, Videocassette, Client, Rental


class TestDataFactory:
    """Фабричные методы для создания тестовых объектов."""

    @staticmethod
    def create_film(title="Матрица", genre="Фантастика", year=1999,
                    director="Вачовски", duration=136, age_limit="16+",
                    description="Описание"):
        return Film(title, genre, year, director, duration, age_limit, description)

    @staticmethod
    def create_cassette(cassette_id="VC-001", film=None):
        if film is None:
            film = TestDataFactory.create_film()
        return Videocassette(cassette_id, film)

    @staticmethod
    def create_client(surname="Иванов", name="Иван", patronymic="Иванович",
                      contact="+79154558289"):
        return Client(surname, name, patronymic, contact)

    @staticmethod
    def create_rental(client=None, cassette=None, start_date=None):
        if client is None:
            client = TestDataFactory.create_client()
        if cassette is None:
            cassette = TestDataFactory.create_cassette()
        if start_date is None:
            start_date = date(2026, 1, 1)
        return Rental(client, cassette, start_date)