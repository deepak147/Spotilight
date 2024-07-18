Install all the packages in requirements.txt using below command

pip install -r requirements.txt

To schedule celery tasks, open two terminals and run the below commands

Terminal 1:
celery -A tasks beat --loglevel=info 

Terminal 2:
celery -A tasks worker --pool=solo -l info