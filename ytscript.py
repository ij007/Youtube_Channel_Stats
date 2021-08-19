import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tkinter import *


root = Tk()
root.title("Youtube Analytics by IJ")



def logout():

    #Clearing Frame
    for child in root.winfo_children():
        child.destroy()

    #removing user info
    if os.path.exists("tocken.pickle"):
        os.remove("tocken.pickle")

    button_login = Button(root, text="Login", padx=20, pady=10, command=login)
    button_login.grid(row=2, column=2)


def login():
    
    
    #Checking for tocken expiration
    for child in root.winfo_children():
        child.destroy()

    credentials = None

    if os.path.exists('tocken.pickle'):
        print("Loading credentials file")
        with open("tocken.pickle","rb") as tocken:
            credentials = pickle.load(tocken)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token :
            print("refreshing tocken")
            credentials.refresh(Request())
        else:
            print("Fetching new tocken")
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                scopes=['https://www.googleapis.com/auth/youtube.channel-memberships.creator',
                        'https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/youtube'])

            flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message='')

            credentials = flow.credentials

            with open('tocken.pickle','wb') as f:
                print("Creating fresh tocken and saving")
                pickle.dump(credentials, f)

    #Fething Data
    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.subscriptions().list(
            part="subscriberSnippet",
            mySubscribers=True
        )
    response_Sublist = request.execute()

    sublist = []

    for items in response_Sublist['items']:
        sublist.append(items['subscriberSnippet']['title'])


    request = youtube.channels().list(
            part="statistics",
            mine=True
        )

    response_Subcount = request.execute()
    subcount = (response_Subcount['items'][0]['statistics']['subscriberCount'])


    #Printing Data
    Subhead = Label(root, text="Recent subscribers : ")
    Subhead.grid(row=0, column=0)

    for i in range(len(sublist)):
        dispSub = Label(root, text=f'{sublist[i]}')
        dispSub.grid(row=i, column=1)

    subCountHead = Label(root, text="Total subscribers : ")
    subCountHead.grid(row=(len(sublist)), column=0)

    subCountLabel = Label(root, text=subcount)
    subCountLabel.grid(row=(len(sublist)), column=1)

    #Logout Button
    button_logout = Button(root, text="Logout", padx=20, pady=10, command=logout)
    button_logout.grid(row=(len(sublist))+1, column=2)



#Entry Point
if os.path.exists("tocken.pickle"):

    login()         #If login data is saved


else:

    #Fresh Login
    button_login = Button(root, text="Login", padx=20, pady=10, command=login)
    button_login.grid(row=2, column=2)



root.mainloop()




