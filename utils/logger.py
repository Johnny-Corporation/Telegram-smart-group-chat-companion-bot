"""Creates main logger """

import logging

# edit this logger for writing into 2 file, in one with debug level, in another with info level

file_handler_debug = logging.FileHandler("output\\debug_logs.log", encoding="utf-8")
file_handler_debug.setLevel(logging.DEBUG)

file_handler_info = logging.FileHandler("output\\info_logs.log", encoding="utf-8")
file_handler_info.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        file_handler_debug,
        file_handler_info,
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
