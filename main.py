import pandas as pd
import tools as t
from analysis import *
import os
import argparse
from os import getcwd, listdir

def main(folder, stages):
	stages = int(stages)
	# # Stage 1
	if stages in [0, 1]:
		print('\tStage 1...')
		df1 = t.r_csv("Data/{}/stage1.csv".format(folder))
		analyze_horizontal(df1, 1, folder, 1)

		dfv1 = t.verticalize(df1)
		analyze_vertical(dfv1, 1, folder, 1)

	# Stage 2
	if stages in [0, 2]:
		print('\tStage 2...')
		df2 = t.r_csv("Data/{}/stage2.csv".format(folder))
		analyze_horizontal(df2, 2, folder, 2)

		dfv2 = t.verticalize(df2)
		analyze_vertical(dfv2, 2, folder, 2)


if __name__ == '__main__':
	"""
	Usage: 'python3 main.py FOLDER_NAME [-s {0|1|2}]
	
	- FOLDER_NAME is container where data is: e.g. BOTS_R_1
	- stage [-s] is which stages to analyze, 0 for all, 1 for stage 1 only, 2 for stage 2 only
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument('folder', nargs='?')
	parser.add_argument('-s', '--stage', default=0)
	args = parser.parse_args()

	if args.folder is None:
		folders = [f for f in listdir('Data') if not f.startswith('.')]
	else:
		folders = [args.folder]
	
	for f in folders:
		print("Analyzing {}".format(f))

		# Check and create plot folders
		if not os.path.exists("Data/{}/plots_stage1".format(f)):
			os.mkdir("Data/{}/plots_stage1".format(f))
			print("\tCreated plots_stage1 folder")
	
		if not os.path.exists("Data/{}/plots_stage2".format(f)):
			os.mkdir("Data/{}/plots_stage2".format(f))
			print("\tCreated plots_stage2 folder")
	
		main(f, args.stage)
