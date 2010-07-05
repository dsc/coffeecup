import logging, os, os.path
import subprocess, shlex, threading, time, signal
from os.path import dirname, basename, join
from subprocess import CalledProcessError

log = logging.getLogger(__name__)


DEFAULT_COFFEE_CMD = '/usr/local/bin/coffee'

class CoffeeScriptMiddleware(object):
    """ CoffeScript WSGI Middleware
    """
    coffee_cmd = None
    static_dir = ''
    
    enabled = True
    watch = True
    find_on_startup=True
    
    app = None
    config = None
    watching = None
    
    
    def __init__(self, app, config=None, watch=True, find_on_startup=True, static_dir=None, coffee_cmd=None):
        self.app = app
        self.config = config or {}
        
        self.coffee_cmd = coffee_cmd or DEFAULT_COFFEE_CMD
        self.static_dir = static_dir or config.get('pylons.paths', {}).get('static_files', os.getcwd())
        self.watching = set()
        
        self.enabled = True
        self.watch = watch
        self.find_on_startup = find_on_startup
        
        if self.watch and self.find_on_startup:
            self.findScripts()
        
        if self.watch:
            self.startWatching()
    
    
    def __call__(self, environ, start_response):
        reqpath = environ.get('PATH_INFO', '')
        
        if reqpath.endswith('.coffee'):
            realpath, newpath = self.handleCoffeeScript(reqpath)
            environ['coffeecup.original_path'] = reqpath
            environ['coffeecup.real_path'] = realpath
            environ['coffeecup.new_path'] = environ['PATH_INFO'] = newpath
        
        return self.app(environ, start_response)
    
    
    def handleCoffeeScript(self, reqpath):
        realpath = self.toStaticPath(reqpath)
        newpath = join( dirname(reqpath), basename(reqpath)[:-7] + '.js')
        try:
            self.compileScript(realpath, reqpath, newpath)
            self.watching.add(realpath)
        except CalledProcessError as ex:
            log.error(
                '\n\t'.join([
                    'Error compiling CoffeeScript:', 
                        'reqpath: %s', 
                        'realpath: %s',
                        'newpath: %s',
                        'command: %s',
                        'retcode: %s',
                        '\t%s',
                ]),
                reqpath, realpath, newpath,
                ex.cmd, ex.returncode, (ex.output or '').replace('\n', '\n\t\t') )
        return realpath, newpath
    
    
    def compileScript(self, realpath, reqpath, newpath):
        log.debug('Coffee request: %s --> %s', reqpath, newpath)
        
        # Let the 404 drop through if the .coffee file doesn't exist
        if not os.path.exists(realpath):
            return
        
        name = basename(realpath)[:-7] + '.js'
        jsfile = join( dirname(realpath), name )
        
        if os.path.exists(jsfile):
            log.debug('File extant: %s', jsfile)
        else:
            log.debug('Compiling %s --> %s', realpath, jsfile)
            cmd = "%s -c '%s'" % (self.coffee_cmd, realpath)
            subprocess.check_call(shlex.split(cmd), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        
    
    
    def toStaticPath(self, virtpath):
        if virtpath.startswith('/'):
            virtpath = virtpath[1:]
        return os.path.abspath( join(self.static_dir, virtpath) )
    
    
    def findScripts(self, root=None, ignore=('.svn', '.git',)):
        root = root or self.static_dir
        for path, dirs, files in os.walk(root, followlinks=True):
            self.watching.update( join(path, f) for f in files if f.endswith('.coffee') )
            for d in ignore:
                if d in dirs: dirs.remove(d)
        log.debug('Found %s scripts to watch: %s', len(self.watching), ', '.join(self.watching))
    
    
    def startWatching(self):
        self.watcher = CoffeeWatcher(self)
        # self.watcher.setDaemon(True)
        self.watcher.start()
    

class CoffeeWatcher(threading.Thread):
    """ Background Thread to run coffee -w. """
    
    update_interval = 10.0
    
    parent = None
    watching = None
    
    running = False
    current = None
    process = None
    
    
    
    def __init__(self, parent, update_interval=10, liveness_interval=0.05):
        super(CoffeeWatcher, self).__init__(name='coffee-watcher')
        self.parent = parent
        self.coffee_cmd = parent.coffee_cmd
        self.watching = parent.watching
        self.current = set()
        self.update_interval = update_interval
        self.liveness_interval = liveness_interval
    
    def run(self):
        self.running = True
        
        try:
            modulus = int(self.update_interval / self.liveness_interval)
            i = 100*modulus / 80
            while self.running and self.parent:
                if i % modulus == 0:
                    self.verifyFiles()
                    
                    if self.watching != self.current:
                        self.restartWatcher()
                
                time.sleep(self.liveness_interval)
                i += 1
            
            self.running = False
        except:
            log.exception('Error in CoffeeWatcher!')
            self.running = False
    
    def verifyFiles(self):
        for f in list(self.watching):
            if not os.path.exists(f):
                log.debug('File Removed: No longer watching %s', f)
                self.watching.remove(f)
    
    def restartWatcher(self):
        self.current = self.watching.copy()
        cmd = '%s -w -c %s' % (self.coffee_cmd, ' '.join("'%s'" % f for f in self.current ))
        
        if self.process:
            log.info('Restarting Watcher: watched set changed! %s', cmd)
            self.process.send_signal(signal.SIGINT)
        else:
            log.info('Starting Watcher:  %s', cmd)
        
        self.process = subprocess.Popen(shlex.split(cmd))
    
    def stop(self):
        if self.process:
            self.process.terminate()
        log.debug('Watcher shutting down')
        self.process = None
        self.running = False
    
    def __del__(self):
        self.stop()

