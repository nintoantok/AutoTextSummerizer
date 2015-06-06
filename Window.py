from Tkinter import  Tk
from Tkinter import  Frame
from Tkinter import  Label
from Tkinter import  Button
from Tkinter import  Entry
from tkFileDialog import askopenfilename
from main import main
from Statistics import Statistics
import threading
import os


#This class handles the UI part completely. 
#If we are running this application with a window based system, 
#this is the entry point
#This software is developed and tested originally in Windows platform. 
#Its the reason behind using TkInter library for UI
#It may still work in Linux platform but not tested 


class Window(Tk):
    def summarize(self):
        #TODO: The following code was added display a busy dialog box while processing
        #it was not working properly. We need to revisit this
        #busyWin=BusyWin()
        #busyWin.show()
        
        #Create instance of main class. 
        #main class is the entry point for command line systems
        m=main()
        #Obtain file name from text box
        file_name=self.textbox1.get()
        if file_name!= None and file_name!="": 
            #Obtaining the important keywords by invoking summarize method of main class
            stat=m.summarize(file_name)
            
            s=self.plainTextFromStatistics(stat, file_name)
            
            #Code the show the output in 'Note pad'
            fileName=self.writeOutptToFile(s)
            osCommandString = "notepad.exe "+fileName
            os.system(osCommandString)
        #TODO Close busy dialog box
        #busyWin.close()
         
    
    def openFileBrowser(self):
        s=askopenfilename(filetypes=[("text  files",".txt"),("html files","*.htm*")])
        self.textbox1.delete(0,512)
        self.textbox1.insert(0,s)
    
    def writeOutptToFile(self,s):
        fileName="output.txt"
        fp=open(fileName,"w")
        fp.write(s)
        fp.close()
        return fileName
    #This function produces html output from Statistics object
    #TODO: to be implemented to support output as an HTML file
    def htmlFromStatistics(self,stat,file_name):
        pass
     
    #This function produces the plain text output from Statistics object
    def plainTextFromStatistics(self,stat,file_name):
        keyWords=stat.keywords
        s=""
        s=s+"SUMMARY OF FILE "+file_name+"\r\n-------------------------------------------\r\n"
        s=s+"Title\r\n--------------------\r\n"
        s=s+stat.title+"\r\n\r\n"
        s=s+"Important keywords\r\n----------------------------"
        for i in keyWords:
            s=s+"\r\n"+i
        s=s+"\r\n\r\n\r\n"
        s=s+"Most Important paragraph\r\n------------------------\r\n"
        s=s+stat.importantPara
        s=s+"\r\n------------------\r\nRating:"+str(stat.importantParaRating)
        s=s+"\r\n\r\n\r\n"
        return s
    
    
    def __init__(self):
        #Creating main window. And initializing components
        Tk.__init__(self)
        f = Frame(self, width=400, height=200)
        f.pack(expand=True)
        #Blank labels are added to make window alignment  better
        Label(f,text="").grid(row=0)
        #Blank labels are added to make window alignment  better
        Label(f,text="  ").grid(row=1,column=0)
        #Add label fileName
        Label(f,text="File Name").grid(row=1,column=1)
        #Adding text box
        self.textbox1=Entry(f,width=20)
        self.textbox1.grid(row=1,column=2)
        #Adding file Browse button. Set its even handler as openFileBrowser()
        Button(f,text="Choose File",command=self.openFileBrowser).grid(row=1,column=3)
        #Blank labels are added to make window alignment  better
        Label(f,text="  ").grid(row=1,column=4)
        #Blank labels are added to make window alignment  better
        Label(f,text="").grid(row=2)
        #Adding Summarize button. Set its even handler as summarize()
        Button(f,text="Summarize",command=self.summarize).grid(row=3,column=2)
        #Adding frame to window
        f.pack_propagate(0)
        #Set window title
        self.title("Auto Text Summarizer")
        self.mainloop()

#This is the busy window supposed to be shown while processing is in progress.
#This part is not complete
class BusyWin(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.w=Tk()
        Label(self.w,text="Processing. Please Wait").pack()
        self.w.protocol("WM_DELETE_WINDOW", self.buyWinCloseHandler)
    def buyWinCloseHandler(self):
        pass
    def show(self):
        self.start()
    def run(self):
        self.w.mainloop()
    def close(self):
        self.w.destroy()

#Entry point to the program
if __name__=="__main__": #If we are directly executing this file only
    Window();