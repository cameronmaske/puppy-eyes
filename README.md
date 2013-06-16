Puppy eyes
----------

A simple image resizer service in flask using redis.

Demo
-------

Try the [demo](http://puppy-eyes.herokuapp.com/)!

On the demo site (or you local copy) you can turn this huge (1620 x 1080 image)

    http://images.cdn.fotopedia.com/flickr-4657421042-hd.jpg

Into a tiny one!

    http://puppy-eyes.herokuapp.com/?link=http://images.cdn.fotopedia.com/flickr-4657421042-hd.jpg


Install
-------

To install you require [Vagrant](http://downloads.vagrantup.com/tags/v1.1.5)(tested on 1.1.5).
To bootup the VM use:

    vagrant up

Setup an .env file with the following....

    DEVELOPMENT=True

Now you can start running the dev server by...

    vagrant ssh
    python puppy-eyes/main.py
               or
    vagrant ssh
    cd puppy-eyes
    foreman start -f Procfile-dev -p 8001



