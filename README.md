# Healthcare Backend System

A comprehensive Django REST API for managing healthcare data including patients, doctors, and their mappings.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Patient Management**: Full CRUD operations for patient records
- **Doctor Management**: Complete doctor profile management
- **Patient-Doctor Mapping**: Assign and manage patient-doctor relationships
- **Secure Access**: Authentication-protected endpoints
- **PostgreSQL Integration**: Robust database operations using Django ORM

## Tech Stack

- **Backend**: Django 4.2.5 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT tokens using djangorestframework-simplejwt
- **Environment Management**: python-decouple

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Patient Management
- `GET /api/patients/` - List all patients (user's own)
- `POST /api/patients/` - Create a new patient
- `GET /api/patients/<id>/` - Get patient details
- `PUT /api/patients/<id>/` - Update patient
- `DELETE /api/patients/<id>/` - Delete patient

### Doctor Management
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Create a new doctor
- `GET /api/doctors/<id>/` - Get doctor details
- `PUT /api/doctors/<id>/` - Update doctor
- `DELETE /api/doctors/<id>/` - Delete doctor

### Patient-Doctor Mapping
- `GET /api/mappings/` - List all active mappings
- `POST /api/mappings/` - Create patient-doctor mapping
- `GET /api/mappings/<patient_id>/` - Get doctors for a patient
- `DELETE /api/mappings/<mapping_id>/` - Remove doctor from patient

### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics

## Setup Instructions

**Note**: This Django backend requires Python and pip to be installed on your system. The following instructions assume you have Python 3.8+ installed.

1. **Clone and Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv healthcare_env
   source healthcare_env/bin/activate  # On Windows: healthcare_env\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Database Configuration**
   ```bash
   # Create PostgreSQL database
   createdb healthcare_db
   
   # Copy environment variables
   cp .env.example .env
   
   # Update .env with your database credentials
   ```

3. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://username:password@localhost:5432/healthcare_db
POSTGRES_DB=healthcare_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Create a Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "address": "123 Main St, City, State",
    "medical_history": "No known allergies"
  }'
```

### Create a Doctor
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Dr. Smith Wilson",
    "email": "dr.smith@hospital.com",
    "phone": "+1987654321",
    "specialization": "Cardiology",
    "license_number": "MD123456",
    "years_of_experience": 15,
    "consultation_fee": "500.00",
    "available_from": "09:00:00",
    "available_to": "17:00:00"
  }'
```

## Security Features

- JWT token-based authentication
- User-specific patient access (users can only see their own patients)
- Input validation and sanitization
- Password validation
- CORS configuration
- Secure database connections

## Models

### User (Custom)
- Extended Django's AbstractUser
- Fields: email, name, username

### Patient
- Personal information: name, email, phone, date_of_birth, gender
- Contact: address
- Medical: medical_history
- System: created_by, timestamps

### Doctor
- Professional info: name, email, phone, specialization, license_number
- Experience: years_of_experience
- Availability: consultation_fee, available_from, available_to

### PatientDoctorMapping
- Links patients to doctors
- Fields: patient, doctor, assigned_at, notes, is_active

## Testing

Run tests using:
```bash
python manage.py test
```

## Admin Interface

Access the admin interface at `http://localhost:8000/admin/` to manage:
- Users
- Patients
- Doctors
- Patient-Doctor Mappings

## Production Considerations

## Railway Deployment

This project is configured for Railway deployment with the following files:
- `railway.json` - Railway-specific configuration
- `Procfile` - Process configuration for Railway
- Added `gunicorn` and `whitenoise` to requirements.txt

To deploy on Railway:
1. Create a Railway account at https://railway.app
2. Connect your GitHub repository
3. Add a PostgreSQL database service
4. Set environment variables in Railway dashboard
5. Deploy the application

Required Railway Environment Variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False for production
- `DATABASE_URL` - Will be provided by Railway PostgreSQL service
- `ALLOWED_HOSTS` - Add your Railway domain

- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Configure proper CORS settings
- Set up database connection pooling
- Implement rate limiting
- Add comprehensive logging
- Configure static file serving

## License

This project is created for the WhatBytes Backend Developer Internship assignment.