from util import *

base_hp = 10984
base_atk = 223

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311 + 679,
	'crit': 5 * 2 + 50,
	'atkp': 24 + 20 + 25,
	'dmgp': 15 + 20
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
		return self.base_atk * (1 + stats.d['atkp']/100) + stats.d['atkf']

	def score(self, dbg=False):
		stats = self.get_stats()
		hp = self.get_hp(stats)
		atk = self.get_atk(stats)
		if stats.d['crit'] > 400:
			cr = 100
			cd = stats.d['crit'] - 200
		else:
			cr = stats.d['crit'] / 4
			cd = stats.d['crit'] / 2
		crit = 1 + cr/100 * cd/100
		dmgp = 1 + stats.d['dmgp']/100
		react_rate = 1.0
		react = react_rate * 1.5 * (1 + melt_p(stats.d['em'])/100) + (1 - react_rate) * 1
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgp)
		return atk * crit * dmgp * react

weapons = [aminus(1), gravestone(1, 12/50), gravestone(5, 12/50), lithic_blade(1, 4), lithic_blade(5, 4), serpent_spine(1, 5), serpent_spine(5, 5)]
chars = [Char(x) for x in weapons]

for c in chars:
	c.optimize(30, 30)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score()
	print(weapons[i]['name'], score, (score - base_score)/base_score*100)
	print(c.mains)
	print(dict(c.subs))
	print()