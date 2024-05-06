### Table of Contents

1. [Installation](#installation)
2. [File Descriptions](#files)

## Installation <a name="installation"></a>

There is the below libraries to run the code here beyond the Anaconda distribution of Python. The code should run with no issues using Python versions 3.10.

<dl>
  <dt>Python Packages used for this project are:</dt>
  <dd>FastAPI</dd>
  <dd>Pydantic</dd>
  <dd>SQLAlchemy</dd>
  <dd>PyMySQL</dd>
</dl>

1. Set up your database 

2. Run the following command to run your web app.
    `python main.py`

3. Go to http://127.0.0.1:8000

## File Descriptions <a name="files"></a>

 recipe_api    
 |- client  
 │   └── client.http # Testing  
 |- database  
 │   └── database.py # DB access  
 |- models  
 │   └── pydantic   
 │   │   └──recipe.py # Validation  
 │   └──models.py # Model  
 |- main.py  
