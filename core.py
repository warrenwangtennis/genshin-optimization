from weapons import *
from artifacts import *

import itertools
from collections import defaultdict
from copy import deepcopy
from enum import Enum

class Stats:
	def __init__(self, x):
		self.d = {**x} if type(x) is dict else {**x.d}

	def add_main(self, field, ct=1):
		ret = Stats(self)
		ret.d[field] += main_vals[field] * ct
		return ret

	def add_sub(self, field, ct=1):
		ret = Stats(self)
		ret.d[field] += sub_vals[field] * ct
		return ret

	def __add__(self, o):
		ret = Stats(self)
		if type(o) is Stats:
			o = o.d
		for k in o:
			ret.d[k] += o[k]
		return ret

	def __str__(self):
		return str(self.d)

def get_single_stat(field, *args):
	return sum(x.d[field] for x in args if field in x.d)

empty_stats = Stats({
	'hpp': 0.0, 
	'hpf': 0.0, 
	'atkp': 0.0, 
	'atkf': 0.0,
	'em': 0.0,
	'cr': 0.0,
	'cd': 0.0,
	'dmgp': 0.0,
	'er': 0.0,
	'energyf': 0.0,
	'nap': 0.0,
	'cap': 0.0,
	'pap': 0.0,
	'ep': 0.0,
	'qp': 0.0,
	'ecr': 0.0,
	'qcr': 0.0,
	'vapep': 0.0,
	'swirlp': 0.0,
	'res': 0.0
})

main_vals = {
	'hpf': 4780,
	'atkf': 311,
	'hpp': 46.6,
	'atkp': 46.6,
	'dmgp': 46.6,
	'cr': 31.1,
	'cd': 62.2,
	'em': 187,
	'er': 51.8
}

sands = ['hpp', 'atkp', 'em', 'er']
goblet = ['atkp', 'hpp', 'dmgp', 'em']
circlet = ['atkp', 'hpp', 'cd', 'em']

def get_mains_candidates(stat_candidates):
	sands2 = list(filter(lambda stat: stat in stat_candidates, sands))
	goblet2 = list(filter(lambda stat: stat in stat_candidates, goblet))
	circlet2 = list(filter(lambda stat: stat in stat_candidates, circlet))
	return itertools.product(sands2, goblet2, circlet2)

def get_subs_candidates(stat_candidates):
	return list(filter(lambda stat: stat in stat_candidates, sub_vals.keys()))

sub_vals = {
	'hpp': 5, 
	'hpf': 254, 
	'atkp': 5, 
	'atkf': 17,
	'cd': 6.6,
	'em': 20,
	'er': 5.5
}

sub_vals_max = {
	'hpp': 5.8, 
	'hpf': 299, 
	'atkp': 5.8, 
	'atkf': 19,
	'cr': 3.9,
	'cd': 7.8,
	'em': 23,
	'er': 6.5
}

class Base_Char:
	def __init__(self, x):
		pass

	def score(self):
		pass

	def score_with_sub(self, sub):
		self.subs[sub] += 1
		ret = self.score()
		self.subs[sub] -= 1
		return ret

	def clear_subs(self):
		self.subs.clear()

	def add_sub(self, sub, ct=1):
		self.subs[sub] += ct

	def optimize(self, mains_type, num_subs, min_crit, max_crit):
		assert 0 <= min_crit <= max_crit <= num_subs
		mains_candidates = itertools.product(sands, goblet, circlet)

		best_mains, best_subs, best_score = None, None, None
		for mains in mains_candidates:
			self.mains = mains
			for num_crit in range(min_crit, max_crit + 1):
				self.clear_subs()
				self.add_sub('cd', num_crit)
				self.optimize_non_crit(num_subs - num_crit)
				score = self.score()
				if best_mains is None or score > best_score:
					best_mains = mains
					best_subs = self.subs.copy()
					best_score = score

		self.mains = best_mains
		self.subs = best_subs

	def optimize_non_crit(self, num_subs):
		for i in range(num_subs):
			best_sub, best_score = None, None
			for sub in sub_vals:
				if sub == 'cd':
					continue
				score = self.score_with_sub(sub)
				if best_score is None or score > best_score:
					best_sub = sub
					best_score = score
			self.add_sub(best_sub)

	def get_stats(self):
		ret = Stats(self.base_stats)
		for main in self.mains:
			ret = ret.add_main(main)
		for sub in self.subs:
			ret = ret.add_sub(sub, self.subs[sub])
		return ret

# class Char_Weapon_BP(Base_Char):
# 	def __init__(self, x, constellation, er_req):
# 		self.weapon = x
# 		self.base_stats = empty_stats + self.base_stats + self.weapon['stats']
# 		self.base_hp = self.base_hp
# 		self.base_atk = self.char_base_atk + self.weapon['base_atk']
# 		self.mains = ()
# 		self.subs = defaultdict(int)
# 		self.constellation = constellation
# 		self.er_req = er_req

# 	def name(self):
# 		return self.char_name + str(self.constellation)

class Team:
	def __init__(self, chars):
		self.chars = chars
		# self.subs = [defaultdict(int) for _ in chars]
		# self.mains = [() for _ in chars]
		self.team_subs = [get_subs_candidates(c.stat_candidates) for c in chars]
		# self.cur_num_subs = [0 for _ in chars]
		# self.cur_num_crit_subs = [0 for _ in chars]

	def score_with_isub(self, isub):
		self.add_isub(isub)
		ret = self.score()
		self.add_isub(isub, -1)
		return ret

	def clear_subs(self):
		self.subs = [defaultdict(int) for _ in self.chars]
		self.cur_num_subs = [0 for _ in self.chars]
		self.cur_num_crit_subs = [0 for _ in self.chars]

	def add_isub(self, isub, ct=1):
		i, sub = isub
		self.subs[i][sub] += ct
		self.cur_num_subs[i] += ct
		if sub == 'cd':
			self.cur_num_crit_subs[i] += ct


	def optimize(self):
		best_mains, best_subs, best_total_score = None, None, None
		for team_mains in itertools.product(*(c.mains_candidates for c in self.chars)):
			self.mains = team_mains
			self.clear_subs()
			while True:
				best_isub, best_score = None, None
				for i, c in enumerate(self.chars):
					if self.cur_num_subs[i] >= c.num_subs:
						continue
					for sub in self.team_subs[i]:
						if sub == 'cd' and self.cur_num_crit_subs[i] >= c.max_crit_subs:
							continue

						score = self.score_with_isub((i, sub))
						if best_score is None or score > best_score:
							best_isub = (i, sub)
							best_score = score

				if best_isub is None:
					break

				self.add_isub(best_isub)

			total_score = self.score()
			if best_mains is None or total_score > best_total_score:
				best_mains = deepcopy(self.mains)
				best_subs = deepcopy(self.subs)
				best_total_score = total_score

		self.mains, self.subs = best_mains, best_subs

	def get_stats(self):
		ret = []
		for i, c in enumerate(self.chars):
			stats = Stats(c.base_stats)
			for main in self.mains[i]:
				stats = stats.add_main(main)
			for sub in self.subs[i]:
				stats = stats.add_sub(sub, self.subs[i][sub])
			ret.append(stats)
		return ret

	def name(self):
		return str(tuple("{0}({1})".format(c.name(), c.weapon["name"]) for c in self.chars))

	def score(self):
		pass




class Artifact_Set(Enum):
	CRIMSON_4 = 1
	BLIZZARD_4 = 2
	SHIM_4 = 3


class Artifacts:
	def __init__(self, piece_stats, sets):
		self.piece_stats = piece_stats
		self.sets = sets
		self.tot_stats = empty_stats
		for x in self.piece_stats:
			self.tot_stats += x

