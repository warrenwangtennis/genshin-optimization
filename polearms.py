from util import *

def deathmatch(r, is_one=False):
	return {
		'base_atk': 454,
		'stats': {
			'atkp': refine_val(16, 32, r) if is_one else refine_val(24, 48, r),
			'cr': 36.8
		},
		'name': 'deathmatch{0}'.format(r)
	}

def homa(r):
	return {
		'base_atk': 608,
		'stats': {
			'cd': 66.2,
			'hpp': refine_val(20, 40, r)
		},
		'homa': r,
		'name': 'homa{0}'.format(r)
	}

def pjw(r, atk_stacks, dmg_stacks):
	return {
		'base_atk': 674,
		'stats': {
			'cr': 22.1,
			'atkp': refine_val(3.2, 6, r) * atk_stacks,
			'dmgp': refine_val(12, 24, r) * dmg_stacks,
		},
		'name': 'pjw{0}_{1},{2}stack'.format(r, atk_stacks, dmg_stacks)
	}

def lithic_spear(r, stacks):
	return {
		'base_atk': 565,
		'stats': {
			'atkp': 27.6 + refine_val(7, 11, r) * stacks,
			'cr': refine_val(3, 7, r) * stacks
		},
		'name': 'lithic_spear{0}_{1}stack'.format(r, stacks)
	}

def dragons_bane(r, uptime):
	return {
		'base_atk': 454,
		'stats': {
			'em': 221,
			'dmgp': refine_val(20, 36, r) * uptime
		},
		'name': 'dragons_bane{0}_{1}uptime'.format(r, uptime)
	}

def the_catch(r):
	return {
		'base_atk': 510,
		'stats': {
			'er': 45.9,
			'qp': refine_val(16, 32, r),
			'qcr': refine_val(6, 12, r)
		}, 
		'name': 'the_catch{0}'.format(r)
	}

def skyward_spine(r):
	return {
		'base_atk': 674,
		'stats': {
			'er': 36.8,
			'cr': refine_val(8, 16, r)
		}, 
		'name': 'skyward_spine{0}'.format(r)
	}

def engulfing_lightning(r):
	return {
		'base_atk': 608,
		'stats': {
			'er': 55.1 + refine_val(30, 50, r) * 2/3, # approx diminish
		},
		'engulfing_lightning': r,
		'name': 'engulfing_lightning{0}'.format(r)
	}