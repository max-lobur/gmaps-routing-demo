from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from flask_cache import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import maps


app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={"CACHE_TYPE": "filesystem",
                           "CACHE_DIR": "./api_cache"})
limiter = Limiter(app, key_func=get_remote_address,
                  storage_uri="memory://")


def coord(raw_coord):
    try:
        lat, lon = raw_coord.split(",")
        lat, lon = float(lat), float(lon)
        assert -85.0 < lat < 85.0
        assert -180.0 < lon < 180.0
        return lat, lon
    except Exception:
        raise ValueError("Coordinate must be in format "
                         "latitude(-90:90),longitude(-180:180)")


class Directions(Resource):
    decorators = [limiter.limit("5 per minute")]

    @cache.cached(timeout=60*60*24, key_prefix=lambda *a, **kw: request.url)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('orig', type=coord, location='args', required=True)
        parser.add_argument('dest', type=coord, location='args', required=True)
        args = parser.parse_args(strict=True)
        try:
            res = maps.directions(args['orig'], args['dest'])
        except maps.OutOfBounds as e:
            return {"error": str(e)}, 400
        return {"polyline": res}

api.add_resource(Directions, '/')


if __name__ == '__main__':
    app.run(port=5000)
