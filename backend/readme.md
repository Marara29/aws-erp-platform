# AWS ERP Platform

Cloud-based ERP platform using AWS infrastructure.

## Project Structure

aws-erp-platform/
├── backend/       # ERP backend API
├── frontend/      # ERP frontend application
├── database/      # SQL schemas and migrations
├── docs/          # Project documentation
├── README.md
└── .gitignore

## Infrastructure

- Backend hosted on AWS EC2
- Database hosted on AWS RDS PostgreSQL
- Source code managed with GitHub
- App process managed with Supervisor

## Development Workflow

1. Pull latest code:
git pull origin main

2. Make changes.

3. Commit and push:
git add .
git commit -m "update ERP code"
git push origin main

4. Restart backend:
sudo supervisorctl restart erp-api

## Security Notice

Do not commit:
- .env
- AWS keys
- RDS password
- SSH .pem files
- Database credentials