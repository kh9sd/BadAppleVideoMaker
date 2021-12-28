import unittest
from quadtree import *


class MyTestCase(unittest.TestCase):
    def test_calcmean(self):
        pass

    def check_equal(self):
        self.assertEqual(check_equal(np.array([[[1, 2], [3, 4]],
                                                                    [[5, 6], [7, 8]]]),
                                     False))

        self.assertEqual(check_equal(np.array([[[1, 1], [1, 1]],
                                                                    [[1, 1], [1, 1]]]),
                                     True))

        self.assertEqual(check_equal(np.array([[[1, 1, 1], [1, 1, 1]],
                                                                    [[1, 1, 1], [1, 1, 1]]]),
                                     True))
        self.assertEqual(check_equal(np.array([[[1, 1, 1], [1, 1, 1]],
                                                                    [[1, 1, 1], [1, 1, 2]]]),
                                     True))

    def test_white(self):
        self.assertEqual(is_white(np.array([255, 255, 255, 255])), True)
        self.assertEqual(is_white(np.array([255, 255, 254, 255])), False)
        self.assertEqual(is_white(np.array([255, 255, 255, 0])), True)
        self.assertEqual(is_white(np.array([255, 255, 254, 0])), False)
        self.assertEqual(is_white(np.array([255, 5, 254, 0])), False)
        self.assertEqual(is_white(np.array([0, 255, 255, 0])), False)

        self.assertEqual(is_white(np.array([255, 255, 255])), True)
        self.assertEqual(is_white(np.array([255, 255, 254])), False)
        self.assertEqual(is_white(np.array([0, 255, 255])), False)
        self.assertEqual(is_white(np.array([255, 0, 254])), False)

    def test_whiteish(self):
        self.assertEquals(is_whiteish(np.array([255, 255, 255, 1])), True)
        self.assertEquals(is_whiteish(np.array([255, 255, 99, 1])), False)
        self.assertEquals(is_whiteish(np.array([255, 1, 255, 1])), False)
        self.assertEquals(is_whiteish(np.array([0, 123, 255, 1])), False)

        self.assertEquals(is_whiteish(np.array([255, 255, 255])), True)
        self.assertEquals(is_whiteish(np.array([255, 255, 99])), False)
        self.assertEquals(is_whiteish(np.array([255, 1, 255])), False)
        self.assertEquals(is_whiteish(np.array([0, 123, 255])), False)


if __name__ == '__main__':
    unittest.main()
