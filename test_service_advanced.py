import unittest
from datetime import date
from models import CassetteStatus, RentalStatus
from service import RentalService
from test_data import TestDataFactory


class TestRentalServiceAAA(unittest.TestCase):
    """Модульные тесты сервиса проката с паттерном AAA."""

    def setUp(self):
        """Общая подготовка для каждого теста (Arrange)."""
        self.service = RentalService()
        self.film = TestDataFactory.create_film()
        self.service.add_film(self.film)
        self.cassette = TestDataFactory.create_cassette("VC-001", self.film)
        self.service.register_cassette(self.cassette)
        self.client = TestDataFactory.create_client()
        self.service.register_client(self.client)

    # ---------- Позитивные тесты ----------

    def test_create_rental_success(self):
        # Arrange (подготовка уже в setUp)
        start_date = date(2026, 1, 1)  # stub даты

        # Act
        success, message = self.service.create_rental(
            self.client, self.cassette, start_date
        )

        # Assert
        self.assertTrue(success)
        self.assertIn("Прокат оформлен", message)
        self.assertEqual(self.cassette.status, CassetteStatus.RENTED)
        self.assertEqual(len(self.service.get_active_rentals()), 1)

    def test_return_on_time_no_fine(self):
        # Arrange
        start = date(2026, 1, 1)
        self.service.create_rental(self.client, self.cassette, start)
        rental = self.service.get_active_rentals()[0]
        return_date = date(2026, 1, 5)  # 4-й день, до срока (7 дней)

        # Act
        success, message = self.service.return_cassette(rental, return_date)

        # Assert
        self.assertTrue(success)
        self.assertEqual(rental.fine, 0)
        self.assertEqual(rental.status, RentalStatus.RETURNED)
        self.assertEqual(self.cassette.status, CassetteStatus.AVAILABLE)
        self.assertIn("штраф не начислен", message)

    # ---------- Негативные тесты ----------

    def test_create_rental_unavailable_cassette(self):
        # Arrange
        self.service.create_rental(self.client, self.cassette, date(2026, 1, 1))

        # Act
        success, message = self.service.create_rental(
            self.client, self.cassette, date(2026, 1, 2)
        )

        # Assert
        self.assertFalse(success)
        self.assertIn("уже выдана", message)

    def test_rental_limit_exceeded(self):
        # Arrange
        cassettes = []
        for i in range(2, 6):
            c = TestDataFactory.create_cassette(f"VC-00{i}", self.film)
            self.service.register_cassette(c)
            cassettes.append(c)
        # Занимаем 3 кассеты
        for c in cassettes[:3]:
            self.service.create_rental(self.client, c, date(2026, 1, 1))

        # Act — пытаемся оформить 4-ю
        success, message = self.service.create_rental(
            self.client, cassettes[3], date(2026, 1, 1)
        )

        # Assert
        self.assertFalse(success)
        self.assertIn("Превышен лимит", message)

    # ---------- Граничные тесты ----------

    def test_return_exactly_on_due_date(self):
        # Arrange
        start = date(2026, 1, 1)
        self.service.create_rental(self.client, self.cassette, start)
        rental = self.service.get_active_rentals()[0]
        due_date = rental.due_date  # 2026-01-08

        # Act — возврат ровно в срок
        success, message = self.service.return_cassette(rental, due_date)

        # Assert
        self.assertTrue(success)
        self.assertEqual(rental.fine, 0)

    def test_return_one_day_overdue(self):
        # Arrange
        start = date(2026, 1, 1)
        self.service.create_rental(self.client, self.cassette, start)
        rental = self.service.get_active_rentals()[0]
        return_date = date(2026, 1, 9)  # просрочка 1 день

        # Act
        success, message = self.service.return_cassette(rental, return_date)

        # Assert
        self.assertTrue(success)
        self.assertEqual(rental.fine, 20.0)

    # ---------- Использование dummy-объекта ----------

    def test_dummy_object_example(self):
        """Dummy-объект: передаётся, но не используется."""
        dummy = None  # не участвует в логике, просто показывает концепцию
        # Arrange
        films = self.service.get_all_films()
        # Act
        count = len(films)
        # Assert
        self.assertEqual(count, 1)
        self.assertIsNone(dummy)


if __name__ == "__main__":
    unittest.main()