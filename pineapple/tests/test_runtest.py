from unittest import TestCase, skip, expectedFailure

import pineapple

class DevNull(object):
    def write(self, _): pass
    def flush(self): pass

def counts(result):
    return [result.testsRun] + [len(x) for x in 
        [result.errors, result.failures, result.skipped, result.expectedFailures, result.unexpectedSuccesses]]


class TestRunTest(TestCase):

    def test_onepass(self):
        class Tester(TestCase):
            def test_one(self):
                '''Test should pass'''
                self.assertEqual(2, 2)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [1, 0, 0, 0, 0, 0])

    def test_twopass(self):
        class Tester(TestCase):
            def test_one(self):
                '''Test should pass'''
                self.assertEqual(2, 2)
            def test_two(self):
                '''Test should pass'''
                self.assertEqual(3, 3)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [2, 0, 0, 0, 0, 0])

    def test_onefail(self):
        class Tester(TestCase):
            def test_one(self):
                '''Test should fail'''
                self.assertEqual(2, 3)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [1, 0, 1, 0, 0, 0])

    def test_oneerror(self):
        class Tester(TestCase):
            def test_one(self):
                '''Test should error'''
                x
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [1, 1, 0, 0, 0, 0])

    def test_oneskip(self):
        class Tester(TestCase):
            @skip("Skip this one")
            def test_one(self):
                '''Test should never run'''
                pass
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [1, 0, 0, 1, 0, 0])

    def test_oneexpected(self):
        class Tester(TestCase):
            @expectedFailure
            def test_one(self):
                '''Test should never run'''
                self.assertEqual(1, 2)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [1, 0, 0, 0, 1, 0])

    def test_oneunexpected(self):
        class Tester(TestCase):
            @expectedFailure
            def test_one(self):
                '''Test should never run'''
                self.assertEqual(2, 2)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [1, 0, 0, 0, 0, 1])

    def test_threepass(self):
        class Tester(TestCase):
            def test_one(self): self.assertEqual(1, 1)
            def test_two(self): self.assertEqual(2, 2)
            def test_three(self): self.assertEqual(3, 3)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [3, 0, 0, 0, 0, 0])

    def test_threepassfail(self):
        class Tester(TestCase):
            def test_one(self): self.assertEqual(1, 1)
            def test_two(self): self.assertEqual(2, 3)
            def test_three(self): self.assertEqual(3, 3)
        result = pineapple.runtest(Tester, stream=DevNull())
        self.assertEqual(counts(result), [3, 0, 1, 0, 0, 0])

    def test_unittest2(self):
        try:
            import unittest2
            class Tester(unittest2.TestCase):
                def test_one(self): self.assertEqual(1, 1)
                def test_two(self): self.assertEqual(2, 3)
                def test_three(self): self.assertEqual(3, 3)
            result = pineapple.runtest(Tester, stream=DevNull())
            self.assertEqual(counts(result), [3, 0, 1, 0, 0, 0])
        except:
            pass
