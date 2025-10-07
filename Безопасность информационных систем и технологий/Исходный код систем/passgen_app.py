from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Генератор паролей</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5" style="max-width: 600px;">
  <h1 class="mb-4 text-center">Генератор паролей по идентификатору</h1>
  <form method="POST" class="mb-4">
    <div class="mb-3">
      <label for="identifier" class="form-label">Введите идентификатор:</label>
      <input type="text" id="identifier" name="identifier" class="form-control" placeholder="Введите идентификатор" required autofocus>
    </div>
    <button type="submit" class="btn btn-primary w-100">Сгенерировать пароль</button>
  </form>

  {% if password %}
  <div class="alert alert-success text-center" role="alert">
    <h4 class="alert-heading">Сгенерированный пароль:</h4>
    <p class="fs-3 fw-bold">{{ password }}</p>
  </div>
  {% endif %}
</div>
</body>
</html>
'''

def generate_password(identifier: str) -> str:
    uppercase_russian = [chr(code) for code in range(ord('А'), ord('Я') + 1)]
    lowercase_russian = [chr(code) for code in range(ord('а'), ord('я') + 1)]

    N = len(identifier)
    Q = N % 6

    password = [''] * 10

    password[0] = random.choice(uppercase_russian)
    password[1] = random.choice(uppercase_russian)

    start_digits_index = 10 - Q - 1
    for i in range(start_digits_index, 10):
        password[i] = str(random.randint(0, 9))

    for i in range(2, start_digits_index):
        password[i] = random.choice(lowercase_russian)

    for i in range(10):
        if password[i] == '':
            password[i] = random.choice(lowercase_russian)

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
