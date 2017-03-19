import unittest

import client


class TestClient(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    @classmethod
    def setUpClass(self):
        self.cache_clientOne = client.cacheClient()
        self.cache_clientTwo = client.cacheClient()

    def test_execute_basic(self):
        self.cache_clientOne.insert('test1', 'cache_clientOneval1')

        self.cache_clientTwo.insert('test1', 'cache_clientTwoval1')

        self.assertEqual(self.cache_clientOne.get('test1'), 'cache_clientTwoval1')

    def test_execute_basic_get(self):

        self.assertEqual(self.cache_clientOne.get('test2'), 'None')


    def test_execute_basic_multi(self):
        self.cache_clientOne.insert("testT1", 2)
        self.cache_clientOne.insert("testT2", 3)
        self.cache_clientTwo.insert("testT2", 4)
        self.cache_clientOne.insert("testT1", 5)
        self.assertEqual(self.cache_clientOne.get('testT2'), '4')



if __name__ == '__main__':
    unittest.main()

