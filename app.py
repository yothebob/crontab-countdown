import os
from datetime import datetime, date
import math
import calendar

class CronRunTime:

    def __init__(self,filename,filepath):
        self.filepath = filepath #="/var/spool/cron"
        self.filename = filename



    def retrieve_crontab_tasks(self):
        '''
        input : filepath (str)
                filename (str)

        output : (list)

        Opens chrontab file according to file name/path and returns all the chrontab commands
        '''

        #os.chdir(self.filepath)
        f = open(self.filename,"r")
        return [line for line in f if "*" in line and "#" not in line]



    def extract_crontab_elements(self,task,time_list=[]):
        '''
        Input : task (str)
                time_list (list)

        Output : time_list (list)
                popped_job (str)

        a function that takes in a chrontab command and returns an array of
        the times [min,hour,dom,month,dow] and the remainder of the command string
        '''
        popped_job = ""
        job_time = ""

        for number in range(len(task)):
            if task[number] == " ":
                if len(job_time) > 0:
                    popped_job = task[number:]
                    break
            else:
                job_time += task[number]
        time_list.append(job_time)

        if len(time_list) >=5:
            return time_list,popped_job
        else:
            return self.extract_crontab_elements(popped_job,time_list)



    def create_functions_dictionary(self):
        '''
        Input : NA
        Output : functions (dict)

        this function reads the crontab file, extracts crontab elements, and puts them
        in a dictionary {'function': [min,hour,dom,month,dow]}
        '''
        tasks = self.retrieve_crontab_tasks()
        functions = {}

        for task in range(len(tasks)):
            times,command = self.extract_crontab_elements(tasks[task],[])
            functions[command] = times

        return functions



    def grab_key_index(self,index,dictionary):
        '''
        Input : index (int)
                dictionary (dict)
        Output : key (str)

        given an index returns that key from a dictionary
        '''
        i = 0
        for key in dictionary.keys():
            if i == int(index):
                return key
            i += 1



    def convert_crontab_time(self,function_time,current_time):
        '''
        Input : function_time (str)
                current_time (int)

        Output : (int or list)

        given a string and a current time, this function will return
        an array of times the function will run or an int number of when it will run.
        If function time == "*/x" it will return a list of the denomiator ex : */1 = 1
        '''
        result_range = []

        if "*" in function_time:
            if "/" in function_time:
                slash_split_time = function_time.split("/")
                return [int(slash_split_time[-1])/1]
            else:
                return current_time

        elif "," in function_time:
            comma_split_time = function_time.split(",")

            for time_arg in comma_split_time:
                if "-" in time_arg:
                    time_range = time_arg.split("-")
                    result_range += [time for time in range(int(time_range[0]),int(time_range[1])+1)]
                else:
                    result_range.append(int(time_arg))
            return result_range

        elif "-" in function_time:
            dash_split_time = function_time.split("-")
            result_range += [time for time in range(int(dash_split_time[0]),int(dash_split_time[1])+1)]
            return result_range

        else:
            return int(function_time)



    def find_next_run_time(self,function_time,current_time,max_time):
        '''
        Input : function_time (int or list)
                current_time (int)
                max_time (int)

        Output : (int)

        given the converted crontab time for a given min, hour or etc, it will process accordingly and return the next run time as an int
        '''

        if type(function_time) is int:
            res = function_time-current_time
            if res < 0:
                return max_time + res
            else:
                return res

        elif type(function_time) is list:
            if len(function_time) == 1:
                next_time = (math.floor(current_time/function_time[0])* function_time[0]) + function_time[0]
                return next_time- current_time
            else:
                closest = 25
                for time in function_time:
                    if time > current_time:
                        if time < closest:
                            closest = time
                return closest



    def display_function_next_run_time(self,function_key,function_values):
        '''
        Input : function_key (str)
                function_values (list)

        Output : NA

        a function that runs the "find_next_run_time" function for each time field,
        displays that in the terminal in a readable fashion
        '''
        now = datetime.now()
        current_times = [now.minute,now.hour,now.day,now.month,now.weekday()]
        fields = ["minute", "hour","day", "month", "day of week"]
        max_day = calendar.monthrange(now.year,now.month)
        max_times = [59,23,max_day[1],12,6]

        print(f"{function_key}")
        for number in range(len(function_values)):
            converted_time = self.convert_crontab_time(function_values[number],current_times[number])
            time_remaining = self.find_next_run_time(converted_time,current_times[number],max_times[number])
            print(f"you have {time_remaining} {fields[number]}/s... ")
        print()



    def terminal_ui(self):
        print('''
            type "check" to check a crontab command time...
            type "all" to check all next run times...
            type "exit" to exit...
            ''')
        user_input = input(":")

        if user_input.lower() == "check":
            functions = self.create_functions_dictionary()
            print(functions)
            function_index = 0

            for key,value in functions.items():
                print(f"{function_index}: {key}")
                function_index += 1

            user_input = input("type the corrisponding number to the function you want to check.\n: ")

            function_key = self.grab_key_index(user_input,functions)
            self.display_function_next_run_time(function_key, functions[function_key])

        elif user_input.lower() == "all":
            functions = self.create_functions_dictionary()

            for key, values in functions.items():
                self.display_function_next_run_time(key,values)

        elif user_input.lower() == "exit":
            exit()
        else:
            print("Sorry please try again..." + "\n"*2)
            self.terminal_ui()


