__author__ = 'nazareno'

import csv

def __get_string_set(set):
    return ', '.join(set)

def convert_to_artist_network(input_file, output_file):
    print "saving network"
    csvreader = csv.reader(open(input_file, "rb"))
    csvwriter = csv.writer(open(output_file, "w"), quoting=csv.QUOTE_NONNUMERIC)

    bybond = {}
    id2name = {}
    connections_count = 0
    duplicates_count = 0

    for row in csvreader:
        bondid = row[0]
        if not bondid in bybond.keys():
            bybond[bondid] = {'artists':[], 'roles':{}}
        bybond[bondid]['artists'].append(row[1])
        bybond[bondid]['roles'].setdefault(row[1], set()).add(row[2])
        id2name[bondid] = row[3]
        id2name[row[1]] = row[4] # artist id to name

    for bondid in bybond.keys():
        connections = []
        artists = bybond[bondid]['artists']

        for i in range(len(artists)):
            for j in range(i+1, len(artists)):
                if artists[i] != artists[j]:
                    connection = [artists[i], artists[j], bondid, __get_string_set(bybond[bondid]['roles'][artists[i]]), __get_string_set(bybond[bondid]['roles'][artists[j]])]
                    if not connection in connections:
                        connections_count+=1
                        connections.append(connection)
                        csvwriter.writerow(connection)
                    else:
                        duplicates_count += 1

    print "found %i connections (%i duplicated connections were discared)" % (connections_count, duplicates_count)


    print "saving id to name mapping"
    id2name_file = csv.writer(open("id-name.csv", "w"))
    for id in id2name.keys():
        id2name_file.writerow([id, id2name[id]])

if __name__ == '__main__':
    convert_to_artist_network("data/connections-wnames-novarious.csv", "artist-network.csv")