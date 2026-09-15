# Студенческая ветка — лабораторная №3
from service import RentalService
from ui import ConsoleUI


def main():
    service = RentalService()
    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()