from website import create_app
# from waitress import serve

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

#  virtualenv venv
# venv\Scripts\activate
# python app.py