from flask import Flask, render_template, request

app = Flask(__name__)

def checksum(data: bytes) -> int:
    return sum(data) % 256

def generate_gamma(a, b, t0, length, mod=256):
    gamma = [t0]
    for _ in range(1, length):
        gamma.append((a * gamma[-1] + b) % mod)
    return gamma

def xor_with_gamma_bytes(text_bytes, gamma):
    length = min(len(text_bytes), len(gamma))
    result = bytearray()
    for i in range(length):
        result.append(text_bytes[i] ^ gamma[i])
    return bytes(result)

@app.route('/', methods=['GET', 'POST'])
def index():
    checksum_result = ""
    gamma_encrypted = ""
    text = ""
    a = 3
    b = 5
    t0 = 1

    if request.method == 'POST':
        text = request.form.get('text', '')
        try:
            a = int(request.form.get('a'))
            b = int(request.form.get('b'))
            t0 = int(request.form.get('t0'))
            if not (0 <= t0 <= 255):
                raise ValueError("t0 out of bounds")
        except (TypeError, ValueError):
            checksum_result = "Ошибка: Параметры a, b должны быть целыми числами, t0 — от 0 до 255."
            return render_template('index.html',
                                   checksum_result=checksum_result,
                                   gamma_encrypted="",
                                   text=text,
                                   a=a, b=b, t0=t0)

        data_bytes = text.encode('utf-8')

        # Контрольная сумма
        cs = checksum(data_bytes)
        checksum_result = f"Контрольная сумма (mod 256): {cs}"

        # Генерация гаммы и шифрование
        gamma = generate_gamma(a, b, t0, len(data_bytes))
        encrypted_bytes = xor_with_gamma_bytes(data_bytes, gamma)
        encrypted_hex = encrypted_bytes.hex()

        # Обратное дешифрование (XOR теми же параметрами)
        decrypted_bytes = xor_with_gamma_bytes(encrypted_bytes, gamma)
        try:
            decrypted_text = decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError:
            decrypted_text = "<Ошибка декодирования UTF-8>"

        gamma_encrypted = f"{encrypted_hex}\nРасшифровано: {decrypted_text}"

    return render_template('index.html',
                           checksum_result=checksum_result,
                           gamma_encrypted=gamma_encrypted,
                           text=text,
                           a=a, b=b, t0=t0)

if __name__ == '__main__':
    app.run(debug=True)
