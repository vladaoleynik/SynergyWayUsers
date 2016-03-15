## Getting Started

To get you started you can need first to install the dependencies.

### Install JavaScript Dependencies

* Get the tools depend upon via `npm`, the [node package manager][npm].
* Get the angular code via `bower`, a [client-side code package manager][bower].

`npm` is preconfigured to automatically run `bower` so you can simply do:

```
npm install
```

Behind the scenes this will also call `bower install`.  

### Install Python Dependencies

Create virtual environment first:

```
virtualenv env
```

Activate your virtual environment:

```
source /env/bin/activate
```

Install dependencies from requirements.txt:
 
```
pip install -r requirements.txt
```

### Create DB, Tables with populated data and Procedures

I have SQL script that contains PostgreSQL DB and Tables create.
Populates it with data and also creates stored procedures.
So you can just do:

```
sudo psql -U postgres -f synergyWayUsers/db/populate_db.sql
```

And then follow instructions that can appear. `synergy_way` user
is created with password `root`.
       
### Run the Application

The simplest way to start Flask server is:

```
python synergyWayUsers/run.py
```

Now browse to the app at `http://localhost:8000/`.
