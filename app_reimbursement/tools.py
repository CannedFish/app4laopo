# -*- coding: utf-8 -*-

def main():
    from reimbursement.app import initialize_app, app
    from reimbursement.database import reset_db

    initialize_app(app)
    with app.app_context():
        reset_db()

if __name__ == '__main__':
    main()
