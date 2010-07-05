# CoffeeCup -- CoffeScript WSGI Middleware

CoffeeCup is Python WSGI middleware wrapper to transparently compile [CoffeeScript](http://jashkenas.github.com/coffee-script) (files ending in `.coffee`) into JavaScript. CoffeeCup is intended for development; you should freeze your production CoffeeScript files before deployment like a good engineer.


## Features

 * Supports the `coffee` executable's ability to watch for changes in the background, recompiling files as needed.
 * Can discover `.coffee` files at startup for watching...
 * ...Or can dynamically update the set of files to watch as requests come in.


## Install


CoffeeCup depends on CoffeeScript, which depends on node.js.

 * [Install node.js](http://nodejs.org/#download)
 * [Install CoffeeScript](http://jashkenas.github.com/coffee-script/#installation)

With that done, clone this repo and install the egg:

    git clone git://github.com/dsc/coffeecup.git
    pip install coffeecup

I'll upload it to pypi eventually.


## Configuration

The `CoffeeScriptMiddleware` takes optional arguments on instantiation:

 * `watch`: Whether to watch for changes. [Default: True]
 * `find_on_startup`: Whether to search the supplied static directory for `.coffee` files to watch and compile. [Default: True]
 * `static_dir`: Path to directory holding static files. [Default: Introspected using Pylons App config if available]
 * `coffee_cmd`: Path to the `coffee` executable. [Default: /usr/local/bin/coffee]

The middleware will also add several keys to the `environ` if it modifies the request:

 * `coffeecup.original_path`: The original request path, taken from `PATH_INFO`.
 * `coffeecup.real_path`: The real filesystem path compiled (if necessary) to serve this request.



## Usage in Pylons

Pylons has awesome support for middleware, making this process totally transparent once set up.

First, edit your `config/middleware.py` file, to filter your static files through CoffeeCup:

    if asbool(static_files):
        # Serve static files
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        static_app = CoffeeScriptMiddleware(static_app, config)
        
        app = Cascade([static_app, app])

You may pass any of the additional config options listed above as keyword arguments when you instantiate the `CoffeeScriptMiddleware`.


## Usage in Other WSGI Stacks

The only serious difference will be that you must specify the static directory manually:

    app = MyApp()
    app = CoffeeScriptMiddleware(app, static_dir='/path/to/static/files')

As before, you can still pass other options.


## Todos

 * At the moment, the `CoffeeScriptMiddleware` currently only handles requests for static files, and determines which files to compile by file extension. It would make sense to add support to match on any request pattern, filtering the output stream through `coffee`.
 * Requests will never recompile `.coffee` files if a `.js` counterpart exists, instead relying on the watcher. It makes sense to add a staleness criterion to the configuration, or perhaps an override flag to the request.


## Contact

Open a ticket at http://github.com/dsc/coffeecup or send me an email at [dsc@less.ly](mailto:dsc@less.ly).