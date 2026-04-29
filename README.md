# AWS ERP Platform

## Overview

AWS ERP Platform is a cloud-based Enterprise Resource Planning (ERP) backend infrastructure designed as a scalable MVP foundation for business management systems. This project demonstrates how to deploy a production-capable ERP environment using modern cloud architecture, backend engineering, and DevOps workflows.

Built with AWS infrastructure, the platform provides a centralized deployment model for ERP applications covering employee management, inventory control, order processing, and reporting modules.

---

## Core Objectives

* Build a deployable ERP backend architecture
* Transition from local development to cloud production hosting
* Establish a scalable SaaS-ready deployment model
* Demonstrate practical AWS, backend, and DevOps engineering skills
* Provide a modular framework for future ERP expansion

---

## Technology Stack

### Cloud Infrastructure

* **AWS EC2** – Application hosting
* **AWS RDS PostgreSQL** – Managed relational database
* **AWS VPC & Security Groups** – Network security and access control

### Backend

* **FastAPI (Python)** – High-performance API framework
* **SQLAlchemy** – ORM and database integration
* **Uvicorn** – ASGI production server
* **Supervisor** – Persistent service management

### Source Control & Deployment

* **GitHub** – Version control and team collaboration
* **SSH** – Secure server access
* **Manual CI/CD Workflow** – Git pull + service restart deployment process

### Future Frontend Compatibility

* React
* Angular
* Other modern frontend frameworks

---

## System Architecture

```text
Users / Browser
      ↓
Frontend Application (React/Angular)
      ↓
AWS EC2 Ubuntu Server (FastAPI Backend API)
      ↓
AWS RDS PostgreSQL Database
```

---

## Current ERP Modules

### Employees

* Employee records
* Department tracking
* Role management
* Active/inactive status

### Inventory

* SKU management
* Quantity tracking
* Unit cost management

### Orders

* Customer orders
* Status tracking
* Revenue totals

### Reports

* Operational data visibility
* Future analytics expansion

---

## Key Features

* Cloud-hosted production backend
* Persistent deployment with Supervisor
* Managed PostgreSQL database
* Modular ERP schema
* Team-ready GitHub repository structure
* Secure environment variable configuration
* Expandable SaaS infrastructure
* AWS deployment experience

---

## Deployment Workflow

### Local Development

```bash
git clone <repo>
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn main:app --reload
```

### Production Deployment

```bash
git pull origin main
source .venv/bin/activate
sudo supervisorctl restart erp-api
```

---

## Security Practices

### Sensitive files excluded via `.gitignore`

* `.env`
* AWS credentials
* RDS passwords
* SSH private keys (`.pem`)
* Virtual environments
* Node modules
* Logs

### Security priorities

* Credential protection
* Infrastructure integrity
* Secure deployment practices
* Team-safe repository management

---

## Professional Value

This project demonstrates practical skills in:

* Cloud architecture design
* AWS infrastructure deployment
* Backend API engineering
* PostgreSQL integration
* Linux server administration
* GitHub collaboration workflows
* DevOps deployment pipelines
* SaaS product foundation development

---

## Potential Industry Applications

* Hotel ERPs
* School ERPs
* Pharmacy ERPs
* Inventory systems
* CRM platforms
* Business operations software

---

## Future Enhancements

* Docker containerization
* Nginx reverse proxy
* SSL/HTTPS
* GitHub Actions CI/CD
* Role-based authentication
* Frontend production deployment
* Monitoring/logging systems
* Multi-tenant SaaS capabilities

---

## Repository Structure

```text
aws-erp-platform/
├── backend/        # Backend API services
├── frontend/       # Frontend application
├── database/       # Schema and migrations
├── docs/           # Documentation
├── README.md
└── .gitignore
```

---



## Author

**Emery Patrick Marara**

Cloud-focused Data Engineer | Data Scientist

---

## License

This project is intended for educational, portfolio, and scalable business development purposes.
