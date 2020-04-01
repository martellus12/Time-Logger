#############################################################################################
#                                                                                           #
#   To be added:    Loading of Topics from Database                                          #
#                   Break Tasks into Functions                                              #
#                                                                                           #
#############################################################################################

import tkinter as tk
from tkinter import messagebox as mb
from tkinter import font
import datetime
import sqlite3
import pytimeparse # From WildWilhelm on GitHub to convert strings of accum and elapsed times to integer seconds
import operator #For sorting the Dictionary based on Subject/Accumulated times

WIDTH = 400
HEIGHT = 750
END = 1000
INSERT = 0

state = 0
pause_count = 0


###   Define Functions   ###############################################################################

def btn_click(choice):
    
    """ This function will populated the Time boxes and enable/disable function buttons depending on the current
        state of the logger.  """
    
    global state
    global pause_count
    global accum_time
    global new_start
    global starttime
    global topic
    global stoptime
    global stop_timing
    global table_state


    
    if subjectlistBox.curselection():  #The process will not start until a subject is chosen from the listbox
        if choice == 'Start':
            starttime = datetime.datetime.now()
            entStart.delete(0,END)
            entStart.insert(0, datetime.datetime.strftime(starttime, '%T'))
            btnStart.config(state = tk.DISABLED)
            btnPause.config(state = tk.NORMAL)
            btnBank.config(state = tk.DISABLED)
            btnReset.config(state = tk.DISABLED)


            
        elif choice == 'Pause':
            stop_timing = datetime.datetime.now()
            entStop.delete(0, END)
            entStop.insert(0, datetime.datetime.strftime(stop_timing, '%T'))
            if state == 0:                          #if this is the first pause
                btnPause.config(bg = 'red')
                if pause_count == 0:                
                    accum_time = stop_timing - starttime
                    pause_count += 1
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
            
            #Reset the Entry Fields:
            entStop.delete(0, END)
            entStart.delete(0,END)
            entElapsedTime.delete(0,END)
            entAccumTime.delete(0,END)
            entPauses.delete(0,END)
            #Reset the Pause Count
            pause_count = 0
                           

        if choice == 'Bank':
            pause_count -= 1 #adjust number of pauses before entering the data to exclude final pause B4 banking time
            commit_date = datetime.date.today()
            subject = subjectlistBox.get(tk.ACTIVE)
            time_started = starttime.strftime('%H:%M:%S')
            time_stopped = stop_timing.strftime('%H:%M:%S')
            accumulated_time = entAccumTime.get()[0:7] #because it's a string
            elapsed_time = entElapsedTime.get()[0:7]   # ditto
            
            conn = sqlite3.connect('subject_time.db')
            c = conn.cursor()       
            c.execute("CREATE TABLE IF NOT EXISTS subject_time(date TEXT, subject TEXT, pauses INTEGER, start_time TEXT, end_time TEXT, accumulated_time, elapsed_time TEXT)")
            
            c.execute("INSERT INTO subject_time(date, subject, pauses, start_time, end_time, accumulated_time, elapsed_time) VALUES(?,?,?,?,?,?,?)",
                      (commit_date,subject,pause_count, time_started, time_stopped, accumulated_time, elapsed_time))
            conn.commit()
            c.close()
            conn.close()
            btn_click('Reset')    
            
    else:
        mb.showwarning(title='Please Select Topic', message = 'Please select a topic before starting')
        
        

def get_rank():
    """This function queries the Database, accumulates the logged time spent on a subject, and
        creates a dictionary based on the results.  The dictionary is then coverted to a list for ranking
        the subjects according to time, with the most studied subject first on the list.  Then, the results
        written to the entry boxes.  """
    
    conn = sqlite3.connect('subject_time.db')
    c = conn.cursor()
    c.execute("SELECT subject, accumulated_time FROM subject_time")
    dat = c.fetchall()
    data_dict = {}
    for  tup in(dat): #Create a Dictionary with the accumulated time converted to seconds(lots of headache, don't ask)

        if tup[0] not in data_dict:
            data_dict[tup[0]] = pytimeparse.parse(tup[1])
        else:
            data_dict[tup[0]] = data_dict[tup[0]] + pytimeparse.parse(tup[1])

    sorted_items = sorted(data_dict.items(), key = operator.itemgetter(1)) #Generate a list sorted by accum time
    sorted_items.reverse() #reverse the list so that the most accumulated time is first on the list
    
     ################################  This is where we begin to populate the Rank Boxes   ####################
             # It's not great code, but it works.  I have to do this because the entry boxes are not indexed and
             # there is no way to populate them using a FOR loop in Tkinter. If the number of subjects in the listbox
             # were to increase, This double-if loop will need to be expanded.  I will revisit this someday to optimize it.
             
    num1 = 1
    print(num1)
    while num1 <= len(sorted_items):
        print('num1 is: {}, while len(sorted_items) is: {}'.format(num1, len(sorted_items)))
        if num1 == 1:
            entRank1.delete(0,END)
            entRank1Time.delete(0, END)
            entRank1.insert(0, sorted_items[0][0])
            entRank1Time.insert(0, datetime.timedelta(seconds = sorted_items[0][1])) # datetime for converting seconds to H:M:S
            num1 += 1
            print(num1)
            
        elif num1 == 2:
            entRank2.delete(0,END)
            entRank2Time.delete(0, END)
            entRank2.insert(0, sorted_items[1][0])
            entRank2Time.insert(0, datetime.timedelta(seconds = sorted_items[1][1]))
            num1 += 1
            print(num1)
        elif num1 == 3:
            entRank3.delete(0,END)
            entRank3Time.delete(0, END)
            entRank3.insert(0, sorted_items[2][0])
            entRank3Time.insert(0, datetime.timedelta(seconds = sorted_items[2][1]))
            num1 += 1
            print(num1)
        elif num1 == 4:
            entRank4.delete(0,END)
            entRank4Time.delete(0, END)
            entRank4.insert(0, sorted_items[3][0])
            entRank4Time.insert(0, datetime.timedelta(seconds = sorted_items[3][1]))
            num1 += 1
            print(num1)
        elif num1 == 5:
            entRank5.delete(0,END)
            entRank5Time.delete(0, END)
            entRank5.insert(0, sorted_items[4][0]) ##########This is where the problem starts
            entRank5Time.insert(0, datetime.timedelta(seconds = sorted_items[4][1]))
            num1 += 1
            print(num1)
        elif num1 == 6:
            entRank6.delete(0,END)
            entRank6Time.delete(0, END)
            entRank6.insert(0, sorted_items[5][0])
            entRank6Time.insert(0, datetime.timedelta(seconds = sorted_items[5][1]))
            num1 += 1
        elif num1 == 7:
            entRank7.delete(0,END)
            entRank7Time.delete(0, END)
            entRank7.insert(0, sorted_items[6][0])
            entRank7Time.insert(0, datetime.timedelta(seconds = sorted_items[6][1]))
            num1 += 1
        elif num1 == 8:
            entRank8.delete(0,END)
            entRank8Time.delete(0, END)
            entRank8.insert(0, sorted_items[7][0])
            entRank8Time.insert(0, datetime.timedelta(seconds = sorted_items[7][1]))
            num1 += 1
        elif num1 == 9:
            entRank9.delete(0,END)
            entRank9Time.delete(0, END)
            entRank9.insert(0, sorted_items[8][0])
            entRank9Time.insert(0, datetime.timedelta(seconds = sorted_items[8][1]))
            num1 += 1
        elif num1 == 10:
            entRank10.delete(0,END)
            entRank10Time.delete(0, END)
            entRank10.insert(0, sorted_items[9][0])
            entRank10Time.insert(0, datetime.timedelta(seconds = sorted_items[9][1]))
            num1 += 1

def change_topic(do):
    
    if do == 'add':
        if subjectlistBox.size() < 10:
            if entTopic.get():
                subjectlistBox.insert(END, entTopic.get())
                entTopic.delete(0,END)
            else:
                mb.showwarning(title='Blank Topic', message = 'No Topic to Add, Please Enter a Topic')
        else:
            mb.showwarning(title='List Box Full', message = 'The List is Full, Please Delete an Item From the List Before Adding Items')
            

    elif do == 'delete':
        if subjectlistBox.curselection():
            deleted_topic = subjectlistBox.curselection()  #This is the index of the topic to be deleted
            deleted_text = subjectlistBox.get(deleted_topic) #This is the text referred to by the index
            subjectlistBox.delete(deleted_topic)
            mb.showinfo(title = 'Topic Deleted', message = 'Deleted Topic: {}'.format(deleted_text))
        else:
            mb.showwarning(title='Blank Topic', message = 'No Topic to Delete, Please Select a Topic to Delete')
                

    
        

  


            
################ SPARE PARTS ROOM CODE  #####################################################################     
        #print(item[0],datetime.datetime.strptime(item[1],'%H:%M:%S').time())  #THIS WORKS!!!!!     
        #print(datetime.time(*map(int, item[1].split(':')))) #This works too!!!!!   
        #time = datetime.datetime.datetime(item[1],'%H:%M:%S').time()

##        data_dict.setdefault(tup[0],0)
##        time = pytimeparse.parse(tup[1])
##        data_dict[tup] = data_dict[tup] +time

            #print(tk.font.families())
            #..font = ('Modern', 30)

############################################################################################################       


timeLog = tk.Tk() #Main Body
timeLog.title('Time Logger')

canvas = tk.Canvas(timeLog, height = HEIGHT, width = WIDTH)
canvas.pack()



############# FRAMES ####################################################

workFrame = tk.Frame(timeLog, bg = 'blue', bd = 5)
workFrame.place(height = 260, width = 400, relx = 0, rely = 0)

reportFrame = tk.Frame(timeLog, bd = 5)
reportFrame.place(height = 500, width = 400, x = 0, y = 260)

############ LABELS #####################################################

lblTopic = tk.Label(workFrame, text = 'Topic (Choose One)', anchor = tk.W)
lblTopic.place(relx = 0, rely = 0, height = 30, width = 128)

lblStart = tk.Label(workFrame, text = 'Start Time', anchor = tk.E)
lblStart.place(relx = 0.5, rely = 0, height = 30, width = 80)

lblStop = tk.Label(workFrame, text = 'Stop Time', anchor = tk.E)
lblStop.place(relx = 0.5, rely = 0.15, height = 30, width = 80)

lblElapsed =tk.Label(workFrame, text = 'Elapsed Time', anchor = tk.E)
lblElapsed.place(relx = 0.5, rely = 0.3, height = 30, width = 80)

lblAccum =tk.Label(workFrame, text = 'Accum. Time', anchor = tk.E)
lblAccum.place(relx = 0.5, rely = 0.45, height = 30, width = 80)


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
entStart.place(height = 30, width = 120, relx = 0.7, rely = 0)

entStop = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entStop.place(height = 30, width = 120, relx = 0.7, rely = 0.15)

entElapsedTime = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entElapsedTime.place(height = 30, width = 120, relx = 0.7, rely = 0.3)

entAccumTime = tk.Entry(workFrame, bd = 3, justify = tk.CENTER)
entAccumTime.place(height = 30, width = 120, relx = 0.7, rely = 0.45)

entPauses = tk.Entry(workFrame, justify = 'center')                               
entPauses.place(relx = 0.61, rely = 0.6, height = 20, width = 32)     
lblPauses = tk.Label(workFrame, text = 'Pauses')                                  
lblPauses.place(relx = 0.5, rely = 0.6, height = 20, width = 40)

entTopic = tk.Entry(workFrame, bd = 3, justify = tk.LEFT)
entTopic.place(relx = 0, rely = 0.6, height = 30, width = 128)



entRank1 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank1Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank2 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank2Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank3 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank3Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank4 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank4Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank5 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank5Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank6 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank6Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank7 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank7Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank8 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank8Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank9 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank9Time = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank10 = tk.Entry(reportFrame, bd = 3, justify = 'center')
entRank10Time = tk.Entry(reportFrame, bd = 3, justify = 'center')

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
btnStart.place(height = 30, width = 80, relx = 0, rely = 0.85)

btnPause = tk.Button(workFrame, text = 'Pause/Res', command = (lambda: btn_click('Pause')))
btnPause.place(height = 30, width = 75, relx = 0.23, rely = 0.85)

btnReset = tk.Button(workFrame, text = 'Reset', command = (lambda: btn_click('Reset')))
btnReset.place(height = 30, width = 75, relx = 0.45, rely = 0.85)

btnBank = tk.Button(workFrame, text = 'Bank It!', command = (lambda: btn_click('Bank')))
btnBank.place(height = 30, width = 120, relx = 0.7, rely = 0.85)

btnRank = tk.Button(reportFrame, text = 'Update Category Ranking', bd = 3, command = (lambda: get_rank()))
btnRank.place(relx = 0.25, y = 0, width = 200, height = 40)

btnAddTopic = tk.Button(workFrame, text = 'Add Topic', bd = 2, command = (lambda: change_topic('add')))
btnAddTopic.place(height = 20, width = 64, relx = 0, rely = .73)

btnDelTopic = tk.Button(workFrame, text = 'Delete Topic', bd = 2, command = (lambda: change_topic('delete')))
btnDelTopic.place(height = 20, width = 80, relx = 0, rely = .48)

#Set buttons initial state
btnPause.config(state = tk.DISABLED)
btnReset.config(state = tk.DISABLED)
btnBank.config(state = tk.DISABLED)

############ LISTBOXES ##################################################
""" NOTE: This code can only handle 10 subjects in the list box.
if more subjects are needed, the number of Rank boxes and the
code that populates them must be expanded."""

subjectlistBox = tk.Listbox(workFrame)
subjectlistBox.place(height = 85, width = 128, x = 0, y = 33)

#List Box Items:
subjectlistBox.insert(1, 'Python')
subjectlistBox.insert(2, 'Javascript')
subjectlistBox.insert(3, 'Django')
subjectlistBox.insert(4, 'PHP')
subjectlistBox.insert(5, 'Server')
subjectlistBox.insert(6, 'Linux/Bash')
subjectlistBox.insert(7, 'Tkinter')
subjectlistBox.insert(8, 'PostGres')
subjectlistBox.insert(9, 'Debugging')
subjectlistBox.insert(10, 'HTML')



timeLog.mainloop()
