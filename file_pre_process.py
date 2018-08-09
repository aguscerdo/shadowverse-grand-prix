from tools import *
import argparse
import re

def main(folder, stages):
    stages = int(stages)
    # # Stage 1
    if stages in [0, 1]:
        path = folder + "/stage1.csv"
        df1 = r_csv(path)
        cleaning_time(path)

    # Stage 2
    if stages in [0, 2]:
        path = folder + "/stage2.csv"
        cleaning_time(path)

# ----------------------------------------------------------------- #
def cleaning_time(path):
    df = r_csv(path)
    if "Wins" not in df.columns:
        turn = has_first(df)
        add_wins_column(path, turn)

    global_fixes(path)

    per_entry(path)


def global_fixes(path):
    # Common global Cleaning
    with open(path, 'r') as file:
        content = file.read()

    # Replace ',<deck> <class>,' --> ',<deck>,'
    for c in ['Shadowcraft', 'Runecraft', 'Forestcraft', 'Swordcraft',
              'Dragoncraft', 'Havencraft', 'Portalcraft', 'Bloodcraft']:
        content = re.sub(r'(?i)([^,])( +{}),'.format(c), r'\1,', content)

    with open(path, 'w') as file:
        file.write(content)



def add_wins_column(path, turn):
    def occurs(s, line):
        return line.count(s)

    # Initial per line fixing
    print("Adding wins")
    with open(path, 'r') as file:
        lines = [x.strip() for x in file.readlines()]

    for i, l in enumerate(lines):
        if i:
            # Append Wins to end
            win_count = occurs("Won", l)
            ltmp = "{},{}".format(l, win_count)
            ltmp = ltmp.replace("Won", '1').replace("Lost", '0')
            # Append times going first
            if turn:
                first_count = occurs('First', l)
                ltmp = "{},{}".format(ltmp, first_count)
                ltmp = ltmp.replace('First', '1').replace('Second', '2')
        else:
            ltmp = l + ",Wins"
            if turn:
                ltmp = ltmp + ",First"
        lines[i] = re.sub(r' +, +',',',ltmp+'\n')

    # Flush the changes
    with open(path, 'w') as file:
        file.writelines(lines)


def per_entry(path):
    df = r_csv(path)
    # Per entry global Cleaning
    print("Top Decks")
    df_popular = most_popular_n(verticalize(df))
    phead(df_popular, 10)

    with open(path, 'r') as file:
        content = file.read()

    for key, val in reversed(list(df_popular.items())):
        print("\nDeck: {} -- Count: {}".format(key, val))

        user_input = str(input("Change '{}' for {} to (empty to skip, Q to exit, null for empty): ".format(key[1], key[0])))
        if not user_input.strip():
            continue
        elif user_input.lower() == "q":
            break
        elif user_input.lower() == 'null':
            user_input = ''

        content = re.sub(r',{},"?{}"?,'.format(key[0], key[1]), r',{},{},'.format(key[0], user_input))

    with open(path, 'w') as file:
        file.write(content)
        print("Write successful")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs='?')
    parser.add_argument('-s', '--stage', default=0)
    args = parser.parse_args()
    main(args.folder, args.stage)
