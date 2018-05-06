# Cats Catalog API

This API allows add and browse images of cats by their breed.


## Installation instructions

1. Install Python3, pip, venv:

`sudo apt install python3 python3-pip python3-venv`

2. Clone this repository:

```
mkdir project
cd ./project
git clone https://github.com/trolleksii/catsapi.git
```

3. Create a new virtual environment with Python 3 interpreter:

 `virtualenv -p python3 ./venv`

4. Activate it:

 `source ./venv/bin/activate`

6. Install required packages from requirements.txt:

`pip install -r ./catsapi/requirements.txt`

7. `cd` into ./catsapi/catapi:

`cd ./catsapi/catapi/`

8. Perform database migrations:

`python manage.py migrate`

9. Run tests to make sure that everything is working as it should:

`python manage.py test`


## Usage instructions

This app has an index page with a brief description of its functionality and very simple demo that fetches random images for selected breed.

Feel free to check out the [API specs]() on GitHub and use this API with a fancier front-end.
