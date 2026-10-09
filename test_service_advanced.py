import unittest
from datetime import date
from models import CassetteStatus, RentalStatus
from service import RentalService
from test_data import TestDataFactory


class TestRentalServiceAAA(unittest.TestCase):
    """Модульные тесты сервиса проката по паттерну AAA (Arrange-Act-Assert)."""

    def setUp(self):
        """Общая подготовка перед КАЖДЫМ тестом (стадия Arrange)."""
        # Создаём чистый сервис для каждого теста — тесты не влияют друг на друга
        self.service = RentalService()

        # Готовим тестовые данные через фабрику (паттерн Object Mother)
        self.film = TestDataFactory.create_film()
        self.service.add_film(self.film)

        self.cassette = TestDataFactory.create_cassette("VC-001", self.film)
        self.service.register_cassette(self.cassette)

        self.client = TestDataFactory.create_client()
        self.service.register_client(self.client)

    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================
    # Проверяют корректное поведение при правильных данных

    def test_create_rental_success(self):
        """Успешное оформление проката: кассета выдана, статус изменён."""
        # --- Arrange ---
        start_date = date(2026, 1, 1)  # фиксированная дата вместо today() (stub)

        # --- Act ---
        success, message = self.service.create_rental(
            self.client, self.cassette, start_date
        )

        # --- Assert ---
        self.assertTrue(success)                                 # операция успешна
        self.assertIn("Прокат оформлен", message)                # правильное сообщение
        self.assertEqual(self.cassette.status, CassetteStatus.RENTED)  # кассета выдана
        self.assertEqual(len(self.service.get_active_rentals()), 1)    # появился 1 прокат

    def test_return_on_time_no_fine(self):
        """Возврат в срок: штраф 0, статусы обновлены."""
        # --- Arrange ---
        start = date(2026, 1, 1)
        self.service.create_rental(self.client, self.cassette, start)
        rental = self.service.get_active_rentals()[0]
        return_date = date(2026, 1, 5)  # 4-й день из 7 — в срок

        # --- Act ---
        success, message = self.service.return_cassette(rental, return_date)

        # --- Assert ---
        self.assertTrue(success)
        self.assertEqual(rental.fine, 0)                                   # штрафа нет
        self.assertEqual(rental.status, RentalStatus.RETURNED)             # прокат закрыт
        self.assertEqual(self.cassette.status, CassetteStatus.AVAILABLE)   # кассета свободна
        self.assertIn("штраф не начислен", message)

    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================
    # Проверяют реакцию системы на некорректные ситуации

    def test_create_rental_unavailable_cassette(self):
        """Нельзя выдать кассету, которая уже у другого клиента."""
        # --- Arrange ---
        # Сначала выдаём кассету — она становится RENTED
        self.service.create_rental(self.client, self.cassette, date(2026, 1, 1))

        # --- Act ---
        # Пытаемся выдать ту же кассету повторно
        success, message = self.service.create_rental(
            self.client, self.cassette, date(2026, 1, 2)
        )

        # --- Assert ---
        self.assertFalse(success)                  # операция отклонена
        self.assertIn("уже выдана", message)       # понятное сообщение об ошибке

    def test_rental_limit_exceeded(self):
        """Нельзя выдать более 3 кассет одному клиенту (бизнес-правило)."""
        # --- Arrange ---
        # Создаём 4 дополнительные кассеты
        cassettes = []
        for i in range(2, 6):
            c = TestDataFactory.create_cassette(f"VC-00{i}", self.film)
            self.service.register_cassette(c)
            cassettes.append(c)

        # Занимаем ровно 3 кассеты — доходим до лимита
        for c in cassettes[:3]:
            self.service.create_rental(self.client, c, date(2026, 1, 1))

        # --- Act ---
        # Пытаемся оформить 4-ю — должна быть ошибка
        success, message = self.service.create_rental(
            self.client, cassettes[3], date(2026, 1, 1)
        )

        # --- Assert ---
        self.assertFalse(success)
        self.assertIn("Превышен лимит", message)

    # ==================== ГРАНИЧНЫЕ ТЕСТЫ ====================
    # Проверяют поведение ровно на границе допустимого диапазона

    def test_return_exactly_on_due_date(self):
        """Возврат РОВНО в плановую дату — ещё не просрочка."""
        # --- Arrange ---
        start = date(2026, 1, 1)
        self.service.create_rental(self.client, self.cassette, start)
        rental = self.service.get_active_rentals()[0]
        due_date = rental.due_date  # плановая дата = 2026-01-08

        # --- Act ---
        success, message = self.service.return_cassette(rental, due_date)

        # --- Assert ---
        self.assertTrue(success)
        self.assertEqual(rental.fine, 0)   # штраф ещё не начисляется

    def test_return_one_day_overdue(self):
        """Возврат на 1 день позже срока — штраф 20 руб. (граница после due_date)."""
        # --- Arrange ---
        start = date(2026, 1, 1)
        self.service.create_rental(self.client, self.cassette, start)
        rental = self.service.get_active_rentals()[0]
        return_date = date(2026, 1, 9)   # due_date = 08.01, просрочка = 1 день

        # --- Act ---
        success, message = self.service.return_cassette(rental, return_date)

        # --- Assert ---
        self.assertTrue(success)
        self.assertEqual(rental.fine, 20.0)   # 1 день × 20 руб.

    # ==================== ПРИМЕР DUMMY-ОБЪЕКТА ====================

    def test_dummy_object_example(self):
        """Dummy-объект: передаётся, но не используется в логике теста."""
        dummy = None   # концептуальный пример dummy-объекта

        # --- Arrange ---
        films = self.service.get_all_films()

        # --- Act ---
        count = len(films)

        # --- Assert ---
        self.assertEqual(count, 1)    # в setUp добавлен ровно 1 фильм
        self.assertIsNone(dummy)      # dummy не участвует в проверке


if __name__ == "__main__":
    unittest.main()