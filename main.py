from __future__ import print_function
from tkinter import *
from googleapiclient.discovery import *
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


class GUI:
    def __init__(self,root):
        self.root = root
        root.title("HairDO")

        self.info = Label(root,text="See on barebones versioon, disabled on Google Calendar API, kunas update disabled some features")
        self.info.grid(row = 0, column = 0)

        self.varv_val = IntVar()
        self.varv = Checkbutton(root, text = "Kas sul on juuksed värvitud hetkel?", variable = self.varv_val)
        self.varv.grid(row=1, column = 0)

        self.brown_val = IntVar()
        self.brown = Checkbutton(root, text = "Naturaalne brünett?", variable = self.brown_val)
        self.brown.grid(row = 2, column = 0)

        self.kuiv_val = IntVar()
        self.kuiv = Checkbutton(root, text="Kas sul on kuivad juuksed", variable=self.kuiv_val)
        self.kuiv.grid(row = 3, column = 0)

        self.vi_val = IntVar()
        self.vi = Checkbutton(root, text = "Kas sul on tihedad juuksed või sul on lokid?", variable=self.vi_val)
        self.vi.grid(row=4, column = 0)

        Label(root, text="Mitme päeva jaoks on vaja kalkulatsioon teha?").grid(row=5,column=0)
        
        self.calctime = Entry()
        self.calctime.grid(row=6, column=0)
        
        self.sub = Button(root, text="Kalkuleeri", command= self.getcalendar)
        self.sub.grid(row=7,column = 0)

        Button(root, text="SITANE", command=self.createevent).grid(row=8, column=0)

    def kalk(self):
        p = 4
        #fsdsdjsdhfsdf 13. self.createevent(self)
        if self.varv_val.get() == 1:
            p = p-1
        if self.kuiv_val.get() == 1:
            p = p-1
        if self.vi_val.get() == 1:
            p = p+1
        if self.brown_val.get() == 1:
            p = 2
       # popupmsg(("Maksimaalselt tohib juukseid pesta "+(str(p))+"x nädalas (kui see tundub vähe siis vaata kaasa antud tekst faili soovitustega)"))
        return p

    def getcalendar(self):
        
    
        self.SCOPES = "https://www.googleapis.com/auth/calendar"
        self.store = file.Storage('secret_token.json')
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)
        self.service = build('calendar', 'v3', http=self.creds.authorize(Http()))
        self.now = datetime.datetime.utcnow()
        self.week = datetime.timedelta(days=7)
        self.now_week = self.now + self.week
        self.now = datetime.datetime.utcnow().isoformat() + 'Z'
        self.now_week = self.now_week.isoformat() + "Z"
        self.events_result = self.service.events().list(calendarId='primary', timeMin=self.now,
                                                        timeMax=self.now_week, singleEvents=True,
                                                        orderBy='startTime').execute()
        a = (self.events_result.get("items", []))
        for i in a:
            print(i["start"])
        print(a)
    
    def createevent(self): #starttime endtime
        event = {
          'summary': 'Pese juukseid šampooniga.',
          'colorId': '11',
          'description': 'Nüüd on aeg, pesta juukseid šampooniga.',
          'start': {
            'dateTime': '2018-12-12T00:00:00+02:00',
            'timeZone': 'UTC+2:00',
          },
          'end': {
            'dateTime': '2018-12-13T00:00:00+02:00',
            'timeZone': 'UTC+2:00',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
          ]
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()

        """
'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'email', 'minutes': 24 * 60},
              {'method': 'popup', 'minutes': 10},
            ],
          },

          'location': '800 Howard St., San Francisco, CA 94103',
        """

    def kuhulisa(self):
        pass #Kunas pesta pmst et kuhu lisada event peaks olema maksimaalselt 36 tundi enne tähtsat eventi ja kui on trenn siis event läheb kirja kohe peale trenni


root = Tk()
gui = GUI(root)
root.mainloop()
