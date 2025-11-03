from flask import Flask, request, render_template
import re
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')

ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET = ALPHABET.replace('ё', '')
ALPHABET_LEN = len(ALPHABET)

def preprocess_text(text):
    text = text.lower().replace('ё', 'е')
    text = re.sub(r'[^а-я]', '', text)
    return text

def group_text(text, group_size=5, line_size=10):
    groups = [text[i:i+group_size] for i in range(0, len(text), group_size)]
    lines = [' '.join(groups[i:i+line_size]) for i in range(0, len(groups), line_size)]
    return '\n'.join(lines)

def vigenere(text, key, mode=True):
    text = preprocess_text(text)
    key = preprocess_text(key)
    if len(key) == 0:
        return "Ключ не может быть пустым"
    result = []
    key_indices = [ALPHABET.index(k) for k in key]
    for i, char in enumerate(text):
        text_idx = ALPHABET.index(char)
        key_idx = key_indices[i % len(key)]
        if mode:
            new_idx = (text_idx + key_idx) % ALPHABET_LEN
        else:
            new_idx = (text_idx - key_idx + ALPHABET_LEN) % ALPHABET_LEN
        result.append(ALPHABET[new_idx])
    return group_text(''.join(result))

def kasiski_examination(ciphertext):
    ciphertext = preprocess_text(ciphertext)
    seqs = {}
    for i in range(len(ciphertext)-3):
        seq = ciphertext[i:i+3]
        seqs.setdefault(seq, []).append(i)
    distances = []
    for positions in seqs.values():
        if len(positions) > 1:
            for i in range(len(positions) - 1):
                distances.append(positions[i+1] - positions[i])
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    if not distances:
        return 1
    gcd_value = distances[0]
    for d in distances[1:]:
        gcd_value = gcd(gcd_value, d)
    return gcd_value

STANDARD_FREQ = {"а":8.01, "б":1.59, "в":4.54, "г":1.70, "д":2.98, "е":8.45, "ж":0.94, "з":1.65, "и":7.35,
                 "й":1.21, "к":3.49, "л":4.40, "м":3.21, "н":6.70, "о":10.97, "п":2.81, "р":4.73, "с":5.47, "т":6.26,
                 "у":2.62, "ф":0.26, "х":0.97, "ц":0.48, "ч":1.44, "ш":0.73, "щ":0.36, "ъ":0.04, "ы":1.90, "ь":1.74,
                 "э":0.32, "ю":0.64, "я":2.01}
STANDARD_FREQ_VECTOR = np.array([STANDARD_FREQ[ch] for ch in ALPHABET]) / 100

def crack_vigenere(ciphertext):
    ciphertext = preprocess_text(ciphertext)
    key_length = kasiski_examination(ciphertext)
    groups = [ciphertext[i::key_length] for i in range(key_length)]
    key = []
    for group in groups:
        min_sum_squares = None
        best_shift = 0
        for i in range(ALPHABET_LEN):
            shifted = [(ALPHABET.index(c) - i) % ALPHABET_LEN for c in group]
            shifted_freq = np.zeros(ALPHABET_LEN)
            for val in shifted:
                shifted_freq[val] += 1
            shifted_freq = shifted_freq / len(group)
            diff = STANDARD_FREQ_VECTOR - shifted_freq
            sum_squares = np.sum(diff**2)
            if (min_sum_squares is None) or (sum_squares < min_sum_squares):
                min_sum_squares = sum_squares
                best_shift = i
        key.append(ALPHABET[best_shift])
    return ''.join(key)

@app.route('/cipher', methods=['GET', 'POST'])
def cipher_page():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        action = request.form['action']
        if action == 'encrypt':
            result = vigenere(text, key, mode=True)
        elif action == 'decrypt':
            result = vigenere(text, key, mode=False)
    return render_template('cipher.html', result=result)

@app.route('/crack', methods=['GET', 'POST'])
def crack_page():
    key_found = ''
    decrypted_text = ''
    if request.method == 'POST':
        text = request.form['text']
        key_found = crack_vigenere(text)
        decrypted_text = vigenere(text, key_found, mode=False)
        decrypted_text = group_text(decrypted_text.replace(' ', ''))
    return render_template('crack.html', key_found=key_found, decrypted_text=decrypted_text)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
