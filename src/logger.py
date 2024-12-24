import logging
import os
from datetime import datetime

# Define the log file name and path
log_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

# Configure logging to log only to a file
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    logging.info("Logging Has Started")
