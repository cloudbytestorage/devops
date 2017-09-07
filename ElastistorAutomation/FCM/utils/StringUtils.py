#!/usr/bin/env python
_author_ = 'naveenkumar b'
_email_ = 'naveen.b@emc.com'

class sUtils:

    @staticmethod
    def CompareIgnoreCase(x, y):
        return x.lower() == y.lower()

    @staticmethod
    def Compare(x, y):
        return x == y

