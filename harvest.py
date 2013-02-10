import os
import csv
import simplejson

import collector
import genres_artists
import util
import settings

from messenger import messenger

def main():
    util.set_api_key()

    messenger.print_task('Fetching song list')
    genres_songs = collector.fetch_songs_from_artists(genres_artists.MAP)

    messenger.print_task('Fetching songs analyses')
    try:
        with open(settings.REGISTRY) as fd:
            downloaded_songs = simplejson.load(fd)
    except JSONDecodeError:
        downloaded_songs = {}

    for genre, songs in genres_songs.iteritems():
        for ith_song, song in enumerate(songs):
            if song.id in downloaded_songs:
                continue

            try:
                analysis = collector.fetch_song_analysis(song)
            except Exception as exc:
                messenger.print_subtask_error(exc)
                continue

            analysis_file = '%s_%d.json' % (genre, ith_song)
            analysis_file = os.path.join(settings.ANALYSES_DIR, analysis_file)
            with open(analysis_file, 'w') as analysis_fd:
                simplejson.dump(analysis, analysis_fd)

            downloaded_songs[song.id] = analysis_file

            # save which songs have are already downloaded to avoid
            # re-downloading their analysis in the future.
            # Ugly and bad as hell. I could append lines to a file or use
            # sqlite but it does not worth it.
            with open(settings.REGISTRY, 'w') as fd:
                simplejson.dump(downloaded_songs, fd)

    messenger.print_task('Constructing dataset')
    analysis_files = os.listdir(settings.ANALYSES_DIR)

    # construct a dict behaving like an enum struct: {'genre': number}
    genres = set([filename.split('_')[0] for filename in analysis_files])
    genres -= settings.IGNORE_GENRES
    genres = dict([(genre, i) for i, genre in enumerate(genres)])

    with open(settings.DATASET_FILE, 'w') as dataset_fd:
        dataset_writer = csv.writer(dataset_fd)
        headers = util.song_features_names()
        dataset_writer.writerow(headers + ['genre'])

        for analysis_file in analysis_files:
            # dirty hack: get genre from filename
            song_genre = analysis_file.split('_')[0]
            if song_genre not in genres:
                continue

            file_path = os.path.join(settings.ANALYSES_DIR, analysis_file)
            with open(file_path) as fd:
                analysis = simplejson.load(fd)

            song_features = util.extract_features(analysis)
            # Construct a csv row containing all the features of a song, sorted
            # by feature name. The last column is a number representing a
            # specific genre.
            csv_row = [song_features[f] for f in headers]
            csv_row.append(genres[song_genre])
            dataset_writer.writerow(csv_row)

    print 'Done.'

if __name__ == '__main__':
    main()
