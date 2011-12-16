#Clicktracker.py   
#Paul Gulley, 2011, ANi
#A small mouse-hook application for Ellie McDonald
import pythoncom, pyHook, datetime, pickle


#Options: 
DriveName = "K:" #Location of output files. also needs to be changed a few other places in the code.
Verbose = True #If true, the program will output all the click information it recieves to the console window. 
Record = False #Record at start?

DataHeader = '''<html><table><tr><th> Position </th> <th> Time </th> <th> Td </th> <th> Click in area? </th></tr>'''

class DataStore:
    def __init__(self, dname, verb, rec):
        self.clicks = ['filler']
        self.dname = dname
        self.rec = rec
        self.verb = verb
    def addclick(self, position, time):
        if len(self.clicks) != 1:
            lasttime = self.clicks[-1]['time']
            timedelta = time - lasttime
        else:
            timedelta = "N/A"
        if self.rec:
            self.clicks.append({'time':time,"pos":position,"timedelta":timedelta,"InArea":"{0}"})
        return True 
    def reportclick(self):
        #outputs data if rec is true
        if self.rec:
            if not type(self.rec) == bool:
                self.rec -= 1#For the 'next x clicks' functionality
            click = self.clicks[-1]
            if self.verb:
                print "Click \nPos:{0} \nTime:{0} \ndt:{2} \n------------ \n".format(click["pos"],click['time'],click['timedelta'])
            else:
                print '.',
            file = open('{0}/output.html'.format(self.dname),'a')
            file.write("<tr><td>{0}</td> <td>{1}</td> <td>{2}</td> <td>{3}</td></tr> \n".format(click["pos"],click["time"].time(),click["timedelta"],click["InArea"]))
            file.close()
        return True

def OnClick(event):
    #called when hook reports clicks 
    time = datetime.datetime.now()
    #loading the data manager
    livedata = open("K:/Datastore.txt", 'r')
    dat = pickle.load(livedata)
    livedata.close()
    #doing the things
    dat.addclick(event.Position, time)
    dat.reportclick()
    #clearing up mem space now that everything is done, getting rid of the data manager instance
    livedata = open("{0}/Datastore.txt".format(dat.dname),"w")
    pickle.dump(dat,livedata)
    del(dat)
    livedata.close()
    return True

def OnKey(event):
    if event.Alt:
        if event.Key == "A":
            #Start Recording switch. prompted at program start. 
            livedata = open("K:/Datastore.txt", 'r')
            dat = pickle.load(livedata)
            livedata.close()
            #doing the things
            dat.rec = True
            #clearing up mem space now that everything is done, getting rid of the data manager instance
            livedata = open("{0}/Datastore.txt".format(dat.dname),"w")
            pickle.dump(dat,livedata)
            del(dat)
            livedata.close()
            print "Recording All Clicks"
        elif event.Key == "Q":
            #Do all of the program wrap up things
            print "Quitting"
            file = open("K:/output.html","a")
            file.write("</table>")
            file.close()
            quit()
        elif event.Key == "R":
            #record only next two following clicks
            livedata = open("K:/Datastore.txt", 'r')
            dat = pickle.load(livedata)
            livedata.close()
            #doing the things
            dat.rec = 2
            #clearing up mem space now that everything is done, getting rid of the data manager instance
            livedata = open("{0}/Datastore.txt".format(dat.dname),"w")
            pickle.dump(dat,livedata)
            del(dat)
            livedata.close()
            print "Recording only the next two clicks"
    return True


#Init all the datastorage things    

dat = DataStore(dname=DriveName,verb=Verbose,rec=Record)
livedata = open("{0}/Datastore.txt".format(DriveName), 'w')
pickle.dump(dat,livedata)
livedata.close()
del(dat)
outputfile = open('{0}/output.html'.format(DriveName), 'w')
outputfile.write(DataHeader) #Data file header
outputfile.close()

#Init the hook
hm = pyHook.HookManager()
hm.SubscribeMouseLeftDown(OnClick)
hm.KeyDown = OnKey
hm.HookMouse()
hm.HookKeyboard()
# wait forever
print "Usage Guide: \n Alt-A to begin recording all clicks \n Alt-R to only record the next two clicks \n \n Pressing Alt-Q at any time will quit the program \n -------------------"
pythoncom.PumpMessages()

