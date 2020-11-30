# RecordSocket
A web application to add and fetch details of students.

[![Python 3.7](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

## Technology stack

- Python 3.7
- Angular CLI 10
- Database : MongoDB
- Backend Hosted on Heroku
- Frontend Hosted on Github Pages
    
## Instructions to Run locally 
1. Install [Python](https://www.python.org/downloads/) and [Angular](https://angular.io/guide/setup-local)
2. Clone this repository and open terminal, change directory to backend folder in the repo. 
3. Run `python -m venv ./venv` to create virtual environment.
4. Run `venv\Scripts\activate` command to activate virtual environment.
5. Run `pip install -r requirements.txt` command to install dependencies.
6. Create a **.env** file in the backend folder, containing
```
MONGODB = <mongodb_uri>
```
7. Run `uvicorn server:app --port 5000`(this will run backend server).
8. Open new terminal and change directory to repo.
9. Open file `src/app/app.component.ts` and change the address in line number 59 to your localhost address.
10. Run `npm install`.
11. Run `ng serve -o`.

## Features
- Authorization: Only those who are authorized can make changes in the database
- Log Management: User can see their previous log.
- FETCH: to obtain details of a entry.
- ADD: to add a new entry to the database.
- UPDATE: to update existing information.
- DELETE: to delete entry from database.

### FETCH 
- Autorization is not Required.
- To get email or name corresponding to Entry Number

Commands Are
1. `FETCH EMAIL <ENTRY_NO>` 
2. `FETCH NAME <ENTRY_NO>` 

### ADD 
- Autorization is Required.
- To add a new entry to the database

Commands Are
1. `ADD <NAME> <ENTRY_NO> <EMAIL>` 

### UPDATE 
- Autorization is Required.
- To update existing information in the database

Commands Are
1. `UPDATE <ENTRY_NO> NAME <NEW_NAME>` 
2. `UPDATE <ENTRY_NO> EMAIL <NEW_EMAIL>` 

### DELETE 
- Autorization is Required.
- To delete record from database.

Commands Are
1. `DELETE <ENTRY_NO>` 
