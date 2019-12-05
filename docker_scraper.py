import scraper as scraper
import schedule
import time

def job():
    scraper.runscript() #Run the script
    return

schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
