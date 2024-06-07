# pyDagFlow

pyDagFlow is a Python library for creating and running directed acyclic graphs (DAGs) of tasks. It is inspired by Apache Airflow, but is designed to be lightweight and easy to use. 

pyDagFlow is build on top of pypubsub. It uses the observer pattern to notify tasks when their dependencies are complete. 