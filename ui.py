from datetime import date
from models import Film, Videocassette, Client
from service import RentalService
from validators import (
    input_non_empty, input_year, input_duration,
    input_phone, input_age_limit, input_menu_choice, input_index,
    input_text_letters_only, input_description,
    input_yes_no, input_title,
)


class ConsoleUI:
    """Консольный интерфейс пользователя."""

    def __init__(self, service):
        self._service = service

    def run(self):
        while True:
            self._print_main_menu()
            choice = input_menu_choice("Выберите пункт: ", [1, 2, 3, 4, 0])
            if choice == "1":
                self._show_films_menu()
            elif choice == "2":
                self._menu_cassettes()
            elif choice == "3":
                self._menu_clients()
            elif choice == "4":
                self._menu_rentals()
            elif choice == "0":
                print("Выход из программы. До свидания!")
                break

    # ---------- Главное меню ----------
    @staticmethod
    def _print_main_menu():
        print("\n" + "=" * 50)
        print("  СИСТЕМА ПРОКАТА ВИДЕОКАССЕТ")
        print("=" * 50)
        print("1. Каталог фильмов")
        print("2. Видеокассеты")
        print("3. Клиенты")
        print("4. Прокат / возврат")
        print("0. Выход")

    # ---------- Меню фильмов ----------
    def _show_films_menu(self):
        while True:
            print("\n--- Каталог фильмов ---")
            print("1. Показать все фильмы")
            print("2. Добавить фильм")
            print("3. Удалить фильм")
            print("4. Найти фильм")
            print("0. Назад")
            choice = input_menu_choice("Выберите пункт: ", [1, 2, 3, 4, 0])

            if choice == "1":
                self._show_all_films()
            elif choice == "2":
                self._add_film()
            elif choice == "3":
                self._remove_film()
            elif choice == "4":
                self._find_film()
            elif choice == "0":
                break

    def _show_all_films(self):
        films = self._service.get_all_films()
        if not films:
            print("Каталог пуст.")
            return
        for f in films:
            print(" -", f)

    def _add_film(self):
        print("\n  Введите данные о фильме.")
        print("  Подсказка: название может содержать буквы, цифры и знаки - : , . ! ? ( ) « »")
        print("  Жанр и режиссёр — только буквы, пробелы и дефис.")
        print("  Год — от 1895 до текущего, длительность — 1..600 мин.,")
        print("  возрастное ограничение — одно из 0+, 6+, 12+, 16+, 18+.")

        title = input_title("Название: ")
        genre = input_text_letters_only("Жанр: ", "жанр", max_length=50)
        year = input_year("Год выпуска: ")
        director = input_text_letters_only("Режиссёр: ", "имя режиссёра", max_length=100)
        duration = input_duration("Длительность (мин): ")
        age_limit = input_age_limit()
        description = input_description("Краткое описание: ")

        film = Film(title, genre, year, director, duration, age_limit, description)
        self._service.add_film(film)
        print(f"Фильм «{title}» добавлен в каталог.")

    def _remove_film(self):
        title = input_title("Введите название фильма для удаления: ")
        film = self._service.find_film(title)
        if film is None:
            print("Фильм не найден.")
            return
        if input_yes_no(f"Удалить фильм «{film.title}»? (y/n): "):
            self._service.remove_film(film)
            print("Фильм удалён.")
        else:
            print("Удаление отменено.")

    def _find_film(self):
        title = input_title("Введите название фильма: ")
        film = self._service.find_film(title)
        print(film if film else "Фильм не найден.")

    # ---------- Меню кассет ----------
    def _menu_cassettes(self):
        while True:
            print("\n--- Видеокассеты ---")
            print("1. Показать все кассеты")
            print("2. Показать свободные кассеты")
            print("3. Зарегистрировать новую кассету")
            print("0. Назад")
            choice = input_menu_choice("Выберите пункт: ", [1, 2, 3, 0])

            if choice == "1":
                self._show_all_cassettes()
            elif choice == "2":
                self._show_available_cassettes()
            elif choice == "3":
                self._register_cassette()
            elif choice == "0":
                break

    def _show_all_cassettes(self):
        cassettes = self._service.get_all_cassettes()
        if not cassettes:
            print("Кассет нет.")
            return
        for c in cassettes:
            print(" -", c)

    def _show_available_cassettes(self):
        cassettes = self._service.get_available_cassettes()
        if not cassettes:
            print("Свободных кассет нет.")
            return
        for c in cassettes:
            print(" -", c)

    def _register_cassette(self):
        cassette_id = input_non_empty("Идентификатор кассеты (например, VC-001): ")
        if self._service.find_cassette(cassette_id):
            print("Кассета с таким ID уже существует.")
            return
        title = input_title("Название фильма на кассете: ")
        film = self._service.find_film(title)
        if film is None:
            print("Фильм не найден в каталоге. Сначала добавьте его.")
            return
        cassette = Videocassette(cassette_id, film)
        self._service.register_cassette(cassette)
        print(f"Кассета №{cassette_id} зарегистрирована.")

    # ---------- Меню клиентов ----------
    def _menu_clients(self):
        while True:
            print("\n--- Клиенты ---")
            print("1. Показать всех клиентов")
            print("2. Зарегистрировать клиента")
            print("3. Найти клиента")
            print("0. Назад")
            choice = input_menu_choice("Выберите пункт: ", [1, 2, 3, 0])

            if choice == "1":
                self._show_all_clients()
            elif choice == "2":
                self._register_client()
            elif choice == "3":
                self._find_client()
            elif choice == "0":
                break

    def _show_all_clients(self):
        clients = self._service.get_all_clients()
        if not clients:
            print("Клиентов нет.")
            return
        for c in clients:
            print(" -", c)

    def _register_client(self):
        print("\n  Введите данные клиента.")
        print("  Подсказка: ФИО — только буквы, пробелы и дефис;")
        print("  телефон — в формате +7XXXXXXXXXX (например, +79154558289).")

        surname = input_text_letters_only("Фамилия: ", "фамилия", max_length=50)
        name = input_text_letters_only("Имя: ", "имя", max_length=50)
        patronymic = input_text_letters_only("Отчество: ", "отчество", max_length=50)
        contact = input_phone("Контакт (телефон в формате +7XXXXXXXXXX): ")

        client = Client(surname, name, patronymic, contact)
        self._service.register_client(client)
        print(f"Клиент «{client.full_name}» зарегистрирован.")

    def _find_client(self):
        print("  Подсказка: вводите только буквы, пробелы и дефис.")
        full_name = input_text_letters_only(
            "ФИО клиента: ", "ФИО клиента", max_length=150
        )
        client = self._service.find_client(full_name)
        print(client if client else "Клиент не найден.")

    # ---------- Меню проката ----------
    def _menu_rentals(self):
        while True:
            print("\n--- Прокат / возврат ---")
            print("1. Оформить прокат")
            print("2. Оформить возврат")
            print("3. Показать активные прокаты")
            print("0. Назад")
            choice = input_menu_choice("Выберите пункт: ", [1, 2, 3, 0])

            if choice == "1":
                self._create_rental()
            elif choice == "2":
                self._return_rental()
            elif choice == "3":
                self._show_active_rentals()
            elif choice == "0":
                break

    def _show_active_rentals(self):
        rentals = self._service.get_active_rentals()
        if not rentals:
            print("Активных прокатов нет.")
            return
        for r in rentals:
            print(r, "\n")

    def _create_rental(self):
        clients = self._service.get_all_clients()
        if not clients:
            print("Сначала зарегистрируйте хотя бы одного клиента.")
            return
        print("Клиенты:")
        self._print_numbered_list(clients, lambda c: c.full_name)

        client = input_index("Введите номер клиента из списка: ", clients)
        if client is None:
            return

        cassettes = self._service.get_available_cassettes()
        if not cassettes:
            print("Свободных кассет нет.")
            return
        print("Свободные кассеты:")
        self._print_numbered_list(cassettes)

        cassette = input_index("Введите номер кассеты из списка: ", cassettes)
        if cassette is None:
            return

        success, message = self._service.create_rental(client, cassette)
        print(message)

    @staticmethod
    def _print_numbered_list(items, formatter=lambda x: str(x)):
        for i, item in enumerate(items, 1):
            print(f"  {i}. {formatter(item)}")

    def _return_rental(self):
        rentals = self._service.get_active_rentals()
        if not rentals:
            print("Активных прокатов нет.")
            return
        print("Активные прокаты:")
        self._print_numbered_list(
            rentals,
            lambda r: f"Кассета №{r.cassette.id} — {r.client.full_name}, "
                      f"до {r.due_date}"
        )

        rental = input_index("Введите номер проката из списка: ", rentals)
        if rental is None:
            return

        success, message = self._service.return_cassette(rental)
        print(message)