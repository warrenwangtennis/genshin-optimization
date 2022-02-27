from core import *
from char_bps import *
from collections import defaultdict
import random

char = HuTao()

def score(build, dbg=False):
	global_.dbg = dbg
	global_.dmg_log = [] if dbg else None


	build.extra_stats = empty_stats

	char.set_build(build)

	# if build.artifacts.tot_stats.d['er'] < 30: # no other source of er
	# 	return build.artifacts.tot_stats.d['er'] - 30



	# persistent
	build.extra_stats = empty_stats + Stats({
		'dmgp': 33, # a4
		'atkf': 6.26/100 * char.get_hp(), # hu tao e
		'res': 20 # zhongli e
	})

	s = build.extra_stats.d

	if Artifact_Set.CRIMSON_4 in build.artifacts.sets:
		s['dmgp'] += 15 + 7.5
		s['vapep'] += 15
	if Artifact_Set.SHIM_4 in build.artifacts.sets:
		s['atkp'] += 18
		s['cap'] += 50

	tot = 0

	# zhongli
	s['em'] += 120 # instructor
	
	# mona
	s['dmgp'] += 60 # q
	s['vapep'] += 15 # c1
	s['atkp'] += 48 + 20 # ttds, tenacity

	tot += char.dmg_ca()

	if dbg:
		global_.dmg_log.append(("total", tot))
		for dmg_type, dmg_val in global_.dmg_log:
			print("{0:15} {1:-12.1f} {2:-8.2f}%".format(dmg_type, dmg_val, dmg_val/tot*100))
	return tot

dbg = False

artifactss = [
    Artifacts([
	    Stats({'hpf': 4780, 'cd': 20.2, 'em': 21, 'hpp': 11.1}),
	    Stats({'atkf': 311, 'hpp': 4.1, 'er': 6.5, 'em': 79, 'cd': 20.2}),
	    Stats({'hpp': 46.6, 'cr': 3.9, 'cd': 13.2, 'em': 79, 'atkf': 16}),
	    Stats({'dmgp': 46.6, 'cr': 5.8, 'hpf': 1046, 'cd': 13.2, 'hpp': 4.1}),
	    Stats({'cr': 31.1, 'em': 58, 'hpf': 239, 'er': 4.5, 'cd': 27.2})
    ], [Artifact_Set.CRIMSON_4]),
    Artifacts([
	    Stats({'hpf': 4780, 'atkp': 11.1, 'cr': 2.7, 'cd': 33.4}),
	    Stats({'atkf': 311, 'cd': 14, 'cr': 9.7, 'atkp': 16.3, 'em': 23}),
	    Stats({'hpp': 46.6, 'cd': 14, 'atkf': 18, 'cr': 10.1}),
	    Stats({'dmgp': 46.6, 'em': 54, 'hpf': 209, 'hpp': 11.1, 'cd': 12.4}),
	    Stats({'cr': 31.1, 'em': 86, 'atkf': 31, 'cd': 7.8})
    ], [Artifact_Set.CRIMSON_4]),
    Artifacts([
	    Stats({'hpf': 4780, 'hpp': 11.1, 'cr': 7.4, 'cd': 21.8}),
	    Stats({'atkf': 311, 'hpf': 269, 'cr': 9.7, 'cd': 20.2}),
	    Stats({'em': 187, 'hpf': 10.5, 'cd': 14.8, 'atkp': 10.5}),
	    Stats({'dmgp': 46.6, 'hpf': 598, 'cr': 3.5, 'atkf': 14, 'cd': 26.4}),
	    Stats({'cr': 31.1, 'atkp': 14, 'em': 68, 'cd': 5.4, 'hpp': 10.5})
    ], [Artifact_Set.SHIM_4])
]

for artifacts in artifactss:
	# build = Build(char, dragons_bane(5, 1), artifacts, None)
	build = Build(char, homa(1), artifacts, None)
	z = score(build, True)
	print(z)

exit()

samples = 100000

"""
hpp sands, crimson 4:
139996.03519287988
{'cr': 12, 'cd': 13}

hpp sands, shim 4:
145411.5346451296
{'cr': 12, 'cd': 12, 'em': 1}

em sands, shim 4:
146342.64324560203
{'cr': 12, 'cd': 12, 'hpp': 1}

"""

res = []
for i in range(samples):
	piece_stats = []

	sub_nums = []

	subs = ['cr', 'cd', 'hpp', 'em']
	weights = [3, 3, 1, 2]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'hpf': main_vals['hpf'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})

	subs = ['cr', 'cd', 'hpp', 'em']
	weights = [3, 3, 1, 2]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'atkf': main_vals['atkf'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	subs = ['cr', 'cd', 'hpp', 'hpf']
	weights = [3, 3, 1, 0]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'em': main_vals['em'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	subs = ['cr', 'cd', 'hpp', 'em']
	weights = [4, 4, 1, 3]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'dmgp': main_vals['dmgp'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})

	subs = ['cd', 'hpp', 'em', 'hpf']
	weights = [4, 1, 2, 0]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'cr': main_vals['cr'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	artifacts = Artifacts(piece_stats, [Artifact_Set.SHIM_4])


	build = Build(char, homa(1), artifacts, None)

	z = score(build, False)

	res.append((z, sub_nums))

res.sort(key=lambda x: x[0])

for x in res[:-10:-1]:
	print(x[0])
	subs = defaultdict(int)
	for y in x[1]:
		for k, v in y.items():
			subs[k] += v
	print(dict(subs))
	print()