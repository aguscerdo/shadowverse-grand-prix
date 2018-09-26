import pandas as pd
import tools
from analysis import *
import os
import argparse
from os import getcwd, listdir

def main(folder, stages):
	stages = int(stages)
	# # Stage 1
	if stages in [0, 1]:
		create_plots_folder(folder, 'stage1')
		
		print('\tStage 1...')
		path = 'Data/{}/stage1.csv'.format(folder)
		df = tools.r_csv(path)
		analyze_horizontal(df, 1, folder)

		dfv = tools.verticalize(df)
		analyze_vertical(dfv, 1, folder)

	# Stage 2
	if stages in [0, 2]:
		path = 'Data/{}/stage2.csv'.format(folder)
		if os.path.exists(path):
			create_plots_folder(folder, 'stage2')

			print('\tStage 2...')
			df = tools.r_csv(path)
			analyze_horizontal(df, 2, folder)
	
			dfv = tools.verticalize(df)
			analyze_vertical(dfv, 2, folder)

	# Finals
	if stages in [0, 3]:
		# ---- Finals A ----
		path = 'Data/{}/finalsa.csv'.format(folder)
		if os.path.exists(path):
			create_plots_folder(folder, 'finals_a')

			print('\tFinal stage A...')
			df = tools.r_csv(path)
			analyze_horizontal(df, 3, folder)
	
			dfv = tools.verticalize(df)
			analyze_vertical(dfv, 3, folder)

		# ---- Finals B ----
		path = 'Data/{}/finalsb.csv'.format(folder)
		if os.path.exists(path):
			create_plots_folder(folder, 'finals_b')
			
			print('\tFinal stage B...')
			df = tools.r_csv(path)
			analyze_horizontal(df, 4, folder)
	
			dfv = tools.verticalize(df)
			analyze_vertical(dfv, 4, folder)
		
		
def create_plots_folder(folder, stage):
	path = "Data/{}/plots_{}".format(folder, stage)
	if not os.path.exists(path):
		os.mkdir(path)
		print("\tCreated plots_{} folder".format(stage))
		
		
if __name__ == '__main__':
	"""
	Usage: 'python3 main.py FOLDER_NAME [-s {0|1|2}]
	
	- FOLDER_NAME is container where data is: e.g. BOTS_R_1.
	- stage [-s] is which stages to analyze, 0 for all, 1 for stage 1 only, 2 for stage 2 only, 3 for Finals.
	- plot [-p] plot while processing. Plotting might use a lot of ram if analyzing ALL folders.
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument('folder', nargs='?', help='Folder name to examine. Empty for ALL')
	parser.add_argument('-s', '--stage', default=0, help='Stage number: 0 for all; 1 for S1; 2 for S2; 3 for Finals')
	parser.add_argument('-p', '--plot', default=False, action='store_true', help='Plot while processing')
	args = parser.parse_args()

	if args.folder is None:
		folders = [f for f in listdir('Data') if not f.startswith('.')]
	else:
		folders = [args.folder]
	tools._change_do_plot(args.plot)
	
	for f in folders:
		print("Analyzing {}".format(f))

		# Check and create plot folders
		main(f, args.stage)


