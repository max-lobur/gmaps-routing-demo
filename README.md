## Map routing demo
Google maps API routing demo app built with flask

#### Installation
```bash
mkvirtualenv map-demo
pip install -r requirements.txt
```

#### Starting an app
A Google API key can be obtained [here](https://developers.google.com/maps/documentation/directions/)
```bash
export GMAPS_KEY=<your_api_key>
export BOUND_CITY="Vinnytsia,UA"
python app/api.py
```

#### Testing with curl
```bash
curl -X GET "http://127.0.0.1:5000/?orig=49.2314,28.4017&dest=49.2322,28.4737"

curl -X GET "http://127.0.0.1:5000/?orig=49.2314,28.4017&dest=49.982504,36.259318"
```

#### Notes:
1. Production app would run behind nginx proxy
2. Rate limiting / Caching / SSL termination would be done via the same nginx proxy and
use external storate e.g. Redis
3. Provider errors are only logged, they must remain 5xx and be
handled on a load-balancer: remove bad worker basing on retcode/healthcheck hoping
that this error is localized to one of the workers.
