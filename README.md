# INMET Database Maker

[![Bandit](https://github.com/josehenriqueroveda/INMET_database/actions/workflows/bandit.yml/badge.svg)](https://github.com/josehenriqueroveda/INMET_database/actions/workflows/bandit.yml)

The **National Institute of Meteorology** of Brazil provides weather station data free of charge via the website: https://bdmep.inmet.gov.br/

The data comes in *.csv* format, containing a header and a table.
I developed this script to read each of these files separately, extract the necessary information from the header, assigning them to new columns and separating only the most relevant columns to create a single weather database.


## Installation
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set the **DB_CONN** and **DATA_PATH** environment variables in a `.env` file.


## Usage
To run the script, simply execute the `main.py` file:
```bash
python main.py
```

This will load all weather station data files in the **DATA_PATH** directory into the database specified by the **DB_CONN** environment variable.

## License
This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
If you find a bug or have a feature request, please open an issue on the repository. If you would like to contribute code, please fork the repository and submit a pull request.

Before submitting a pull request, please make sure that your code adheres to the following guidelines:
 - Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
 - Write docstrings for all functions and classes.
 - Write unit tests for all functions and classes.
 - Make sure that all tests pass by running pytest.
 - Keep the code simple and easy to understand.
