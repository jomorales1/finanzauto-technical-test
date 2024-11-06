
# finanzauto-technical-test

## Description

This project is a RESTful API for managing products, built with FastAPI and SQLModel. It includes authentication and various endpoints for product operations.

## Implementation decisions

- **Relational database:** For this use case a relational db was selected (postgres) due the nature of the data to be stored. Products are often used in transactional models with relations to entities such as categories, orders, inventory where is important to have data integrity through ACID operations.

## How to Execute the API with Docker

1. **Build the Docker images:**

    ```sh
    docker-compose build
    ```

2. **Start the services:**

    ```sh
    docker-compose up
    ```

The Swagger documentation will be available at the `/docs` endpoint. A Postman collection is included in the project files to facilitate the interaction with the service.

## Authentication

The API uses JWT for authentication. To obtain a token, you need to send a POST request to the `/v1/auth/token` endpoint with your `client_id` and `client_secret`.

Example request:

```sh
curl -X POST "http://localhost:8000/v1/auth/token" -H "Content-Type: application/json" -d '{"username": "your_client_id", "password": "your_client_secret"}'
```

The response will include an `access_token` which should be used in the `Authorization` header for subsequent requests.

## Products Endpoints

- **GET /v1/products**

    Retrieve a list of products with pagination.

    Query Parameters:
    - `page`: Page number (default: 1)
    - `limit`: Number of items per page (default: 10, max: 100)

- **GET /v1/products/{id}**

    Retrieve a single product by its ID. Requires authentication.

- **POST /v1/products**

    Create a new product. Requires authentication.

    Request Body:
    - `name`: Name of the product
    - `price`: Price of the product
    - `quantity`: Quantity of the product

- **PUT /v1/products/{id}**

    Update an existing product by its ID. Requires authentication.

    Request Body:
    - `name`: Name of the product
    - `price`: Price of the product
    - `quantity`: Quantity of the product

- **DELETE /v1/products/{id}**

    Delete a product by its ID. Requires authentication.

## Unit Tests

Several unit tests were included to ensure protected endpoints require a valid JWT token and the parameters hava a valid structure. Follow the following steps to run the tests:

1. **Ensure the Docker containers are running:**

    ```sh
    docker-compose up
    ```

2. **Run the tests:**

    ```sh
    docker-compose exec api pytest
    ```