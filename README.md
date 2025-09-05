# PC Builder Project

## Review

This is a Flask web application for assembling and managing PC components: motherboards, processors, video cards, RAM, etc. The compatibility of components is checked.

---

## Structure

```text
├── alembic               # Migration managment
├── app
│   ├── __init__.py       # Creating app
│   ├── api               # Application programming interface
│   ├── config.py         # Loading .env file and get "settings" instance
│   ├── database_data.py  # Generate data for database (Example of these PC assemblies)
│   ├── database.py       # SQLAlchemy database configuration
│   ├── forms.py          # Validation Flask-WTForms
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # Flask routes
│   ├── static            # CSS
│   └── templates         # HTML
├── docker-compose.yml    # Application configuration for docker 
├── Dockerfile            # Instructions for building a docker image 
├── README.md             # Project discription
├── requirements.txt      # Requirements for installation
└── run.py                # Project launcher
```

### 1. Install Docker

* Docker: [https://www.docker.com/](https://www.docker.com/)

### 2. Launch docker image

On Linux/MacOS/Windows:
```
docker compose up --build
```

### 3. Follow the link
   [http://127.0.0.1:8000](http://127.0.0.1:8000)


