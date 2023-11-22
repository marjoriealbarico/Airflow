from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def print_and_return():
    message = "This message will be printed and returned"
    print(message)
    return message

def print_received(**kwargs):
    ti = kwargs['ti']
    message_received = ti.xcom_pull(task_ids='print_task')

    # Printing the received message
    print("Received message:", message_received)

default_args = {
    'owner': 'aaaa',
    'start_date': datetime(2023, 11, 14),
    # Other default args...
}

with DAG('print_task_info', default_args=default_args, schedule_interval=None) as dag:
    task_print_info = PythonOperator(
        task_id='print_task',
        python_callable=print_and_return,
        provide_context=True
    )

    task_print_received = PythonOperator(
        task_id='print_received_task',
        python_callable=print_received,
        provide_context=True
    )

    task_print_info >> task_print_received
