import logging
#import os
#from logging.handlers import RotatingFileHandler

#LOG_DIR = "logs"
#os.makedirs(LOG_DIR, exist_ok=True)

#LOG_FILE = os.path.join(LOG_DIR, "app.log")

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:  # evita múltiples handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

      #  file_handler = RotatingFileHandler(
       #     LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding='utf-8'
       # )
      #  file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        #logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
