# Flask Inventory Management System

A modern web-based inventory management system built with Flask, SQLAlchemy, and Bootstrap 5.

## Features

- **Product Management**: Full CRUD operations for products
- **Location Management**: Manage warehouse/storage locations
- **Movement Tracking**: Track inventory movements (in/out/transfers)
- **Balance Reports**: View current inventory levels per product and location
- **Modern UI**: Bootstrap 5 with gradient backgrounds and responsive design

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed the Database

```bash
python seed.py
```

### 3. Run the Application

```bash
python run.py
```

Or using Flask CLI:

```bash
flask run
```

The application will be available at `http://localhost:5000`

## Database

- Default: SQLite (`sqlite:///app.db`)
- MySQL supported: Set `DATABASE_URL` environment variable

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-WTF
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Database**: SQLite (default), MySQL-ready
