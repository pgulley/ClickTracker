#checkdata.py
#Paul Gulley, 2011, ANi
#Part two of the mouse hooker for Ellie McDonald
import pythoncom, pyHook, datetime, pickle
DRIVENAME = "K:"
DATAFILE = "{0}/output.html".format(DRIVENAME)
DATAHEADER ='''<html><table><tr><th> Position </th> <th> Time </th> <th> Td </th> <th> Click in area? </th></tr>'''
class DataStore:
    def __init__(self, loc):
        self.posrec = False
        self.pos1 = [False,False]
        self.pos2 = [False,False]
        self.loc = loc
    def addclick(self, position, time):
        print self.posrec
        if self.posrec == 4:
            self.pos1[0] = position
            print "2: click the bottom-right extremity of first area"
            self.posrec -= 1
            return
        elif self.posrec == 3:
            self.pos1[1] = position
            print "3: click the top-left extremity of second area"
            self.posrec -= 1
            return             
        elif self.posrec == 2:
            self.pos2[0] = position
            print "4: click the bottom-right extremity of second area"
            self.posrec -= 1
            return 
        elif self.posrec == 1:
            self.pos2[1] = position
            print 'You are now done setting the click areas. '
            self.posrec = False
            self.reportclick()
        return True 
    def reportclick(self):
        OFile = open(self.loc,'r')
        NFile = open("K:/finaloutput.html",'a')
        for line in OFile:
            if line[2] == 'r':
                position = line[7:20].strip('<>td/()').split(',')
				
                print position
                InArea = False
                if self.pos1[0][0] < position[0] <self.pos1[1][0] and self.pos1[0][1] < position[1] < self.pos1[1][1]:
                    InArea = True
                if self.pos2[0][0] < position[0] <self.pos2[1][0] and self.pos2[0][1] < position[1] < self.pos2[1][1]:
                    InArea = True
                NFile.write(line.format(InArea))

    
        
def OnClick(event):
    #called when hook reports clicks 
    time = datetime.datetime.now()
    #loading the data manager
    livedata = open("K:/analysis.txt", 'r')
    dat = pickle.load(livedata)
    livedata.close()
    #doing the things
    dat.addclick(event.Position, time)
    #clearing up mem space now that everything is done, getting rid of the data manager instance
    livedata = open("K:/analysis.txt","w")
    pickle.dump(dat,livedata)
    del(dat)
    livedata.close()
    return True

def OnKey(event):
    if event.Alt:
        if event.Key == "Q":
            #Do all of the program wrap up things
            print "Quitting"
            file = open("K:/output.html","a")
            file.write("</table>")
            file.close()
            quit()
        elif event.Key == "S":
            livedata = open("K:/analysis.txt", 'r')
            dat = pickle.load(livedata)
            livedata.close()
            #doing the things
            dat.posrec = 4
            #clearing up mem space now that everything is done, getting rid of the data manager instance
            livedata = open("K:/analysis.txt","w")
            pickle.dump(dat,livedata)
            del(dat)
            livedata.close()
            print "Setting click areas. \n1: click the top-left extremity of the first area"
    return True


#Init all the datastorage things    

dat = DataStore(loc=DATAFILE)
livedata = open('{0}/analysis.txt'.format(DRIVENAME), 'w')
pickle.dump(dat,livedata)
livedata.close()
del(dat)
outputfile = open('{0}/finaloutput.html'.format(DRIVENAME), 'w')
outputfile.write(DATAHEADER) #Data file header
outputfile.close()
#Init the hook
hm = pyHook.HookManager()
hm.SubscribeMouseLeftDown(OnClick)
hm.KeyDown = OnKey
hm.HookMouse()
hm.HookKeyboard()
# wait forever
print " Press Alt-S to begin setting click areas. \n Pressing Alt-Q at any time will quit the program \n -------------------"
pythoncom.PumpMessages()