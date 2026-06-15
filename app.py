from flask import Flask, render_template, request
from sdes import SDES

app = Flask(__name__)
sdes = SDES()

EXAMPLES = {
    'plaintext': '00101000',
    'key': '1100011110',
    'ciphertext': '10001010',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    mode = request.form.get('mode', 'encrypt')
    input_data = request.form.get('input_data', '').strip()
    key = request.form.get('key', '').strip()

    if request.method == 'POST':
        try:
            result = sdes.process(input_data, key, mode)
        except ValueError as exc:
            error = str(exc)

    return render_template(
        'index.html',
        result=result,
        error=error,
        mode=mode,
        input_data=input_data,
        key=key,
        examples=EXAMPLES
    )

if __name__ == '__main__':
    app.run(debug=True)