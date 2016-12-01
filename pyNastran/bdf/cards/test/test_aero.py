"""
tests aero cards
"""
from __future__ import print_function
import os
import unittest
import numpy as np

import pyNastran
from pyNastran.utils.log import SimpleLogger
from pyNastran.bdf.bdf import BDF, CORD2R, BDFCard, SET1, GRID
from pyNastran.bdf.cards.aero import (
    FLFACT, AEFACT, AEPARM, AERO, AEROS,
    CAERO1, CAERO2, CAERO3, CAERO4, CAERO5,
    PAERO1, PAERO2, PAERO3, PAERO4, PAERO5,
    AELIST, FLUTTER, TRIM, CSSCHD, MKAERO1, MKAERO2, GUST, AESURF, AESURFS,
    AELINK, DIVERG,
    SPLINE1, SPLINE2 #, SPLINE3, SPLINE4, SPLINE5
)

root_path = pyNastran.__path__[0]
#test_path = os.path.join(root_path, 'bdf', 'cards', 'test')

comment_bad = 'this is a bad comment'
comment_good = 'this is a good comment\n'
class TestAero(unittest.TestCase):
    """
    The Aero cards are:
     * AEFACT
     * AELINK
     * AELIST
     * AEPARM
     * AESTAT
     * AESURF / AESURFS
     * AERO / AEROS
     * CSSCHD
     * CAERO1 / CAERO2 / CAERO3 / CAERO4 / CAERO5
     * FLFACT
     * FLUTTER
     * GUST
     * MKAERO1 / MKAERO2
     * PAERO1 / PAERO2 / PAERO3
     * SPLINE1 / SPLINE2 / SPLINE4 / SPLINE5
    """
    def test_aefact_1(self):
        """checks the AEFACT card"""
        data = ['AEFACT', 97, .3, 0.7, 1.0]
        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        model.add_card(data, data[0], comment_bad, is_list=True)

        data = ['AEFACT', 97, .3, 0.7, 1.0]
        model.add_card(data, data[0], comment_bad, is_list=True)

        data = ['AEFACT', '98', '.3', '0.7', '1.0']
        model.add_card(data, data[0], comment_good, is_list=True)

        msg = '$this is a bad comment\nAEFACT        97      .3      .7      1.\n'
        aefact97 = model.aefacts[97]
        aefact98 = model.aefacts[98]
        self.assertTrue(all(aefact97.Di == [.3, .7, 1.0]))
        self.assertTrue(all(aefact98.Di == [.3, .7, 1.0]))

        out = aefact97.write_card(8, None)
        self.assertEqual(msg, out)

        msg = '$this is a good comment\nAEFACT        98      .3      .7      1.\n'
        out = aefact98.write_card(8, None)
        self.assertEqual(msg, out)

        #data = ['AEFACT', 99, .3, 0.7, 1.0, None, 'cat']
        #with self.assertRaises(SyntaxError):
            #model.add_card(data, data[0], comment_good, is_list=True)

        #data = ['AEFACT', 100, .3, 0.7, 1.0, 'cat']
        #with self.assertRaises(SyntaxError):
            #model.add_card(data, data[0], comment_good, is_list=True)

        #data = ['AEFACT', 101, .3, 0.7, 1.0, 2]
        #with self.assertRaises(SyntaxError):
            #model.add_card(data, data[0], comment_good, is_list=True)

        Di = [1., 2., 3.]
        aefact = AEFACT(200, Di, comment='')
        aefact.validate()
        aefact.write_card()

    def test_aelink_1(self):
        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        id = 10
        label = 'CS'
        independent_labels = ['A', 'B', 'C']
        Cis = [1.0, 2.0]
        aelink = AELINK(id, label, independent_labels, Cis, comment='')
        with self.assertRaises(RuntimeError):
            aelink.validate()
        str(aelink)
        aelink.write_card()

        card = ['AELINK', id, label, independent_labels[0], Cis[0],
                independent_labels[1], Cis[1], independent_labels[2]]
        with self.assertRaises(AssertionError):
            model.add_card(card, 'AELINK')

        card = ['AELINK', id, label, independent_labels[0], Cis[0],
                independent_labels[1], Cis[1]]
        model.add_card(card, 'AELINK', comment='cat')



    def test_aelist_1(self):
        """checks the AELIST card"""
        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        data = ['AELIST', 75, 1001, 'THRU', 1075, 1101, 'THRU', 1109, 1201, 1202]
        model.add_card(data, data[0], comment_bad, is_list=True)
        elements = list(range(1001, 1076)) + list(range(1101, 1110)) + [1201, 1202]
        aelist = AELIST(74, elements)
        aelist.validate()
        aelist.write_card()
        aelist75 = model.aelists[75]
        #print(aelist.elements)
        #print(elements)
        self.assertTrue(elements == aelist75.elements)

        elements = list(range(1001, 1076)) + list(range(1101, 1110)) + [1108, 1202]
        data = ['AELIST', 76, 1001, 'THRU', 1075, 1101, 'THRU', 1109, 1108, 1202]
        model.add_card(data, data[0], comment_bad, is_list=True)
        aelist76 = model.aelists[76]
        #print(aelist76 .elements)
        #print(elements)
        self.assertFalse(elements == aelist76.elements)

        elements = list(set(elements))
        elements.sort()
        self.assertTrue(elements == aelist76.elements)

    def test_aeparm_1(self):
        """checks the AEPARM card"""
        aeparm = AEPARM.add_card(BDFCard(['AEPARM', 100, 'THRUST', 'lb']),
                                 comment='aeparm_comment')
        aeparm = AEPARM(100, 'THRUST', 'lb', comment='aeparm_comment')
        aeparm.validate()
        aeparm.write_card()

   # def test_aestat_1(self):
   # def test_aesurf_1(self):
    def test_aesurfs_1(self):
        """checks the AESURFS cards"""
        aesid = 6001
        label = 'ELEV'
        list1 = 6002
        list2 = 6003
        card = ['AESURFS', aesid, label, None, list1, None, list2]
        bdf_card = BDFCard(card, has_none=True)
        model = BDF()
        model.add_card(bdf_card, 'AESURFS', comment='aesurfs',
                       is_list=True, has_none=True)
        aesurfs = AESURFS(aesid, label, list1, list2, comment='aesurfs')
        str(aesurfs)
        aesurfs.write_card()

    def test_aero_1(self):
        """checks the AERO card"""
        acsid = 0.
        velocity = None
        cref = 1.0
        rho_ref = 1.0
        aero = AERO(velocity, cref, rho_ref, acsid=acsid, sym_xz=0, sym_xy=0,
                    comment='aero card')
        with self.assertRaises(TypeError):
            aero.validate()

        acsid = 0
        aero = AERO(velocity, cref, rho_ref, acsid=acsid, sym_xz=0., sym_xy=0,
                    comment='aero card')
        with self.assertRaises(TypeError):
            aero.validate()

        aero = AERO(velocity, cref, rho_ref, acsid=acsid, sym_xz=0, sym_xy=0.,
                    comment='aero card')
        with self.assertRaises(TypeError):
            aero.validate()

        aero = AERO(velocity, cref, rho_ref, acsid=acsid, sym_xz=0, sym_xy=0.,
                    comment='aero card')
        with self.assertRaises(TypeError):
            aero.validate()

        aero = AERO(velocity, cref, rho_ref, acsid=None, sym_xz=0, sym_xy=0,
                    comment='aero card')
        aero.validate()
        aero.write_card()
        aero.raw_fields()

        model = BDF()
        aero.cross_reference(model)
        aero.write_card()
        aero.raw_fields()

        aero.uncross_reference()
        aero.write_card()
        aero.raw_fields()

    def test_aeros_1(self):
        """checks the AEROS card"""
        #acsid = 0.
        #velocity = None
        cref = 1.0
        bref = 2.0
        sref = 100.
        acsid = 0
        rcsid = 0
        aeros = AEROS.add_card(BDFCard(['AERO', acsid, rcsid, cref, bref, sref]))
        aeros = AEROS(cref, bref, sref, acsid, rcsid, sym_xz=0, sym_xy=0,
                      comment='aeros card')
        aeros.validate()
        aeros.write_card()
        aeros.raw_fields()

        acsid = None
        rcsid = None
        sym_xz = None
        sym_xy = None
        aeros = AEROS(cref, bref, sref, acsid, rcsid, sym_xz=sym_xz, sym_xy=sym_xy,
                      comment='aeros card')
        aeros.validate()
        aeros.write_card()
        aeros.raw_fields()


    def test_caero1_1(self):
        """checks the CAERO1/PAERO1/AEROS/AEFACT card"""
        eid = 1
        pid = 10
        cp = 4
        nspan = None
        lspan = 3
        nchord = None
        lchord = 4
        igid = 0
        p1 = [0., 0., 0.]
        x12 = 5.
        p4 = [2., 3., 4.]
        x43 = 1.

        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        caero = CAERO1.add_card(BDFCard(['CAERO1', eid, pid, cp, nspan, nchord, lspan, lchord,
                                         igid, ] + p1 + [x12] + p4 + [x43]))
        caero.validate()
        caero = CAERO1.add_card(BDFCard(['CAERO1', eid, pid, None, nspan, nchord, lspan, lchord,
                                         igid, ] + p1 + [x12] + p4 + [x43]))
        caero.validate()
        caero = CAERO1(eid, pid, cp, nspan, lspan, nchord, lchord, igid, p1,
                       x12, p4, x43, comment='caero1')
        caero.raw_fields()
        caero.validate()
        caero.write_card()
        model.caeros[eid] = caero

        p1 = [0., 0., 0.]
        p2 = [1., 0., 0.]
        p3 = [0.2, 1., 0.]
        p4 = [0.1, 1., 0.]
        nspan = 5
        nchord = 10
        igid = -1
        caeroq = CAERO1.add_quad(eid, pid, cp, nspan, nchord, igid, p1, p2, p3, p4,
                                 spanwise='y', comment='')
        caeroq.validate()

        span = 0.1
        chord = 0.05
        igid = -1
        caeroq = CAERO1.add_quad(eid, pid, cp, span, chord, igid, p1, p2, p3, p4,
                                 spanwise='y', comment='')
        caeroq.validate()


        p1 = [0., 0., 0.]
        p2 = [1., 0., 0.]
        p3 = [0.2, 0., 1.]
        p4 = [0.1, 0., 1.]
        span = 0.1
        chord = 0.05
        igid = -1
        caeroq = CAERO1.add_quad(eid, pid, cp, span, chord, igid, p1, p2, p3, p4,
                                 spanwise='z', comment='')
        caeroq.validate()

        paero = PAERO1(pid, Bi=None, comment='')
        paero.validate()
        paero.write_card()
        model.paeros[pid] = paero

        coord = CORD2R(cp, rid=0, origin=None, zaxis=None, xzplane=None,
                       comment='')
        coord.validate()
        model.coords[cp] = coord

        #acsid = 0.
        #velocity = None
        cref = 1.0
        bref = 2.0
        sref = 100.
        acsid = 0
        rcsid = 0
        aeros = AEROS(cref, bref, sref, acsid, rcsid, sym_xz=0, sym_xy=0,
                      comment='')
        aeros.validate()
        aeros.write_card()
        model.aeros = aeros

        aefact = AEFACT(lspan, [0., 1., 2., 3., 4., 5.])
        aefact.validate()
        model.aefacts[lspan] = aefact

        aefact = AEFACT(lchord, [2., 3., 4., 5., 6., 7.])
        aefact.validate()
        model.aefacts[lchord] = aefact

        paero.cross_reference(model)
        caero.cross_reference(model)
        caero.get_npanel_points_elements()
        caero.get_points()
        caero.panel_points_elements()

        caero.write_card()
        model.uncross_reference()
        model.cross_reference()
        model.uncross_reference()
        #model.safe_cross_reference()
        caero.safe_cross_reference(model)
        caero.panel_points_elements()
        caero.raw_fields()

    def test_spline1(self):
        """checks the SPLINE1 card"""
        eid = 1
        caero_id = 1
        box1 = 1
        box2 = 10
        setg = 1
        spline = SPLINE1(eid, caero_id, box1, box2, setg, dz=0., method='IPS',
                         usage='BOTH', nelements=10,
                         melements=10, comment='$ spline1')
        spline.validate()
        spline.write_card(size=8, is_double=False)

    def test_spline2(self):
        """checks the SPLINE2 card"""
        #| SPLINE2 | EID  | CAERO |  ID1  |  ID2  | SETG | DZ | DTOR | CID |
        #|         | DTHX | DTHY  | None  | USAGE |      |    |      |     |
        #+---------+------+-------+-------+-------+------+----+------+-----+
        #| SPLINE2 |   5  |   8   |  12   | 24    | 60   | 0. | 1.0  |  3  |
        #|         |  1.  |       |       |       |      |    |      |     |

        cid = 3
        origin = [0., 0., 0.]
        xaxis = [1., 0., 0.]
        xyplane = [0., 1., 0.]
        coord = CORD2R.add_axes(cid, rid=0, origin=origin,
                                xaxis=xaxis, yaxis=None, zaxis=None,
                                xyplane=xyplane, yzplane=None, xzplane=None,
                                comment='comment')
        eid = 8
        pid = 10
        cp = 0
        nsb = 4
        nint = 2
        lsb = None
        lint = None
        p1 = [0., 0., 0.]
        x12 = 42.
        igid = None
        caero2 = CAERO2(eid, pid, igid, p1, x12,
                        cp=cp, nsb=nsb, nint=nint, lsb=lsb, lint=lint,
                        comment='this is a caero')
        #caero = CAERO2(eid, pid, cp, nsb, nint, lsb, lint, igid, p1, x12)

        sid = 60
        ids = [7, 13]
        set_obj = SET1(sid, ids, is_skin=False, comment='set card')
        grid7 = GRID(nid=7, cp=0, xyz=[7., 0., 0.], cd=0, ps='', seid=0, comment='')
        grid13 = GRID(nid=13, cp=0, xyz=[13., 0., 0.], cd=0, ps='', seid=0, comment='')

        model = BDF(log=None)
        model.add_coord(coord)
        model.add_caero(caero2)
        model.add_set(set_obj)
        model.add_node(grid7)
        model.add_node(grid13)

        eid = 5
        caero = 8
        id1 = 12
        id2 = 24
        setg = 60
        dz = 0.
        dtor = 1.0
        cid = 3
        dthx = 1.
        dthy = None
        usage = None
        card = ['SPLINE2', eid, caero, id1, id2, setg, dz, dtor, cid,
                dthx, dthy, None, usage]

        bdf_card = BDFCard(card, has_none=True)
        spline_a = SPLINE2.add_card(bdf_card, comment='spline2_a')
        spline_a.write_card()

        spline_b = SPLINE2(eid, caero, id1, id2, setg, dz, dtor, cid, dthx,
                           dthy, usage, comment='spline2_b')
        spline_b.validate()
        spline_b.write_card()
        spline_b.cross_reference(model)
        spline_b.write_card()


    def test_caero2_1(self):
        """checks the CAERO2/PAERO2/AERO/AEFACT card"""
        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        eid = 1
        pid = 10
        cp = 4
        nsb = 0
        nint = 0

        lsb = 3
        lint = 6
        igid = 0
        p1 = [0., 1., 2.]
        x12 = 10.
        caero = CAERO2.add_card(BDFCard(['CAERO2', eid, pid, cp, nsb, nint,
                                         lsb, lint, igid, ] + p1 + [x12]))

        #---------------
        caero = CAERO2(eid, pid, igid, p1, x12,
                       cp=cp, nsb=0, nint=nint, lsb=0, lint=lint,
                       comment='this is a caero')
        with self.assertRaises(ValueError):
            caero.validate()

        caero = CAERO2(eid, pid, igid, p1, x12,
                       cp=cp, nsb=lsb, nint=0, lsb=lsb, lint=0,
                       comment='this is a caero')
        with self.assertRaises(ValueError):
            caero.validate()

        #---------------
        caero = CAERO2(eid, pid, igid, p1, x12,
                       cp=cp, nsb=nsb, nint=nint, lsb=lsb, lint=lint,
                       comment='this is a caero')
        caero.validate()
        caero.write_card()

        aefact = AEFACT.add_card(BDFCard(['AEFACT', lint, 0., 1., 2., 3., 4., 5.]))
        aefact = AEFACT(lint, [0., 1., 2., 3., 4., 5.])
        aefact.validate()
        aefact.write_card()
        model.aefacts[lint] = aefact

        orient = 'Z'
        width = 10.
        AR = 2.
        lrsb = 0
        lrib = 3
        lth1 = 0
        lth2 = 0
        thi = [0]
        thn = [0]
        paero = PAERO2.add_card(BDFCard(['PAERO2', pid, orient, width, AR,
                                         lrsb, lrib, lth1, lth2] + thi + thn),
                                comment='paero')
        paero = PAERO2(pid, orient, width, AR, lrsb, lrib, lth1, lth2, thi, thn)
        paero.validate()
        paero.write_card()
        model.paeros[pid] = paero

        coord = CORD2R.add_card(BDFCard(['CORD2R', cp, 0,
                                         0., 0., 0.,
                                         0., 0., 1.,
                                         1., 0., 0.]))
        coord = CORD2R(cp, rid=0, origin=None, zaxis=None, xzplane=None,
                       comment='')
        coord.validate()
        model.coords[cp] = coord

        aefact = AEFACT(lrib, [0., 1., 2., 3., 4., 5.])
        aefact.validate()
        model.aefacts[lrib] = aefact

        acsid = 0
        velocity = None
        cref = 1.0
        rho_ref = 1.0

        aero = AERO.add_card(BDFCard(['AERO', acsid, velocity, cref, rho_ref]))
        aero = AERO(velocity, cref, rho_ref, acsid=acsid,
                    comment='')
        aero.validate()
        aero.write_card()
        model.aero = aero

        paero.cross_reference(model)
        caero.cross_reference(model)
        paero.raw_fields()
        caero.raw_fields()
        caero.uncross_reference()
        caero.raw_fields()
        caero.cross_reference(model)
        caero.get_points_elements_3d()

        caero.get_points()
        #caero.get_points_elements_3d()
        xyz, elems = caero.get_points_elements_3d()
        model.uncross_reference()
        model.safe_cross_reference()
        model.uncross_reference()
        model.write_bdf('aero.temp')
        os.remove('aero.temp')

        model.cross_reference()
        model.write_bdf('aero.temp')
        os.remove('aero.temp')

        nsb = 4
        nint = 2
        lsb = None
        lint = None
        caero2 = CAERO2(eid, pid, igid, p1, x12,
                        cp=cp, nsb=nsb, nint=nint, lsb=lsb, lint=lint,
                        comment='this is a caero')
        caero2.validate()
        caero2.cross_reference(model)
        caero2.write_card()

    def test_caero3_1(self):
        """checks the CAERO3/PAERO3"""
        eid = 100
        pid = 200
        cp = 4
        list_w = 5
        list_c1 = 6
        list_c2 = 7
        p1 = [0., 0., 0.]
        x12 = 10.
        p4 = [5., 10., 0.]
        x43 = 3.

        nbox = 10
        ncontrol_surfaces = 0
        x = None
        y = None

        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        coord = CORD2R.add_card(BDFCard(['CORD2R', cp, 0,
                                         0., 0., 0.,
                                         0., 0., 1.,
                                         1., 0., 0.]))
        coord = CORD2R(cp, rid=0, origin=None, zaxis=None, xzplane=None,
                       comment='')
        coord.validate()
        model.coords[cp] = coord

        paero = PAERO3(pid, nbox, ncontrol_surfaces, x, y)
        model.paeros[pid] = paero

        card = ['CAERO3', 2000, 20001, 0, 22, 33, None, None, None,
                1.0, 0.0, 0., 100., 17., 130., 0., 100.]
        bdf_card = BDFCard(card, has_none=True)
        caero3a = CAERO3.add_card(bdf_card, comment='msg')
        caero3a.validate()
        caero3a.write_card()
        caero3a.raw_fields()

        caero3b = CAERO3(eid, pid, cp, list_w, list_c1, list_c2, p1, x12, p4,
                         x43, comment='caero3')
        model.caeros[pid] = caero3b

        caero3b.write_card()
        caero3b.cross_reference(model)
        caero3b.write_card()
        caero3a.raw_fields()
        caero3b.uncross_reference()
        caero3b.write_card()
        caero3a.raw_fields()

    def test_caero4_1(self):
        """checks the CAERO4/PAERO4"""
        pid = 1001
        docs = []
        caocs = []
        gapocs = []
        paero4 = PAERO4(pid, docs, caocs, gapocs,
                        cla=0, lcla=0, circ=0, lcirc=0,
                        comment='')

        x1 = 0.
        y1 = 0.
        z1 = 0.
        x12 = 100.
        x4 = 50.
        y4 = 0.
        z4 = 0.
        x43 = 10.

        eid = 1000
        nspan = 4  # number of stations
        lspan = 0  # AEFACT
        cp = 0
        card = ['CAERO4', eid, pid, cp, nspan, lspan, None, None, None,
                x1, y1, z1, x12, x4, y4, z4, x43]

        bdf_card = BDFCard(card, has_none=True)
        caero4a = CAERO4.add_card(bdf_card, comment='msg')
        caero4a.validate()
        caero4a.write_card()
        caero4a.raw_fields()

        p1 = [x1, y1, z1]
        p4 = [x4, y4, z4]
        caero4b = CAERO4(eid, pid, cp, nspan, lspan, p1, x12, p4, x43,
                         comment='msg2')
        caero4b.validate()
        caero4b.write_card()
        caero4b.raw_fields()

        model = BDF()
        model.add_paero(paero4)

        caero4b.cross_reference(model)
        caero4b.write_card()
        caero4b.raw_fields()
        p1, p2, p3, p4 = caero4b.get_points()


    def test_caero5_1(self):
        """checks the CAERO5/PAERO5"""
        pid = 6001
        caoci = [0., 0.5, 1.0]
        paero5 = PAERO5(pid, caoci,
                        nalpha=0, lalpha=0, nxis=0, lxis=0, ntaus=0, ltaus=0,
                        comment='msg')

        eid = 6000
        cp = 0
        nspan = 5
        lspan = 0
        ntheory = 0
        nthick = 0
        x1 = 0.
        y1 = 0.
        z1 = 0.
        x12 = 1.
        x4 = 0.2
        y4 = 1.
        z4 = 0.
        x43 = 0.8
        p1 = [x1, y1, z1]
        p4 = [x4, y4, z4]
        caero5 = CAERO5(eid, pid, p1, x12, p4, x43,
                        cp=cp, nspan=nspan, lspan=lspan,
                        ntheory=ntheory, nthick=nthick,
                        comment='msg')

        model = BDF()
        model.add_paero(paero5)
        caero5.cross_reference(model)
        npoints, nelements = caero5.get_npanel_points_elements()
        points, elements = caero5.panel_points_elements()

        caero5.write_card()
        #caero5.raw_fields()

        caero5.uncross_reference()
        caero5.write_card()
        #caero5.raw_fields()


   # def test_paero1_1(self):
   # def test_paero2_1(self):
   # def test_paero3_1(self):
   # def test_paero4_1(self):
   # def test_paero5_1(self):

   # def test_spline1_1(self):
   # def test_spline2_1(self):
   # def test_spline3_1(self):
   # def test_spline4_1(self):
   # def test_spline5_1(self):

    def test_aesurf(self):
        """checks the AESURF/AELIST cards"""
        aesid = 10
        label = 'FLAP'
        cid1 = 0
        aelist_id1 = 10
        cid2 = None
        alid2 = None
        aesurf1 = AESURF(aesid, label, cid1, aelist_id1, cid2, alid2,
                         #eff, ldw,
                         #crefc, crefs, pllim, pulim,
                         #hmllim, hmulim, tqllim, tqulim,
                         comment='aesurf comment')
        aesurf2 = AESURF.add_card(BDFCard(
            [
                'AESURF', aesid, label, cid1, aelist_id1, cid2, alid2,
                #eff, ldw,
                #crefc, crefs, pllim, pulim,
                #hmllim, hmulim, tqllim, tqulim,
            ]), comment='aesurf comment')
        #assert aesurf1 == aesurf2

        cid2 = 1
        aelist_id1 = 10
        aesurf2 = AESURF.add_card(BDFCard(
            [
                'AESURF', aesid, label, cid1, aelist_id1, cid2, alid2,
                #eff, ldw,
                #crefc, crefs, pllim, pulim,
                #hmllim, hmulim, tqllim, tqulim,
            ]), comment='aesurf comment')

        aesurf1.validate()
        aesurf2.validate()
        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        model.aesurf[aesid] = aesurf1

        elements = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        aelist = AELIST(aesid, elements)
        model.aelists[aelist_id1] = aelist
        aesurf1.cross_reference(model)
        aesurf1.write_card()
        aesurf1.raw_fields()
        aesurf1.uncross_reference()
        aesurf1.write_card()
        aesurf1.cross_reference(model)
        aesurf1.raw_fields()

    def test_flutter(self):
        """checks the FLUTTER/FLFACT cards"""
        log = SimpleLogger(level='warning')
        model = BDF(log=log)
        sid = 75
        method = 'PKNL'
        idensity = 76
        imach = 77
        ireduced_freq_velocity = 78

        flutter1 = FLUTTER(sid, method, idensity, imach, ireduced_freq_velocity)
        flutter2 = FLUTTER.add_card(BDFCard(['FLUTTER', sid, method, idensity, imach,
                                             ireduced_freq_velocity]), comment='flutter card')
        flutter1.validate()
        flutter1.write_card()
        flutter2.validate()
        flutter2.write_card()
        model.flutters[75] = flutter1

        densities = np.linspace(0., 1.)
        density = FLFACT(idensity, densities)
        model.flfacts[idensity] = density

        machs = np.linspace(0.7, 0.8)
        mach = FLFACT(imach, machs)
        mach = FLFACT.add_card(BDFCard(['FLFACT', imach] + list(machs)), comment='flfact card')
        mach.write_card(size=16)
        model.flfacts[imach] = mach

        velocities = np.linspace(3., 4.)
        velocity = FLFACT(ireduced_freq_velocity, velocities)
        velocity.validate()
        velocity.write_card()
        assert velocity.min() == 3., velocities
        assert velocity.max() == 4., velocities
        model.flfacts[ireduced_freq_velocity] = velocity

        model.cross_reference()
        #model.uncross_reference()
        #model.safe_cross_reference()

    def test_mkaero1(self):
        """checks the MKAERO1 card"""
        machs = [0.5, 0.75]
        reduced_freqs = [0.1, 0.2, 0.3, 0.4]
        mkaero = MKAERO1(machs, reduced_freqs, comment='mkaero')
        mkaero.validate()
        mkaero.write_card()
        mkaero = MKAERO1.add_card(BDFCard(
            ['MKAERO', 0.5, 0.75, None, None, None, None, None, None,
             0.1, 0.2, 0.3, 0.4],
        ))

        machs = [0.5, 0.75]
        reduced_freqs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]
        mkaero = MKAERO1(machs, reduced_freqs, comment='mkaero')
        mkaero.validate()
        mkaero.write_card()

    def test_mkaero2(self):
        """checks the MKAERO2 card"""
        machs = [0.5, 0.75, 0.8]
        reduced_freqs = [0.1, 0.2, 0.3]
        mkaero = MKAERO2(machs, reduced_freqs, comment='mkaero2')
        mkaero.validate()
        mkaero.write_card()

        machs = [0.5, 0.75]
        reduced_freqs = [0.1, 0.2]
        mkaero = MKAERO2(machs, reduced_freqs, comment='mkaero2')
        mkaero.validate()
        mkaero.write_card()

        mkaero = MKAERO2.add_card(BDFCard(['MKAERO2'] + machs + reduced_freqs), comment='mkaero2')
        mkaero.validate()
        mkaero.write_card()

    def test_diverg(self):
        """checks the DIVERG card"""
        log = SimpleLogger(level='warning')
        model = BDF(log=log)

        sid = 100
        nroots = 21
        machs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        x0 = 3.
        V = 42.
        diverg = DIVERG(sid, nroots, machs, comment='divergence')
        diverg.validate()
        diverg.write_card()

        diverg = model.add_card(['DIVERG', sid, nroots] + machs, 'DIVERG', comment='divergence')
        #diverg.validate()
        #diverg.write_card()

    def test_trim(self):
        """checks the TRIM card"""
        log = SimpleLogger(level='warning')
        model = BDF(log=log)

        sid = 100
        mach = 0.75
        q = 100.
        labels = ['ALPHA', 'ALPHA']
        uxs = [10., 20.]
        trim = TRIM(sid, mach, q, labels, uxs)
        with self.assertRaises(RuntimeError):
            trim.validate()

        labels = ['ALPHA']
        uxs = [10., 20.]
        trim = TRIM(sid, mach, q, labels, uxs)
        with self.assertRaises(RuntimeError):
            trim.validate()

        labels = ['ALPHA', 'BETA']
        uxs = [10., 20.]
        trim = TRIM(sid, mach, q, labels, uxs)
        trim.validate()
        trim.write_card()

        labels = ['ALPHA']
        uxs = [10.]
        trim = TRIM(sid, mach, q, labels, uxs, aeqr=3.0, comment='')
        trim.validate()
        trim.write_card()

        labels = ['ALPHA', 'BETA']
        uxs = [10., 20.]
        trim = TRIM(sid, mach, q, labels, uxs, aeqr=3.0, comment='')
        trim.validate()
        trim.write_card()

        model.add_card(['TRIM', sid, mach, q, labels[0], uxs[0]], 'TRIM', comment='$ trim')

    def test_gust(self):
        """checks the GUST card"""
        sid = 100
        dload = 200
        wg = 50.
        x0 = 3.
        V = 42.
        gust = GUST(sid, dload, wg, x0, V, comment='gust load')
        gust.validate()
        gust.write_card()

        gust2 = GUST.add_card(BDFCard(['GUST', sid, dload, wg, x0, V]), comment='gust load')
        gust2.validate()
        gust2.write_card()

    def test_csschd(self):
        """checks the CSSCHD card"""
        #sid = 10
        #aesid = 0
        #lalpha = None
        #lmach = None
        #lschd = None

        sid = 5
        aesid = 50
        lalpha = 12
        lmach = 15
        lschd = 25

        card = ['CSSCHD', sid, aesid, lalpha, lmach, lschd]
        bdf_card = BDFCard(card, has_none=True)
        csshcd1 = CSSCHD.add_card(bdf_card, comment='csschd card')
        csshcd1.validate()
        csshcd1.write_card()

        label = 'ELEV'
        cid1 = 0
        alid1 = 37
        aesurf = AESURF(aesid, label, cid1, alid1)

        aefact_sid = alid1
        Di = [0., 0.5, 1.]
        aefact_elev = AEFACT(aefact_sid, Di)

        aefact_sid = lalpha
        Di = [0., 5., 10.]
        aefact_alpha = AEFACT(aefact_sid, Di)

        aefact_sid = lmach
        Di = [0., 0.7, 0.8]
        aefact_mach = AEFACT(aefact_sid, Di)

        aefact_sid = lschd
        Di = [0., 15., 30., 45.]
        aefact_delta = AEFACT(aefact_sid, Di)

        model = BDF()
        model.add_aesurf(aesurf)
        model.add_aefact(aefact_elev)
        model.add_aefact(aefact_alpha)
        model.add_aefact(aefact_mach)
        model.add_aefact(aefact_delta)

        csshcd1.cross_reference(model)
        csshcd1.write_card()
        csshcd1.uncross_reference()
        csshcd1.write_card()

        #-----------
        lalpha = None
        lmach = None
        csshcd2 = CSSCHD(sid, aesid, lschd, lalpha=lalpha, lmach=lmach, comment='cssch card')
        csshcd2.write_card()
        with self.assertRaises(RuntimeError):
            csshcd2.validate()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
