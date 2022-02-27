from util import *

def black_sword(r):
	return {
		'base_atk': 510,
		'stats': {
			'cr': 27.6,
			'nap': refine_val(20, 40, r),
			'cap': refine_val(20, 40, r)
		},
		'name': 'black_sword{0}'.format(r)
	}

def jade_cutter(r):
	return {
		'base_atk': 542,
		'stats': {
			'cr': 44.1,
			'hpp': refine_val(20, 40, r)
		},
		'jade_cutter': r,
		'name': 'jade_cutter{0}'.format(r)
	}

def aquila_favonia(r):
	return {
		'base_atk': 674,
		'stats': {
			'atkp': refine_val(20, 40, r)
			# ignore damage passive
		},
		'name': 'aquila_favonia{0}'.format(r)
	}

def summit(r, stacks, shield_uptime):
	return {
		'base_atk': 608,
		'stats': {
			'atkp': 49.6 + refine_val(4, 8, r) * stacks * (1*(1-shield_uptime) + 2*shield_uptime)
		},
		'name': 'summit{0}'.format(r)
	}

def mistsplitter(r):
	return {
		'base_atk': 674,
		'stats': {
			'cd': 44.1,
			'dmgp': 12
		},
		'mistsplitter': r,
		'name': 'mistsplitter{0}'.format(r)
	}

def iron_sting(r, stacks):
	return {
		'base_atk': 510,
		'stats': {
			'em': 165,
			'dmgp': refine_val(6, 12, r) * stacks
		},
		'name': 'iron_sting{0},{1:.2f}stacks'.format(r, stacks)
	}

def freedom_sworn(r, uptime):
	return {
		'base_atk': 608,
		'stats': {
			'em': 198,
			'dmgp': refine_val(10, 20, r)
		},
		'freedom_sworn': {
		    'nap': refine_val(16, 32, r) * uptime,
		    'cap': refine_val(16, 32, r) * uptime,
		    'pap': refine_val(16, 32, r) * uptime,
		    'atkp': refine_val(20, 40, r) * uptime
		},
		'name': 'freedom_sworn{0},{1:.2f}uptime'.format(r, uptime)
	}

def favonius_sword(r):
	return {
		'base_atk': 454,
		'stats': {
			'er': 61.3
		},
		'favonius_sword': r,
		'name': 'favonius_sword{0}'.format(r)
	}

def sac_sword(r):
	return {
		'base_atk': 454,
		'stats': {
			'er': 61.3
		},
		'sac_sword': r,
		'name': 'sac_sword{0}'.format(r)
	}

def lions_roar(r, effectiveness):
	return {
		'base_atk': 510,
		'stats': {
			'er': 41.3,
			'dmgp': refine_val(20, 36, r) * effectiveness
		},
		'lions_roar': r,
		'name': 'lions_roar{0},{1:.2f}effectiveness'.format(r, effectiveness)
	}