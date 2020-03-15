# Time-Logger
This App will log the time spent on activities and store the data in a sqlite3 database.  It will also rank activities by time.
This project was created using Python 3.8 and includes the following modules:

sqlite3 (standard library)

datetime (standard library)

tkinter (PIP install)

The app works by having the user choose a category from the list box and clicking on the START button, at which time the Elapsed 
Time and Accumulated Time will begin recording.  The user can click the PAUSE button to stop the activity timing, and this is 
indicated by the PAUSE button turning red and the Pause count incrementing. At this point, the Elapsed Time and Accumulated Time 
will diverge, with the Elapsed Time continuing to accrue while the Accumulated Time remains static.  When the PAUSE Button is 
pressed again, the PAUSE button will turn grey and the Accumulted Time will begin to accrue again.  The PAUSE button can be repeatedly
pressed during a session.  To record the session time in the database, the user pauses the session a final time and then 
clicks the BANK IT! button.  This will send the data to the sqlite3 database.  To view the updated rankings based on the recently 
acquired data, the user would click the UPDATE CATEGORY RANKING button.  To start a new session, the user will click the RESET button, 
resulting in the clearing of all data and resetting of the counters. CAUTION: Pressing the RESET button will destroy the data, it will
NOT send data to the database!
