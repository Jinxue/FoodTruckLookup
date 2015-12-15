'''
Created on Dec 15, 2015

@author: Jinxue Zhang
Unit test
'''
import unittest
from FoodTruckLookup.BackEndWebService import FoodTruckLoopup
import time

class OnTheFlyTest(unittest.TestCase):
    def setUp(self):
        self.ft = FoodTruckLoopup(37.73, -122.40, 1000000)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print "%s: using %.3f seconds." % (self.id(), t)
            
    def test_BasicFTTestCase(self):
        res = self.ft.obtainFoodTruckOnTheFly(37.77, -122.38, 2000)
        self.assertTrue(res[0] > 0)
        print res[0]

    def test_BasicFTTestCase2(self):
        res = self.ft.obtainFoodTruckOnTheFly(37.78, -122.39, 1000)
        self.assertTrue(res[0] > 0)
        print res[0]

    def test_LargerRadius(self):
        res = self.ft.obtainFoodTruckOnTheFly(37.73, -122.40, 100000)
        self.assertTrue(res[0] > 0)
        print res[0]

    def test_SmallerRadius(self):
        res = self.ft.obtainFoodTruckOnTheFly(37.73, -122.40, 100)
        self.assertTrue(res[0] == 0)
        print res[0]

    def test_OutRange(self):
        res = self.ft.obtainFoodTruckOnTheFly(137.73, 122.40, 1000)
        self.assertTrue(res[0] == 0)
        print res[0]
        
class CacheTest(unittest.TestCase):
    def setUp(self):
        self.ft = FoodTruckLoopup(37.73, -122.40, 1000000)
        self.startTime = time.time()
    
    def outputTime(self):
        tmp = time.time()
        t, self.startTime = tmp - self.startTime, tmp
        return "%s: using %.3f seconds." % (self.id(), t)

    def test_Whole(self):
        res = self.ft.obtainFoodTruckOnWithCache(37.77, -122.38, 2000)
        self.assertTrue(res[0] > 0)
        print res[0], self.outputTime()

        res = self.ft.obtainFoodTruckOnWithCache(37.78, -122.39, 1000)
        self.assertTrue(res[0] > 0)
        print res[0], self.outputTime()

        res = self.ft.obtainFoodTruckOnWithCache(37.73, -122.40, 100000)
        self.assertTrue(res[0] > 0)
        print res[0], self.outputTime()

        res = self.ft.obtainFoodTruckOnWithCache(37.73, -122.40, 100)
        self.assertTrue(res[0] == 0)
        print res[0], self.outputTime()

        res = self.ft.obtainFoodTruckOnWithCache(137.73, 122.40, 1000)
        self.assertTrue(res[0] == 0)
        print res[0], self.outputTime()
        
if __name__ == '__main__':
    unittest.main()
