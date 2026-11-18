
# api-test-lab
[![API tests](https://github.com/panguloNORGE/api-test-lab/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/panguloNORGE/api-test-lab/actions/workflows/tests.yml)
free API running on Docker container, do API calls tests with pytest. Docker compose to start the API and trigger the tests, github actions to run tests whenever we push code 

How to run
docker compose up --build --abort-on-container-exit --exit-code-from tests

Design choices
Black-box tests over HTTP; the API address comes from API_URL
Each test creates and deletes its own data (pytest fixtures)
Compose waits for the API health check before running the tests
