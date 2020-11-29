# RecordSocket
A web application to add and fetch details of students.

[![Python 3.7](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

## Technology stack

- Python 3.7
- Angular CLI 10
- Database : MongoDB
    
## Instructions to Run locally 
1. Install [Python](https://www.python.org/downloads/) and [Angular](https://angular.io/)
2. Clone this repository and open terminal, change directory to backend folder in the repo. 
3. Run `python -m venv ./venv` to create virtual environment.
4. Run `venv\Scripts\activate` command to activate virtual environment.
5. Run `pip install -r requirements.txt` command to install dependencies.
6. Create a **.env** file in the backend folder, containing

```
MONGODB = <mongodb_uri>
```
7. Run python server.py(this will run backend server).
8. Open new terminal and change directory to repo.
9. Run `npm install`.
10. Run `ng serve`.

