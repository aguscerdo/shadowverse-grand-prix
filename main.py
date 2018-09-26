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
		path = 'Data/{}/stage1.csv'.format(folder)
		df = t.r_csv(path)
		analyze_horizontal(df, 1, folder)

		dfv = t.verticalize(df)
		analyze_vertical(dfv, 1, folder)

	# Stage 2
	if stages in [0, 2]:
		print('\tStage 2...')
		path = 'Data/{}/stage2.csv'.format(folder)
		df = t.r_csv(path)
		analyze_horizontal(df, 2, folder)

		dfv = t.verticalize(df)
		analyze_vertical(dfv, 2, folder)

	# Finals
	if stages in [0, 3]:
		print('\tFinal stage A...')
		path = 'Data/{}/finalsa.csv'.format(folder)
		df = t.r_csv(path)
		analyze_horizontal(df, 3, folder)

		dfv = t.verticalize(df)
		analyze_vertical(dfv, 3, folder)

		print('\tFinal stage B...')
		path = 'Data/{}/finalsb.csv'.format(folder)
		df = t.r_csv(path)
		analyze_horizontal(df, 4, folder)

		dfv = t.verticalize(df)
		analyze_vertical(dfv, 4, folder)
		
		
if __name__ == '__main__':
	"""
	Usage: 'python3 main.py FOLDER_NAME [-s {0|1|2}]
	
	- FOLDER_NAME is container where data is: e.g. BOTS_R_1
	- stage [-s] is which stages to analyze, 0 for all, 1 for stage 1 only, 2 for stage 2 only, 3 for Finals
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
			
		if not os.path.exists("Data/{}/plots_finals_a".format(f)):
			os.mkdir("Data/{}/plots_finals_a".format(f))
			print("\tCreated plots_finals_a folder")
		
		if not os.path.exists("Data/{}/plots_finals_b".format(f)):
			os.mkdir("Data/{}/plots_finals_b".format(f))
			print("\tCreated plots_finals_b folder")
		main(f, args.stage)
