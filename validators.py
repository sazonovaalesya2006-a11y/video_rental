"""Модуль валидации пользовательского ввода."""

import re
from datetime import date


def input_non_empty(prompt):
    """Запрашивает непустую строку. Повторяет ввод, пока не получит корректные данные."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Ошибка: поле не может быть пустым. Попробуйте снова.")


def input_int(prompt, min_value=None, max_value=None):
    """Запрашивает целое число с проверкой диапазона."""
    while True:
        raw = input(prompt).strip()
        if not raw.lstrip("-").isdigit():
            print("  Ошибка: нужно ввести целое число (только цифры).")
            continue
        value = int(raw)
        if min_value is not None and value < min_value:
            print(f"  Ошибка: значение должно быть не меньше {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"  Ошибка: значение должно быть не больше {max_value}.")
            continue
        return value


def input_year(prompt="Год выпуска: "):
    """Год выпуска: от 1895 (рождение кинематографа) до текущего года."""
    current_year = date.today().year
    return input_int(prompt, min_value=1895, max_value=current_year)


def input_duration(prompt="Длительность (мин): "):
    """Длительность фильма в минутах: 1..600."""
    return input_int(prompt, min_value=1, max_value=600)


def input_phone(prompt="Контакт (телефон в формате +7XXXXXXXXXX): "):
    """
    Телефон в строгом формате +7XXXXXXXXXX (12 символов: +7 и 10 цифр).
    Пример: +79154558289
    """
    pattern = re.compile(r"^\+7\d{10}$")
    while True:
        value = input(prompt).strip().replace(" ", "").replace("-", "")
        if pattern.match(value):
            return value
        print("  Ошибка: телефон должен быть в формате +7XXXXXXXXXX, "
              "например +79154558289.")


def input_age_limit(prompt="Возрастное ограничение (0+, 6+, 12+, 16+, 18+): "):
    """Возрастное ограничение — только из допустимого набора."""
    allowed = {"0+", "6+", "12+", "16+", "18+"}
    while True:
        value = input(prompt).strip()
        if value in allowed:
            return value
        print(f"  Ошибка: допустимые значения — {', '.join(sorted(allowed))}.")


def input_menu_choice(prompt, valid_choices):
    """Запрашивает пункт меню, проверяя, что он входит в список допустимых."""
    valid = {str(c) for c in valid_choices}
    while True:
        value = input(prompt).strip()
        if value in valid:
            return value
        print(f"  Ошибка: допустимые пункты — {', '.join(sorted(valid))}.")


def input_index(prompt, items):
    """
    Запрашивает номер элемента из списка (1-based).
    Возвращает сам элемент или None, если список пуст.
    """
    if not items:
        return None
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("  Ошибка: введите номер из списка (только цифры).")
            continue
        idx = int(raw) - 1
        if 0 <= idx < len(items):
            return items[idx]
        print(f"  Ошибка: введите число от 1 до {len(items)}.")

def input_text_letters_only(prompt, field_name="поле", max_length=100):
    """
    Текстовое поле: только буквы (русские/латинские), пробелы и дефис.
    Подходит для названий, жанров, ФИО, режиссёров.
    """
    # \s — пробел, \- — дефис, а-яё/А-ЯЁ — русские буквы, a-zA-Z — латинские
    pattern = re.compile(r"^[А-Яа-яЁёA-Za-z\s\-]+$")

    while True:
        value = input(prompt).strip()
        if not value:
            print(f"  Ошибка: {field_name} не может быть пустым.")
            continue
        if len(value) > max_length:
            print(f"  Ошибка: {field_name} не должно превышать "
                  f"{max_length} символов.")
            continue
        if not pattern.match(value):
            print(f"  Ошибка: {field_name} может содержать только буквы, "
                  f"пробелы и дефис.")
            continue
        return value


def input_description(prompt="Краткое описание: ", max_length=500):
    """
    Описание фильма: буквы, цифры, пробелы и базовая пунктуация (. , ! ? - ( ) : ; « »).
    """
    allowed = re.compile(r"^[А-Яа-яЁёA-Za-z0-9\s\-.,!?():;«»\"']+$")

    while True:
        value = input(prompt).strip()
        if not value:
            print("  Ошибка: описание не может быть пустым.")
            continue
        if len(value) > max_length:
            print(f"  Ошибка: описание не должно превышать {max_length} символов.")
            continue
        if not allowed.match(value):
            print("  Ошибка: описание может содержать буквы, цифры, пробелы "
                  "и знаки . , ! ? - ( ) : ; « »")
            continue
        return value

def input_yes_no(prompt="Подтвердите (y/n): "):
    """Запрашивает подтверждение y/n (или д/н на русском). Возвращает True/False."""
    yes = {"y", "yes", "д", "да"}
    no = {"n", "no", "н", "нет"}
    while True:
        value = input(prompt).strip().lower()
        if value in yes:
            return True
        if value in no:
            return False
        print("  Ошибка: введите 'y' (да) или 'n' (нет).")


def input_title(prompt="Название: ", max_length=150):
    """
    Название фильма: буквы (рус/лат), цифры, пробелы и базовая пунктуация.
    Например: «Терминатор 2», «Матрица: Перезагрузка», «Криминальное чтиво (1994)».
    """
    allowed = re.compile(r"^[А-Яа-яЁёA-Za-z0-9\s\-:,.!?()«»\"'&]+$")

    while True:
        value = input(prompt).strip()
        if not value:
            print("  Ошибка: название не может быть пустым.")
            continue
        if len(value) > max_length:
            print(f"  Ошибка: название не должно превышать {max_length} символов.")
            continue
        if not allowed.match(value):
            print("  Ошибка: название может содержать буквы, цифры, пробелы "
                  "и знаки - : , . ! ? ( ) « » \" ' &")
            continue
        return value