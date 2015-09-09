import sys
import time
import unittest

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
CHECK = u'\u2713 '
HEAVY_CHECK = u'\u2714 '
CROSS = u'\u2717 '
HEAVY_CROSS = u'\u2718 '
SKULL = u'\u2620 '
SKIP = u'\u2014 '

def color(txt, color=WHITE, bold=True, bgcolor=None, inverse=False):
    '''Construct string to use ANSI color escapes around text'''
    boldtxt = "0"
    if bold:
        boldtxt = "1"
    colortxt = ""
    if color is not None:
        colortxt = ";{}".format(30 + color)
    bgcolortxt = ""
    if bgcolor is not None:
        bgcolortxt = ";{}".format(40 + bgcolor)
    inversetxt = ""
    if inverse:
        inversetxt = ";7"
    return u"\x1b[{}{}{}{}m{}\x1b[0m".format(boldtxt, colortxt, bgcolortxt, inversetxt, txt)


class PineappleTextTestResult(unittest.result.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by PineappleTextTestRunner.
    """
    separator1 = u'\u2550' * 70 + '\n'
    separator2 = u'\u2500' * 70 + '\n'

    def __init__(self, stream):
        super(PineappleTextTestResult, self).__init__()
        self.stream = stream

    def getName(self, test):
        return test._testMethodName

    def getDescription(self, test):
        doc_line = test.shortDescription()
        if doc_line:
            return doc_line
        return ''

    def startTest(self, test):
        super(PineappleTextTestResult, self).startTest(test)
        self.stream.write(u"  {}\n".format(color(self.getName(test), color=WHITE, bold=True)))
        self.stream.write(u"    ")
        self.stream.flush()

    def addDescription(self, test):
        self.stream.write(' ')
        self.stream.write(color(self.getDescription(test), color=WHITE, bold=False))
        self.stream.write('\n')

    def addSuccess(self, test):
        super(PineappleTextTestResult, self).addSuccess(test)
        self.stream.write(color(CHECK, color=GREEN))
        self.addDescription(test)

    def addError(self, test, err):
        super(PineappleTextTestResult, self).addError(test, err)
        self.stream.write(color(HEAVY_CROSS, color=RED, bold=True, inverse=True))
        self.addDescription(test)

    def addFailure(self, test, err):
        super(PineappleTextTestResult, self).addFailure(test, err)
        self.stream.write(color(CROSS, color=RED))
        self.addDescription(test)

    def addSkip(self, test, reason):
        super(PineappleTextTestResult, self).addSkip(test, reason)
        self.stream.write(color(SKIP, color=YELLOW))
        self.addDescription(test)

    def addExpectedFailure(self, test, err):
        super(PineappleTextTestResult, self).addExpectedFailure(test, err)
        self.stream.write(color(CHECK, color=GREEN))
        self.addDescription(test)

    def addUnexpectedSuccess(self, test):
        super(PineappleTextTestResult, self).addUnexpectedSuccess(test)
        self.stream.write(color(CROSS, color=RED))
        self.addDescription(test)

    def numErrors(self):
        return len(self.errors) + len(self.failures)

    def printErrors(self):
        self.stream.write('\n')
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            headline = u"{}: {}".format(flavour, self.getDescription(test))
            err_body = u"{}\n".format(err)
            self.stream.write(color(self.separator1))
            self.stream.write(color(headline, color=YELLOW, bgcolor=RED))
            self.stream.write('\n')
            self.stream.write(color(self.separator2))
            self.stream.write(err_body)

class PineappleTextTestRunner(object):
    """A test runner class that displays results in pretty form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    
    Uses color escapes and a few unicode symbols.
    """
    resultclass = PineappleTextTestResult

    def __init__(self, failfast=False, resultclass=None, verbosity=1, stream=sys.stderr):
        self.stream = stream
        self.verbosity = verbosity
        self.failfast = failfast
        if resultclass is not None:
            self.resultclass = resultclass

    def _makeResult(self):
        return self.resultclass(self.stream)

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        result.failfast = self.failfast
        result.buffer = False
        self.stream.write('\n')
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        if result.numErrors() > 0:
            self.stream.write(result.separator2)
            self.stream.write('\n')
        run = result.testsRun

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
            expectedFails, unexpectedSuccesses, skipped = results
        except AttributeError:
            pass

        infos = []
        if not result.wasSuccessful():
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        info_txt = ''
        if infos:
            info_txt = "  ({})".format(", ".join(infos))

        msg_txt = u"{} test{} completed".format(run, run != 1 and 's' or '')
        time_txt = u"  ({:.3f} ms)".format(timeTaken*1000)
        self.stream.write('  ')
        if result.wasSuccessful():
            self.stream.write(color(CHECK, color=GREEN))
            self.stream.write(color(msg_txt, color=GREEN))
            self.stream.write(color(info_txt, color=WHITE, bold=False))
            self.stream.write(color(time_txt, color=WHITE, bold=False))
            self.stream.write('\n')
        else:
            self.stream.write(color(CROSS, color=RED))
            self.stream.write(color(msg_txt, color=RED))
            self.stream.write(color(info_txt, color=WHITE, bold=True))
            self.stream.write(color(time_txt, color=WHITE, bold=False))
            self.stream.write('\n')
        self.stream.write('\n')

        return result


class PineappleHTMLTestResult(unittest.result.TestResult):
    """A test result class that also keeps track of successes"""

    def __init__(self):
        super(PineappleHTMLTestResult, self).__init__()
        self.successes = []

    def getName(self, test):
        return test._testMethodName

    def getDescription(self, test):
        doc_line = test.shortDescription()
        if doc_line:
            return doc_line
        return self.getName(test)

    def addSuccess(self, test):
        self.successes.append((test, None))


class PineappleHTMLTestRunner(object):
    """A test runner class that displays results in pretty HTML form.

    """

    def __init__(self, failfast=False, verbosity=1):
        self.verbosity = verbosity
        self.failfast = failfast

    def table_of_result(self, result):
        """Convert unittest Result object into HTML table"""
        rows = []
        def add(label, lst, style):
            for test, backtrace in lst:
                rows.append([label, result.getDescription(test), style])
        add(CHECK, result.successes, u'unittest-success')
        add(CROSS, result.failures, u'unittest-failure')
        add(HEAVY_CROSS, result.errors, u'unittest-error')
        add(SKIP, result.skipped, u'unittest-skipped')
        add(CHECK, result.expectedFailures, u'unittest-success')
        add(CROSS, result.unexpectedSuccesses, u'unittest-failure')
        bd = u'\n'.join([u'<p class="unittest-test {}">{}<span class="unittest-name">{}</span></p>'.format(row[2], row[0], row[1]) for row in rows])
        return u'{}'.format(bd)

    def summary_of_result(self, result, timeTaken):
        """Formulate paragraph summary line at end"""
        run = result.testsRun

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
            expectedFails, unexpectedSuccesses, skipped = results
        except AttributeError:
            pass

        infos = []
        if not result.wasSuccessful():
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append(u"failures=%d" % failed)
            if errored:
                infos.append(u"errors=%d" % errored)
        if skipped:
            infos.append(u"skipped=%d" % skipped)
        if expectedFails:
            infos.append(u"expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append(u"unexpected successes=%d" % unexpectedSuccesses)

        msg_txt = u"<span class='unittest-number'>{} test{} completed</span>".format(run, run != 1 and 's' or '')
        info_txt = u''
        if infos:
            info_txt = u"<span class='unittest-info'>({})</span>".format(", ".join(infos))
        time_txt = u"<span class='unittest-time'>({:.3f} ms)</span>".format(timeTaken*1000)
        result_txt = u"<span class='unittest-result'>{}</span>".format("OK" if result.wasSuccessful() else "FAILED")
        class_txt = u"unittest-success" if result.wasSuccessful() else u"unittest-failure"
        return u"<p class='unittest {}'>{} {} {}</p><p class='unittest {}'>{}</p>".format(class_txt, msg_txt, info_txt, time_txt, class_txt, result_txt)

    def list_of_errors(self, result):
        """Make list of errors"""
        separator = u'<div class="unittest-separator"></div>' 
        res = []
        def describe(style, tag, lst):
            for test, err in lst:
                headline = u"<p class='{}'>{}: {}</p>".format(style, tag, result.getDescription(test))
                body = u"<pre class='{}'>{}</pre>".format(u'unittest-traceback', err)
                res.append(separator)
                res.append(headline)
                res.append(body)
        describe(u'unittest-error unittest-header', u'ERROR', result.errors)
        describe(u'unittest-failure unittest-header', u'FAILURE', result.failures)
        return u'\n'.join(res)

    def run(self, test):
        "Run the given test case or test suite."
        result = PineappleHTMLTestResult()
        result.failfast = self.failfast
        result.buffer = False
        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
        stopTime = time.time()
        timeTaken = stopTime - startTime

        table = self.table_of_result(result)
        msg = self.summary_of_result(result, timeTaken)
        errs = self.list_of_errors(result)

        import IPython.display
        return IPython.display.HTML(u'<div class="unittest">{}{}{}</div>'.format(table, msg, errs))


def runtest(*args, **kwargs):
    loader = unittest.TestLoader()
    runner = kwargs.get('runner', PineappleTextTestRunner)
    if 'runner' in kwargs:
        del kwargs['runner']
    suite_list = []
    for arg in args:
        suite = loader.loadTestsFromTestCase(arg)
        suite_list.append(suite)
    big_suite = unittest.TestSuite(suite_list)
    runner = runner(**kwargs)
    return runner.run(big_suite);

def runtestHTML(*args, **kwargs):
    kwargs['runner'] = PineappleHTMLTestRunner
    return runtest(*args, **kwargs)
