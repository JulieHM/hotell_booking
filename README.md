# Skikkelig Fancy Hotell

This is a website for Skikkelig Fancy Hotell. FILLERTEXT (Ikke ferdig enda)

## URL

http://127.0.0.1:8000/booking/

Because the website is run locally, this will be the URL after running the server
## Prerequisites

* [Python 3.7](https://www.python.org/downloads/release/python-382/) or later
* MySQL package for Python. [Read this first.](#License) Can be installed with the following command:

    ```
    pip install mysql-connector
    ```
    If there is an error related to the SQL package while running the server, try:
    ```
    pip install mysql-connector-python
    ```

## Running the website locally
### Step 1: Download the project

Go to [the gitlab repository](https://gitlab.stud.iie.ntnu.no/tdt4140-2020/40) and download the projcet as a zip file.

Instead you can also run the command:
```
git clone git@gitlab.stud.idi.ntnu.no:tdt4140-2020/40.git
```


**Both methods require you to be connected to [NTNU VPN](https://innsida.ntnu.no/wiki/-/wiki/English/Install+vpn)**

### Step 2: Intall required pip packages
To install required pip packages, move to the project directory (where `requirements.txt` is located) and run the following:
```
pip install -r requirements.txt
```

### Step 3: Run the server locally
To run the server locally, make sure you are in the same directory as the project and run the following command:

```
python manage.py runserver
```

This would look something like this if you just extracted the zip file to your desktop:
```
C:\Users\user_name\Desktop\40-master\fancyhotel python manage.py runserver
```

### Running the tests
The different test commands can get executed in the terminal at `manage.py` level.

* Running all the tests at once using the command: 
    ``` 
    python (or “python3” depending on python version) manage.py test booking. 
    ``` 

* If you want to run a specified test write the whole path. For example: 
    ```
    python3 manage.py test booking.tests.test_views.TestViews.test_index_GET  
    ```
&nbsp; 

 Test coverage is implemented, but first you have to install coverage: 
```
pip install coverage.
```

Then run the coverage command in the terminal: 
```
coverage run ./manage.py test booking.
```

To get the report type: 
```
coverage report.
```
&nbsp; 

*More about tests and coverage: [Oversikt over kodekvalitet](https://gitlab.stud.idi.ntnu.no/tdt4140-2020/40/-/wikis/Oversikt-over-kodekvalitet)*

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [CrispyForms](Some link)
* [Noe Mer?](Some link)


## Contributing

- 
- 
- Magnus Krumbacher
-
-

## Versioning



## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Licence

## Acknowledgments

