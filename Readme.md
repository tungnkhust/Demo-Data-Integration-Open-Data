
# 1. Set up environment
### Setting up a virtual environment

[Conda](https://conda.io/) can be used to set up a virtual environment with the version of Python required for Comet. If you already have a Python 3.6 or 3.7 environment you want to use, you can skip this section

1. [Download and install Conda](https://conda.io/docs/download.html).

2. Create a Conda environment with Python 3.6

```sh
conda create -n demo python=3.6.10
```

3. Activate the Conda environment.

```sh
conda activate demo
```

4. Install requirement
```
pip install -r requirements.txt
```

# 2. How to run
1. Set AIRFLOW_HOME to the current folder (must is `absolute path`)
```
export AIRFLOW_HOME=/home/tungnk/Desktop/Data-Integration/BTQT/Demo-Data-Integration-Open-Data
airflow users  create --role Admin --username demo --email demo@gmail.com --firstname demo --lastname demo --password demo
```

2. Run as standalone
```
# Init DB
airflow db init

# create admin user
airflow users  create --role Admin --username demo --email demo@gmail.com --firstname demo --lastname demo --password demo

# run webserver
airflow webserver -p 8080

# run scheduler
airflow scheduler
```

**Note: If you open new terminal tab, you must EXPORT AIRFLOW_HOME