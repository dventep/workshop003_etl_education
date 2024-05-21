# Installing

### Step by step for execution

Following instructions are based on Windows 11 OS:

1. **Requirements**: To have the required tools for the execution of the repository correctly, so it's necessary to have the following:

   - <img src="https://github.com/get-icon/geticon/raw/master/icons/python.svg" alt="Python" width="21px" height="21px"> <img src="https://github.com/get-icon/geticon/raw/master/icons/pandas-icon.svg" alt="Pandas Python" width="21px" height="21px"> <img src="https://github.com/get-icon/geticon/raw/master/icons/numpy-icon.svg" alt="Numpy Python" width="21px" height="21px"> **[Python](https://www.python.org)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/git-icon.svg" alt="Git" width="21px" height="21px"> **[Git](https://git-scm.com/about)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/postgresql-logo.svg" alt="PostgreSQL" width="21px" height="21px"> **[Postgres](https://www.postgresql.org/)**.
   - <img src="https://github.com/get-icon/geticon/raw/master/icons/postgresql.svg" alt="PgAdmin 4" width="21px" height="21px"> **[PgAdmin 4](https://www.pgadmin.org/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/github-icon.svg" alt="GitHub" width="21px" height="21px"> **[GitHub](https://github.com/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/visual-studio-code.svg" alt="Visual Studio Code" width="21px" height="21px"> **[Visual Studio Code](https://code.visualstudio.com/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/airflow.svg" alt="Airflow" width="21px" height="21px"> **[Apache Airflow](https://airflow.apache.org/docs/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/jupyter.svg" alt="Jupyter Notebook" width="21px" height="21px"> **[Jupyter Notebook](https://jupyter.org/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/docker-icon.svg" alt="Docker" width="21px" height="21px"> **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**.

2. Create folders to execute airflow.

   We must create some folders for the correct execution of airflow, which are:

   - _plugins_
   - _logs_
   - _config/airflow_

3. Create credentials files to connect Postgres database.

   The files must are locate from root folder in:
   - _./config/airflow/_ with name: _credentials.ini_
   - _./config/_ with name: *servers_pgadmin.json*
   - _./config/_ with name: *pgpass*
   - _./config/_ with name: *process.env*
   
   Its structure must be such as the following in which between single quotation marks (') the whole content including the quotation marks must be replaced by the respective information:

>[!NOTE]
> Remember that our credentials will depend entirely on our docker-compose configuration.
> 
> Where:
> - <host>: 'postgres' (default)
> - <database>: 'airflow' (selected)
> - <username>: 'airflow' (selected)
> - <password>: 'airflow' (selected)
> - <port>: 5432 (default)
>

   - _./config/airflow/credentials.ini_

      ```ini
      [postgresql]
      host=<host>
      database=<database>
      user=<username>
      password=<password>
      port=<port>
      ```

   - *./config/servers_pgadmin.json*

      ```json
      {
         "Servers": {
            "1": {
                  "Name": "Airflow server",
                  "Group": "PostgreSQL",
                  "Host": "<host>",
                  "Port": <port>,
                  "MaintenanceDB": "postgres",
                  "Username": "<username>",
                  "PassFile": "/pgpass",
                  "SSLMode": "prefer",
                  "SSLCompression": 0,
                  "Timeout": 10,
                  "UseSSHTunnel": 0
            }
         }
      }
      ```
   
   - *./config/pgpass*

   ```plaintext
      <host>:<port>:<database>:<username>:<password>
   ```
   
   - *./config/process.env*

   ```.env
      DATABASE_HOST=<host>
      POSTGRES_DB=<database>
      POSTGRES_USER=<username>
      POSTGRES_PASSWORD=<password>
      PGADMIN_DEFAULT_EMAIL=admin@airflow.com
      PGADMIN_DEFAULT_PASSWORD=airflow
   ```

4. Now we will run the `docker compose` and to later give life to the `airflow-init` function.

   1. Run in console the command from the base folder: `docker-compose up`.

   2. Let's start the function with the command: `docker-compose up airflow-init`.

5. Create virtual environment for Python, select it and install the libraries of requirements.txt file:

   ```python
   python -m venv venv
   
   pip install -r requirements.txt
   ```

6. Choose venv as Kernel for .ipynb files in the folder **notebooks**.
   ![Evidence selection of Venv](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/evidence_selection_of_venv.png)