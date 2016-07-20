import unittest
from unittest import mock as m
from tools import funciones_aux as f


# 1/7 funciones testeadas del modulo funciones_aux

class TestFunciones(unittest.TestCase):

    def test_stop(self):
        with m.patch('builtins.input', side_effect=['a', 'c', 'd']):
            assert f.stop("mensaje")
            assert f.stop("mensaje")
            assert f.stop("mensaje")
