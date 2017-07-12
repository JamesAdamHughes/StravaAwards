import ConfigParser
import os
config = ConfigParser.RawConfigParser()

def read(path):
    print "reading config..." + path
    #print config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))
    print config.read(path)

def getConfigVar(value, section='development'):
    print '[config] sections: ' + str(config.sections())
    print '[config] using section ' + section
    enviroment = os.getenv('ENVIROMENT')
    print '[config] enviroment ' + str(enviroment)
    return config.get(section, value)


def addSectionAndValue(section, name, value):
    config.add_section(section)
    config.set(section, name, value)
