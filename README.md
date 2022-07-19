# One-Identity-Python-Homework
## Installation, build and run (Ubuntu)
### Download the projecct from here:
https://github.com/mmarcell264/One-Identity-Python-Homework/archive/refs/heads/main.zip
### Or install git and clone repository to your desired location:
```shell
sudo apt update
```
```shell
sudo apt-get install git-all
```
```shell
git clone https://github.com/mmarcell264/One-Identity-Python-Homework.git
```
### Project setup (from the project root):
```shell
cd installation_and_setup
```
#### Install required softwares:
```shell
sudo chmod +x install_softwares.sh
```
```shell
sudo bash install_softwares.sh
```
#### Setup postgresql:
```shell
sudo chmod +x postgres_setup.sh
```
```shell
sudo bash postgres_setup.sh -u <your_db_user_name> -p <your_db_user_password> -d <your_db_name>
```
#### Setup python enviroment:
```shell
sudo chmod +x python_enviroment_setup.sh
```
```shell
sudo bash python_enviroment_setup.sh
```
#### Activate virtual enviroment and testing and run server (from the project root):
```shell
source venv/bin/activate
```
```shell
cd backend/key_value_server/
```
##### Migrate (virtual env must be activated):
```shell
python3 manage.py migrate
```
##### Create superuser (e-mail can be empty, but username and password must be set) (virtual env must be activated):
```shell
python3 manage.py createsuperuser
```
##### Run tests (virtual env must be activated):
```shell
python3 manage.py test
```
##### Start server (virtual env must be activated):
```shell
python3 manage.py runserver
```
## Manual testing:

You can test the API endpoint with httpie from a new terminal. (It was installed with install_softwares.sh) Or you can install Postman and have an UI.

Install Postman:
```shell
sudo snap install postman
```

### End points (with the base settings of the running server):
- http://127.0.0.1:8000/api/: 
 
  Return the server status -> **http http://127.0.0.1:8000/api/** . If the server is running it will returns with: { "status": "Server is running." }.

- http://127.0.0.1:8000/api/token-auth/ (you need this to work with the API main functionality): 

  Return a token to a user -> **http POST http://127.0.0.1:8000/api/token-auth/ username=<your_user_name> password=<your_password>** . It will return something like this: { "token": "your_token" }.

- http://127.0.0.1:8000/api/add/: 
 
  Add a key-value pair -> **http POST http://127.0.0.1:8000/api/add/  'Authorization: Bearer <your_token>' key="key" value="value"** . It will return something like this:  { "status": "Key-value pair has been successfully created."}

- http://127.0.0.1:8000/api/get/<:key>/value/: 
 
  Return a key's value -> **http http://127.0.0.1:8000/api/get/<:key>/value/ 'Authorization: Bearer <your_token>'** . It will return something like this: { "value": "your_key's_value" }.
  
- http://127.0.0.1:8000/api/get/keys/?prefix="<prefix>": 

  Return keys with the specified value prefix -> **http http://127.0.0.1:8000/api/get/keys/?prefix="<your_prefix>" 'Authorization: Bearer <your_token>'** . It will return something like this: { "count": number, "next": link, "previous": link, "results": [ { "key": "key_value" }, ... ] }
  
## Technical descisions:
### Database:
When I saw that a key-value server had to be implemented, I thought of 3 databases that could be used. Two of them are NoSQL and one is SQL. These are:
#### Redis (NoSQL):
Redis is a key value database. Where key values can take many different forms, such as strings, bitmaps, lists, sets. But without the keys, the values cannot be used and keys must be defined based on the values of one of the requirements. Therefore, I have dropped this database.
#### MongoDB (NoSQL):
Data is stored in documents with key-value pairs. Here too, values can have multiple types, such as a list or even a nested document. Easily scalable. Aggregation is one of the main function. But since both keys and values can be just strings, I chose an other databse. 
#### PostgreSQL (SQL):
It is full-text search enigne. It supports stemming and ranking the results (orders results based on how often the query terms appear and how close together they are). We can specify weights to queries and they will be ordered by relevancy to their weights. It is supports trigram similarity too. One of the best supported databases in django. And since both the key and the values should be string, I chose this database. I worked with Table(id, key, value) schame, where key column must hold unique values.
  
### Backend technology:
I worked with Django. It is very robust framework. Robustness is both an advantage and a disadvantage (especially for beginners). It has many functions, and some of them have keyword arguments that are poorly documented. So it can be difficult for beginners to fully understand the functions at the beginning, although they can be very helpful. The Django has several safety features like SQL injection protection which is achived with its own ORM and Cross site request forgery (CSRF) protection ( https://docs.djangoproject.com/en/4.0/topics/security/). Django follows MVT (Model-View-Template) architecture, so if we want to use it to build an API we need an other library which extends its features, that library is caleed django rest framework. I used this too.

We can write API endpoints with functions and classes( or we can inherit from generic classes too, like mixins or GenericAPIVIew). I decided to use function-based endpoints because my every endpoint support only one tpe of http request method and class-based endpoints are preferable in my opinion when an endpoint supports multiple request methods.
  
I don't know if it's a feature or a bug, but my ORM class that has two Charfield variables. When I instantiate it accepts int values in the variables (it doesn't throw  validation error). And after I save the ORM class istance to the database replaces them with string. I think this can confuse users and lead to the conclusion that the application handles ints as well, so I introduced a validation in the add endpoint that checks the key-value types to see if they are really strings.
  
I use pagination at the endpoint where the keys are returned by value prefix, because if there are many matches it can be very costly to send them to the user at once. (Django uses lazy fetch so the query is only evaluated if result is needed)
  
I use throttling to defend against basic DoS attack, but without authentication it is easy to get around with IP spoofing (fairly new security vulnerability, if i know right it, it has not been fixed yet) (source: https://stackoverflow.com/questions/70688368/which-version-of-django-rest-framework-is-affected-by-ip-spoofing, direct link: https://portswigger.net/daily-swig/ip-spoofing-bug-leaves-django-rest-applications-open-to-ddos-password-cracking-attacks). That's why I use authentication too, to be precise basic token based authentication. If you want to use the API main functionality you have to be logged in. The reason I don't use basic authentication because then POST and PUT requests need CSRF token.I have overridden the basic token-based class to geenerate and accept token this way 'Bearer <toke>' instead of the base 'Token <token>'. Postman accepts the former('Bearer') format by default. And throttling cannot be trusted fully with authentication too, cause it is not implemented thread safe  (source: https://github.com/encode/django-rest-framework/issues/8127). So if we want a proper DoS protection we need a web server like nginex (that can be used as preverse proxy and load balancer too). (The token authentication is not safe over Http too.)
  
I installed an aditional library too what is called  django-cors-headers. It is a middleware and responsible for the Cross-Origin Resource Sharing Headers. Django rest framework by default does not add this headers and if we want a UI frontend to our API, the javascript fetch function for example needs this Headers. And with this package we can set which origins are allowed too.
  
I outsourced the Django application's security key and the important database connection parameters to an .env file.

  
  











