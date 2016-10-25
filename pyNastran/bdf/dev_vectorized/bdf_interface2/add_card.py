from pyNastran.bdf.dev_vectorized.bdf_interface2.attributes import BDFAttributes


class AddCard(BDFAttributes):
    """defines methods to add card objects to the BDF"""
    def __init__(self):

    def add_param(self, param, allow_overwrites=False):
        """adds a PARAM object"""
        key = param.key
        if key in self.params and not allow_overwrites:
            if not param._is_same_card(self.params[key]):
                #if param.key in self.params:
                    #msg = 'key=%s param=%s old_param=%s' % (key, param, self.params[key])
                    #raise KeyError(msg)
                self.log.warning('key=%s param=%s old_param=%s' %
                                 (key, param, self.params[key]))
                self.params[key] = param
        else:
            self.params[key] = param
            self._type_to_id_map[param.type].append(key)

        pass
    def add_plotel(self, elem, allow_overwrites=False):
        """adds an PLOTEL object"""
        key = elem.eid
        assert key > 0, 'eid=%s must be positive; elem=\n%s' % (key, elem)
        if not allow_overwrites:
            if key in self.elements:
                if elem._is_same_card(self.elements[key]):
                    self._duplicate_elements.append(elem)
                    if self._stop_on_duplicate_error:
                        self.pop_parse_errors()
            elif key in self.plotels:
                if not elem._is_same_card(self.plotels[key]):
                    assert elem.eid not in self.plotels, 'eid=%s\nold_element=\n%snew_element=\n%s' % (elem.eid, self.plotels[elem.eid], elem)
        self.plotels[key] = elem
        self._type_to_id_map[elem.type].append(key)

    def add_aero(self, aero):
        """adds an AERO object"""
        # only one AERO card allowed
        assert self.aero is None, '\naero=\n%s old=\n%s' % (aero, self.aero)
        self.aero = aero
        #self._type_to_id_map[aero.type].append(key)

    def add_aeros(self, aeros):
        """adds an AEROS object"""
        # only one AEROS card allowed
        assert self.aeros is None, '\naeros=\n%s old=\n%s' % (aeros, self.aeros)
        self.aeros = aeros
        #self._type_to_id_map[aeros.type].append(key)

    def add_aefact(self, aefact, allow_overwrites=False):
        """adds an AEFACT object"""
        key = aefact.sid
        if key in self.aefacts and not allow_overwrites:
            if not aefact._is_same_card(self.aefacts[key]):
                assert key not in self.aefacts, 'AEFACT.sid=%s\nold=\n%snew=\n%s' % (key, self.aefacts[key], aefact)
        else:
            assert key > 0, 'sid=%s method=\n%s' % (key, aefact)
            self.aefacts[key] = aefact
            self._type_to_id_map[aefact.type].append(key)

    def add_aelist(self, aelist):
        """adds an AELIST object"""
        key = aelist.sid
        assert key not in self.aelists, 'AELIST.sid=%s\nold=\n%snew=\n%s' % (key, self.aelists[key], aelist)
        assert key >= 0
        self.aelists[key] = aelist
        self._type_to_id_map[aelist.type].append(key)

    def add_aelink(self, aelink):
        """adds an AELINK object"""
        key = aelink.id
        assert key >= 0
        if key not in self.aelinks:
            self.aelinks[key] = []
        self.aelinks[key].append(aelink)
        self._type_to_id_map[aelink.type].append(key)
        #assert key not in self.aestats,'\naestat=%s oldAESTAT=\n%s' %(aestat,self.aestats[key])

    def add_aecomp(self, aecomp):
        """adds an AECOMP object"""
        key = aecomp.name
        assert key not in self.aecomps, '\naecomp=\n%s oldAECOMP=\n%s' % (aecomp, self.aecomps[key])
        self.aecomps[key] = aecomp
        self._type_to_id_map[aecomp.type].append(key)

    def add_aeparm(self, aeparam):
        """adds an AEPARM object"""
        key = aeparam.id
        assert key not in self.aeparams, '\naeparam=\n%s oldAEPARM=\n%s' % (aeparam, self.aeparams[key])
        assert key >= 0
        self.aeparams[key] = aeparam
        self._type_to_id_map[aeparam.type].append(key)

    def add_aestat(self, aestat):
        """adds an AESTAT object"""
        key = aestat.id
        assert key not in self.aestats, '\naestat=\n%s old=\n%s' % (
            aestat, self.aestats[key])
        assert key >= 0
        self.aestats[key] = aestat
        self._type_to_id_map[aestat.type].append(key)

    def add_aesurf(self, aesurf):
        """adds an AESURF object"""
        key = aesurf.aesid
        assert key not in self.aesurf, '\naesurf=\n%s old=\n%s' % (
            aesurf, self.aesurf[key])
        assert key >= 0
        self.aesurf[key] = aesurf
        self._type_to_id_map[aesurf.type].append(key)

    def add_aesurfs(self, aesurfs):
        """adds an AESURFS object"""
        key = aesurfs.aesid
        assert key not in self.aesurf, '\naesurfs=\n%s old=\n%s' % (
            aesurfs, self.aesurfs[key])
        assert key >= 0
        self.aesurfs[key] = aesurfs
        self._type_to_id_map[aesurfs.type].append(key)

    def add_csschd(self, csschd):
        """adds an CSSCHD object"""
        key = csschd.sid
        assert key not in self.csschds, '\nCSSCHD=\n%s old=\n%s' % (csschd, self.csschds[key])
        assert key >= 0
        self.csschds[key] = csschd
        self._type_to_id_map[csschd.type].append(key)

    def add_caero(self, caero):
        """adds an CAERO1/CAERO2/CAERO3/CAERO4/CAERO5 object"""
        key = caero.eid
        assert key not in self.caeros, '\ncaero=\n|%s| old_caero=\n|%s|' % (
            caero, self.caeros[key])
        assert key > 0
        self.caeros[key] = caero
        self._type_to_id_map[caero.type].append(key)

    def add_paero(self, paero):
        key = paero.pid
        assert key not in self.paeros, '\npaero=\n|%s| old_paero=\n|%s|' % (
            paero, self.paeros[key])
        assert key > 0, 'paero.pid = %r' % (key)
        self.paeros[key] = paero
        self._type_to_id_map[paero.type].append(key)

    def add_monpnt(self, monitor_point):
        """adds an MONPNT object"""
        key = monitor_point.name
        assert key not in self.monitor_points, '\nmonitor_point=\n%soldMNTPNT=\n%s' % (
            monitor_point, self.monitor_points[key])
        self.monitor_points.append(monitor_point)
        self._type_to_id_map[monitor_point.type].append(len(self.monitor_points) - 1)

    def add_spline(self, spline):
        """adds an SPLINE1/SPLINE2/SPLINE3/SPLINE4/SPLINE5 object"""
        assert spline.eid not in self.splines
        assert spline.eid > 0
        key = spline.eid
        self.splines[key] = spline
        self._type_to_id_map[spline.type].append(key)

    def add_gust(self, gust):
        """adds an GUST object"""
        key = gust.sid
        assert key not in self.gusts
        assert key > 0
        self.gusts[key] = gust
        self._type_to_id_map[gust.type].append(key)

    def add_trim(self, trim, allow_overwrites=False):
        """adds an TRIM object"""
        key = trim.sid
        if not allow_overwrites:
            assert key not in self.trims, 'TRIM=%s  old=\n%snew=\n%s' % (key, self.trims[key], trim)
        assert key > 0, 'key=%r trim=\n%s' % (key, trim)
        self.trims[key] = trim
        self._type_to_id_map[trim.type].append(key)

    def add_diverg(self, diverg, allow_overwrites=False):
        """adds an DIVERG object"""
        key = diverg.sid
        if not allow_overwrites:
            assert key not in self.divergs, 'DIVERG=%s  old=\n%snew=\n%s' % (key, self.divergs[key], diverg)
        assert key > 0, 'key=%r diverg=\n%s' % (key, diverg)
        self.divergs[key] = diverg
        self._type_to_id_map[diverg.type].append(key)

    def add_flutter(self, flutter):
        """adds an FLUTTER object"""
        key = flutter.sid
        assert key not in self.flutters, 'FLUTTER=%s old=\n%snew=\n%s' % (key, self.flutters[key], flutter)
        assert key > 0
        self.flutters[key] = flutter
        self._type_to_id_map[flutter.type].append(key)

    def add_flfact(self, flfact):
        """adds an FLFACT object"""
        key = flfact.sid
        #assert key not in self.flfacts
        assert key > 0
        self.flfacts[key] = flfact  # set id...
        self._type_to_id_map[flfact.type].append(key)


    def add_set(self, set_obj):
        """adds an SET1/SET3 object"""
        key = set_obj.sid
        assert key >= 0
        if key in self.sets:
            self.sets[key].add_set(set_obj)
        else:
            self.sets[key] = set_obj
            self._type_to_id_map[set_obj.type].append(key)

    def add_aset(self, set_obj):
        """adds an ASET/ASET1 object"""
        self.asets.append(set_obj)

    def add_bset(self, set_obj):
        """adds an BSET/BSET1 object"""
        self.bsets.append(set_obj)

    def add_cset(self, set_obj):
        """adds an CSET/USET1 object"""
        self.csets.append(set_obj)

    def add_qset(self, set_obj):
        """adds an QSET/QSET1 object"""
        self.qsets.append(set_obj)

    def add_uset(self, set_obj):
        """adds an USET/USET1 object"""
        key = set_obj.name
        if key in self.usets:
            self.usets[key].append(set_obj)
        else:
            self.usets[key] = [set_obj]

    def add_sebset(self, set_obj):
        """adds an SEBSET/SEBSET1 object"""
        self.se_bsets.append(set_obj)

    def add_secset(self, set_obj):
        """adds an SECSET/SECSTE1 object"""
        self.se_csets.append(set_obj)

    def add_seqset(self, set_obj):
        """adds an SEQSET/SEQSET1 object"""
        self.se_qsets.append(set_obj)

    def add_seuset(self, set_obj):
        """adds an SEUSET/SEUSET1 object"""
        key = set_obj.name
        if key in self.se_usets:
            self.se_usets[key].append(set_obj)
        else:
            self.se_usets[key] = [set_obj]

    def add_seset(self, set_obj):
        """adds an SESET object"""
        key = set_obj.seid
        assert key >= 0
        if key in self.se_sets:
            old_set = self.se_sets[key]
            set_obj.add_seset(old_set)
        self.se_sets[key] = set_obj
        self._type_to_id_map[set_obj.type].append(key)

    def add_method(self, method, allow_overwrites=False):
        key = method.sid
        if key in self.methods and not allow_overwrites:
            if not method._is_same_card(self.methods[key]):
                assert key not in self.methods, 'sid=%s\nold_method=\n%snew_method=\n%s' % (key, self.methods[key], method)
        else:
            assert key > 0, 'sid=%s method=\n%s' % (key, method)
            self.methods[key] = method
            self._type_to_id_map[method.type].append(key)

    def add_cmethod(self, method, allow_overwrites=False):
        key = method.sid
        if key in self.cMethods and not allow_overwrites:
            if not method._is_same_card(self.cMethods[key]):
                assert key not in self.cMethods, 'sid=%s\nold_cmethod=\n%snew_cmethod=\n%s' % (key, self.cMethods[key], method)
        else:
            assert key > 0, 'sid=%s cMethod=\n%s' % (key, method)
            self.cMethods[key] = method
            self._type_to_id_map[method.type].append(key)

    def add_mkaero(self, mkaero):
        """adds an MKAERO1/MKAERO2 object"""
        self.mkaeros.append(mkaero)