from core import *
from collections import defaultdict
import global_

class Char_Weapon_BP(Base_Char):
	def __init__(self, x, constellation, er_req):
		self.weapon = x
		self.base_stats = empty_stats + self.char_base_stats + self.weapon['stats']
		self.base_hp = self.base_hp
		self.base_atk = self.char_base_atk + self.weapon['base_atk']
		self.mains = ()
		self.subs = defaultdict(int)
		self.constellation = constellation
		self.er_req = er_req

	def name(self):
		return self.char_name + str(self.constellation)

class Raiden(Char_Weapon_BP):
	char_name = 'Raiden'
	base_hp = 12907
	char_base_atk = 337
	q_cost = 90

	char_base_stats = Stats({
		'hpf': 4780,
		'atkf': 311,
		'cr': 5 * 2,
		'cd': 50,
		'er': 100
	})

	num_subs = 30
	min_crit_subs = 20
	max_crit_subs = 30
	mains_candidates = [('er', 'atkp', 'cd'), ('atkp', 'atkp', 'cd'), ('er', 'dmgp', 'cd'), ('atkp', 'dmgp', 'cd')]
	stat_candidates = ['atkp', 'dmgp', 'cd', 'er']

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		atkp = stats.d['atkp']
		if 'engulfing_lightning' in self.weapon:
			r = self.weapon['engulfing_lightning']
			atkp += min((stats.d['er'] - 100) * refine_val(28, 56, r)/100, refine_val(80, 120, r))
		atk = self.base_atk * (1 + atkp/100) + stats.d['atkf']
		return atk

	def dmg_e(self, stats, res_skill, res_ticks, ticks, in_q):
		multiplier_skill = 210.96
		multiplier_ticks = 75.6 * ticks
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm((stats.d['cr'] + stats.d['ecr'])*2 + stats.d['cd'])
		dmgm = 1 + (stats.d['dmgp'] + stats.d['ep'] + (stats.d['er'] - 100) * 0.4)/100
		resm_skill = (1 - res_skill/100)
		resm_ticks = (1 - res_ticks/100)
		defm = get_defm(60 if in_q and self.constellation >= 2 else 0)
		ret = multiplier_skill/100 * atk * critm * dmgm * resm_skill * defm + multiplier_ticks/100 * atk * critm * dmgm * resm_ticks * defm
		if global_.dbg:
			global_.dmg_log.append(("raiden e", ret))
		return ret

	def dmg_q(self, stats, res, num_n5):
		# Q + (N5) x num_n5
		if self.constellation < 3:
			multiplier = (721.44 + 7 * 60) + (79.82 + 78.42 + 96.02 + 55.11 + 55.26 + 131.92 + 1.31 * 60 * 6) * num_n5
		else:
			multiplier = (851.7 + 8.26 * 60) + (93.54 + 91.91 + 112.54 + 64.58 + 64.77 + 154.61 + 1.54 * 60 * 6) * num_n5
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm((stats.d['cr'] + stats.d['qcr'])*2 + stats.d['cd'])
		dmgm = 1 + (stats.d['dmgp'] + stats.d['qp'] + min(0.25 * stats.d['er'], 75) + (stats.d['er'] - 100) * 0.4)/100
		resm = (1 - res/100)
		defm = get_defm(60 if self.constellation >= 2 else 0)
		ret = multiplier/100 * atk * critm * dmgm * resm * defm
		if global_.dbg:
			global_.dmg_log.append(("raiden q", ret))
		return ret

class Yae(Char_Weapon_BP):
	char_name = 'Yae'
	base_hp = 11284
	char_base_atk = 264
	q_cost = 90

	char_base_stats = Stats({
		'hpf': 4780,
		'atkf': 311,
		'cr': 5 * 2 + 19.2,
		'cd': 50,
		'er': 100
	})

	num_subs = 30
	min_crit_subs = 20
	max_crit_subs = 30
	mains_candidates = [('atkp', 'dmgp', 'cd')]
	stat_candidates = ['atkp', 'dmgp', 'cd', 'er']

	def __init__(self, x, constellation, er_req):
		super().__init__(x, constellation, er_req)
		if constellation >= 1:
			self.er_req -= 8*3 # assume 3 e's

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']
		return atk

	def dmg_e(self, stats, res, ticks, num_e=3):
		multiplier = 151.8 * ticks * num_e
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm((stats.d['cr'] + stats.d['ecr'])*2 + stats.d['cd'])
		resm = (1 - res/100)
		dmgm = 1 + (stats.d['dmgp'] + stats.d['ep'] + stats.d['em'] * 0.12)/100
		ret = multiplier/100 * atk * critm * dmgm * resm * get_defm(0)
		if global_.dbg:
			global_.dmg_log.append(("yae e", ret))
		return ret

	def dmg_q(self, stats, res, num_e=3):
		multiplier = 468 + 528.77*num_e
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm((stats.d['cr'] + stats.d['qcr'])*2 + stats.d['cd'])
		resm = (1 - res/100)
		dmgm = 1 + (stats.d['dmgp'] + stats.d['qp'])/100
		ret = multiplier/100 * atk * critm * dmgm * resm * get_defm(0)
		if global_.dbg:
			global_.dmg_log.append(("yae q", ret))
		return ret

class Kazuha(Char_Weapon_BP):
	char_name = 'Kazuha'
	base_hp = 13348
	char_base_atk = 297
	q_cost = 60

	char_base_stats = Stats({
		'hpf': 4780,
		'atkf': 311,
		'cr': 5 * 2,
		'cd': 50,
		'em': 115.2,
		'er': 100
	})

	num_subs = 30
	min_crit_subs = 0
	max_crit_subs = 0
	mains_candidates = [('em', 'em', 'em')]
	stat_candidates = ['em', 'er']

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']
		return atk

	def dmg_e(self, stats, res1, res2):
		# only swirl dmg
		ret = self.dmg_swirl(stats, res1) + self.dmg_swirl(stats, res2)
		if global_.dbg:
			global_.dmg_log.append(("kazuha e", ret))
		return ret

	def dmg_q(self, stats, res):
		# only swirl dmg
		ret = 6 * self.dmg_swirl(stats, res)
		if global_.dbg:
			global_.dmg_log.append(("kazuha q", ret))
		return ret

	def dmg_swirl(self, stats, res):
		return 868 * (1 + swirlp_from_em(stats.d['em'])/100 + stats.d['swirlp']/100) * (1 - res/100) # no defense

class Bennett(Char_Weapon_BP):
	char_name = 'Bennett'
	base_hp = 12397
	char_base_atk = 191
	q_cost = 60

	char_base_stats = Stats({
		'hpf': 4780,
		'atkf': 311,
		'cr': 5 * 2,
		'cd': 50,
		'er': 126.7
	})

	num_subs = 0
	min_crit_subs = 0
	max_crit_subs = 0
	mains_candidates = [('em', 'em', 'em')]
	stat_candidates = ['em']

	def __init__(self, x, constellation, er_req):
		super().__init__(x, constellation, er_req)
		if constellation < 5:
			print('bennett must be at least c5')
			exit()

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']
		return atk

	def q_atkf_buff(self, stats):
		batkp = 100.8 if self.constellation < 5 else 119
		if self.constellation >= 1:
			batkp += 20
		return self.base_atk * batkp/100

class Xingqiu(Char_Weapon_BP):
	char_name = 'Xingqiu'
	base_hp = 10222
	char_base_atk = 202
	q_cost = 80

	char_base_stats = Stats({
		'hpf': 4780,
		'atkf': 311,
		'atkp': 24,
		'cr': 5 * 2,
		'cd': 50,
		'dmgp': 20,
		'er': 100
	})

	num_subs = 30
	min_crit_subs = 20
	max_crit_subs = 30
	mains_candidates = [('atkp', 'dmgp', 'cd'), ('er', 'dmgp', 'cd')]
	stat_candidates = ['atkp', 'dmgp', 'cd', 'er']

	def __init__(self, x, constellation, er_req, er_from_c6=20):
		super().__init__(x, constellation, er_req)

		if constellation != 6:
			print('xq must be c6')
			exit()

		if 'sac_sword' in self.weapon:
			r = self.weapon['sac_sword']
			if r < 4:
				print('sac_sword refinement ' + r + ' not supported')
				exit()
			self.er_req -= 40

		self.er_req -= er_from_c6

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		hp = self.get_hp(stats)
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']
		if 'jade_cutter' in self.weapon:
			atk += refine_val(1.2, 2.4, self.weapon['jade_cutter'])/100 * hp
		return atk

	def dmg_e(self, stats, res, in_q):
		multiplier = 357 + 406.3
		c4m = 1.5 if self.constellation >= 4 and in_q else 1
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm((stats.d['cr'] + stats.d['ecr'])*2 + stats.d['cd'])
		resm = (1 - res/100)
		dmgm = 1 + (stats.d['dmgp'] + stats.d['ep'])/100
		ret = multiplier/100 * atk * critm * dmgm * resm * get_defm(0) * c4m
		if global_.dbg:
			global_.dmg_log.append(("xingqiu e", ret))
		return ret

	def dmg_q(self, stats, res, ticks):
		multiplier = 115.33 * (2 + 3 + 5)/3 * ticks
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm((stats.d['cr'] + stats.d['qcr'])*2 + stats.d['cd'])
		resm = (1 - res/100)
		dmgm = 1 + (stats.d['dmgp'] + stats.d['qp'])/100
		ret = multiplier/100 * atk * critm * dmgm * resm * get_defm(0)
		if global_.dbg:
			global_.dmg_log.append(("xingqiu q", ret))
		return ret