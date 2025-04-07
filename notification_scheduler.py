import os
import sys
import time
import logging
import schedule
import django
from datetime import datetime

# Configure logging to a file
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'notification_scheduler_log.txt')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import the notification task function
from apps.notification.tasks import send_upcoming_class_notifications

def run_notification_task():
    """
    Run the notification task and log the results.
    """
    now = datetime.now()
    logging.info(f"Running notification task at {now}")
    
    try:
        # Run the notification task directly
        send_upcoming_class_notifications()
        logging.info("Notification task completed successfully")
    except Exception as e:
        logging.error(f"Error running notification task: {str(e)}")
    
    logging.info("Task finished")

def main():
    """
    Main function to set up and run the scheduler.
    """
    logging.info("Starting notification scheduler...")
    
    # Schedule the task to run every minute
    schedule.every(1).minutes.do(run_notification_task)
    
    # Run the task immediately on startup
    run_notification_task()
    
    logging.info("Scheduler is running. Press Ctrl+C to exit.")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
    except Exception as e:
        logging.error(f"Scheduler error: {str(e)}")
    
    logging.info("Scheduler stopped.")

if __name__ == "__main__":
    main()
