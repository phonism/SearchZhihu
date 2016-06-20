# -*- coding: utf-8 -*-
import logging
from logging import handlers
from conf import config
MAX_SIZE = 8000 #20M
handler = None

level_dict = {"NOTSET": 0, "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}

def getLogger(name):
    ''' Create and return a logger with the specified name. '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    module_name = name.split(".")[1].upper()
    log_dir = config.conf_dict["DEFAULT_LOG_DIR"]
    if config.conf_dict.has_key(module_name + "_LOG_DIR"):
        log_dir = config.conf_dict[module_name + "_LOG_DIR"]
    log_level = config.conf_dict["DEFAULT_LOG_LEVEL"]
    if config.conf_dict.has_key(module_name + "_LOG_LEVEL"):
        log_level = config.conf_dict[module_name + "_LOG_LEVEL"]
    handler = handlers.RotatingFileHandler(log_dir, 'a', MAX_SIZE, 10)
    handler.setLevel(level_dict[log_level])
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level_dict[log_level])
    logger.info('Log Start!')
    return logger

