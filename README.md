
# Push Up Logger

Push Up Logger is a Flask-based web application designed to help users log their push-up workouts, track progress over time, and manage their profiles. The application integrates with Firebase for storing profile pictures and PostgreSQL for managing user and workout data.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Setting Up Virtual Environment](#setting-up-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
  - [Firebase Setup](#firebase-setup)
- [Running the Application](#running-the-application)
  - [Local Development](#local-development)
  - [Production Deployment](#production-deployment)
- [Features Overview](#features-overview)
  - [User Authentication](#user-authentication)
  - [Profile Management](#profile-management)
  - [Workout Logging](#workout-logging)
  - [Workout History](#workout-history)
  - [Update/Delete Workouts](#update-delete-workouts)

## Introduction
Push Up Logger is a web application that enables users to track their push-up workouts, view their workout history, and manage their profiles. This application is built using Flask, with PostgreSQL as the database, and Firebase for storing profile pictures. It’s designed for anyone who wants to keep a record of their workout progress and improve their fitness routine.

## Prerequisites
Before running Push Up Logger, ensure that your system meets the following requirements:
- **Python 3.12 or higher**
- **PostgreSQL** (for managing user and workout data)
- **pip** (Python package installer)
- **Firebase account** for storing profile pictures
- **Git** for version control

## Installation

### Clone the Repository
To get started, clone the repository to your local machine:

```bash
git clone https://github.com/ZakiDhiblawe/push_up.git
cd push_up_logger
```

### Setting Up Virtual Environment
Create and activate a virtual environment to manage your dependencies:

For Windows:
```bash
python -m venv venv
venv\Scriptsctivate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Installing Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables
Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
FLASK_APP=app.py
SECRET_KEY=your_secret_key_here
MAIL_USERNAME=your_email_here
MAIL_PASSWORD=your_password_here
DATABASE_URL=your_postgresql_url_here
```

### Database Setup
Ensure PostgreSQL is installed and running on your machine. Create a database for the application:

```sql
CREATE DATABASE pushups_logger;
```

Run the migrations to set up the database schema:

```bash
flask db upgrade
```

### Firebase Setup
1. Go to your Firebase Console.
2. Create a new project and set up Firebase Storage.
3. Download the `firebase_credentials.json` file and place it in the root directory of the project.
4. Update the Firebase configuration in the `main.py` file:

```python
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your_bucket_url_here'
})
```

## Running the Application

### Local Development
To run the application locally, use the following command:

```bash
flask run
```
Access the application by navigating to `http://127.0.0.1:5000` in your web browser.

### Production Deployment
For production, use Gunicorn to serve the application:

```bash
gunicorn app:app
```
Ensure the production environment is configured correctly with all necessary environment variables.

## Features Overview

### User Authentication
- **Sign Up**: Users can create an account with their email, name, and a strong password.
- **Login/Logout**: Secure login and logout functionality.
- **Password Reset**: Users can reset their password via email.

### Profile Management
- **Update Profile**: Users can update their name, email, and profile picture.
- **Change Password**: Users can change their password securely.

### Workout Logging
- **Log Workouts**: Users can log push-up workouts with the number of push-ups and optional comments.
- **View Today's Progress**: Users can see the total push-ups logged for the current day.

### Workout History
- **View History**: Users can view a history of their workouts, filter by date, and see their progress over time.
- **Track Progress**: Aggregated data for daily and monthly push-up totals.

### Update/Delete Workouts
- **Update Workouts**: Modify the details of previously logged workouts.
- **Delete Workouts**: Remove workouts from the history.
