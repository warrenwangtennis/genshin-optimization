from util import *

base_hp = 9787
base_atk = 212

base_stats = Stats({
	'hpf': 4780,
	'atkf': 311,
	'crit': 5 * 2 + 50,
	'dmgp': 24 + 12
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
		if dbg:
			print(hp, atk, cr, cd, stats.d['em'], dmgp)
		return atk * crit * dmgp

	def copy(self):
		return Char(self)
weapons = [empty_weapon(510), lost_prayer(1, 0)]
# weapons = [solar_pearl(1), solar_pearl(5), widsith(1, 1/3), widsith(5, 1/3), lost_prayer(1, 0), lost_prayer(5, 0), skyward_atlas(1), skyward_atlas(5), memory(1, 4.5, 1), memory(5, 4.5, 1)]
chars = [Char(x) for x in weapons]
for c in chars:
	c.optimize(30, 25)
base_score = chars[0].score()

for i, c in enumerate(chars):
	score = c.score()
	print(weapons[i]['name'], score, (score - base_score)/base_score*100)
	print(c.mains)
	print(dict(c.subs))