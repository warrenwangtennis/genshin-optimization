from core import *
import global_

class Char_BP():
	def __init__(self, constellation, er_req):
		self.constellation = constellation
		self.er_req = er_req

	def name(self):
		return self.char_name + str(self.constellation)

class Build:
	def __init__(self, char, weapon, artifacts, extra_stats):
		self.char = char
		self.weapon = weapon
		self.weapon_stats = Stats(weapon['stats'])
		self.artifacts = artifacts
		self.extra_stats = extra_stats
		self.constellation = 0

	def get_stats(self):
		# print(empty_stats , self.char.base_stats , self.artifacts.tot_stats , self.extra_stats)
		return empty_stats + self.char.base_stats + self.weapon_stats + self.artifacts.tot_stats + self.extra_stats

	def get_single_stat(self, field):
		return get_single_stat(field, self.char.base_stats, self.weapon_stats, self.artifacts.tot_stats, self.extra_stats)

class Ayaka:
	char_name = 'Ayaka'
	base_hp = 12858
	char_base_atk = 342
	q_cost = 80

	base_stats = Stats({
		'cr': 5,
		'cd': 50 + 38.4,
		'er': 100
	})

	# references build, can dynamically change
	def set_build(self, build):
		self.build = build

	def get_base_atk(self):
		w = self.build.weapon
		return self.char_base_atk + w['base_atk']

	def get_hp(self):
		hpp = self.build.get_single_stat('hpp')
		hpf = self.build.get_single_stat('hpf')
		return self.base_hp * (1 + hpp/100) + hpf

	def get_atk(self):
		w = self.build.weapon
		atkp = self.build.get_single_stat('atkp')
		atkf = self.build.get_single_stat('atkf')
		atk = self.get_base_atk() * (1 + atkp/100) + atkf
		if 'jade_cutter' in w:
			hp = self.get_hp()
			atk += refine_val(1.2, 2.4, w['jade_cutter'])/100 * hp
		return atk

	def dmg_na(self, num=1):
		multiplier = 90.39
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		nap = self.build.get_single_stat('nap')
		ep = self.build.get_single_stat('ep')
		res = self.build.get_single_stat('res')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + nap)/100
		resm = 1 - res/100
		defm = get_defm(0)
		ret = (multiplier/100 * atk * critm * dmgm * resm * defm) * num
		if global_.dbg:
			global_.dmg_log.append(("ayaka na x" + str(num), ret))
		return ret

	def dmg_n4c(self, num=1):
		multiplier_na = 90.39+96.24+123.79+44.77*3
		multiplier_ca = 108.97*3
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		nap = self.build.get_single_stat('nap')
		cap = self.build.get_single_stat('cap')
		ep = self.build.get_single_stat('ep')
		res = self.build.get_single_stat('res')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm_na = 1 + (dmgp + nap)/100
		dmgm_ca = 1 + (dmgp + cap)/100
		resm = 1 - res/100
		defm = get_defm(0)
		ret = (multiplier_na/100 * atk * critm * dmgm_na * resm * defm + multiplier_ca/100 * atk * critm * dmgm_ca * resm * defm) * num
		if global_.dbg:
			global_.dmg_log.append(("ayaka n4c x" + str(num), ret))
		return ret

	def dmg_e(self):
		multiplier = 430.56
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		ep = self.build.get_single_stat('ep')
		res = self.build.get_single_stat('res')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + ep)/100
		resm = 1 - res/100
		defm = get_defm(0)
		ret = multiplier/100 * atk * critm * dmgm * resm * defm
		if global_.dbg:
			global_.dmg_log.append(("ayaka e", ret))
		return ret

	def dmg_q(self):
		multiplier_tick = 202.14
		multiplier_end = 303.21
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		qp = self.build.get_single_stat('qp')
		res = self.build.get_single_stat('res')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + qp)/100
		resm = 1 - res/100
		defm = get_defm(0)
		# print(atk, cr, cd, dmgm, resm, defm)
		ret = (multiplier_tick*20 + multiplier_end)/100 * atk * critm * dmgm * resm * defm
		if global_.dbg:
			global_.dmg_log.append(("ayaka q", ret))
		return ret

	def dmg_q_tick(self, num=1):
		multiplier = 202.14
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		qp = self.build.get_single_stat('qp')
		res = self.build.get_single_stat('res')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + qp)/100
		resm = 1 - res/100
		defm = get_defm(0, 90, 93)
		# print(atk, cr, cd, dmgm, resm, defm)
		ret = multiplier/100 * atk * critm * dmgm * resm * defm * num
		if global_.dbg:
			global_.dmg_log.append(("ayaka q_tick x" +str(num), ret))
		return ret

class HuTao:
	char_name = 'HuTao'
	base_hp = 15552
	char_base_atk = 106
	q_cost = 60

	base_stats = Stats({
		'cr': 5,
		'cd': 50 + 38.4,
		'er': 100
	})

	# references build, can dynamically change
	def set_build(self, build):
		self.build = build

	def get_base_atk(self):
		w = self.build.weapon
		return self.char_base_atk + w['base_atk']

	def get_hp(self):
		hpp = self.build.get_single_stat('hpp')
		hpf = self.build.get_single_stat('hpf')
		return self.base_hp * (1 + hpp/100) + hpf

	def get_atk(self):
		w = self.build.weapon
		atkp = self.build.get_single_stat('atkp')
		atkf = self.build.get_single_stat('atkf')
		atk = self.get_base_atk() * (1 + atkp/100) + atkf
		if 'homa' in w:
			hp = self.get_hp()
			atk += refine_val(1.8, 3.4, w['homa'])/100 * hp
		return atk

	def dmg_n1c(self, vape_rate=1, num=1):
		multiplier_na = 83.65
		multiplier_ca = 242.57
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		nap = self.build.get_single_stat('nap')
		cap = self.build.get_single_stat('cap')
		res = self.build.get_single_stat('res')
		em = self.build.get_single_stat('em')
		vapep = self.build.get_single_stat('vapep')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm_na = 1 + (dmgp + nap)/100
		dmgm_ca = 1 + (dmgp + cap)/100
		resm = 1 - res/100
		defm = get_defm(0)
		reactm = 1.5 * (1 + (vapep_from_em(em) + vapep)/100) * vape_rate + (1 - vape_rate)
		ret = (multiplier_na/100 * dmgm_na + multiplier_ca/100 * dmgm_ca) * atk * critm * resm * defm * reactm * num
		if global_.dbg:
			global_.dmg_log.append(("hu tao n1c x" + str(num), ret))
		return ret

	def dmg_ca(self, vape_rate=1, num=1):
		multiplier = 242.57
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		cap = self.build.get_single_stat('cap')
		res = self.build.get_single_stat('res')
		em = self.build.get_single_stat('em')
		vapep = self.build.get_single_stat('vapep')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + cap)/100
		resm = 1 - res/100
		defm = get_defm(0)
		reactm = 1.5 * (1 + (vapep_from_em(em) + vapep)/100) * vape_rate + (1 - vape_rate)
		ret = multiplier/100 * dmgm * atk * critm * resm * defm * reactm * num
		if global_.dbg:
			global_.dmg_log.append(("hu tao ca x" + str(num), ret))
		return ret

	def dmg_e(self, vape_rate=1, num=1):
		multiplier = 115.2
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		ep = self.build.get_single_stat('ep')
		res = self.build.get_single_stat('res')
		em = self.build.get_single_stat('em')
		vapep = self.build.get_single_stat('vapep')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + ep)/100
		resm = 1 - res/100
		defm = get_defm(0)
		reactm = 1.5 * (1 + (vapep_from_em(em) + vapep)/100) * vape_rate + (1 - vape_rate)
		ret = multiplier/100 * atk * critm * dmgm * resm * defm * reactm * num
		if global_.dbg:
			global_.dmg_log.append(("hu tao e x" + str(num), ret))
		return ret

	def dmg_q(self, vape_rate=1):
		multiplier = 617.44
		atk = self.get_atk()
		cr = self.build.get_single_stat('cr')
		cd = self.build.get_single_stat('cd')
		dmgp = self.build.get_single_stat('dmgp')
		qp = self.build.get_single_stat('qp')
		res = self.build.get_single_stat('res')
		em = self.build.get_single_stat('em')
		vapep = self.build.get_single_stat('vapep')
		res = 10 - res if res < 10 else -(res - 10)/2
		critm = 1 + min(cr, 100)/100 * cd/100
		dmgm = 1 + (dmgp + qp)/100
		resm = 1 - res/100
		defm = get_defm(0)
		reactm = 1.5 * (1 + (vapep_from_em(em) + vapep)/100) * vape_rate + (1 - vape_rate)
		ret = multiplier/100 * atk * critm * dmgm * resm * reactm * defm
		if global_.dbg:
			print(atk, cr, cd, em, dmgm, resm, defm, reactm)
			global_.dmg_log.append(("hu tao q", ret))
		return ret