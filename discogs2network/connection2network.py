__author__ = 'nazareno'

import csv


def convert_to_artist_network(input_file, output_file):
    print "saving network"
    csvreader = csv.reader(open(input_file, "rb"))
    csvwriter = csv.writer(open(output_file, "w"), quoting=csv.QUOTE_NONNUMERIC)

    bybond = {}
    id2name = {}

    for row in csvreader:
        bondid = row[0]
        if not bondid in bybond.keys():
            bybond[bondid] = {'artists':[], 'roles':set()}
        bybond[bondid]['artists'].append(row[1])
        bybond[bondid]['roles'].add(row[2])
        id2name[bondid] = row[3]
        id2name[row[1]] = row[4] # artist id to name

    for bondid in bybond.keys():
        artists = bybond[bondid]['artists']
        roles = ', '.join(bybond[bondid]['roles'])

        for i in range(len(artists)):
            for j in range(i+1, len(artists)):
                if artists[i] != artists[j]:
                    csvwriter.writerow([artists[i], artists[j], bondid, roles, id2name[artists[i]], id2name[artists[j]]])

    print "saving id to name mapping"
    id2name_file = csv.writer(open("id-name.csv", "w"))
    for id in id2name.keys():
        id2name_file.writerow([id, id2name[id]])

if __name__ == '__main__':
    convert_to_artist_network("data/connections-wnames-novarious.csv", "artist-network.csv")