import os
from app import create_app
from app.models import db

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    if not os.path.exists(os.path.join(app.instance_path, 'database.db')):
        init_db()
    app.run(debug=True)
