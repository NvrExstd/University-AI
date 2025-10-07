from flask import Flask, request, render_template_string
import random
import string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Генератор паролей</title>
<style>
  body {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #f0f0f0;
    height: 100vh;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .container {
    background-color: #2f4f7f;
    padding: 30px 40px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    width: 100%;
    max-width: 420px;
    text-align: center;
  }
  h1 {
    margin-bottom: 25px;
    font-weight: 700;
    font-size: 1.8rem;
  }
  label {
    display: block;
    text-align: left;
    margin-bottom: 8px;
    font-weight: 600;
  }
  input[type="text"] {
    width: 100%;
    padding: 12px 15px;
    border-radius: 12px;
    border: none;
    font-size: 1rem;
    outline: none;
    background-color: #e9ecef;
    color: #333;
    box-sizing: border-box;
    margin-bottom: 20px;
    transition: box-shadow 0.3s ease;
  }
  input[type="text"]:focus {
    box-shadow: 0 0 8px 3px #72c07a;
    background-color: #fff;
  }
  button {
    background: linear-gradient(90deg, #4CAF50, #379933);
    border: none;
    padding: 12px 0;
    width: 100%;
    font-size: 1.1rem;
    font-weight: 700;
    color: white;
    border-radius: 30px;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(55, 153, 51, 0.8);
    transition: background 0.3s ease;
  }
  button:hover {
    background: linear-gradient(90deg, #3a8e36, #2d6a29);
  }
  .password-output {
    background-color: #f1f8e9;
    color: #254d00;
    margin-top: 30px;
    border-radius: 15px;
    padding: 20px;
    font-size: 1.5rem;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(37, 77, 0, 0.5);
    word-break: break-all;
  }
</style>
</head>
<body>
<div class="container">
  <h1>Генератор паролей по идентификатору</h1>
  <form method="POST">
    <label for="identifier">Введите идентификатор:</label>
    <input type="text" id="identifier" name="identifier" placeholder="Введите идентификатор" required autofocus>
    <button type="submit">Сгенерировать пароль</button>
  </form>
  {% if password %}
  <div class="password-output" role="alert" aria-live="polite">
    {{ password }}
  </div>
  {% endif %}
</div>
</body>
</html>
'''


def generate_password(identifier: str) -> str:
    M = 11
    N = len(identifier)
    Q = N % 8

    digits = [str(random.randint(0, 9)) for _ in range(2)]  # b1, b2 - random digits
    uppercase_english = [random.choice(string.ascii_uppercase) for _ in range(Q + 1)]  # b3,...b3+Q
    symbols = [random.choice(list('!"#$%&\'()*')) for _ in range(M - 2 - (Q + 1))]  # remaining positions

    password = digits + uppercase_english + symbols

    return ''.join(password)

@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = generate_password(identifier)
    return render_template_string(HTML_TEMPLATE, password=password)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
