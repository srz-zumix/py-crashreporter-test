import sys
import os
import backtracepython as bt
import bugsnag
from raygun4py import raygunprovider
import rollbar
import sentry_sdk

from dotenv import load_dotenv

try:
    import unittest2 as unittest
except:
    import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


load_dotenv()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class test_base(unittest.TestCase):

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture
        return super(test_base, self).setUp()

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.capture.close()
        return super(test_base, self).tearDown()

    def stdoout(self):
        value = self.capture.getvalue()
        return value

    def report(self, on_error):
        try:
            data = open("foo.txt").read()
        except Exception as e:
            on_error(e)
        try:
            raise Exception('spam', 'eggs')            
        except Exception as e:
            on_error(e)


class test_backtrace(test_base):
    @classmethod
    def setUpClass(cls):
        try:
            bc_token = os.environ['BACKTRACE_TOKEN']
        except:
            raise unittest.SkipTest('BACKTRACE_TOKEN is not found..')
        if not bc_token:
            raise unittest.SkipTest('BACKTRACE_TOKEN empty..')
        try:
            bc_host = os.environ['BACKTRACE_HOSTNAME']
        except:
            raise unittest.SkipTest('BACKTRACE_HOSTNAME is not found..')
        if not bc_host:
            raise unittest.SkipTest('BACKTRACE_HOSTNAME empty..')
        bt.initialize(
            endpoint=f"https://submit.backtrace.io/{bc_host}/{bc_token}/json",
            token=bc_token
        )

    @classmethod
    def tearDownClass(cls):
        bt.finalize()

    def setUp(self):    
        return super(test_backtrace, self).setUp()

    def tearDown(self):
        return super(test_backtrace, self).tearDown()

    def test_report(self):
        self.report((lambda _: bt.send_last_exception()))

    def test_send_report(self):
        bt.send_report("TEST")


class test_bugsnag(test_base):
    @classmethod
    def setUpClass(cls):
        try:
            api_key = os.environ['BUGSNAG_API_KEY']
        except:
            raise unittest.SkipTest('BUGSNAG_API_KEY is not found..')
        if not api_key:
            raise unittest.SkipTest('BUGSNAG_API_KEY is empty..')
        bugsnag.configure(
            api_key=api_key
        )

    def setUp(self):        
        return super(test_bugsnag, self).setUp()

    def tearDown(self):
        return super(test_bugsnag, self).tearDown()

    def test_report(self):
        self.report((lambda e: bugsnag.notify(e)))


class test_raygun(test_base):

    @classmethod
    def setUpClass(cls):
        try:
            api_key = os.environ['RAYGUN_API_KEY']
        except:
            raise unittest.SkipTest('RAYGUN_API_KEY is not found..')
        if not api_key:
            raise unittest.SkipTest('RAYGUN_API_KEY is empty..')
        cls.raygun = raygunprovider.RaygunSender(api_key)

    def setUp(self):        
        return super(test_raygun, self).setUp()

    def tearDown(self):
        return super(test_raygun, self).tearDown()

    def test_report(self):
        self.report((lambda _: test_raygun.raygun.send_exception()))


class test_rollbar(test_base):

    @classmethod
    def setUpClass(cls):
        try:
            token = os.environ['ROLLBAR_TOKEN']
        except:
            raise unittest.SkipTest('ROLLBAR_TOKEN is not found..')
        if not token:
            raise unittest.SkipTest('ROLLBAR_TOKEN is empty..')
        rollbar.init(token)

    def setUp(self):        
        return super(test_rollbar, self).setUp()

    def tearDown(self):
        return super(test_rollbar, self).tearDown()

    def test_report(self):
        self.report((lambda _: rollbar.report_exc_info()))
        

class test_sentry(test_base):

    @classmethod
    def setUpClass(cls):
        try:
            url = os.environ['SENTRY_URL']
        except:
            raise unittest.SkipTest('SENTRY_URL is not found..')
        if not url:
            raise unittest.SkipTest('SENTRY_URL is empty..')
        sentry_sdk.init(
            url,

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0
        )

    def setUp(self):        
        return super(test_sentry, self).setUp()

    def tearDown(self):
        return super(test_sentry, self).tearDown()

    def test_report(self):
        self.report((lambda e: sentry_sdk.capture_exception(e)))


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
