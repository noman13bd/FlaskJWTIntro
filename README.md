# FlaskJWTIntro

1. clone the repo and `CD` into the folder
2. `python3 -m venv env`
3. `pip install -r requirements.txt`
4. `python3 app.py`

# End Point Requests
1. Login to get JWT. (123456 is hard coded password)
```
curl --location --request POST 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "un":"noman",
    "pwd": "123456"
}'```

2. access restriced end point with the token 
```curl --location --request GET 'http://127.0.0.1:5000/auth?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDQwNTUzMjIsInVzZXIiOiJub21hbiJ9.DSr27L5qHYXWcGw99PgSkBj2iUqWOh5n0Kyi04vS2FA'```