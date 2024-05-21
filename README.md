# Happiness score - Workshop 003


### Description

In this repository we will develop a training procedure for a model that allows us to predict happiness within a given space described by several variables. It is based on 5 files in csv format that besides describing the year they are from, contain information of different characteristics that will help us to achieve the objective.

This process was carried out by means of Airflow with two dags, the first one starts with the creation of the database where the data will be loaded; from this comes the listening of a Kafka channel (topic) for the reception of data that via streaming will be received to predict the value we are looking for and finally upload it to a database. While the Kafka channel is listening, the other dag extracts the data from the 5 files, joins and transforms them and then sends them through the same Kafka channel to the receiver.

The tools used are:

   - <img src="https://github.com/get-icon/geticon/raw/master/icons/python.svg" alt="Python" width="21px" height="21px"> <img src="https://github.com/get-icon/geticon/raw/master/icons/pandas-icon.svg" alt="Pandas Python" width="21px" height="21px"> <img src="https://github.com/get-icon/geticon/raw/master/icons/numpy-icon.svg" alt="Numpy Python" width="21px" height="21px"> **[Python](https://www.python.org)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/git-icon.svg" alt="Git" width="21px" height="21px"> **[Git](https://git-scm.com/about)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/postgresql-logo.svg" alt="PostgreSQL" width="21px" height="21px"> **[Postgres](https://www.postgresql.org/)**.
   - <img src="https://github.com/get-icon/geticon/raw/master/icons/postgresql.svg" alt="PgAdmin 4" width="21px" height="21px"> **[PgAdmin 4](https://www.pgadmin.org/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/github-icon.svg" alt="GitHub" width="21px" height="21px"> **[GitHub](https://github.com/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/visual-studio-code.svg" alt="Visual Studio Code" width="21px" height="21px"> **[Visual Studio Code](https://code.visualstudio.com/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/airflow.svg" alt="Airflow" width="21px" height="21px"> **[Apache Airflow](https://airflow.apache.org/docs/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/jupyter.svg" alt="Jupyter Notebook" width="21px" height="21px"> **[Jupyter Notebook](https://jupyter.org/)**.

---
### Purpose - Raison d'être

The project is aimed at demonstrating the skills necessary to train a model in a basic way and provide good results. In addition, to demonstrate the execution of Kafka and its data transmission.

>[!NOTE]
> <span style="color:#5b753f">This project is the third workshop of the ETL subject of Artificial Intelligence & Data Engineering at the Universidad Autónoma de Occidente under the teaching of [Javier Alejandro Vergara Zorilla](https://www.linkedin.com/in/javier-alejandro-vergara/).</span>

---
### Data arquitecture diagram

   Let's see the flow of data in this project. Below there is a diagram, these will allow to have a more visual knowledge of the process that is carried out in the notebook that is in this repository.

- **Metadata of diagram:**
  In this part, there are a few explaining of every block and his properties that you will look in the diagram.

   - **Streamer dag**:
      This dag is in charge of processing the files and sending the information row by row through kafka to the **Viewer** dag.

   - **Viewer dag**:
      This dag communicates with the database engine, creates one and loads the data.

   - **Data sources**:
      In this we have the set of datasets that contain the information we require to predict the **happiness_score**. This datasets are called 2015, 2016, 2017, 2018 and 2019. 

   - **Tasks**.
      This contains all the tasks that Airflow will execute once this is requested:

      - **Extract**. 
         This task extracts the data from each CSV file.

      - **Transform**.
         This task transforms the extracted data to make it ready for concatenation.

      - **Concatenate datasets**.
         This task concatenates the data leaving only one dataset.

      - **Transform concatenated**.
         It performs the necessary transformations to send the data and predict.

      - **Data streaming**.
         It sends the data row by row through Kafka to a channel for further processing.

      - **Create table**.
         Creates the database in which the received data plus the prediction column will be stored.

      - **Consumer data**.
         This task consumes all the data sent by the Kafka channel until it receives the messages destined to indicate its resumption with the process.

      - **It loads the data into the previously created database.**.


#### Airflow: Flow diagram.
   ![Local Flow - Data Arquitecture Diagram](https://gist.githubusercontent.com/dventep/00758162d6f26179210bfee9dfc97a51/raw/b159a30ee5a4f33095c536a3f873ae1495736db8/Airflow%2520Flow%2520Chart%2520-%2520Workshop%2520003%2520ETL.png)
   
---
### Installing guide

Read [installing_README.md](installing_README.md) for details on step by step to install the requirements to deploy this repository.

---
### Project organization

```
   ├── config
   │   ├── airflow
   │   │   └── credentials.ini                  <- Credentials file to connect with PostgreSQL.
   │   ├── pgpass                               <- Credentials file for PgAdmin connect with PostgreSQL.
   │   ├── process.env                          <- Credentials file for environment to used by docker-compose.yaml to Postgres container.
   │   └── servers_pgadmin.json                 <- Credentials file to autoconnect the airflow server in PgAdmin.
   ├── dags
   │   ├── streamer_workshop_003_dag
   │   │   ├── streamer_dag.py                  <- This file provides the configuration and execution of airflow as programmed.
   │   │   └── streamer_process.py              <- Provides the functions to be executed by streamer_dag.py
   │   └── viewer_workshop_003_dag
   │       ├── viewer_dag.py                    <- This file provides the configuration and execution of airflow as programmed.
   │       └── viewer_process.py                <- Provides the functions to be executed by viewer_dag.py
   ├── data
   │   ├── 2015.csv                             <- Data of file 2015 in CSV format.
   │   ├── 2016.csv                             <- Data of file 2016 in CSV format.
   │   ├── 2017.csv                             <- Data of file 2017 in CSV format.
   │   ├── 2018.csv                             <- Data of file 2018 in CSV format.
   │   └── 2019.csv                             <- Data of file 2019 in CSV format.
   ├── files
   │   └── Document - WORKSHOP 002.pdf          <- Descriptive document of the entire process.
   ├── logs
   ├── notebooks
   │   └── eda_main.ipynb                       <- Exploratory Data Analysis (EDA) Report: PostgreSQL data preprocessing, insights.
   ├── plugins
   ├── shared_functions
   │   ├── database_models
   │   │   └── sql_classes.py                   <- SQL classes for database tables.
   │   ├── apply_columns.py                     <- Code to apply of the date from viewer_process.py and streamer_process.py. 
   │   ├── connect_database.py                  <- Code to establish and manage PostgreSQL database connection module. 
   │   └── kafka_functions.py                   <- Code to execute kafka and its functions. 
   ├── installing_README.md                     <- Installation instructions for required tools and process.
   ├── README.md                                <- The README to start the ETL process dashboard with Python and randomly generated candidate data.
   ├── requirements.txt                         <- Python package dependencies for project.
   ├── .gitignore                               <- All files to avoid being read.
   ├── docker-compose.yaml                      <- File for orchestrating all configured services
   └── Dockerfile                               <- It contains the instructions to execute the airflow image and commands inside the container.
```

---
### Conclusions

The process is successfully completed with different tools in which AWS RDS and Ngrok are new to me, and Looker Studio very little previously. Although it’s a pity that they were randomly generated data, because the analysis could lend itself to be much deeper, finding correlations and using whisker plots for some variables.

Throughout the process, some insights about this exploration and conclusions:

- Column removed due to its assigning automately by SQLAlchemy:

   - _sa_instance_state

- 10 columns to 16 columns loaded in **applicant** table in the database.

- 24 technologies were grouped into 8.

- 165 candidates have submitted a minimum of two applications.

- 13.4% of candidates are will be hired.

- As we can see, even randomly generated:

   - The software technology has more movement.

   - Despite critical times such as the pandemic that affected the whole world, it did not affect hiring.

   - The company is either growing a lot or the employee turnover is gigantic.

---
### Evidence

   1. Complete and correct execution of dag Streamer_workshop_003_dag..

      ![Streamer_workshop_003_dag](https://gist.githubusercontent.com/dventep/00758162d6f26179210bfee9dfc97a51/raw/b159a30ee5a4f33095c536a3f873ae1495736db8/streamer_workshop_003_dag.png)

   2. Complete and correct execution of dag Viewer_workshop_003_dag.

      ![Viewer_workshop_003_dag](https://gist.githubusercontent.com/dventep/00758162d6f26179210bfee9dfc97a51/raw/b159a30ee5a4f33095c536a3f873ae1495736db8/viewer_workshop_003_dag.png.png)

   4. Connection with Local PostgreSQL from PgAdmin.
      ![PgAdmin with PostgreSQL]()

---
### My support resources

- <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/github-icon.svg" alt="GitHub" width="21px" height="21px"> <img src="https://avatars.githubusercontent.com/u/92474551" alt="Me" width="21px" height="21px" style="border-radius: 50%"> Github: [Workshop 003 - ETL Education Repository](https://github.com/dventep/workshop003_etl_education/tree/develop).
- <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/github-icon.svg" alt="GitHub" width="21px" height="21px"> <img src="https://avatars.githubusercontent.com/u/92474551" alt="Me" width="21px" height="21px" style="border-radius: 50%"> Gist: [Workshop 003 - ETL Education Gist](https://gist.github.com/dventep/00758162d6f26179210bfee9dfc97a51).
