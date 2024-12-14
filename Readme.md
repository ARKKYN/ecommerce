# RESTful API for E-Commerce Platform

## About

Simple e-commerce servie with a RESTful API for a view product, add product and order placement.

## Tech Stack

- FastAPI
- SQLite
- Docker
- Pytest

## Endpoints
- GET /products - Get all products
- POST /products - Create a new product
- POST /orders - Create a new order

 Please use the below file to test/view the endpoints using Postman.

 ```
 ecommerce.postman_collection.json
 ```

## Requirements

- Python 3.11
- Docker
- Poetry

## Run the project

To run the project using Docker, you can use the following commands:
```
docker build -t <tag> .
```

```
docker run -d -p 8000:8000 <tag>
```

To run the project on your local machine, you can use the following commands:

```
pip install poetry
poetry install
uvicorn main:app --reload
```

## To Test the project

```
ENVIRONMENT=test poetry run coverage run --source=shop -m pytest ```
