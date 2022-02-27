from util import *

def solar_pearl(r):
	return {
		'base_atk': 510,
		'stats': {
			'cr': 27.6,
			'nap': refine_val(20, 40, r),
			'ep': refine_val(20, 40, r),
			'qp': refine_val(20, 40, r)
		},
		'name': 'solar_pearl{0}'.format(r)
	}

def lost_prayer(r, stacks):
	return {
		'base_atk': 608,
		'stats': {
			'cr': 33.1,
			'dmgp': refine_val(8, 16, r) * stacks
		},
		'name': 'lost_prayer{0}'.format(r)
	}

def skyward_atlas(r):
	return {
		'base_atk': 674,
		'stats': {
			'atkp': 33.1,
			'dmgp': refine_val(12, 24, r) # no phys dmg effect
		},
		'name': 'skyward_atlas{0}'.format(r)
	}

def memory(r, stacks, shield_uptime):
	return {
		'base_atk': 608,
		'stats': {
			'atkp': 49.6 + refine_val(4, 8, r) * stacks * (1*(1-shield_uptime) + 2*shield_uptime)
		},
		'name': 'memory{0}'.format(r)
	}

def widsith(r, atkp_uptime, dmgp_uptime, em_uptime):
	return {
		'base_atk': 510,
		'stats': {
			'cd': 55.1,
			'atkp': refine_val(60, 120, r) * atkp_uptime,
			'dmgp': refine_val(48, 96, r) * dmgp_uptime,
			'em': refine_val(240, 480, r) * em_uptime
		},
		'name': 'widsith{0}_{1:.2f}atkp_{2:.2f}dmgp_{3:.2f}em'.format(r, atkp_uptime*100, dmgp_uptime*100, em_uptime*100)
	}

def fav_codex(r):
	return {
		'base_atk': 510,
		'stats': {
			'er': 45.9
		},
		'name': 'fav_codex{0}'.format(r)
	}

def kagura(r, stacks, max_stacks_uptime):
	return {
	    'base_atk': 608,
	    'stats': {
	        'cd': 66.2,
	        'ep': refine_val(12, 24, r) * stacks,
	        'dmgp': refine_val(12, 24, r) * max_stacks_uptime
	    },
	    'name': 'kagura{0}'.format(r)
	}