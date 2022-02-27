from swords import *
from claymores import *
from polearms import *
from bows import *
from catalysts import *

def empty_weapon(base_atk):
	return {
		'base_atk': base_atk,
		'stats': {},
		'name': 'empty_{0}atk'.format(base_atk)
	}