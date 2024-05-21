# Installing

### Step by step for execution

Following instructions are based on Windows 11 OS:

1. **Requirements**: To have the required tools for the execution of the repository correctly, so it's necessary to have the following:

   - <img src="https://github.com/get-icon/geticon/raw/master/icons/python.svg" alt="Python" width="21px" height="21px"> <img src="https://github.com/get-icon/geticon/raw/master/icons/pandas-icon.svg" alt="Pandas Python" width="21px" height="21px"> <img src="https://github.com/get-icon/geticon/raw/master/icons/numpy-icon.svg" alt="Numpy Python" width="21px" height="21px"> **[Python](https://www.python.org/downloads/)** _(Optional: used version 3.10.3)_.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/git-icon.svg" alt="Git" width="21px" height="21px"> **[Git](https://git-scm.com/downloads)** _(Optional: used version 2.43.0)_.
   - <img src="https://assets-global.website-files.com/63ed4bc7a4b189da942a6b8c/63ef8624e010d9861920be4e_ngrok-favicon.svg" alt="Git" width="21px" height="21px"> **[Ngrok](https://ngrok.com/download)** _(Optional: used version 3.6.0, this is only requirement if you want to connect Looker Studio to Local PostgreSQL)_.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/postgresql-logo.svg" alt="PostgreSQL" width="21px" height="21px"> **[Postgres](https://www.postgresql.org/download)** _(Optional: used version 16.1)_.
   - <img src="https://github.com/get-icon/geticon/raw/master/icons/postgresql.svg" alt="PgAdmin 4" width="21px" height="21px"> **[PgAdmin 4](https://www.pgadmin.org/download/)** _(Optional: used version 7.8, PosgreSQL's installation brings PgAdmin 4)_.
   - <img src="https://github.com/get-icon/geticon/raw/master/icons/aws.svg" alt="AWS" width="21px" height="21px"> <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/aws-rds.svg" alt="AWS RDS" width="21px" height="21px"> **[AWS RDS](https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwiwkpv2pKSEAxWPuVoFHf2EAbwYABAAGgJ2dQ&ase=2&gclid=CjwKCAiA_aGuBhACEiwAly57MTL4U4hy14avuIvQqnyTW3qLO0oDvonHgfXrsmleQHE-rEK8zTKxlxoCHoMQAvD_BwE&ohost=www.google.com&cid=CAESVeD2Jr0_QQpQLU5ADLjI5Fz49bQCraF74sHyYXzpOCr12nkr91opntblv7p3tuhYFZXQE7r84QneeMHj3shjJg64CTJEDkXS3koCfOUcMVWMdTTk_b0&sig=AOD64_0-ZEYfY4AJ3dBJsNKYxvHHnBtuXw&q&nis=4&adurl&ved=2ahUKEwjcrZT2pKSEAxUpfjABHe_IApcQ0Qx6BAgIEAE)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/github-icon.svg" alt="GitHub" width="21px" height="21px"> **[GitHub](https://github.com/)**.
   - <img src="https://raw.githubusercontent.com/get-icon/geticon/fc0f660daee147afb4a56c64e12bde6486b73e39/icons/looker-icon.svg" alt="Looker Studio" width="21px" height="21px"> **[Looker Studio](https://lookerstudio.google.com/)**.

2. Create credentials file to connect local Postgres.

   The file must is locate from root folder in _./code/config/_ with name _credentials.ini_. Its structure must be such as the following in which between single quotation marks (') the whole content including the quotation marks must be replaced by the respective information:

   ```ini
   [postgresql]
   host='localhost (default)'
   database=etl_workshop_first
   user='postgres (default)'
   password=' (default)'
   port='5432 (default)'
   ```

>[!NOTE]
> If you notice, AWS RDS was mentioned and in the .gitignore file there is aws_credentials.ini filename. In the process as will be evidenced below, you will find the screenshots of part of the services and connections established in AWS to connect me from the execution of these notebooks to Looker Studio.
>
> The service at this moment is down for the elimination of unnecessary costs, if it's needed in a few adjustments it will be implemented.

3. Create virtual environment for Python:

   ```python
   python -m venv venv
   ```
4. Choose venv as Kernel for .ipynb files in the folder **notebooks**.
   ![Evidence selection of Venv](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/evidence_selection_of_venv.png)

   In each file in **notebooks**, there is a code line to install required libraries if necessary with the title '_Install requirement libraries_'.

   As it's in the following screenshot:
  ![Evidence of section Install requirement libraries](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/evidence_of_section_install_requiremente_libraries.png)

5. Create the _TCP tunnel_ to connect _Local PostgreSQL_ to _Looker Studio_.

   After install _Ngrok_, we need to execute it and sign in with our accounts to get tokens, because to create the tunnel, Ngrok require a token.

   Finally, knowing our port on which PostgreSQL is running, we execute the following where 'port' is the port that we know:

   ```bash
   ngrok tcp port
   ```
   Such as:
   ![Evidence of Ngrok is running](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/evidence_of_ngrok_is_running.png)
   According the example, our host is `4.tcp.ngrok.io` and our port `10297` to put in "*database authentication*" in PostgreSQL connector of _Looker Studio_.

6. Explorate the notebooks in the folder **notebooks**. There are two notebooks: _load_csv_file_ and _EDA_report_.

   - **load_csv_file:** Its objective is take the raw dataset in a csv file and load it in a PosgreSQL database within the **raw_applicant** table.
   - **eda_report:** Its objective is take data of **raw_applicant**, explore, transform, analyze and load it in the same database within **applicant** table.

>[!NOTE]
> To execute in order, let's start with **load_csv_file** and later **eda_report**.

7. Then executed every notebook, we should verify the existence of the database.

   As the AWS RDS service will only be active on occasions that merit it, according to the project, it will have been performed on the local PostgreSQL; so openning PgAdmin 4 we will be able to verify the existence of the database and the records loaded.

8. Now, we go to Looker Studio to look the dashboard created with these data.

   **Link of the dashboard:** [Dashboard in Looker Studio](https://lookerstudio.google.com/reporting/7c98a50e-d58f-4e4e-a8e8-17a09b233513).

   If we want, could update the data by editing the connection previously established with our credentials or create a new dashboard:

   1. Click on _Add data_ option:
      ![Click on Add data](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/add_data_option_in_looker_studio.png)

   2. Choose PosgreSQL Connector:
      ![To choose PostgreSQL Connector in Looker Studio](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/choose_postgresql_connector_in_looker_studio.png)

   3. Use our credentials to connect and choose _applicant_ table of the database.

      To use our credentials, we need according Ngrok gave us, our host and port:

      ```ini
      host = 4.tcp.ngrok.io
      port = 10297
      database = etl_workshop_first
      user = --------
      password = --------
      ```

      ![Config to connect Looker Studio with PostgreSQL](https://gist.githubusercontent.com/dventep/579f1646c6d6011e4e8314fb85482eba/raw/79d0afa23cb3a60b23821531b35c07fea0cb1790/config_to_connect_looker_studio_with_postgresql.png)

      Now, we have the data sync with Looker Studio.