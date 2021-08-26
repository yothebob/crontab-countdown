import re
import os

filepath = ""
filename = "crontab_cases.txt"


def retrieve_crontab_tasks(filename):
    '''
    input : filename (str)
    output : tasks (list)

    Opens chrontab file according to file name/path and returns all the chrontab commands
    '''

    f = open(filename,"r")
    tasks = [line for line in f if "*" in line]
    #print(tasks)
    return tasks





def extract_crontab_times(task,time_list=[]):
    '''
    Input : task (str)
            time_list (list)

    Output : time_list (list)

    a function that takes in a chrontab command and returns an array of the times [min,hour,dom,month,dow]
    '''
    popped_job = ""
    job_time = ""

    for number in range(len(task)):
        if task[number] == " ":
            if len(job_time) > 0:
                popped_job = task[number:-1]
                break
        else:
            job_time += task[number]
    time_list.append(job_time)
    print(time_list)
    if len(time_list) >=5:
        return time_list
    else:
        return extract_crontab_times(popped_job,time_list)



tasks = retrieve_crontab_tasks(filename)
cronjobs = []

for task in range(len(tasks)):
    var = extract_crontab_times(tasks[task],[])
    cronjobs.append(var)
print(cronjobs)
