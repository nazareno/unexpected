__author__ = 'nazareno'

import csv


def convert_to_artist_network(input_file, output_file):
    csvreader = csv.reader(open(input_file, "rb"))
    csvwriter = csv.writer(open(output_file, "w"), quoting=csv.QUOTE_NONNUMERIC)

    bybond = {}

    for row in csvreader:
        bondid = row[0]
        if not bondid in bybond.keys():
            bybond[bondid] = {'artists':[], 'roles':set()}
        bybond[bondid]['artists'].append(row[1])
        bybond[bondid]['roles'].add(row[2])

    for bondid in bybond.keys():
        artists = bybond[bondid]['artists']
        roles = str(bybond[bondid]['roles']) #''.join("%s" % ', '.join(x) for x in bybond[bondid]['roles'])

        for i in range(len(artists)):
            for j in range(i+1, len(artists)):
                if artists[i] != artists[j]:
                    csvwriter.writerow([artists[i], artists[j], bondid, roles])



if __name__ == '__main__':
    convert_to_artist_network("data/connections-wnames-novarious.csv", "artist-network.csv")