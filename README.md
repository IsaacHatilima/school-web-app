# school-web-app

#Create Profile
Using Once virtual environment has been activated. create you admin profile by running the command
->py manage.py shell
from authentication.models import User, Profile
This will switch to shell where you can run commands to your models directs. Once that has been done, creat the profile with the command below
->prof = Profile.objects.create(firstname='John', lastname='Doe', cell='123456', marital_status='Single')
->prof (This will print the Profile instance)
After creating the profile, create the user instance by running the command below:
->user = User.objects.create_superuser(email='isaac@mail.com', username='isaac', role='System Admin', profile=prof, password='Password1')
-> user (This will print the User instance)
Run the exit command below to exit shell and start the server
->exit() 
