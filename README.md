
# Barbershop Application

This is a Barbershop management application built with FastAPI and Tkinter. It allows you to register haircuts, view historical data, and manage haircut records.

## Features

- Register new haircuts
- View total income and number of haircuts
- Filter haircut records by date and type
- Delete haircut records
- View historical data
- REST API for managing haircuts

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd barbershop
    ```

2. Install dependencies using Pipenv:
    ```sh
    pipenv install
    ```

3. Activate the virtual environment:
    ```sh
    pipenv shell
    ```

## Usage

### Running the FastAPI Server

To start the FastAPI server, run:
```sh
uvicorn barbershop.app:app --reload
```

The server will be available at http://127.0.0.1:8000.

Running the Tkinter Application
To start the Tkinter application, run:

Testing
To run the tests, use:

# TODO
    - <input disabled="" type="checkbox"> Add connection to database (noSql)<br>
    - <input disabled="" type="checkbox"> Add styles to buttons and forms<br>
    - <input disabled="" type="checkbox"> Improve logic for buttons in haircuts tables<br>
    - <input disabled="" type="checkbox"> Use pydantic when possible<br>
    - <input disabled="" type="checkbox"> Find a solution to "tabs" in Tkinter<br>
    - <input disabled="" type="checkbox"> Add filters with correct logic<br>
    - <input disabled="" type="checkbox"> Add IA for improvements<br>
    - <input disabled="" type="checkbox"> Add graphics using matplotlib (in a new tab)<br>

# License
This project is licensed under the MIT License.
