"""Демонстрация возврата кассеты с просрочкой и штрафом."""
from datetime import date
from models import Film, Videocassette, Client
from service import RentalService


def main():
    print("=" * 55)
    print("  ДЕМОНСТРАЦИЯ: ВОЗВРАТ С ПРОСРОЧКОЙ И ШТРАФОМ")
    print("=" * 55)

    service = RentalService()

    # Регистрируем фильм
    film = Film("Матрица", "Фантастика", 1999, "Вачовски",
                136, "16+", "Фильм о Нео")
    service.add_film(film)
    print(f"\n[1] Добавлен фильм: {film}")

    # Регистрируем кассету
    cassette = Videocassette("VC-001", film)
    service.register_cassette(cassette)
    print(f"[2] Зарегистрирована кассета: {cassette}")

    # Регистрируем клиента
    client = Client("Иванов", "Иван", "Иванович", "+79154558289")
    service.register_client(client)
    print(f"[3] Зарегистрирован клиент: {client}")

    # Оформляем прокат с датой начала в прошлом (для демонстрации)
    start_date = date(2026, 9, 1)  # выдача 1 сентября
    success, msg = service.create_rental(client, cassette, start_date)
    print(f"\n[4] Оформление проката:")
    print(f"    {msg}")
    print(f"    Дата выдачи:       {start_date}")
    print(f"    Плановая дата возврата: {start_date.replace(day=start_date.day) + __import__('datetime').timedelta(days=7)}")

    rental = service.get_active_rentals()[0]

    # Оформляем возврат позже срока (демонстрация штрафа)
    return_date = date(2026, 9, 15)  # возврат 15 сентября
    print(f"\n[5] Возврат кассеты:")
    print(f"    Фактическая дата возврата: {return_date}")

    overdue_days = (return_date - rental.due_date).days
    print(f"    Плановая дата возврата:    {rental.due_date}")
    print(f"    Просрочка:                 {overdue_days} дн.")

    success, msg = service.return_cassette(rental, return_date)
    print(f"\n[6] Результат операции:")
    print(f"    {msg}")

    print("\n" + "=" * 55)
    print("  ИТОГ:")
    print(f"  • Стоимость проката:  {rental.cost:.2f} руб.")
    print(f"  • Штраф за просрочку: {rental.fine:.2f} руб.")
    print(f"  • Итого к оплате:     {rental.cost + rental.fine:.2f} руб.")
    print(f"  • Статус проката:     {rental.status.value}")
    print(f"  • Статус кассеты:     {cassette.status.value}")
    print("=" * 55)


if __name__ == "__main__":
    main()