import ConfigParser
import os

WORKDIR = os.path.split(os.path.realpath(__file__))[0]
CONFIG = os.path.join(WORKDIR, "conf.ini")

def get_conf():
    config = ConfigParser.ConfigParser()
    config.readfp(open(CONFIG))
    conf_dict = {}
    for section in config.sections():
        for item in config.items(section):
            conf_dict[item[0].upper()] = item[1]
    return conf_dict

conf_dict = get_conf()
