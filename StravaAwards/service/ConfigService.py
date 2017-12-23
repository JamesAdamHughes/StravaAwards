import ConfigParser
import os
config = ConfigParser.RawConfigParser()

def read(path):
    print "reading config..." + path
    enviroment = os.getenv('ENVIROMENT')
    print '[config] loading enviroment ' + str(enviroment)
    print config.read(path)

def getConfigVar(value, section='development'):
    enviroment = os.getenv('ENVIROMENT')
    print '[config] loading enviroment ' + str(enviroment)
    return config.get(enviroment, value)


def addSectionAndValue(section, name, value):
    config.add_section(section)
    config.set(section, name, value)
