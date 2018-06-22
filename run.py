#encoding:utf-8
from app import app
from src.main import Main

if __name__ == '__main__':
    Main.run()
    app.run(debug=True)
