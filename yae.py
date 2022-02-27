from util import *
from collections import defaultdict

base_hp = 11284
base_atk = 264

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'atkp': 18 + 18,
	'crit': 5 * 2 + 50 + 38.4
})

class Char(Base_Char):
	def __init__(self, x):
		if type(x) is Char:
			print('???')
			exit()
			self.weapon = x.weapon
			self.base_stats = Stats(x.base_stats)
			self.base_hp = x.base_hp
			self.base_atk = x.base_atk
			self.mains = x.mains
			self.subs = {**x.subs}
		else:
			self.weapon = x
			self.base_stats = empty_stats + base_stats + self.weapon['stats']
			self.base_hp = base_hp
			self.base_atk = base_atk + self.weapon['base_atk']
			self.mains = ()
			self.subs = defaultdict(int)

	def get_hp(self, stats):
		return self.base_hp * (1 + stats.d['hpp']/100) + stats.d['hpf']

	def get_atk(self, stats):
		hp = self.get_hp(stats)
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']
		if 'homa' in self.weapon:
			atk += hp * refine_val(1.8, 3.4, self.weapon['homa'])/100

		return atk

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		critm, cr, cd = get_critm(stats.d['crit'])
		e_proportion, q_proportion = 0.7, 0.3
		dmgm_e = 1 + (stats.d['dmgp'] + stats.d['em']*0.12 + stats.d['ep'])/100
		dmgm_q = 1 + (stats.d['dmgp'])/100

		tot = e_proportion * atk * critm * dmgm_e + q_proportion * atk * critm * dmgm_q
		
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgm_e, dmgm_q)
		return tot

	def copy(self):
		return Char(self)


weapons = [solar_pearl(1), widsith(1, 0.25/3, 0.25/3, 0.25/3), widsith(5, 0.25/3, 0.25/3, 0.25/3), lost_prayer(1, 0), skyward_atlas(1), kagura(1, 3, 1), kagura(5, 3, 1)]
# weapons = [solar_pearl(1), widsith(1, 0, 0.5, 0), widsith(5, 0, 0.5, 0), kagura(1, 2, 0.5), kagura(5, 2, 0.5)]
chars = [Char(x) for x in weapons]
for c in chars:
	c.optimize(30, 30)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score(False)
	print(weapons[i]['name'], score, (score - base_score)/base_score*100)
	# print(c.mains)
	# print(dict(c.subs))
	# print()
	# print(c.score(True))

# for c in chars:
# 	# print(c.get_hp(c.get_stats()), c.get_atk(c.get_stats()), c.get_stats().d['crit'], c.get_stats().d['em'])
# 	print(c.real_dmg())

