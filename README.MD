# Social Network API

#### Roee Cohen Shahar

## Virtual Environment

Activate the venv and download all packages

```bash
cd BASE_DIR/av_proj
source Scripts/activate
pip install -r requirements.txt
```


## Server Setup

```bash
cd src/social_network
PYTHONPATH manage.py runserver <PORTNUMBER>
```
Now you can go into http://localhost:PORTNUMBER/admin, see and change the current database as you wish.
```
admin_authentication : (username = roeec, password = 123456)
```

## API
### user signup
#### post request - url: *http://localhost:PORTNUMBER/users/*
data dictionary example
```python
data = {"username": "alexc", "email": "alex@clearbit.com", "password": "yzyzyz"}
```
Email is optional. Sending this request without an email address will not trigger *hunterIO* and *clearbit*. Retrieves full user object.

### user login
#### post request - url: *http://localhost:PORTNUMBER/api/token/*
data dictionary example
```python
data = {"username": "alexc", "password": "yzyzyz"}
```
Retrieves **access** and **refresh** tokens.

The 3 following API calls requires access token(the user is logged in) and therefore any of them need to be sent with the following header - 

```python
headers = {"Authorization": "Bearer " + access_token}  
```
If the **access** token is expired, you'll need to get a new one using the **refresh** token.
 
**post request - url: http://localhost:PORTNUMBER/api/token/refresh**
data dictionary example
```python
data = {"refresh": refresh_token}  
```

### Post Creation
#### post request - url: *http://localhost:PORTNUMBER/post/*
data dictionary example
```python
data = {'content': "this is the post's content"}
```
Requires authentication (access token). Retrieves post Id as in the database. Like and unlike requires this post id.

### Post Like
#### post request - url: *http://localhost:PORTNUMBER/like/*
data dictionary example
```python
data = {'post_id': post_id}
```
Requires authentication (access token). Retrieves post Id as in the database. If the user already likes that post, it does nothing.

### Post Unlike
#### post request - url: *http://localhost:PORTNUMBER/unlike/*
data dictionary example
```python
data = {'post_id': post_id}
```
Requires authentication (access token). Retrieves post Id as in the database. If the user does not like the that post, it does nothing.

## Bot

```bash
cd ../bot
PYTHONPATH bot.py
``` 
Bot's configuration file is located in the same dir as bot.py. Because of limitation of using the free versions of *hunterIO* and *clearbit*, the bot is not using any emails upon signups.

