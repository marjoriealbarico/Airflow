import airflow
from datetime import datetime
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import json


def data_transform():
    
    # clean and load "tranche age" data
    df_age = pd.read_csv('data/code-tranches-dage-donnees-urgences.csv', delimiter=';', header=None)
    df_age.columns = ['Code tranches d\'age', 'tranche d\'age']
    df_age['tranche d\'age'] = df_age['tranche d\'age'].str.replace('"', '').str.replace(' ans', '')
    df_age[['age min', 'age max']] = df_age['tranche d\'age'].str.split('-', expand=True)
    df_age['age min'] = pd.to_numeric(df_age['age min'], errors='coerce')
    df_age['age max'] = pd.to_numeric(df_age['age max'].str.replace(' ou plus', ''), errors='coerce')
    df_age.loc[df_age['tranche d\'age'].fillna('').str.contains('Tous âges'), ['age min', 'age max']] = [0, 120]
    df_age.loc[df_age['tranche d\'age'].fillna('').str.contains('75 ou plus'), ['age min', 'age max']] = [75, 120]
    cleaned_df_age = df_age[df_age['Code tranches d\'age'] != 'Code tranches d\'age'].copy()
    cleaned_df_age.drop(columns=['tranche d\'age'], inplace=True)
    postgres_sql_upload = PostgresHook(postgres_conn_id="postgres_connexion")
    cleaned_df_age.to_sql('tranche_age', postgres_sql_upload.get_sqlalchemy_engine(), if_exists='replace', chunksize=1000)

    # clean and load "departments-region" data
    with open('data/departements-region.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    alpha_numeric_mapping = {entry['num_dep']: idx for idx, entry in enumerate(data, start=1)}
    for entry in data:
        entry['num_dep'] = alpha_numeric_mapping[entry['num_dep']]
    df = pd.DataFrame(data)
    df_cleaned_dept = df.rename(columns={'num_dep': 'num_dep_int'})
    cleaned_df_dept = df_cleaned_dept.copy()
    postgres_sql_upload = PostgresHook(postgres_conn_id="postgres_connexion")
    cleaned_df_dept.to_sql('departments_region', postgres_sql_upload.get_sqlalchemy_engine(), if_exists='replace', chunksize=1000)
    
    #clean and load "données-urgences" data
    df_urgences = pd.read_csv('data/donnees-urgences-SOS-medecins.csv', delimiter=';', low_memory=False)
    df_urgences['dep'] = df_urgences['dep'].str.replace(r'\D', '', regex=True)
    # Convert the 'dep' column to integers
    df_urgences['dep'] = pd.to_numeric(df_urgences['dep'], errors='coerce')
    columns_to_drop = [
        'nbre_acte_corona', 'nbre_acte_tot', 'nbre_acte_corona_h', 'nbre_acte_corona_f',
        'nbre_acte_tot_h', 'nbre_acte_tot_f'
    ]
    df_cleaned_urgences = df_urgences.drop(columns=columns_to_drop, errors='ignore')
    postgres_sql_upload = PostgresHook(postgres_conn_id="postgres_connexion")
    df_cleaned_urgences.to_sql('urgences_covid', postgres_sql_upload.get_sqlalchemy_engine(), if_exists='replace', chunksize=1000)
    
    return

def send_email_on_failure(context):
    # Logic to send email on failure
    # Access relevant context information like task instance, dag, etc.
    print("Sending email on failure")
    # Example code to send an email using Airflow's EmailOperator or external service

default_args = {
    'owner':'aairflow',
    # 'email':
    # 'email
    'depends_on_past': False
}
    
with DAG (
    'ETL_projet',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    on_failure_callback=send_email_on_failure
) as dag:
    create_table_age = PostgresOperator(
        task_id="create_table_age",
        postgres_conn_id="postgres_connexion",
        sql="/sql/create_table_age.sql",
        dag=dag
    )
    create_table_dept = PostgresOperator(
        task_id="create_table_dept",
        postgres_conn_id="postgres_connexion",
        sql="/sql/create_table_dept.sql",
        dag=dag
    )
    create_table_urgences = PostgresOperator(
        task_id="create_table_urgences",
        postgres_conn_id="postgres_connexion",
        sql="/sql/create_table_urgences.sql",
        dag=dag
    )
    transform_and_load = PythonOperator(
        task_id="transform_and_load",
        python_callable=data_transform,
        provide_context=True,
        dag=dag
    )
    
    [create_table_age, create_table_dept] >> create_table_urgences >> transform_and_load
    
