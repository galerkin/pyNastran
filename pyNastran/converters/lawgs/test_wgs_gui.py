import os
import unittest

from pyNastran.gui.testing_methods import FakeGUIMethods
from pyNastran.converters.lawgs.wgs_io import LaWGS_IO
import pyNastran

pkg_path = pyNastran.__path__[0]
model_path = os.path.join(pkg_path, 'converters', 'lawgs')


class LaWGS_GUI(LaWGS_IO, FakeGUIMethods):
    def __init__(self):
        FakeGUIMethods.__init__(self)
        LaWGS_IO.__init__(self)


class TestLawgsGUI(unittest.TestCase):

    def test_tmx_geometry(self):
        geometry_filename = os.path.join(model_path, 'tmx1242.wgs')

        test = LaWGS_GUI()
        #test.load_nastran_geometry(geometry_filename)
        test.load_lawgs_geometry(geometry_filename)

    def test_tmd_geometry(self):
        geometry_filename = os.path.join(model_path, 'tnd6480.wgs')

        test = LaWGS_GUI()
        test.load_lawgs_geometry(geometry_filename)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

