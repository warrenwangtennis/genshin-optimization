from util import *
from collections import defaultdict

base_hp = 15552
base_atk = 106

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'cr': 5,
	'cd': 50 + 38.4,
	'dmgp': 15 + 7.5 + 33
})

class Char(Base_Char):
	def __init__(self, x):
		if type(x) is Char:
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
		atk = self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf'] + min(5.96/100 * hp, 4 * self.base_atk)
		if 'homa' in self.weapon:
			atk += hp * refine_val(1.8, 3.4, self.weapon['homa'])/100

		return atk

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		critm, cr, cd = get_optimal_critm(stats.d['cr']*2 + stats.d['cd'])
		dmgp = 1 + stats.d['dmgp']/100
		react_rate = 1.0
		react = react_rate * 1.5 * (1 + melt_p(stats.d['em'])/100 + 0.15) + (1 - react_rate) * 1
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgp)
		return atk * critm * dmgp * react


	def real_dmg(self):
		score = self.score()
		return 587.93/100 * score * 0.9 * 0.5

	def copy(self):
		return Char(self)

# weapons = [deathmatch(1, False), homa1(), homa5(), lithic_spear(1, 4), lithic_spear(5, 4), dragons_bane(1, 1), dragons_bane(5, 1)]
# weapons = [deathmatch(1, False), homa1(), homa5()]
weapons = [deathmatch(1, False), deathmatch(5, False), dragons_bane(1, 1), dragons_bane(5, 1), homa(1), homa(5)]
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

