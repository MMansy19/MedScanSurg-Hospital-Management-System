from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# Running Flask steps:
# (1) cd C:\Radiology-Department-Database-Project 
# if you don't have a virtual environment :virtualenv venv
# (2) venv\Scripts\activate
# (3) python app.py

