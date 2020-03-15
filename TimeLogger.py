import tkinter as tk
from tkinter import messagebox as mb
from tkinter import font
import datetime

#print(tk.font.families())
#..font = ('Modern', 30)

WIDTH = 400
HEIGHT = 700
END = 1000
INSERT = 0



state = 0
pause_count = 0

###   Define Functions   ###############################################################################

def btn_click(choice):
    global state
    global pause_count
    global accum_time
    global new_start
    global starttime
    global topic
    global stoptime
    global totalET


    
    if subjectlistBox.curselection():
        if choice == 'Start':
            starttime = datetime.datetime.now()
            entStart.delete(0,END)
            entStart.insert(0, datetime.datetime.strftime(starttime, '%T'))
            btnStart.config(state = tk.DISABLED)
            btnPause.config(state = tk.NORMAL)


            
        elif choice == 'Pause':
            stop_timing = datetime.datetime.now()
            entStop.delete(0, END)
            entStop.insert(0, datetime.datetime.strftime(stop_timing, '%T'))
            if state == 0:                          #if this is the first pause
                btnPause.config(bg = 'red')
                if pause_count == 0:                
                    accum_time = stop_timing - starttime
                    print('First Accum Time')
                    pause_count = pause_count + 1
                    state = 1
                    entElapsedTime.delete(0,END)
                    entElapsedTime.insert(0, stop_timing - starttime)
                    entAccumTime.delete(0, END)
                    entAccumTime.insert(0, accum_time)
                    btnReset.config(state = tk.NORMAL)
                    btnBank.config(state = tk.NORMAL)
                    
                else:                               #if this is not the first pause
                    accum_interval  = stop_timing - new_start
                    accum_time = accum_time + accum_interval
                    print('Second Accum Time')
                    pause_count += 1
                    state = 1
                    entAccumTime.delete(0, END)
                    entAccumTime.insert(0, accum_time)
                    entElapsedTime.delete(0, END)
                    entElapsedTime.insert(0, stop_timing - starttime)
                    btnReset.config(state = tk.NORMAL)
                    btnBank.config(state = tk.NORMAL)
                    
                entPauses.delete(0, END)
                entPauses.insert(0, pause_count)
            else:                                   #If already in Pause state, pressing Pause 
                                                    #again will resume timing and accumulation
                    btnPause.configure(bg = '#E0E0E0')
                    new_start = datetime.datetime.now()
                    state = 0
                    btnReset.config(state = tk.DISABLED)
                    btnBank.config(state = tk.DISABLED)
                    entElapsedTime.delete(0, END)
                    entElapsedTime.insert(0, stop_timing - starttime)
                    print('should be starting accumtime')



                    
        elif choice == 'Reset':
            stoptime = datetime.datetime.now()
            topic = subjectlistBox.get(subjectlistBox.curselection())
            totalET = stoptime - starttime
            btnStart.config(state = tk.NORMAL)
            btnPause.config(state = tk.DISABLED, bg = '#E0E0E0')
            btnReset.config(state = tk.DISABLED)
            btnBank.config(state = tk.DISABLED)
            #Reset the ListBox choice:
            subjectlistBox.select_clear(0,END)
            state = 0
            
            
            
            #get the string version of start time from Start Time Box:
            #startstring = entStart.get()
            #"""now convert string to datetime object, take out the weird Jan 1 1900 part and
            #make it the current day/year/month using .replace(): (note- can't use %T format for some reason)"""
            #starttime = datetime.datetime.strptime(startstring, '%H:%M:%S').replace(stoptime.year, stoptime.month, stoptime.day)
            #print(starttime)
            #print('starttime is a {} value'.format(type(starttime)))
            print(starttime)
            print(stoptime)
            print(topic)
            print(accum_time)
            print(totalET)
            print(pause_count)
            print(subjectlistBox.get(tk.ACTIVE))################
            #Reset the Entry Fields:
            entStop.delete(0, END)
            entStart.delete(0,END)
            entElapsedTime.delete(0,END)
            entAccumTime.delete(0,END)
            entPauses.delete(0,END)
            #Reset the Pause Count
            pause_count = 0
            

            

            ###This code gets the index of the list box and uses it to determine the list item
            ## and puts it in the Accum Time entry field.  Its pretty stupid but it works
            #indx = subjectlistBox.curselection()
            #entAccumTime.delete(0,END)
            #entAccumTime.insert(0,subjectlistBox.get(indx))
                           

        if choice == 'Bank':
            pass
    else:
        mb.showwarning(title='Please Select Topic', message = 'Please select a topic before starting')
        
        

def get_rank():
    pass
    




timeLog = tk.Tk() #Main Body
timeLog.title('Time Logger')

canvas = tk.Canvas(timeLog, height = HEIGHT, width = WIDTH, bg = 'yellow')
canvas.pack()



############# FRAMES ####################################################

workFrame = tk.Frame(timeLog, bg = 'blue', bd = 5)
workFrame.place(height = 200, width = 400, relx = 0, rely = 0)

reportFrame = tk.Frame(timeLog, bg = 'red', bd = 5)
reportFrame.place(height = 500, width = 400, x = 0, y = 200)

############ LABELS #####################################################

lblTopic = tk.Label(workFrame, text = 'Topic', anchor = tk.W)
lblTopic.place(relx = 0, rely = 0, relheight = 0.15
               , relwidth = 0.25)

lblStart = tk.Label(workFrame, text = 'Start Time', anchor = tk.E)
lblStart.place(relx = 0.5, rely = 0, relheight = 0.15, relwidth = 0.2)

lblStop = tk.Label(workFrame, text = 'Stop Time', anchor = tk.E)
lblStop.place(relx = 0.5, rely = 0.2, relheight = 0.15, relwidth = 0.2)

lblElapsed =tk.Label(workFrame, text = 'Elapsed Time', anchor = tk.E)
lblElapsed.place(relx = 0.5, rely = 0.4, relheight = 0.15, relwidth = 0.2)

lblAccum =tk.Label(workFrame, text = 'Accum. Time', anchor = tk.E)
lblAccum.place(relx = 0.5, rely = 0.6, relheight = 0.15, relwidth = 0.2)


lbl1 = tk.Label(reportFrame, text = '#1')
lbl1Time = tk.Label(reportFrame, text = 'Time: ')
lbl2 = tk.Label(reportFrame, text = '#2')
lbl2Time = tk.Label(reportFrame, text = 'Time: ')
lbl3 = tk.Label(reportFrame, text = '#3')
lbl3Time = tk.Label(reportFrame, text = 'Time: ')
lbl4 = tk.Label(reportFrame, text = '#4')
lbl4Time = tk.Label(reportFrame, text = 'Time: ')
lbl5 = tk.Label(reportFrame, text = '#5')
lbl5Time = tk.Label(reportFrame, text = 'Time: ')
lbl6 = tk.Label(reportFrame, text = '#6')
lbl6Time = tk.Label(reportFrame, text = 'Time: ')
lbl7 = tk.Label(reportFrame, text = '#7')
lbl7Time = tk.Label(reportFrame, text = 'Time: ')
lbl8 = tk.Label(reportFrame, text = '#8')
lbl8Time = tk.Label(reportFrame, text = 'Time: ')
lbl9 = tk.Label(reportFrame, text = '#9')
lbl9Time = tk.Label(reportFrame, text = 'Time: ')
lbl10 = tk.Label(reportFrame, text = '#10')
lbl10Time = tk.Label(reportFrame, text = 'Time: ')

lbl1.place(relx = 0, rely = 0.1, width = 25, height = 30)
lbl1Time.place(relx = 0.5, rely = 0.1, width = 35, height = 30)
lbl2.place(relx = 0, rely = 0.19, width = 25, height = 30)
lbl2Time.place(relx = 0.5, rely = 0.19, width = 35, height = 30)
lbl3.place(relx = 0, rely = 0.28, width = 25, height = 30)
lbl3Time.place(relx = 0.5, rely = 0.28, width = 35, height = 30)
lbl4.place(relx = 0, rely = 0.37, width = 25, height = 30)
lbl4Time.place(relx = 0.5, rely = 0.37, width = 35, height = 30)
lbl5.place(relx = 0, rely = 0.46, width = 25, height = 30)
lbl5Time.place(relx = 0.5, rely = 0.46, width = 35, height = 30)
lbl6.place(relx = 0, rely = 0.55, width = 25, height = 30)
lbl6Time.place(relx = 0.5, rely = 0.55, width = 35, height = 30)
lbl7.place(relx = 0, rely = 0.64, width = 25, height = 30)
lbl7Time.place(relx = 0.5, rely = 0.64, width = 35, height = 30)
lbl8.place(relx = 0, rely = 0.73, width = 25, height = 30)
lbl8Time.place(relx = 0.5, rely = 0.73, width = 35, height = 30)
lbl9.place(relx = 0, rely = 0.82, width = 25, height = 30)
lbl9Time.place(relx = 0.5, rely = 0.82, width = 35, height = 30)
lbl10.place(relx = 0, rely = 0.91, width = 25, height = 30)
lbl10Time.place(relx = 0.5, rely = 0.91, width = 35, height = 30)


########### ENTRY FIELDS ################################################

entStart = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entStart.place(relheight = 0.15, relwidth = 0.3, relx = 0.7, rely = 0)

entStop = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entStop.place(relheight = 0.15, relwidth = 0.3, relx = 0.7, rely = 0.20)

entElapsedTime = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entElapsedTime.place(relheight = 0.15, relwidth = 0.3, relx = 0.7, rely = 0.4)

entAccumTime = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entAccumTime.place(relheight = 0.15, relwidth = 0.3, relx = 0.7, rely = 0.6)

entPauses = tk.Entry(workFrame, justify = 'center')                               
entPauses.place(relx = 0.1, rely = 0.7, relheight = 0.1, relwidth = 0.1)     
lblPauses = tk.Label(workFrame, text = 'Pauses')                                  
lblPauses.place(relx = 0, rely = 0.7, relheight = 0.1, relwidth = 0.1)

entRank1 = tk.Entry(reportFrame, bd = 3)
entRank1Time = tk.Entry(reportFrame, bd = 3)
entRank2 = tk.Entry(reportFrame, bd = 3)
entRank2Time = tk.Entry(reportFrame, bd = 3)
entRank3 = tk.Entry(reportFrame, bd = 3)
entRank3Time = tk.Entry(reportFrame, bd = 3)
entRank4 = tk.Entry(reportFrame, bd = 3)
entRank4Time = tk.Entry(reportFrame, bd = 3)
entRank5 = tk.Entry(reportFrame, bd = 3)
entRank5Time = tk.Entry(reportFrame, bd = 3)
entRank6 = tk.Entry(reportFrame, bd = 3)
entRank6Time = tk.Entry(reportFrame, bd = 3)
entRank7 = tk.Entry(reportFrame, bd = 3)
entRank7Time = tk.Entry(reportFrame, bd = 3)
entRank8 = tk.Entry(reportFrame, bd = 3)
entRank8Time = tk.Entry(reportFrame, bd = 3)
entRank9 = tk.Entry(reportFrame, bd = 3)
entRank9Time = tk.Entry(reportFrame, bd = 3)
entRank10 = tk.Entry(reportFrame, bd = 3)
entRank10Time = tk.Entry(reportFrame, bd = 3)

entRank1.place(height  = 30, width = 100, relx = 0.1, rely = 0.1)
entRank1Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.1)
entRank2.place(height  = 30, width = 100, relx = 0.1, rely = 0.19)
entRank2Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.19)
entRank3.place(height  = 30, width = 100, relx = 0.1, rely = 0.28)
entRank3Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.28)
entRank4.place(height  = 30, width = 100, relx = 0.1, rely = 0.37)
entRank4Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.37)
entRank5.place(height  = 30, width = 100, relx = 0.1, rely = 0.46)
entRank5Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.46)
entRank6.place(height  = 30, width = 100, relx = 0.1, rely = 0.55)
entRank6Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.55)
entRank7.place(height  = 30, width = 100, relx = 0.1, rely = 0.64)
entRank7Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.64)
entRank8.place(height  = 30, width = 100, relx = 0.1, rely = 0.73)
entRank8Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.73)
entRank9.place(height  = 30, width = 100, relx = 0.1, rely = 0.82)
entRank9Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.82)
entRank10.place(height = 30, width = 100, relx = 0.1, rely = 0.91)
entRank10Time.place(height  = 30, width = 150, relx = 0.6, rely = 0.91)

############ BUTTONS ####################################################

btnStart = tk.Button(workFrame, text = 'Time Start', command = (lambda: btn_click('Start')))
btnStart.place(relheight = 0.15, relwidth = 0.2, relx = 0, rely = 0.85)

btnPause = tk.Button(workFrame, text = 'Pause/Res', command = (lambda: btn_click('Pause')))
btnPause.place(relheight = 0.15, relwidth = 0.15, relx = 0.25, rely = 0.85)

btnReset = tk.Button(workFrame, text = 'Reset', command = (lambda: btn_click('Reset')))
btnReset.place(relheight = 0.15, relwidth = 0.15, relx = 0.45, rely = 0.85)

btnBank = tk.Button(workFrame, text = 'Bank It!', command = (lambda: btn_click('Bank')))
btnBank.place(relheight = 0.15, relwidth = 0.3, relx = 0.7, rely = 0.85)

btnRank = tk.Button(reportFrame, text = 'Update Category Ranking', bd = 3, command = (lambda: get_rank()))
btnRank.place(relx = 0.25, y = 0, width = 200, height = 40)

############ LISTBOXES ##################################################

subjectlistBox = tk.Listbox(workFrame)
subjectlistBox.place(relheight = 0.4, relwidth = 0.32, relx = 0, rely = 0.2)

#List Box Items:
subjectlistBox.insert(1, 'Python')
subjectlistBox.insert(2, 'Javascript')
subjectlistBox.insert(3, 'Django')
subjectlistBox.insert(4, 'PHP')
subjectlistBox.insert(5, 'Server')
subjectlistBox.insert(6, 'Linux/Bash')
subjectlistBox.insert(7, 'Tkinter')
subjectlistBox.insert(8, 'React')
subjectlistBox.insert(9, 'PostGres')



timeLog.mainloop()
