# CoffeeCup -- CoffeeScript WSGI Middleware

CoffeeCup is Python WSGI [middleware](http://www.python.org/dev/peps/pep-0333/) wrapper to transparently compile [CoffeeScript](http://jashkenas.github.com/coffee-script) into JavaScript on demand. CoffeeCup is intended to speed development; you really ought to manually compile your scripts before deployment to production like a good engineer.


## Features

 * Supports the `coffee` executable's ability to watch for changes in the background, recompiling files as needed.
 * Can discover `.coffee` files at startup for watching...
 * ...Or can dynamically update the set of files to watch as requests come in.


## Install


CoffeeCup depends on CoffeeScript, which depends on [node.js](http://nodejs.org).

 * [Install node.js](http://nodejs.org/#download)
 * [Install CoffeeScript](http://jashkenas.github.com/coffee-script/#installation)

With that done, clone this repo and install the egg:

    git clone git://github.com/dsc/coffeecup.git
    pip install -e ./coffeecup/

I'll upload it to pypi eventually.


## Configuration

The `CoffeeScriptMiddleware` takes optional arguments on instantiation:

 * `static_dir`: Path to directory holding static files. [Default: Introspected using Pylons app config if available]
 * `coffee_cmd`: Path to the `coffee` executable. [Default: `/usr/local/bin/coffee`]
 * `watch`: Whether to watch for changes. [Default: `True`]
 * `find_on_startup`: Whether to search the supplied static directory for `.coffee` files to watch and compile. [Default: `False`]

The middleware will also add several keys to the `environ` if it modifies the request:

 * `coffeecup.new_path`: The new request path that CoffeeCup set `PATH_INFO` to.
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
 * Requests will never recompile `.coffee` files if a `.js` counterpart exists, instead relying on the watcher. I can see a few cases where you'd want a staleness criterion or an override flag instead of relying on the watcher.


## Contact

Open a ticket on [github](http://github.com/dsc/coffeecup) or send me an email at [dsc@less.ly](mailto:dsc@less.ly).
