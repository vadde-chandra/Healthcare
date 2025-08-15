// Healthcare Backend System
// This is a Django-based backend system for healthcare management

console.log(`
🏥 Healthcare Backend System
============================

This is a Django REST API backend system for healthcare management.

To set up and run this system:

1. Create a Python virtual environment:
   python -m venv healthcare_env

2. Activate the virtual environment:
   - Linux/Mac: source healthcare_env/bin/activate
   - Windows: healthcare_env\\Scripts\\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up your PostgreSQL database and update .env file

5. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

6. Create a superuser:
   python manage.py createsuperuser

7. Start the development server:
   python manage.py runserver

📚 Check README.md for detailed setup instructions and API documentation.
`);