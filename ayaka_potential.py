from core import *
from char_bps import *
from collections import defaultdict
import random

char = Ayaka()

def score(build, dbg=False):
	global_.dbg = dbg
	global_.dmg_log = [] if dbg else None

	# print(build.get_stats())

	build.extra_stats = empty_stats

	char.set_build(build)

	if build.artifacts.tot_stats.d['er'] < 30: # no other source of er
		return build.artifacts.tot_stats.d['er'] - 30



	# persistent
	build.extra_stats = empty_stats + Stats({
		'dmgp': 18 + 0.04*1010, # a4 (keep 100% uptime), kazuha
		'cr': 15, # cryo resonance
		'res': 40, # vv
	})

	s = build.extra_stats.d

	# if 'mistsplitter' in build.weapon:
	# 	s['dmgp'] += refine_val(12, 24, build.weapon['mistsplitter'])

	if Artifact_Set.BLIZZARD_4 in build.artifacts.sets:
		s['cr'] += 40
		s['dmgp'] += 15

	tot = 0

	# diona
	s['atkp'] += 20 # noblesse
	
	# mona
	s['dmgp'] += 60 # q
	s['atkp'] += 48 + 20 # ttds, tenacity

	tot += char.dmg_na()

	# mistsplitter 0 -> 3
	if 'mistsplitter' in build.weapon:
		s['dmgp'] += refine_val(28, 56, build.weapon['mistsplitter'])

	tot += char.dmg_q()

	# return char.dmg_q_tick()

	tot += char.dmg_e()

	s['nap'] += 30 # ayaka a1
	s['cap'] += 30 # ayaka

	tot += char.dmg_n4c(1)

	s['dmgp'] -= 60 # -mona q
	s['atkp'] -= 48 + 20 # -mona ttds, tenacity
	s['atkp'] -= 20 # -diona noblesse

	tot += char.dmg_n4c(1)

	s['nap'] -= 30 # ayaka a1
	s['cap'] -= 30 # ayaka

	tot += char.dmg_n4c(2)

	# mistsplitter 3 -> 2
	if 'mistsplitter' in build.weapon:
		s['dmgp'] -= refine_val(12, 24, build.weapon['mistsplitter'])


	tot += char.dmg_e()

	if dbg:
		global_.dmg_log.append(("total", tot))
		for dmg_type, dmg_val in global_.dmg_log:
			print("{0:15} {1:-12.1f} {2:-8.2f}%".format(dmg_type, dmg_val, dmg_val/tot*100))

		# for x in all_stats:
		# 	print(x.d)

	return tot

dbg = False

subss = [{'atkp': 15.7, 'atkf': 29, 'cr': 38.9, 'cd': 115.8-62.2, 'er': 46},
{'atkp': 0, 'atkf': 35, 'cr': 38.1, 'cd': 132.9-62.2, 'er': 33},
{'atkp': 15.7, 'atkf': 35, 'cr': 28.4, 'cd': 142.2-62.2, 'er': 30}
]

for subs in subss:
	piece_stats = [Stats({'atkp': 46.6, 'atkf': 311, 'dmgp': 46.6, 'cd': 62.2}), Stats(subs)]
	artifacts = Artifacts(piece_stats, [Artifact_Set.BLIZZARD_4])
	build = Build(char, mistsplitter(1), artifacts, None)
	z = score(build, True)
	print(z, subs)
exit()

samples = 100000

res = []
for i in range(samples):
	piece_stats = []

	sub_nums = []

	subs = ['cr', 'cd', 'atkp', 'er']
	weights = [1, 10, 2, 2]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'hpf': main_vals['hpf'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})

	subs = ['cr', 'cd', 'atkp', 'er']
	weights = [1, 10, 2, 2]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'atkf': main_vals['atkf'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	subs = ['cr', 'cd', 'atkf', 'er']
	weights = [1, 10, 0, 2]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'atkp': main_vals['atkp'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	subs = ['cr', 'cd', 'atkp', 'er']
	weights = [1, 10, 2, 2]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'dmgp': main_vals['dmgp'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	subs = ['cr', 'atkf', 'atkp', 'er']
	weights = [1, 0, 1, 1]
	nums = [1, 1, 1, 1]
	for idx in random.choices(range(4), weights, k=5):
		nums[idx] += 1
	piece_stats.append(Stats({'cd': main_vals['cd'], **{subs[idx]: sub_vals_max[subs[idx]] * nums[idx] for idx in range(4)}}))
	sub_nums.append({subs[idx]: nums[idx] - 1 for idx in range(4) if nums[idx] > 1})


	artifacts = Artifacts(piece_stats, [Artifact_Set.BLIZZARD_4])


	build = Build(char, mistsplitter(1), artifacts, None)

	z = score(build, False)

	res.append((z, sub_nums))

res.sort(key=lambda x: x[0])

for x in res[:-30:-1]:
	print(x[0])
	subs = defaultdict(int)
	for y in x[1]:
		for k, v in y.items():
			subs[k] += v
	print(dict(subs))
	print()