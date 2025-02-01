# Django REST API

This is a learning project for me to learn using Django + Python. I have rarely used Python and never used Django in a professional capacity up until now but I felt curious and wanted to dedicate some free time to see what the world of programming looks outside of PHP + Symfony.

Also I wondered whether I should take my career as a software developer down a new path, coding Python for a change.

My goal is to create a REST API with Django using as little third party software as possible, which is why I haven't used the Django REST Framework and am using built-in tools like Unittest instead of e.g. Pytest.

## Running the API

You need to have GIT and Docker installed to install the API. You can use the API with a HTTP client like Postman or curl.

1. Clone the GIT repository
2. Copy `.env.dist` to `.env` 
3. Run `make init`
4. Run `make start_server` to run the server
5. The API will now be accessible at [http://localhost:8000/](http://localhost:8000/)

## API documentation

I find writing documentation is an important but tedious task, which is why I am relying on Swagger to do the job for me much better than I could have done it myself. Please visit [http://localhost:8000/docs/](http://localhost:8000/docs/) to view the documentation.