import os
import urlparse
import requests
import redis
from PIL import Image
from StringIO import StringIO
from flask import Flask, request, send_file, redirect, render_template

#----------------------------------------
# Initialization
#----------------------------------------

REDIS_URL = urlparse.urlparse(os.environ.get('REDISCLOUD_URL', 'redis://:@localhost:6379/'))

app = Flask(__name__)

# Debug is set to either true or false depending on the env
if os.environ.get('DEVELOPMENT'):
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False

#----------------------------------------
# Helper functions.
#----------------------------------------
def ratio(height, width):
    ratio = float(width) / float(height)
    return ratio


def sanitze(value):
    # Make sure people don't crash the server with huge image sizes.
    value = int(value)
    if value > 400:
        value = 400
    return value


def measurements(image, width=None, height=None):
    # Get the current image size.
    (current_width, current_height) = image.size
    ratio = float(current_width) / float(current_height)

    #If nothing is passed in, set the width.
    if not width and not height:
        width = 150

    # If only the width passed in, calculate the new height.
    if width:
        width = sanitze(width)
        height = int(width / ratio)

    # If only the height passed in, calculate the new width.
    elif height:
        height = sanitze(height)
        width = int(height * ratio)
    return (width, height)


#----------------------------------------
# Routes
#----------------------------------------
@app.route("/")
def hello():
    url = request.args.get('link')
    # Have they entered a url?
    if not url:
        return render_template('index.html')
    try:
        width = request.args.get('width')
        height = request.args.get('height')
        # Generate a key for redis based on width, height and url.
        key = "{}-{}-{}".format(url, width, height)
        # Open redis.
        r = redis.StrictRedis(
            host=REDIS_URL.hostname, port=REDIS_URL.port,
            password=REDIS_URL.password)
        # Have we already cached the image?
        cached = r.get(key)
        if cached:
            # Get the image out of the cache.
            buffer_image = StringIO(cached)
            buffer_image.seek(0)
        else:
            # Download the image.
            response = requests.get(url)
            # Open the image.
            image = Image.open(StringIO(response.content))
            # Calculate the desired height and width of the image.
            desired_width, desired_height = measurements(image, width, height)
            buffer_image = StringIO()
            print "Numbers is", desired_width, desired_height
            resized_image = image.resize((desired_width, desired_height), Image.ANTIALIAS)
            resized_image.save(buffer_image, 'JPEG', quality=90)
            buffer_image.seek(0)
            # Store the image in redis, set to expire in 5 hours.
            r.setex(key, (60*60*5), buffer_image.getvalue())
        # Serve the image.
        return send_file(buffer_image, mimetype='image/jpeg')
    except:
        # If something went horribly wrong.
        # Let's just redirect them to the url.
        return redirect(url)


#----------------------------------------
# launch - used in dev.
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    app.run(host='0.0.0.0', port=port)
