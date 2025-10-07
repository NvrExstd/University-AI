import random

def generate_password(identifier: str) -> str:
# Русский алфавит
    uppercase_russian = [chr(code) for code in range(ord('А'), ord('Я') + 1)]
    lowercase_russian = [chr(code) for code in range(ord('а'), ord('я') + 1)]

    N = len(identifier)
    Q = N % 6

    password = [''] * 10

    # b1, b2 - заглавные буквы
    password[0] = random.choice(uppercase_russian)
    password[1] = random.choice(uppercase_russian)

    # b(10-Q) до b10 - цифры (включительно)
    start_digits_index = 10 - Q - 1  # смещение с 0
    for i in range(start_digits_index, 10):
        password[i] = str(random.randint(0, 9))

    # b3 до b(10-Q-1) - строчные буквы
    # индексы с 2 по start_digits_index-1
    for i in range(2, start_digits_index):
        password[i] = random.choice(lowercase_russian)

    # Если промежуток отсутствует (например, Q=5), заполним пустые позиции строчными буквами
    for i in range(10):
        if password[i] == '':
            password[i] = random.choice(lowercase_russian)
    return ''.join(password)

if __name__ == "__main__":
    user_identifier = input("Введите идентификатор: ")
    generated_password = generate_password(user_identifier)
    print("Сгенерированный пароль:", generated_password)