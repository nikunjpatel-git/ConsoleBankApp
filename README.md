# ConsoleBankApp
It is a basic console python application that can carry out simple bank portal functions along with login and registration. It uses MySql as database so as to store the customer data. 

I have used ```unittest``` and ```mock``` packages for unit testing; and ```coverage``` for unit test coverage.

## Mysql Database Setup

Run the ```Tabels_DDL.sql``` script and you'll be ready to work on the database used in the project.

PS: Change the **hostname** and **password** (as per your mysql server credentials) used in the ```database/dbconnector.py``` to connect to the database.

## Create a vitual environment
Refer [this](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/) link to create a virtual environment first.


## Installating project dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies required for the project using the ```requirements.txt``` file.

```bash
pip install -r requirements.txt
```

## Start the project

Go to the root folder of project and type the below command in terminal.

```bash
python3 Home.py

```

## Run test cases and check code  coverage

Go to the root folder of project and follow the below steps in terminal.

- To run all unittests
```bash
python3 -m unittest discover

```

- To run coverage on all unittests
```bash
coverage run --source=. -m unittest discover

```

- To generate coverage report in terminal
```bash
coverage report -m

```

- To generate a html report for coverage run the following command and Then navigate and open the path:  **main_project_folder/htmlcov/index.html**
This will open the html page in the default browser displaying the coverage data in a tabular form. 
```bash
coverage html

```
