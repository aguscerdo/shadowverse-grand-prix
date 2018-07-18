from tools import *
import argparse
import pandas

def main(folder, stages):
    stages = int(stages)
    # # Stage 1
    if stages in [0, 1]:
        path = folder + "/stage1.csv"
        df1 = r_csv(path)
        cleaning_time(df1, path)

    # Stage 2
    if stages in [0, 2]:
        path = folder + "/stage2.csv"
        df1 = r_csv(path)
        cleaning_time(df1, path)

# ----------------------------------------------------------------- #
def cleaning_time(df_h, path):
    def occurs(s, line):
        return line.count(s)

    # Initial per line fixing
    if "Wins" not in df_h.columns:
        print("Adding wins")
        with open(path, 'r') as file:
            lines = [x.strip() for x in file.readlines()]

        turn = has_first(df_h)
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
            ltmp = ltmp + '\n'
            print(ltmp)
            lines[i] = ltmp

        # Flush the changes
        with open(path, 'w') as file:
            file.writelines(lines)

    print("Top Decks")
    df_popular = most_popular_n(verticalize(df_h))
    phead(df_popular, 10)

    with open(path, 'r') as file:
        content = file.read()

    for key, val in reversed(list(df_popular.items())):
        print("\nDeck: {} -- Count: {}".format(key, val))

        user_input = str(input("Change '{}' to (empty to skip, Q to exit): ".format(key[1])))
        if not user_input:
            continue
        if user_input == "Q":
            break

        content = content.replace(",{},".format(key[1]), ",{},".format(user_input))

    with open(path, 'w') as file:
        file.write(content)
        print("Write successful")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', nargs='?')
    parser.add_argument('-s', '--stage', default=0)
    args = parser.parse_args()
    main(args.folder, args.stage)


