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
1. Production app would run behind nginx reverse proxy / AWS ELB / Other infra.
2. Rate limiting / Caching / SSL termination would be done by the infra. 
Motivation: the less traffic come through infra down to the app - the better 
response time / DOS resistance this setup will have. It is common to have infra 
responsible for these aspects because they are similar for most of the apps and 
are well-implemented as a 3rd-party / IaaS solutions.
    * Nginx SSL termination [config sample](nginx.ssl-termination.sample),[Tutorial](https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html)
    * AWS SSL termination [Tutorial](https://aws.amazon.com/blogs/aws/elastic-load-balancer-support-for-ssl-termination/)
    * Nginx rate limiting  [config sample](nginx.rate-limit.sample), [Tutorial](https://medium.freecodecamp.com/nginx-rate-limiting-in-a-nutshell-128fe9e0126c) 
    * AWS rate limiting [Tutorial](http://docs.aws.amazon.com/waf/latest/developerguide/tutorials-rate-based-blocking.html)
    * Nginx caching (implemented with memcached) [config sample](nginx.cache.sample), [Tutorial](http://blog.octo.com/en/http-caching-with-nginx-and-memcached/)
    * AWS caching [Tutorial](http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html), [Overview](https://aws.amazon.com/caching/)
3. Provider errors are only logged, they must remain 5xx and be
handled on a load-balancer: remove bad worker basing on retcode/healthcheck hoping
that this error is localized to one of the workers.
