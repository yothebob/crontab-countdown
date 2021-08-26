from cronruntime import CronRunTime


# cronpath /var/spool/cron
#cron filename brandon

def main():
    test_filepath = "/home/brandon/Documents/crontab-test"
    test_filename = "crontab_cases.txt"

    filename = "brandon"

    crontab = CronRunTime(test_filename,test_filepath)

    #terminal interface
    crontab.terminal_ui()

if __name__ == "__main__":
    main()
