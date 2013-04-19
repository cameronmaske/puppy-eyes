import os
import urlparse
import requests
import redis
from PIL import Image
from StringIO import StringIO
from flask import Flask, request, send_file

#----------------------------------------
# initialization
#----------------------------------------

REDIS_URL = urlparse.urlparse(os.environ.get('REDISCLOUD_URL', 'redis://:@localhost:6379/'))

app = Flask(__name__)

# Debug is set to either true or false depending on the env
if os.environ.get('DEVELOPMENT'):
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False


#----------------------------------------
# controllers
#----------------------------------------


@app.route("/")
def hello():
    url = request.args.get('url')
    if not url:
        return "Woof woof!"
    # Open redis.
    r = redis.StrictRedis()
    # Have we already cached the image?
    cached = r.get(url)
    if cached:
        print "Got image from cache."
        buffer_image = StringIO(cached)
        buffer_image.seek(0)
    else:
        print "Downloading image."
        # Download the image.
        response = requests.get(url)
        # Open the image.
        image = Image.open(StringIO(response.content))
        # Get it's current size.
        (current_width, current_height) = image.size
        # We want a width of 150px.
        desired_width = 150
        # But we want to keep the ratio the same.
        ratio = float(current_width) / float(current_height)
        # Determine a new hegiht.
        height = int(desired_width / ratio)

        buffer_image = StringIO()
        resized_image = image.resize((desired_width, height), Image.ANTIALIAS)
        resized_image.save(buffer_image, 'JPEG', quality=90)
        buffer_image.seek(0)
        r.setex(url, (60*60*5), buffer_image.getvalue())

    return send_file(buffer_image, mimetype='image/jpeg')


#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    app.run(host='0.0.0.0', port=port)