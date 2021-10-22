from cryptography.fernet import Fernet
from flask import Flask, jsonify, render_template, request
from forms import ReadPath
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY



def function(path):
    key = Fernet.generate_key()

    with open('myKey.key', 'wb') as myKey:
        myKey.write(key)

    with open('myKey.key', 'rb') as myKey:
        key = myKey.read()

    # print(key)

    #Encryption
    keySave = Fernet(key)

    with open(path, 'rb') as sourceFile:
        original = sourceFile.read()

    encryption = keySave.encrypt(original)

    with open('EncryptedFile.csv', 'wb') as encryptedFile:
        encryptedFile.write(encryption)

    #Decryption
    with open('myKey.key', 'rb') as myKey:
        key = myKey.read()

    keySave = Fernet(key)

    with open('EncryptedFile.csv', 'rb') as encryptedFile:
        encrypted = encryptedFile.read()

    decryption = keySave.decrypt(encrypted)

    with open('DecryptedFile.csv', 'wb') as decryptedFile:
        decryptedFile.write(decryption)



@app.route('/', methods=['GET', 'POST'])
def add_numbers():
    path = None
    form = ReadPath()

    if request.method == 'POST':
        path = form.path.data
        function(path)


    return render_template('index.html', form=form)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
