from util import *
from collections import defaultdict

base_hp = 0
base_atk = 264

base_statss = [Stats({
	'hpf': 0,
	'atkf': 311 + 54,
	'atkp': 46.6 + 11.1 + 18 + 18,
	'em': 65,
	'dmgp': 46.6,
	'cr': (121.4 - 27.6),
	'cd': 147.1
}), Stats({
	'hpf': 0,
	'atkf': 311 + 35,
	'atkp': 46.6 + 11.1 + 18 + 18,
	'em': 42,
	'dmgp': 46.6,
	'cr': (99.2 - 27.6),
	'cd': 184.5
})]


class Char(Base_Char):
	def __init__(self, x, _base_stats):
		self.weapon = x
		self.base_stats = empty_stats + _base_stats + self.weapon['stats']
		self.base_hp = base_hp
		self.base_atk = base_atk + self.weapon['base_atk']
		self.mains = ()
		self.subs = defaultdict(int)

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		hp = self.get_hp(stats)
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']

		return atk

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		cr = min(stats.d['cr'], 100)
		cd = stats.d['cd']
		critm = 1 + cr/100 * cd/100
		e_dps = 170.64*3/3 # 3 instances of E at one tick per 3s each
		q_dps = (468 + 528.77*3)/22 # base dmg and 3 instances per E active, 22s cooldown
		e_proportion, q_proportion = e_dps/(e_dps+q_dps), q_dps/(e_dps + q_dps)
		dmgm_e = 1 + (stats.d['dmgp'] + stats.d['em']*0.12 + stats.d['ep'])/100
		dmgm_q = 1 + (stats.d['dmgp'])/100

		tot = e_proportion * atk * critm * dmgm_e + q_proportion * atk * critm * dmgm_q
		
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgm_e, dmgm_q)
		return tot

	def copy(self):
		return Char(self)

weapons = [solar_pearl(5), widsith(1, 0.25/3, 0.25/3, 0.25/3), widsith(5, 0.25/3, 0.25/3, 0.25/3), widsith(5, 0.3, 0, 0), widsith(5, 0, 0.3, 0), lost_prayer(1, 0), skyward_atlas(1), skyward_atlas(5), kagura(1, 3, 1), kagura(5, 3, 1)]
# weapons = [solar_pearl(1), widsith(1, 0, 0.5, 0), widsith(5, 0, 0.5, 0), kagura(1, 3, 1), kagura(5, 3, 1)]

chars = []
for w in weapons:
	chars_candidates = [Char(w, base_stats) for base_stats in base_statss]
	best_char = max(chars_candidates, key=lambda c: c.score(False))
	chars.append(best_char)

base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score(True)
	print("{0} {1:.0f} {2:.2f}".format(weapons[i]['name'], score, (score - base_score)/base_score*100))
	# print(c.mains)
	# print(dict(c.subs))
	print()
	# print(c.score(True))

# for c in chars:
# 	# print(c.get_hp(c.get_stats()), c.get_atk(c.get_stats()), c.get_stats().d['crit'], c.get_stats().d['em'])
# 	print(c.real_dmg())

