from __init__ import create_app, db
from models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        try:
            escrow_user = User(username="ESCROW", email = "escrow@admin.com", coins = 9999999)
            db.session.add(escrow_user)
            db.session.commit()
        except:
            print("db already created")
        print("db created")
    app.secret_key = "super secret key"
    app.run(debug = True)