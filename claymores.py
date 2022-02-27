from util import *

def aminus(r):
	return {
		'base_atk': 565,
		'stats': {
			'atkp': 27.6,
			# ignore physical damage effect
		},
		'name': 'aminus{0}'.format(r)
	}

def gravestone(r, uptime):
	return {
		'base_atk': 608,
		'stats': {
			'atkp': 49.6 + refine_val(20, 40, r) + refine_val(40, 80, r) * uptime
		},
		'name': 'gravestone{0}'.format(r)
	}

def lithic_blade(r, stacks):
	return {
		'base_atk': 510,
		'stats': {
			'atkp': 41.3 + refine_val(7, 11, r) * stacks,
			'crit': refine_val(3, 7, r)*2 * stacks
		},
		'homa': 0,
		'name': 'lithic_blade{0}_{1}stack'.format(r, stacks)
	}

def serpent_spine(r, stacks):
	return {
		'base_atk': 510,
		'stats': {
			'crit': 27.6*2,
			'dmgp': refine_val(6, 10, r) * stacks
		},
		'homa': 0,
		'name': 'serpent_spine{0}_{1}stack'.format(r, stacks)
	}