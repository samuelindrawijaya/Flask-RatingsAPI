from app import create_app, db
from app.seeds import seed_data

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)