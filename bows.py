from util import *

def prototype_crescent(r, uptime):
	return {
		'base_atk': 510,
		'stats': {
			'atkp': 41.3 + refine_val(36, 72, r) * uptime
		},
		'name': 'prototype_crescent{0}_{1:.2f}uptime'.format(r, uptime)
	}

def amos(r, stacks=5):
	return {
		'base_atk': 608,
		'stats': {
			'atkp': 49.6,
			'dmgp': refine_val(12, 24, r) + refine_val(8, 16, r) * stacks
		},
		'name': 'amos{0}_{1}stack'.format(r, stacks)
	}

def skyward_harp(r):
	return {
		'base_atk': 674,
		'stats': {
			'cr': 22.1,
			'cd': refine_val(20, 40, r)
			# ignore physical dmg effect
		},
		'name': 'skyward_harp{0}'.format(r)
	}

def rust(r):
	return {
		'base_atk': 510,
		'stats': {
			'atkp': 41.3,
			'dmgp': refine_val(40, 80, r)
		},
		'name': 'rust{0}'.format(r)
	}

def thundering_pulse(r):
	return {
		'base_atk': 608,
		'stats': {
	        'atkp': refine_val(20, 40, r),
			'cd': 66.2,
			'dmgp': refine_val(40, 80, r) # always 3 stacks
		},
		'name': 'thundering_pulse{0}'.format(r)
	}