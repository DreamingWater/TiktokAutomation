# Lenovo-"Xie Yan"


"""操作日志记录
"""
import sys
import time
from loguru import logger
from pathlib import Path

from tiktok_config import Data_Storage_storage_Dir

log_path = Path(Data_Storage_storage_Dir, "log")


def error_only(record):
    """
    error 日志 判断
    Args:
        record:

    Returns: 若日志级别为ERROR, 输出TRUE

    """
    return record["level"].name == "ERROR"

def not_info_only(record):
    return record["level"].name != "INFO"

# class Loggings:
#     __instance = None
#     t = time.strftime("%Y_%m_%d")
#     logger.add(f"{log_path}/logger_{t}.log",  format="{time:YYYY-MM-DD HH:mm:ss} {level} {file}:{line} -- {message}",rotation="50MB", encoding="utf-8", enqueue=True,
#                retention="10 days")
#     logger.add(f"{log_path}/error_{t}.log", rotation="50MB", encoding="utf-8", enqueue=True,filter=error_only,
#                retention="10 days")
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.__instance:
#             cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)
#
#         return cls.__instance
#
# def info(self, msg):
#     return logger.info(msg)
#
# def debug(self, msg):
#     return logger.debug(msg)
#
# def warning(self, msg):
#     return logger.warning(msg)
#
# def error(self, msg):
#     return logger.error(msg)
def loguru_config():
    t = time.strftime("%Y_%m_%d")
    logger.remove()
    logger.add(f"{log_path}/logger_{t}.log", format="{time:YYYY-MM-DD HH:mm:ss} {level} {file}:{line} -- {message}",
               rotation="50MB", encoding="utf-8", enqueue=True,
               retention="10 days")
    logger.add(f"{log_path}/error_{t}.log", rotation="50MB", encoding="utf-8", enqueue=True, filter=error_only,
               retention="10 days")
    # logger.add(sys.stderr,  filter=not_info_only, enqueue=True)
    logger.add(sys.stderr, enqueue=True)
