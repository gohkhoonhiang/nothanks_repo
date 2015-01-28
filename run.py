#!venv/bin/python
from app.app import nothanksapp

if __name__ == '__main__':
    nothanksapp.run(host='0.0.0.0', debug=True)
