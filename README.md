# test-work

# First
Run create env.cmd in scripts folder (command promt window will be closed automaticly)

# Second 
Run call env && install requirements.cmd in scripts folder

# Enjoy
# For test APIs
run runserver.cmd in scripts folder
and check 127.0.0.1:8000


# For testing "Redistribute students" 
py manage.py shell
from training_system.tasks import start
start().delay()   # you could run start() without delay(), if you commented out @shared_task in tasks.py!
