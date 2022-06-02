# Dynamically Generating DAGs in Airflow using TaskFlowAPI
This repository contains examples for dynamically generating Airflow 2.x DAGs using TaskFlow API. 

Sometimes manually writing DAGs isn't practical.
For example, when we have a lot of DAGs that do similar things with just a parameter changing between them 
or maybe we need a set of DAGs to load tables, but we don't want to manually update DAGs every time those tables change. 
In these cases, and others, it can make more sense to dynamically generate DAGs.
Because everything in Airflow is code, it is possible dynamically generate DAGs using Python alone. 


We use the method with a single Python file which generates DAGs based on some input parameter(s) (e.g. a list of APIs or tables). 
This requires creating many DAGs that all follow a similar pattern. 
Before Apache Airflow 2.2, DAGs that were dynamically generated and then removed didn’t disappear automatically, but this has been fixed.
