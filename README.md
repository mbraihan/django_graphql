# GraphQl & Django

This is a sample application that utilizes GraphQL, designs a schema for movies and details how to create the GraphQL API with Graphene and Django.

## Setting up

Clone this repo, and in the directory follow these steps:


```
# Create virtual environment
python3 -m venv env
# Activate virtual environment
. env/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run DB migration
python manage.py migrate
# Optional: load test data
python manage.py loaddata movies.json
# Run the application
python manage.py runserver
```
If you go to http://127.0.0.1:5000/graphql/, you'll be able to interact with the API there.
