import re
import os
from datetime import datetime, date

filepath = ""
filename = "crontab_cases.txt"

# cronpath /var/spool/cron
#cron filename brandon


def retrieve_crontab_tasks(filepath,filename):
    '''
    input : filepath (str)
            filename (str)

    output : (list)

    Opens chrontab file according to file name/path and returns all the chrontab commands
    '''

    f = open(filename,"r")
    return [line for line in f if "*" in line and "#" not in line]



def extract_crontab_elements(task,time_list=[]):
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
        return extract_crontab_elements(popped_job,time_list)



def create_functions_dictionary():
    '''
    Input : NA
    Output : functions (dict)

    this function reads the crontab file, extracts crontab elements, and puts them
    in a dictionary {'function': [min,hour,dom,month,dow]}
    '''
    tasks = retrieve_crontab_tasks(filepath,filename)
    functions = {}

    for task in range(len(tasks)):
        times,command = extract_crontab_elements(tasks[task],[])
        functions[command] = times

    return functions



def grab_key_index(index,dictionary):
    '''
    Input : index (int)
            dictionary (dict)
    Output : key (str)

    given an index returns that key from a dictionary
    '''
    i = 0
    for key in dictionary.keys():
        #print(key)
        if i == int(index):
            return key
        i += 1



def convert_crontab_time(function_time,current_time):
    print("\n")
    print(function_time)
    result_range = []

    if "*" in function_time:
        if "/" in function_time:
            print("found /")
            slash_split_time = function_time.split("/")
            print(slash_split_time)
            print(int(slash_split_time[-1])/1)
        else:
            print(current_time + 1)
            return current_time + 1

    elif "," in function_time:
        print("found ,")
        comma_split_time = function_time.split(",")
        print(comma_split_time)

        for time_arg in comma_split_time:
            if "-" in time_arg:
                print(time_arg)
                time_range = time_arg.split("-")
                result_range += [time for time in range(int(time_range[0]),int(time_range[1])+1)]
                print(result_range)
            else:
                result_range.append(int(time_arg))
        print(result_range)
        return result_range

    elif "-" in function_time:
        print("found -")
        dash_split_time = function_time.split("-")
        result_range += [time for time in range(int(dash_split_time[0]),int(dash_split_time[1])+1)]
        print(result_range)
        return result_range

    else:
        print(function_time)
        return function_time



def terminal_ui():
    print('''
        type "check" to check a crontab command time...
        type "exit" to exit
        ''')
    user_input = input(":")

    if user_input.lower() == "check":
        functions = create_functions_dictionary()
        print(functions)
        function_index = 0

        for key,value in functions.items():
            print(f"{function_index}: {key}")
            function_index += 1

        user_input = input("type the corrisponding number to the function you want to check.\n: ")
        print(grab_key_index(int(user_input),functions))
        print(functions[grab_key_index(int(user_input),functions)])

        now = datetime.now()

        current_times = [now.minute,now.hour,now.day,now.month,now.weekday()]
        function_times = functions[grab_key_index(user_input,functions)]

        for number in range(len(function_times)):
            convert_crontab_time(function_times[number],current_times[number])

    elif user_input.lower() == "exit":
        exit()
    else:
        print("Sorry please try again..." + "\n"*2)
        terminal_ui()



'''
Testing below \/\/\/\/\/\/

'''
x = datetime.now()
min = x.minute
hour = x.hour
day = x.day
month = x.month
dow = x.weekday()
print(min,hour)
print(day,month)
print(dow)
terminal_ui()
