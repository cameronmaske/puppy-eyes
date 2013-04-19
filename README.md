Puppy eyes
----------

A simple image resizer service in flask using redis.

Install
-------

To install you require [Vagrant](http://downloads.vagrantup.com/tags/v1.1.5)(tested on 1.1.5).
To bootup the VM use:

    vagrant up

Setup an .env file with the following....

    DEVELOPMENT=True
    REDIS_URL=redis://:@localhost:6379/

Now you can to start the server run

    vagrant ssh
    python puppy-eyes/main.py
               or
    cd puppy-eyes
    foreman start -f Procfile-dev -p 8001


