Tubus web application (Proof of concept)

Python version 3.7.4  
Using Flask and Bootstrap   
Deployed in Heroku and using Amazon Web Services  

**Project structure:**  
worker.py defines a python process to run in the background, in another thread. 
app.py contains the flask application.  
templates and static folders contain the front-end part of the application.     
src folder englobes the application functionality and algorithms.   
common folder is for utilities used across the project and for the manager of AWS.

For installing all **dependencies**:  
**-** `pip install -r requirements.txt `  

To run **locally**:    
**-** run `worker.py` and `app.py`