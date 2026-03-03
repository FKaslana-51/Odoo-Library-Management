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
- Odoo 19 Community

## 🔧 1. Install PostgreSQL 15
### Step 1 — Download
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
