# 327-scrum-bucket
Repo for CISC 327 group assignments.

[![Python PEP8](https://github.com/Ensaurus/327-scrum-bucket/actions/workflows/style_check.yml/badge.svg?branch=main)](https://github.com/Ensaurus/327-scrum-bucket/actions/workflows/style_check.yml)
[![Pytest-All](https://github.com/Ensaurus/327-scrum-bucket/actions/workflows/pytest.yml/badge.svg)](https://github.com/Ensaurus/327-scrum-bucket/actions/workflows/pytest.yml)

#  **Document Structure**
```
327-scrum-bucket

├── .github/workflows
│   ├── pytest.yml
│   └── style_check.yml
├── qbay
│   ├── templates
│   │   ├── base.html
│   │   ├── booking.html
│   │   ├── create_listing.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── listing.html
│   │   ├── profile_update.html
│   │   ├── register.html
│   │   └── update_listing.html
│   ├── __init__.py
│   ├── __main__.py
│   ├── controllers.py
│   └── models.py
├── qbay_test
│   ├── frontend
│   │  ├── test_booking.py
│   │  ├── test_listing_creation.py
│   │  ├── test_login.py
│   │  ├── test_profile_update.py
│   │  ├── test_registration.py
│   │  └── test_update_listing.py
│   ├── Generic_SQLI.txt
│   ├── __init__.py
│   ├── conftest.py
│   └── test_models.py
├── .gitignore
├── A0-contract.md
├── Dockerfile
├── LISENSE
├── README.md
├── db_init.sql
├── docker-compose.yml
├── pull_request_template.md
├── requirements.txt
├── sprint4_progress.md
├── sprint4_progress.png
├── sprint5_progress.md
├── sprint5_progress.png
├── sprint6_progress.md
├── sprint6a_progress.png
├── sprint6b_progress.png
└── wait-for-it.sh


```

#  **Docker Run Commands**

To run the web-app
```
docker pull lobus/scrum_bucket_qbay:latest
docker run -p 8081:8081 lobus/scrum_bucket_qbay:latest python3 -m qbay
```

To run the entire system:
```
docker-compose up
```
