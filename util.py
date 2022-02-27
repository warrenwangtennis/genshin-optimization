def meltp_from_em(em):
	percent = -0.000000000013885*(em)**4 + 0.000000060870867*(em)**3 - 0.000127973809274*(em)**2 + 0.196821095573654*(em) + 0.024542903165184
	return percent

def vapep_from_em(em):
	percent = -0.000000000013885*(em)**4 + 0.000000060870867*(em)**3 - 0.000127973809274*(em)**2 + 0.196821095573654*(em) + 0.024542903165184
	return percent

def swirlp_from_em(em):
	return 16 * em/(em+2000) * 100

def get_defm(shred=0, my_lvl=90, ur_lvl=100):
	return ((my_lvl + 100) / ((my_lvl + 100) + (ur_lvl + 100)*(1-shred/100)))

def refine_val(lo, hi, r):
	return (hi - lo)/4 * (r - 1) + lo

def get_optimal_critm(crit):
	if crit > 400:
		cr = 100
		cd = crit - 200
	else:
		cr = crit / 4
		cd = crit / 2
	return 1 + cr/100 * cd/100, cr, cd

def from_mist(stacks, weapon):
	if 'mistsplitter' in weapon:
		r = weapon['mistsplitter']
	else:
		return 0
	if r is None:
		return 0
	if stacks == 1:
		return refine_val(8, 16, r)
	elif stacks == 2:
		return refine_val(16, 32, r)
	elif stacks == 3:
		return refine_val(28, 56, r)
	else:
		return 0

