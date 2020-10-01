#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

echo SECRET_KEY: $SECRET_KEY > secrets.yaml
echo database_password: $database_password >> secrets.yaml
echo Ocp_Apim_Subscription_Key: $Ocp_Apim_Subscription_Key >> secrets.yaml
echo storage_account_key: $storage_account_key >> secrets.yaml

python /code/manage.py runserver 0.0.0.0:8000
