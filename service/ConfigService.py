import ConfigParser

config = ConfigParser.RawConfigParser()

def read():
    config.read('config.cfg')

def getConfigVar(value, section='development'):
    return config.get(section, value)

