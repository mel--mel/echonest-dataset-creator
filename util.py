import scipy
from pyechonest import config

import settings

def set_api_key():
    """
    Ensures there is an EchoNest API key available.
    """
    if settings.ECHO_NEST_API_KEY == '':
        settings.ECHO_NEST_API_KEY = raw_input("Echo nest api key: ")
    config.ECHO_NEST_API_KEY = settings.ECHO_NEST_API_KEY

def song_features_names():
    """
    Features extracted from a song.

    IMPORTANT: Each and every of this feature should be returned from
               extract_features().
    """
    return sorted([
        'danceability',
        'loudness',
        'energy',
        'speechiness',
        'loudness_max',
        'timbre_variance',
        'end_of_fade_in',
        'start_of_fade_out',
        'key_confidence',
        'tempo',
    ])

def extract_features(song_analysis):
    """
    Args:
        song_analysis: dictionary containing all info EchoNest provides
                       for the song in question
    Returns:
        features: dictionary containing the following features:
                  [danceability, loudness, energy, speechiness, loudness max
                  values mean, timbre variance]

    IMPORTANT: The features returned must much the ones return by
               song_features_names().
    """
    features = {}

    features['danceability'] = song_analysis['audio_summary']['danceability']
    features['loudness'] = song_analysis['audio_summary']['loudness']
    features['energy'] = song_analysis['audio_summary']['energy']
    features['speechiness'] = song_analysis['audio_summary']['speechiness']
    features['end_of_fade_in'] = song_analysis['track']['end_of_fade_in']
    features['start_of_fade_out'] = song_analysis['track']['start_of_fade_out']
    features['key_confidence'] = song_analysis['track']['key_confidence']
    features['tempo'] = song_analysis['track']['tempo']

    timbre_values = []
    loudness_max_values = []

    for segment in song_analysis['segments']:
        timbre_values.extend(segment['timbre'])
        loudness_max_values.append(segment['loudness_max'])

    features['loudness_max'] = scipy.array(loudness_max_values).mean()
    features['timbre_variance'] = scipy.array(timbre_values).var()

    return features
