from unittest import TestCase, makeSuite, TextTestRunner


class run_test(TestCase):

    def setUp(self):
        return 1

    def test1(self):
        return 1

    def test2(self):
        return 1

    def tearDown(self):
        return 1


if __name__ == '__main__':
        print("=====AutoTest Start======")
        suite = makeSuite(run_test)
        runner = TextTestRunner()
        runner.run(suite)
        print("=====AutoTest Over======")