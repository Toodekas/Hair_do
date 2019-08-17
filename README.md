# Hair_do
Python program that takes events from Google calendar and places events on days you should wash your hair for maximum hair growth
Currently it only fills out the whole week with days you should/can wash your hair

The way to run it is:
1) make sure you have python installed
2) have installed pip
3) run this command in the library using pip
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
4) run the main.py code
5) a window with your google login should come in


Issues and possible future fixes:
The Google Calendar API does not yet support adding a "reminder" or a "task" it only lets you add events in the future I'd like it to
display it as a reminder
Currently it only supports organizing your hairwashing for a week in the future I want this to be something like where it automatically
changes in the background depending on when and where your dates are

