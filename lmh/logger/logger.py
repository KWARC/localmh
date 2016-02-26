from lmh.logger import levels, escape

import sys
import traceback

class Logger(object):
    """
    Represents a logger used by lmh. Should be subclassed. 
    """
    
    def __init__(self, name):
        """
        Creates a new logger instance. 
        
        Arguments:
            name
                Name of this logger
        """
        
        self.name = name
    
    def _log(self, *message, newline = True, level = levels.InfoLogLevel()):
        """
        Protected method used to log output. Should be overridden by subclass. 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            level
                LogLevel() object representing the logLevel of this message. 
                Defaults to NoLogLevel()
        """
        raise NotImplementedError
    
    def log(self, *message, newline = True, flush = False, level = levels.NoLogLevel()):
        """
        Writes a message to the log. 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            flush
                Should output be flushed automatically? If set to True automatically
                calls self.flush(). 
            level
                LogLevel() object representing the logLevel of this message. 
                Defaults to NoLogLevel()
        """
        
        self._log(*message, newline = newline, level = level)
        
        if flush:
            self.flush()
    
    def flush(self):
        """
        Flushes output of this logger. Should be overridden by subclass. 
        """
        raise NotImplementedError
    
    def info(self, *message, newline = True, flush = False):
        """
        Writes a message to the log with the Info LogLevel. 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            flush
                Should output be flushed automatically? If set to True automatically
                calls self.flush(). 
        """
        
        return self.log(*message, newline = newline, flush = flush, level = levels.InfoLogLevel())
    
    def warn(self, *message, newline = True, flush = False):
        """
        Writes a message to the log with the Warn LogLevel. 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            flush
                Should output be flushed automatically? If set to True automatically
                calls self.flush(). 
        """
        
        return self.log(*message, newline = newline, flush = flush, level = levels.WarnLogLevel())
    
    def error(self, *message, newline = True, flush = False):
        """
        Writes a message to the log with the Error LogLevel. 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            flush
                Should output be flushed automatically? If set to True automatically
                calls self.flush(). 
        """
        
        return self.log(*message, newline = newline, flush = flush, level = levels.ErrorLogLevel())
    
    def fatal(self, *message, newline = True, flush = False):
        """
        Writes a message to the log with the Fatal LogLevel. If not overridden by
        subclass redirects call to self.log(). 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            flush
                Should output be flushed automatically? If set to True automatically
                calls self.flush(). 
        """
        
        return self.log(*message, newline = newline, flush = flush, level = levels.FatalLogLevel())
    
    def get_exception_string(self, exception):
        """
        Returns a string representing the exception. 
        
        Arguments:
            exception
                Exception to format
        Returns:
            A string representing the exception and its traceback
        """
        
        return ''.join(traceback.format_exception(exception.__class__, exception, exception.__traceback__))
        

class StandardLogger(Logger):
    """
    Represents a Logger that logs to stdout / stderr. 
    """
    
    def __init__(self):
        """
        Creates a new logger instance. 
        """
        super(StandardLogger, self).__init__('standard')
    
    def _log(self, *message, newline = True, level = levels.NoLogLevel()):
        """
        Protected method used to log output. Should be overridden by subclass. 
        
        Arguments:
            *message
                List of objects that should be written to the log
            newline
                Should a newline be added at the end of the log message? Defaults
                to true. 
            level
                LogLevel() object representing the logLevel of this message. 
                Defaults to NoLogLevel()
        """
        
        msg = ' '.join(list(map(str, message)))
        
        if newline:
            msg += '\n'
        
        # nothing special, just print
        if level == levels.NoLogLevel():
            sys.stdout.write(msg)
        
        # Info + Warn ==> STDOUT
        elif level == levels.InfoLogLevel():
            sys.stdout.write('[%s] %s' % (escape.Green('info'), msg))
        elif level == levels.WarnLogLevel():
            sys.stdout.write('[%s] %s' % (escape.Yellow('warn'), msg))
        
        # Error + Fatal ==> STDERR
        elif level == levels.ErrorLogLevel():
            sys.stderr.write('[%s] %s' % (escape.Red('error'), msg))
        elif level == levels.FatalLogLevel():
            sys.stderr.write('[%s] %s' % (escape.Magenta('fatal'), msg))
    
    def flush(self):
        """
        Flushes output of this logger. Should be overridden by subclass. 
        """
        
        sys.stdout.flush()
        sys.stderr.flush()