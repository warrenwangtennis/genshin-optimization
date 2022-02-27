from util import *
from collections import defaultdict

base_hp = 15552
base_atk = 106

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311 + 679 * (0.9 + 0.2),
	'atkp': 20 + 48 + 25,
	'crit': 5 * 2 + 50 + 38.4,
	'dmgp': 15 + 7.5 + 33 + 56,
	'em': 120
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
		if self.weapon['homa'] == 1:
			atk += 1.8/100 * hp
		elif self.weapon['homa'] == 2:
			atk += 3.4/100 * hp

		return atk

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		cr = 100
		cd = stats.d['crit'] - 5 * 2
		crit = 1 + cr/100 * cd/100
		dmgp = 1 + stats.d['dmgp']/100
		react = 2 * (1 + melt_p(stats.d['em'])/100 + 0.15)
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgp)
		return atk * crit * dmgp * react


	def real_dmg(self):
		score = self.score()
		return 558/100 * score * 0.9 * 0.5

	def copy(self):
		return Char(self)

weapons = [homa1()]
chars = [Char(x) for x in weapons]
for c in chars:
	c.optimize(25, 25)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score(True)
	print(weapons[i]['name'], score, (score - base_score)/base_score*100)
	print(c.mains)
	print(dict(c.subs))
	print(c.real_dmg())

# for c in chars:
# 	# print(c.get_hp(c.get_stats()), c.get_atk(c.get_stats()), c.get_stats().d['crit'], c.get_stats().d['em'])
# 	print(c.real_dmg())

