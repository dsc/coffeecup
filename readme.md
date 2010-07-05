# CoffeeCup -- CoffeScript WSGI Middleware

CoffeeCup is Python WSGI middleware wrapper to transparently compile [CoffeeScript](http://jashkenas.github.com/coffee-script) (files ending in `.coffee`) into JavaScript. I wrote it for my own Pylons apps, so it has a bit of a bias in features.


## Features

 * Supports the `coffee` executable's ability to watch for changes in the background, recompiling files as needed.
 * Can discover `.coffee` files at startup for watching...
 * ...Or can dynamically update the set of files to watch as requests come in.


## Configuration

The `CoffeeScriptMiddleware` takes optional arguments on instantiation:

 * `watch`: Whether to watch for changes. [Default: True]
 * `find_on_startup`: Whether to search the supplied static directory for `.coffee` files to watch and compile. [Default: True]
 * `static_dir`: Path to directory holding static files. [Default: Introspected using Pylons App config if available]
 * `coffee_cmd`: Path to the `coffee` executable. [Default: /usr/local/bin/coffee]


## Usage in Pylons

Pylons has awesome support for middleware, making this process totally transparent once set up.

First, edit your `config/middleware.py` file, to filter your static files through CoffeeCup:

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        static_app = CoffeeScriptMiddleware(static_app, config)
        
        app = Cascade([static_app, app])

You may pass any of the additional config options listed above as keyword arguments when you instantiate the `CoffeeScriptMiddleware`.


## Limitations

At the moment, the `CoffeeScriptMiddleware` currently only handles requests for static files, and determines which files to compile by file extension. It would make sense to add support to match on any request pattern, filtering the output stream through `coffee`.


## Contact

Open a ticket at http://github.com/dsc/coffeecup or send me an email at [dsc@less.ly](mailto:dsc@less.ly).