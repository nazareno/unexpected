__author__ = 'nazareno'

import pickle
import csv


def output_release(release, csv_writer):
    title = release['title']
    sources = release['artists'].values()

    if len(release['extraartists'].keys()) == 0:
        return

    others = release['extraartists']['artist']
    if not isinstance(others, list):
        others = [others]

    for bond_person in others:
        bondid = bond_person['id']
        bondname = bond_person['name']
        bondrole = bond_person['role']

        for artist in sources:
            if isinstance(artist, list):
                artist = artist[0]
            source_id = artist['id']
            source_name = artist['name']
            if bondid != source_id:
                csv_writer.writerow([bondid, source_id, bondrole.encode("UTF-8"), bondname.encode("UTF-8"), source_name.encode("UTF-8"), title.encode("UTF-8")])


def release_pickle2connection(source_file, dest_file = "connections-wnames.csv"):
    connections = open(dest_file, "w")
    csv_writer = csv.writer(connections, quoting=csv.QUOTE_NONNUMERIC)

    f = open(source_file, "rb" )
    while True:
        try:
            release = pickle.load(f)
            output_release(release, csv_writer)
        except EOFError:
            break


if __name__ == '__main__':
    release_pickle2connection("data/our-releases-jazz-60s-to-80s.pickle")