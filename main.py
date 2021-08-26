import app


# cronpath /var/spool/cron
#cron filename brandon

def main():
    filename = "crontab_cases.txt"
    filepath = ""
    crontab = app.CronRunTime(filename,filepath)

    #terminal interface
    crontab.terminal_ui()


if __name__ == "__main__":
    main()
