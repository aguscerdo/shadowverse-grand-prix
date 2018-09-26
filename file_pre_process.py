from tools import *
import argparse
import re
import pandas as pd
from numpy import NaN
from os import listdir

def main(folder, stages):
	stages = int(stages)
	# # Stage 1
	if stages in [0, 1]:
		path = 'Data/{}/stage1.csv'.format(folder)
		print('\nCleaning Stage 1...')
		cleaning_time(path)

	# Stage 2
	if stages in [0, 2]:
		path = 'Data/{}/stage2.csv'.format(folder)
		print('\nCleaning Stage 2...')
		cleaning_time(path)
		
	# Finals
	if stages in [0, 3]:
		path = 'Data/{}/finalsa.csv'.format(folder)
		print('\nCleaning Finals A...')
		cleaning_time(path)
		
		path = 'Data/{}/finalsb.csv'.format(folder)
		print('\nCleaning Finals B...')
		cleaning_time(path)


# ----------------------------------------------------------------- #
def cleaning_time(path):
	df = r_csv(path)
	if "Wins" not in df.columns:
		turn = has_first(df)
		add_columns(path, turn)

	global_fixes(path)
	per_entry(path)


def global_fixes(path):
	df = r_csv(path)

	# Replace '<deck> <class>' -> '<deck>' AND '<class>: <deck>' -> '<deck>'
	for c in ['Blood', 'Dragon', 'Forest', 'Haven',
			  'Portal', 'Rune', 'Shadow', 'Sword']:
		replace_dict = {
			r'(?i)([^ ]*)( +{}(craft)?)'.format(c): r'\1',
			r'(?i)^{}(craft)?: +([^ ]*)'.format(c): r'\2'
		}
		df.replace(replace_dict, regex=True, inplace=True)

	# Remove Trailing spaces
	replace_dict = {
		r'^(\s+)([^\s]*)': r'\2',
		r'([^\s]*)(\s+)$': r'\1'
	}
	df.replace(replace_dict, inplace=True, regex=True)

	# Capitalize first letter
	for i in ['', 1, 2, 3, 4, 5]:
		key = 'Archetype{}'.format(i)
		if key in df.columns:
			df[key] = df[key].str.title()

	# Remove bad links'
	if 'Link' in df.columns:
		df[~df.Link.isna() & df.Link.str.match(r'[^(http)]')] = NaN
		df[~df.Link.isna() & df.Link.str.match(r'^((?!(shadowverse|bagoum)).)*$')] = NaN

	w_csv(df, path)


def add_columns(path, turn):
	df = r_csv(path)

	# Add Wins column
	df['Wins'] = (df == 'Won').T.sum()
	df.replace('Won', 1, inplace=True)
	df.replace('Lost', 0, inplace=True)

	# Add First column
	if turn:
		df['First'] = (df == 'Won').T.sum()
		df.replace('First', 1, inplace=True)
		df.replace('Second', 2, inplace=True)

	w_csv(df, path)


def per_entry(path):
	df = r_csv(path)
	df_popular = most_popular_n(verticalize(df))
	df_popular.sort_index(0, 0, inplace=True)

	current_class = ""
	for key, val in list(df_popular.items()):
		if key[0] != current_class:
			current_class = key[0]
			print("\n-------------------- {} --------------------".format(current_class))
			curr_df = df_popular.loc[current_class]
			curr_df.sort_values(ascending=False, inplace=True)
			phead(curr_df)
		
		print("\nDeck: {} -- Count: {}".format(key, val))
		user_input = str(input("Change '{}' for {} to (empty to skip, Q to exit, null for empty): ".format(key[1], key[0])))
		
		if not user_input.strip():
			continue
		elif user_input.lower() == "q":
			break
		elif user_input.lower() == 'null':
			user_input = ''

		for i in ['', 1, 2, 3, 4, 5]:
			deck_i = 'Class{}'.format(i)
			archetype_i = 'Archetype{}'.format(i)
			if archetype_i not in df.columns: continue
			df.loc[(df[deck_i] == key[0]) & (df[archetype_i] == key[1]), archetype_i] = user_input

	w_csv(df, path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('folder', nargs='?')
	parser.add_argument('-s', '--stage', default=0)
	args = parser.parse_args()
	
	if args.folder is None:
		folders = [f for f in listdir('Data') if not f.startswith('.')]
	else:
		folders = [args.folder]
	
	for f in folders:
		print("Cleaning {}".format(f))
		main(f, args.stage)