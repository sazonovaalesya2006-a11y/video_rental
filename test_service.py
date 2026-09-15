import unittest
from datetime import date, timedelta
from models import Film, Videocassette, Client, CassetteStatus, RentalStatus
from service import RentalService


class TestRentalService(unittest.TestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.service = RentalService()

        # Добавляем фильм
        self.film = Film("Матрица", "Фантастика", 1999, "Вачовски", 136, "16+", "Описание")
        self.service.add_film(self.film)

        # Регистрируем кассету
        self.cassette = Videocassette("VC-001", self.film)
        self.service.register_cassette(self.cassette)

        # Регистрируем клиента
        self.client = Client("Иванов", "Иван", "Иванович", "+79154558289")
        self.service.register_client(self.client)

    def test_create_rental_success(self):
        """Успешное оформление проката."""
        success, message = self.service.create_rental(self.client, self.cassette, date(2026, 1, 1))
        self.assertTrue(success)
        self.assertIn("Прокат оформлен", message)
        self.assertEqual(self.cassette.status, CassetteStatus.RENTED)
        self.assertEqual(len(self.service.get_active_rentals()), 1)

    def test_create_rental_unavailable_cassette(self):
        """Нельзя выдать уже выданную кассету."""
        self.service.create_rental(self.client, self.cassette, date(2026, 1, 1))
        success, message = self.service.create_rental(self.client, self.cassette, date(2026, 1, 2))
        self.assertFalse(success)
        self.assertIn("уже выдана", message)

    def test_rental_limit_exceeded(self):
        """Нельзя выдать более 3 кассет одному клиенту."""
        # Создаём ещё 3 кассеты
        for i in range(2, 5):
            cassette = Videocassette(f"VC-00{i}", self.film)
            self.service.register_cassette(cassette)
            self.service.create_rental(self.client, cassette, date(2026, 1, 1))

        # Пытаемся выдать 4-ю
        cassette4 = Videocassette("VC-005", self.film)
        self.service.register_cassette(cassette4)
        success, message = self.service.create_rental(self.client, cassette4, date(2026, 1, 1))
        self.assertFalse(success)
        self.assertIn("Превышен лимит", message)

    def test_return_on_time(self):
        """Возврат в срок — штраф 0."""
        self.service.create_rental(self.client, self.cassette, date(2026, 1, 1))
        rental = self.service.get_active_rentals()[0]
        # Возврат на 5-й день (срок 7 дней)
        success, message = self.service.return_cassette(rental, date(2026, 1, 5))
        self.assertTrue(success)
        self.assertIn("штраф не начислен", message)
        self.assertEqual(rental.fine, 0)
        self.assertEqual(rental.cassette.status, CassetteStatus.AVAILABLE)

    def test_return_overdue(self):
        """Возврат с просрочкой — штраф 20 руб. за каждый день."""
        self.service.create_rental(self.client, self.cassette, date(2026, 1, 1))
        rental = self.service.get_active_rentals()[0]
        # Возврат на 10-й день (просрочка 3 дня: 8, 9, 10)
        success, message = self.service.return_cassette(rental, date(2026, 1, 10))
        self.assertTrue(success)
        # Просрочка: due_date = 8 января, возврат 10 января → 2 дня (9 и 10) ???
        # Точный расчёт: due_date = 2026-01-08. return_date = 2026-01-10. Разница = 2 дня.
        # Штраф = 2 * 20 = 40 руб.
        self.assertEqual(rental.fine, 40.0)
        self.assertIn("Штраф: 40.00", message)

    def test_find_client(self):
        """Поиск клиента по ФИО."""
        found = self.service.find_client("Иванов Иван Иванович")
        self.assertIsNotNone(found)
        self.assertEqual(found.contact, "+79154558289")

    def test_find_film(self):
        """Поиск фильма по названию."""
        found = self.service.find_film("Матрица")
        self.assertIsNotNone(found)
        self.assertEqual(found.year, 1999)


if __name__ == "__main__":
    unittest.main()