Strava awards thing

To setup (on dev)
* Install ```gunicorn``` 
* Install ```ngrok``` 
* Run ```./run``` and then ```ngrok http 8000```
** This should be done from the folder with ```wsgi.py```
** This will forward traffic from ngrok to the server (need this for subscriptions) 

