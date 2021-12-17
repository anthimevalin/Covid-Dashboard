# Covid-Dashboard
This Covid Dashboard application allows users to view Covid-related statistics from Public Health England as well as Covid-related news obtained from newsapi.org.

TABLE OF CONTENTS

SYSTEM REQUIREMENTS
2.USER DOCUMENTATION 2.1 INSTALLATION 2.2 FEATURES 2.2.1 DASHBOARD GUI 2.2.2 LOGGING

DEVELOPER NOTES 3.1 HIGH-LEVEL ARCHITECTURE 3.2 DESCRIPTION OF THE CODE AND HOW TO EXTEND 3.3 KNOWN BUGS AND LIMITATIONS
—————————

SYSTEM REQUIREMENTS
In order to run and use the covid, you will need the following: A computer running an internet browser application Internet connection Python interpreter

2.USER DOCUMENTATION 2.1 INSTALLATION Download the zip file. Type the following command in your terminal: python covid_dashboard.py Once the flask is running, enter in your browser the following to access the application: http://127.0.0.1:5000/index

2.2 FEATURES The Dashboard provides a GUI that allows you to obtain covid-related cases, hospitalisations, deaths and other related information and news via the Public Health England database and a commercial news service.

2.2.1 DASHBOARD GUI The Graphical User Interface allows you to create custom reports, and schedule updates for news and official health data. The updates can be delayed and/or recurring on a daily basis.

2.2.2 LOGGING The Dashboard logs information and warnings into a log file. The log file allows users and/or developers to identify problems and enable them to solve and/or debug problems encountered when running the software. The Dashboard uses built-in Python logging with WARNING levels as the default. The other levels can be set via command line option.

Show how work! The Dashboard saves the output to a log file associated with the current session and overwrites the log file each time the session is launched. Hence, if you want to save the log file you must copy it and rename it otherwise the file will be lost.

DEVELOPER NOTES
3.1 HIGH-LEVEL ARCHITECTURE 3.2 DESCRIPTION OF THE CODE AND HOW TO EXTEND 3.3 KNOWN BUGS AND LIMITATIONS
