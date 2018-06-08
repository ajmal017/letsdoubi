

import sys
import configparser


def get_settings():
	# Get configuration from setting.ini file
	configParser = configparser.ConfigParser()   
	configFilePath = r'../conf/setting.ini'
	configParser.read(configFilePath)
	return configParser