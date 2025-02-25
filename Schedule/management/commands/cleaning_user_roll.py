from django.core.management.base import BaseCommand

# Custom management command for rolling a new user for cleaning duty
# Ran by heroku scheduler on every monday 
# (job will be ran by scheduler every day but will execute the instructions only on Monday, since
# there is no option in the provided scheduler to run once a week)
class Command(BaseCommand):
    help = "<Command for running a job that rolls a new user for cleaning duty>"
    def handle(self, *args, **kwargs):
        from Schedule.jobs import cleaning_user_roll
        self.stdout.write("Starting cleanup roll job")
        cleaning_user_roll(False,7,True)
        self.stdout.write("Ended cleanup roll job")