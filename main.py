import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from flask import Flask, render_template, request

from forms import ReadPath

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(32)

DEFAULT_KEY_FILE = 'myKey.key'


def _truthy(value):
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def load_key():
    """Return the Fernet key from the environment or a local key file.

    When neither is present, a new key is written to the key file.
    """
    configured = os.environ.get('ENCRYPTION_KEY', '').strip()
    if configured:
        return configured.encode('utf-8')

    key_path = os.environ.get('ENCRYPTION_KEY_FILE', DEFAULT_KEY_FILE)
    if os.path.isfile(key_path):
        with open(key_path, 'rb') as key_file:
            stored = key_file.read().strip()
        if stored:
            return stored

    key = Fernet.generate_key()
    descriptor = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, 'wb') as key_file:
        key_file.write(key)
    return key


def function(path):
    fernet = Fernet(load_key())

    with open(path, 'rb') as source_file:
        original = source_file.read()

    encrypted = fernet.encrypt(original)

    with open('EncryptedFile.csv', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    fernet = Fernet(load_key())

    with open('EncryptedFile.csv', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open('DecryptedFile.csv', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)


@app.route('/', methods=['GET', 'POST'])
def add_numbers():
    form = ReadPath()

    if request.method == 'POST':
        path = form.path.data
        function(path)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    load_key()
    debug = _truthy(os.environ.get('FLASK_DEBUG', '0'))
    app.run(debug=debug, host='0.0.0.0')
