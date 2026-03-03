# 📚 Library Advanced Management (Odoo 19)
Advanced Library Management System built using Odoo 19 and PostgreSQL 15.

## This project demonstrates:
- Custom Odoo module development
- Multi-model relational architecture
- Computed fields & business logic
- State machine workflow
- Scheduled actions (cron)
- Migration compatibility for Odoo 17+

## 🖥 System Requirements
- Windows 10 / 11
- Python (bundled with Odoo)
- PostgreSQL 15
- Odoo 19 

## 🏗 Module Structure
   ```bash
     library_advanced/
   │
   ├── __init__.py
   ├── __manifest__.py
   │
   ├── models/
   │   ├── book_category.py
   │   ├── book.py
   │   ├── member.py
   │   ├── borrowing.py
   │   ├── borrowing_line.py
   │
   ├── views/
   │   ├── book_views.xml
   │   ├── member_views.xml
   │   ├── borrowing_views.xml
   │   ├── menu.xml
   │
   ├── security/
   │   └── ir.model.access.csv
   │
   └── data/
       ├── sequence.xml
       └── cron.xml
   ```

## 🔧 1. Install PostgreSQL 15
### Step 1 — Download PostgreSQL 15
Download PostgreSQL 15 from:
https://www.postgresql.org/download/windows/

### Step 2 — Install
During installation:
Set password for postgres
Keep default port: 5432
Install pgAdmin (optional)

## 🗄 2. Create Dedicated Database User (Recommended)
Open Command Prompt:
   ```bash
  cd "C:\Program Files\PostgreSQL\15\bin"
  psql -U postgres
   ```
Then create a dedicated user for Odoo:
   ```bash
  CREATE USER library WITH PASSWORD '1234';
  ALTER USER library CREATEDB;
  ALTER USER library WITH SUPERUSER;
   ```
Check roles:
   ```bash
  \du
   ```
Exit
   ```bash
  \q
   ```

## 🏢 3. Install Odoo 19
### Step 1 — Download Odoo 19
Download Odoo 19 from:
https://nightly.odoo.com/19.0/nightly/windows/

### Step 2 — Install
Recommended: Install outside ProgramFiles
   ```bash
   C:\Odoo 19.0
   ```

## ⚙ 4. Configure Odoo (odoo.conf)
Open: 
   ```bash
   C:\Odoo19\server\odoo.conf
   ```
Update database configuration:
   ```bash
   db_user = library
   db_password = 1234
   db_host = localhost
   db_port = 5432
   ```

## ▶ 5. Start Odoo
Open Command Prompt:
   ```bash
  cd C:\Odoo19\server
  ..\python\python.exe odoo-bin
   ```
Open in browser:
   ```bash
  http://localhost:8069
   ```

## 📦 6. Install the Module
Place this module inside:
   ```bash
  C:\Odoo19\server\odoo\addons\
   ```
Then:
1. Go to Apps
2. Click "Update Apps List"
3. Search for: "Library Advanced Management"
4. Click Install
