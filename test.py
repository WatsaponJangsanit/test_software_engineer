# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 20:26:21 2019

@author: Junior
"""

import unittest

from my_functions import cal_xy

class TestPosition(unittest.TestCase):
    
    def test_cal_xy(self):
        
        center = [12.0,10.0]
        degrees = 45.246
        distance = 1000.3145

        result = cal_xy(center, degrees, distance)
        self.assertEqual(result, (1270, 929))

if __name__ == '__main__':
    unittest.main()