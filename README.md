# Flask File Encryption and Decryption

A small Flask app that encrypts a file with a Fernet key and decrypts that ciphertext back to a second file, so you can check that the bytes match.

## What it does

Open the home page, enter a path to a file on disk, and submit. The app:

1. Loads a Fernet key from the `ENCRYPTION_KEY` environment variable, or from a key file (default `myKey.key`).
2. Encrypts the file and writes `EncryptedFile.csv`.
3. Decrypts `EncryptedFile.csv` and writes `DecryptedFile.csv`.

The same key is reused on later runs. A key file is created on first run only when `ENCRYPTION_KEY` is unset and the file is missing.

This repository includes a sample input, `health-medicare-drug-spending (1).csv`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` if you want to set `SECRET_KEY`, `FLASK_DEBUG`, or `ENCRYPTION_KEY`. With a copied `.env` and an empty `ENCRYPTION_KEY`, the app creates `myKey.key` the first time it runs.

To choose your own key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Put that value in `ENCRYPTION_KEY`. Do not commit `.env` or `*.key` files.

## Environment variables

| Variable | Required | Description |
| --- | --- | --- |
| `SECRET_KEY` | No | Flask secret used to sign the session and the form token. A random value is used for the process when this is unset. |
| `FLASK_DEBUG` | No | `1`, `true`, `yes`, or `on` turns on the Flask debugger. Any other value, including the default `0`, leaves it off. |
| `ENCRYPTION_KEY` | No | Fernet key. When set, this is used instead of the key file. |
| `ENCRYPTION_KEY_FILE` | No | Path of the key file used when `ENCRYPTION_KEY` is empty. Defaults to `myKey.key`. |

`.env` in the working directory is loaded at startup. Variables already set in the environment are left as they are.

## Usage

```bash
python main.py
```

The server listens on `0.0.0.0:5000`. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/), enter a file path, and submit. Then compare the original file with `DecryptedFile.csv`.

Example path:

```text
health-medicare-drug-spending (1).csv
```

`EncryptedFile.csv` and `DecryptedFile.csv` are written in the working directory. Both are gitignored, along with `myKey.key`.

## License

MIT. Copyright (c) 2026 Pradeep Kumar Dasari. See [LICENSE](LICENSE).
