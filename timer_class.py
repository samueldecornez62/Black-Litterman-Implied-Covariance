'''
Samuel Decornez
2024-07-19
Exercise 2.1.1 to 2.1.5.
'''


'''================================================================================
Main Program:
Create a Timer class, with start and end method. 
Display appropriate error messages, and add a method to retrieve last timer result.
Note: This function only contains the Timer class. 
Any testing and calling it will be in the main file in this section's folder. 
================================================================================'''


#Part a and b: Create Timer class
#Create method (functions) that our object will perform
#One for starting the timer, another for ending the timer
#Static or class decorator not necessary

#Part c: edits made to initialization function __init__ (adding running),
# with errors added to start and end methods

#Part d: configure timer involves changing the end method to display units.
# Also, define a method to set units after initializing a new units variable in __init__

#Part e: add a new initialized variable that holds None.
# Define a new method to store this value, and output it on request in main()




#Import time package
import time

#Create the timer class
#Use object as only input
class Timer(object):
    #First, initialization function (this will get updated as we progress through the question).
    # A summary is provided above this class definition
    def __init__(self):
        #We initialize start and end to None to correctly handle errors of timer already running
        self._start = None
        self._end = None
        #We initialize running to false to check in the loop coming in below methods (part c)
        self._running = False
        #Also want to initialize units in main function, default to seconds (part d, units)
        self._unit = 'seconds'
        #Part e, add new variable
        self._last_timer_result = None



    #Add start method
    def start(self):
        #Check if the timer is running and give error if this is called again while already running
        #Already running corresponds to "== True" (not necessary)
        if self._running:
            print('[ERROR]. Timer is already running.')
            # raise RuntimeError('Timer already running')
        #Record start time
        else:
            print('Starting timer.')
            self._start = time.time()
            #Set running status to true; if called again the runtime error is raised
            self._running = True

    #Add end method
    def end(self):
        #Check if timer is running and give error if it is not
        if not self._running:
            #Print error message
            print('[ERROR]. No timer currently running to end. ')
            # raise RuntimeError('Timer not running')

        #To handle error message correctly, the remaining written code in this method
        # is wrapped in an "else" statement
        else:
            #Record ending time
            print('Ending timer.')
            self._end = time.time()
            #Calculate elapsed time from both methods as difference between methods, and print message to user
            elapsed_time = self._end - self._start
            #To retrieve last time result in last_timer_result method, store this elapsed_time
            self._last_timer_result = elapsed_time
            # Creating a new timer instance with t = Timer() (see main, where functions are called)
            # will call __init__ and set running to false,
            # but if a new timer is not initialized we can run into problems.
            # Therefore, hard set running status to False here in end method
            self._running = False

            #Remove following line when configuring timer for appropriate units; units handled directly below
            # print('Total elapsed time: {} seconds\n'.format(elapsed_time))

            #Configure timer to display correct units
            if self._unit == 'seconds':
                print('Total elapsed time: {} seconds\n'.format(elapsed_time))
            elif self._unit == 'minutes':
                print('Total elapsed time: {} minutes\n'.format(elapsed_time/60))
            elif self._unit == 'hours':
                print('Total elapsed time: {} hours\n'.format(elapsed_time/3600))

    def set_unit(self, unit):
        #Make sure unit is a valid one
        if unit in ['seconds', 'minutes', 'hours']:
            self._unit = unit
        #Move value error from end method to this one
        else:
            #Print error message
            print('[ERROR]. Invalid unit. Please select seconds, minutes, or hours.')
            # raise ValueError('Unit must be either seconds or minutes or hours')



    #Define method to retrieve last timer result
    def last_timer_result(self):
        #Make sure there is some last result to report (i.e. raise error if timer has not been used)
        if self._last_timer_result is None:
            #Print error message
            print('[ERROR]. Timer has not run. No last result to report. ')
            # raise RuntimeError('No last timer result')
        #Now if there is a result to store, store it
        last_timer_value = self._last_timer_result
        #Now take code from above end method to display units correctly
        if self._unit == 'seconds':
            return last_timer_value
        elif self._unit == 'minutes':
            return last_timer_value/60
        else:
            return last_timer_value/3600

