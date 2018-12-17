from __future__ import print_function
from tkinter import *
from googleapiclient.discovery import *
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import os

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
        self.root.configure(background="gray")
        self.optionsframe = LabelFrame(self.root, text="Kalkulatsiooni valikud", bd=3, bg="gray", fg="blue", font=("Helvetica 9 bold"))
        self.buttonframe = Canvas(self.root)
        root.title("HairDo")

        Label(self.root, text="HairDo", font=("Helvetica 18 bold"), fg="white",background="gray28", width=27).grid(row=0, column=0, columnspan=2)

        self.varv_val = IntVar()
        self.varv = Checkbutton(self.optionsframe, text = "Kas sul on juuksed värvitud hetkel?", variable = self.varv_val, bg="gray")
        self.varv.grid(row=0, column = 0, sticky=W)

        self.brown_val = IntVar()
        self.brown = Checkbutton(self.optionsframe, text = "Naturaalne brünett?", variable = self.brown_val, bg="gray")
        self.brown.grid(row = 1, column = 0, sticky=W)

        self.kuiv_val = IntVar()
        self.kuiv = Checkbutton(self.optionsframe, text="Kas sul on kuivad juuksed", variable=self.kuiv_val, bg="gray")
        self.kuiv.grid(row = 2, column = 0, sticky=W)

        self.vi_val = IntVar()
        self.vi = Checkbutton(self.optionsframe, text = "Kas sul on tihedad juuksed või sul on lokid?", variable=self.vi_val, bg="gray")
        self.vi.grid(row=3, column = 0,sticky=W)

        self.optionsframe.grid(row=1, column=0)
        
        self.sub = Button(self.buttonframe, text="Logi sisse", width=12, command= self.getcalendar, fg="white", bg="gray28", font=("Helvetica 9 bold"))
        self.sub.grid(row=0,column = 0)

        Button(self.buttonframe, text="Logi välja", width=12, command=self.rm_cred, fg="white", bg="gray28", font=("Helvetica 9 bold")).grid(row=1, column=0)

        Button(self.buttonframe, text="Lisa eventid", width=12,command=self.kuhulisa_nonmain, fg="white", bg="gray28", font=("Helvetica 9 bold")).grid(row=2, column=0)

        self.buttonframe.grid(row=1, column=1)

        Label(text="NB! Sa pead ennem sisse logima, kui evente üritad lisada!", bg="gray").grid(row=2, column=0, columnspan=2)
        
    def getcalendar(self):
        
        self.pikkus = self.kalk()
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
        self.sorted_dic_events = {}
        colors = self.service.colors().get().execute()
        ac = []
        ab = []
        for i in a:
            if i["colorId"] == '3':
                ac.append(i["start"]["dateTime"][0:10])
                self.sorted_dic_events["main_event"] = ac
            if i["colorId"] == '2':
                ab.append(i["end"]["dateTime"][0:10])
                self.sorted_dic_events["trenn"] = ab

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

    def createevent(self, start_time, end_time): #starttime endtime 2015-05-28T09:00:00-07:00
        event = {
          'summary': 'Pese juukseid šampooniga.',
          'colorId': '11',
          'description': 'Nüüd on aeg, pesta juukseid šampooniga.',
          'start': {
            'dateTime': start_time,
            'timeZone': 'UTC+2:00',
          },
          'end': {
            'dateTime': end_time,
            'timeZone': 'UTC+2:00',
          },
          'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
          ]
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()


    def kuhulisa(self):
        pass #Kunas pesta pmst et kuhu lisada event peaks olema maksimaalselt 36 tundi enne tähtsat eventi ja kui on trenn siis event läheb kirja kohe peale trenni
        """if main_üritus-trenn_aeg <= 36h:
            return trenn_aeg_end
        elif main_üritus-trenn_aeg > 36h:
            #Pesta pigem 12h enne ürituse algust
            if main_üritus_start - 12h == "clear":
                return main_üritus_start -12"""

    def kuhulisa_nonmain(self):
        self.trennide_arv = len(self.sorted_dic_events["trenn"])
        self.event_starts = []
        self.event_ends = []
        if self.trennide_arv == self.pikkus:
            for item in self.sorted_dic_events["trenn"]:
                self.event_starts.append(item+"T00:00:00+02:00")
                date2 = datetime.datetime.strptime(item,"%Y-%m-%d")
                uus_date2 = date2 + datetime.timedelta(days=1)
                uuem_date2 = uus_date2.strftime("%Y-%m-%dT00:00:00+02:00")
                self.event_ends.append(uuem_date2)
        elif self.trennide_arv < self.pikkus:
            self.vahe = self.pikkus-self.trennide_arv
            for i in range(1,self.vahe+1):
                asdf = self.sorted_dic_events["trenn"][-i]
                date = datetime.datetime.strptime(asdf,"%Y-%m-%d")
                uus_date = date + datetime.timedelta(days=3)
                uus_date3 = uus_date + datetime.timedelta(days=1)
                uuem_date = uus_date.strftime("%Y-%m-%dT00:00:00+02:00")
                uuem_date3 = uus_date3.strftime("%Y-%m-%dT00:00:00+02:00")
                self.event_starts.append(uuem_date)
                self.event_ends.append(uuem_date3)
            for item in self.sorted_dic_events["trenn"]:
                self.event_starts.append(item+"T00:00:00+02:00")
                date4 = datetime.datetime.strptime(item, "%Y-%m-%d")
                uus_date4 = date4 + datetime.timedelta(days=1)
                uuem_date4 = uus_date4.strftime("%Y-%m-%dT00:00:00+02:00")
                self.event_ends.append(uuem_date4)
        print(self.event_starts)
        print(self.event_ends)
        for i in range(0, len(self.event_starts)):
            self.createevent(self.event_starts[i], self.event_ends[i])

    def rm_cred(self):
        """
        try:
            os.remove("credentials.json")
        except:
            print("No file such as credentials.json!")
            """
        try:
            os.remove("secret_token.json")
        except:
            print("No file such as secret_token.json!")




root = Tk()
gui = GUI(root)
root.mainloop()
