from util import *
from collections import defaultdict

base_hp = 15552
base_atk = 106

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311 + 1.39*865 + 372,
	'atkp': 20 + 48 + 25,
	'em': 120,
	'crit': 50 + 38.4,
	'dmgp': 15 + 7.5 + 33 + 35.2 + 60 + 25
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
		cr = 100
		cd = stats.d['crit']
		crit = 1 + cr/100 * cd/100
		dmgp = 1 + stats.d['dmgp']/100
		react_rate = 1.0
		react = react_rate * 2.0 * (1 + melt_p(stats.d['em'])/100 + 0.15) + (1 - react_rate) * 1
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgp)
		return atk * crit * dmgp * react


	def real_dmg(self):
		score = self.score()
		return 617.44/100 * score * 1.4 * (90+100)/(200+90+93)

	def copy(self):
		return Char(self)

weapons = [homa(1)]
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
	print(c.score(True))

# for c in chars:
# 	# print(c.get_hp(c.get_stats()), c.get_atk(c.get_stats()), c.get_stats().d['crit'], c.get_stats().d['em'])
# 	print(c.real_dmg())

