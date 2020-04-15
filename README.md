# Skikkelig Fancy Hotell

This is a website for Skikkelig Fancy Hotell. FILLERTEXT (Ikke ferdig enda)


## URL

http://127.0.0.1:8000/booking/

Because the website is run locally, this will be the URL to the website after running the server (Guide on how to do that below)


## Prerequisites

* [Python 3.7](https://www.python.org/downloads/release/python-382/) or later

* MySQL package for Python. Can be installed with the following command:

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

### Step 2: Jump to the directory of the project
This can be done with:
```
cd <Path for the project folder>
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

Tests

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

- Magnus Krumbacher
- 
-
-
-

## Versioning



## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

Licence

## Acknowledgments



