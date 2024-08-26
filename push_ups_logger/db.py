from push_ups_logger import create_app, db  # Replace 'yourapp' with your actual app package name

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
