import pyechonest.song
import urllib2
import simplejson

import util

from messenger import messenger

def fetch_songs_from_artists(genres_artists):
    """
    Transforms genres -> artists..

    {
        'metal': ['megadeth', 'opeth'],
        'jazz': ['Louis Armstrong', 'Billy Holiday'],
        ...
    }

    ..to genres -> songs..

    {
        'metal': ['megadeth_song_1', 'megadeth_song_2', 'opeth_song_1', ...],
        'jazz': ['armstrong_song1', 'holiday_song1', ...],
        ...
    }

    ..by fetching all available songs for the corresponding artists from
    EchoNest.
    """
    genres_songs = {}

    for genre, artists in genres_artists.iteritems():
        messenger.print_subtask('Genre: %s' % genre)
        genres_songs[genre] = []

        for artist in artists:
            messenger.print_subtask('Artist: %s' % artist, relative_level=1)
            artist_songs = pyechonest.song.search(artist=artist)
            genres_songs[genre].extend(artist_songs)

    return genres_songs

def fetch_song_analysis(song):
    """
    Fetches song analysis of `song` from EchoNest.

    Args:
        song: a pyechonest Song object
    Returns:
        analysis: a dictionary containing all info EchoNest provides for the
                  song in question
    """
    opener = urllib2.build_opener()

    title = song.title if song.title else 'Unknown title'
    artist = song.artist_name if song.artist_name else 'Unknown artist'
    messenger.print_subtask('%s - %s' % (artist, title))

    song.get_audio_summary()
    analysis_url = song.audio_summary['analysis_url']

    request = urllib2.Request(analysis_url)
    f = opener.open(request)
    analysis = simplejson.load(f)

    analysis['audio_summary'] = song.audio_summary

    return analysis
