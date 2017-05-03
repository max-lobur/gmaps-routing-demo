import os
import googlemaps
import traceback

bounds = os.environ['BOUND_CITY']
mode = os.environ.get('ROUTE_MODE', 'driving')
gmaps = googlemaps.Client(key=os.environ['GMAPS_KEY'])


class ProviderError(Exception):
    pass


class OutOfBounds(Exception):
    pass


def directions(orig, dest):
    _validate_bounds(orig, bounds)
    _validate_bounds(dest, bounds)

    try:
        steps = gmaps.directions(orig, dest, mode=mode)[0]['legs'][0]['steps']
    except Exception as e:
        traceback.print_exc()
        raise ProviderError(repr(e))

    points = []
    for step in steps:
        points.append((step['start_location']['lat'],
                       step['start_location']['lng']))
        points.append((step['end_location']['lat'],
                       step['end_location']['lng']))
    return points


def _validate_bounds(coord, bound_city):
    try:
        geo = gmaps.reverse_geocode(coord)[0]['address_components']
    except Exception as e:
        traceback.print_exc()
        raise ProviderError(repr(e))

    try:
        city = filter(lambda g: 'locality' in g['types'], geo)[0]['short_name']
        country = filter(lambda g: 'country' in g['types'], geo)[0]['short_name']
    except IndexError:
        raise OutOfBounds("Cannot determine city or country. "
                          "Location must be within {}".format(bound_city))
    cur_city = "{},{}".format(city, country)
    if cur_city != bound_city:
        raise OutOfBounds("Location must be within {}, "
                          "but {}{} given".format(bound_city, cur_city, coord))
