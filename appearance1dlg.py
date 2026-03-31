import wx
import planets
import chart
import options
import mtexts

#---------------------------------------------------------------------------
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)
#---------------------------------------------------------------------------

class Appearance1Dlg(wx.Dialog):
	def __init__(self, parent):
		# CORRECCIÓN: Eliminamos 'pre' y llamamos directamente al constructor
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Appearance1'], pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
		
		if hasattr(wx, 'DIALOG_EX_CONTEXTHELP'):
			self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)

		# main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		# main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		# In Chart
		inchart = wx.StaticBox(self, label=mtexts.txts['InChart'])
		inchartsizer = wx.StaticBoxSizer(inchart, wx.HORIZONTAL)
		
		asps = wx.StaticBox(self, label='')
		vsizer = wx.StaticBoxSizer(asps, wx.VERTICAL)
		self.aspectsckb = wx.CheckBox(self, -1, mtexts.txts['Aspects'])
		vsizer.Add(self.aspectsckb, 0, wx.ALIGN_LEFT|wx.ALL|wx.TOP, 2)
		
		vsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.conjunctiockb = wx.CheckBox(self, -1, mtexts.txts['Conjunctio'])
		vsubsizer.Add(self.conjunctiockb, 0, wx.ALL, 2)
		self.semisextilckb = wx.CheckBox(self, -1, mtexts.txts['Semisextil'])
		vsubsizer.Add(self.semisextilckb, 0, wx.ALL, 2)
		self.semiquadratckb = wx.CheckBox(self, -1, mtexts.txts['Semiquadrat'])
		vsubsizer.Add(self.semiquadratckb, 0, wx.ALL, 2)
		self.sextilckb = wx.CheckBox(self, -1, mtexts.txts['Sextil'])
		vsubsizer.Add(self.sextilckb, 0, wx.ALL, 2)
		self.quintileckb = wx.CheckBox(self, -1, mtexts.txts['Quintile'])
		vsubsizer.Add(self.quintileckb, 0, wx.ALL, 2)
		self.quadratckb = wx.CheckBox(self, -1, mtexts.txts['Quadrat'])
		vsubsizer.Add(self.quadratckb, 0, wx.ALL, 2)
		self.trigonckb = wx.CheckBox(self, -1, mtexts.txts['Trigon'])
		vsubsizer.Add(self.trigonckb, 0, wx.ALL, 2)
		self.sesquiquadratckb = wx.CheckBox(self, -1, mtexts.txts['Sesquiquadrat'])
		vsubsizer.Add(self.sesquiquadratckb, 0, wx.ALL, 2)
		self.biquintileckb = wx.CheckBox(self, -1, mtexts.txts['Biquintile'])
		vsubsizer.Add(self.biquintileckb, 0, wx.ALL, 2)
		self.quinqunxckb = wx.CheckBox(self, -1, mtexts.txts['Quinqunx'])
		vsubsizer.Add(self.quinqunxckb, 0, wx.ALL, 2)
		self.oppositiockb = wx.CheckBox(self, -1, mtexts.txts['Oppositio'])
		vsubsizer.Add(self.oppositiockb, 0, wx.ALL, 2)
		
		vsizer.Add(vsubsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 12)
		self.Bind(wx.EVT_CHECKBOX, self.onAspects, id=self.aspectsckb.GetId())

		self.symbolsckb = wx.CheckBox(self, -1, mtexts.txts['WithSymbols'])
		vsizer.Add(self.symbolsckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.traditionalaspectsckb = wx.CheckBox(self, -1, mtexts.txts['AspectsDontCross'])
		vsizer.Add(self.traditionalaspectsckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		inchartsizer.Add(vsizer, 0, wx.LEFT|wx.BOTTOM, 5)

		vsizer2 = wx.BoxSizer(wx.VERTICAL)
		self.uranusckb = wx.CheckBox(self, -1, mtexts.txts['Uranus'])
		vsizer2.Add(self.uranusckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.neptuneckb = wx.CheckBox(self, -1, mtexts.txts['Neptune'])
		vsizer2.Add(self.neptuneckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.plutockb = wx.CheckBox(self, -1, mtexts.txts['Pluto'])
		vsizer2.Add(self.plutockb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.shownodesckb = wx.CheckBox(self, -1, mtexts.txts['Nodes'])
		vsizer2.Add(self.shownodesckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.Bind(wx.EVT_CHECKBOX, self.onNodes, id=self.shownodesckb.GetId())
		
		vnodessubsizer = wx.BoxSizer(wx.VERTICAL)
		self.asps2nodesckb = wx.CheckBox(self, -1, mtexts.txts['Asps2Nodes'])
		vnodessubsizer.Add(self.asps2nodesckb, 0, wx.ALL, 2)
		vsizer2.Add(vnodessubsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 12)
		
		self.lofckb = wx.CheckBox(self, -1, mtexts.txts['LotOfFortune'])
		self.Bind(wx.EVT_CHECKBOX, self.onLoF, id=self.lofckb.GetId())
		vsizer2.Add(self.lofckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		
		vlofsubsizer = wx.BoxSizer(wx.VERTICAL)
		self.asps2lofckb = wx.CheckBox(self, -1, mtexts.txts['Asps2LoF'])
		vlofsubsizer.Add(self.asps2lofckb, 0, wx.ALL, 2)
		vsizer2.Add(vlofsubsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 12)
		
		self.housesckb = wx.CheckBox(self, -1, mtexts.txts['Houses'])
		vsizer2.Add(self.housesckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.intablesckb = wx.CheckBox(self, -1, mtexts.txts['InTables'])
		vsizer2.Add(self.intablesckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.positionsckb = wx.CheckBox(self, -1, mtexts.txts['Positions'])
		vsizer2.Add(self.positionsckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		self.termsckb = wx.CheckBox(self, -1, mtexts.txts['Terms'])
		vsizer2.Add(self.termsckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.decansckb = wx.CheckBox(self, -1, mtexts.txts['Decans'])
		vsizer2.Add(self.decansckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		inchartsizer.Add(vsizer2, 0, wx.TOP|wx.LEFT, 5)

		vsizer3 = wx.BoxSizer(wx.VERTICAL)
		self.nonerb = wx.RadioButton(self, -1, mtexts.txts['None'], style=wx.RB_GROUP)
		self.Bind(wx.EVT_RADIOBUTTON, self.onNone, id=self.nonerb.GetId())
		vsizer3.Add(self.nonerb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.fixstarsrb = wx.RadioButton(self, -1, mtexts.txts['FixStars'])
		self.Bind(wx.EVT_RADIOBUTTON, self.onFixStars, id=self.fixstarsrb.GetId())
		vsizer3.Add(self.fixstarsrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		
		vfssubsizer = wx.BoxSizer(wx.VERTICAL)
		self.fixstarsnodesckb = wx.CheckBox(self, -1, mtexts.txts['Nodes'])
		vfssubsizer.Add(self.fixstarsnodesckb, 0, wx.ALL, 2)
		self.fixstarshcsckb = wx.CheckBox(self, -1, mtexts.txts['IntermHCS'])
		vfssubsizer.Add(self.fixstarshcsckb, 0, wx.ALL, 2)
		self.fixstarslofckb = wx.CheckBox(self, -1, mtexts.txts['LoF'])
		vfssubsizer.Add(self.fixstarslofckb, 0, wx.ALL, 2)
		vsizer3.Add(vfssubsizer, 0, wx.ALIGN_LEFT|wx.LEFT, 12)
		
		self.dodecsrb = wx.RadioButton(self, -1, mtexts.txts['Dodecatemoria'])
		self.Bind(wx.EVT_RADIOBUTTON, self.onDodec, id=self.dodecsrb.GetId())
		vsizer3.Add(self.dodecsrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.antisrb = wx.RadioButton(self, -1, mtexts.txts['Antiscia'])
		self.Bind(wx.EVT_RADIOBUTTON, self.onAntis, id=self.antisrb.GetId())
		vsizer3.Add(self.antisrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.cantisrb = wx.RadioButton(self, -1, mtexts.txts['ContraAntiscia'])
		self.Bind(wx.EVT_RADIOBUTTON, self.onCAntis, id=self.cantisrb.GetId())
		vsizer3.Add(self.cantisrb, 0, wx.ALIGN_LEFT|wx.ALL, 2)
		self.topocentricckb = wx.CheckBox(self, -1, mtexts.txts['Topocentric'])
		vsizer3.Add(self.topocentricckb, 0, wx.ALIGN_LEFT|wx.ALL, 2)

		inchartsizer.Add(vsizer3, 0, wx.TOP|wx.LEFT, 5)

		vsizerbig = wx.BoxSizer(wx.VERTICAL)
		vsizerbig.Add(inchartsizer, 0, wx.GROW|wx.RIGHT|wx.TOP, 5)

		# Traditional name of Fixstars
		tradfs = wx.StaticBox(self, label='')
		tradfssizer = wx.StaticBoxSizer(tradfs, wx.VERTICAL)
		self.tradfsckb = wx.CheckBox(self, -1, mtexts.txts['ShowTradFSNamesInPDList'])
		tradfssizer.Add(self.tradfsckb, 0, wx.GROW|wx.RIGHT|wx.TOP, 5)

		vsizerbig.Add(tradfssizer, 0, wx.GROW|wx.RIGHT, 5)
		mhsizer.Add(vsizerbig, 0, wx.LEFT, 5)

		self.Bind(wx.EVT_CHECKBOX, self.onUranus, self.uranusckb)
		self.Bind(wx.EVT_CHECKBOX, self.onNeptune, self.neptuneckb)
		self.Bind(wx.EVT_CHECKBOX, self.onPluto, self.plutockb)

		vsizer_col = wx.BoxSizer(wx.VERTICAL)

		# Color Table
		color = wx.StaticBox(self, label=mtexts.txts["Color"])
		colorsizer = wx.StaticBoxSizer(color, wx.VERTICAL)
		self.bwrb = wx.RadioButton(self, -1, mtexts.txts['BlackAndWhite'], style=wx.RB_GROUP)
		colorsizer.Add(self.bwrb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 2)
		self.colorrb = wx.RadioButton(self, -1, mtexts.txts['InColor'])
		colorsizer.Add(self.colorrb, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, 2)

		vsizer_col.Add(colorsizer, 0, wx.GROW|wx.RIGHT, 5)
		
		# Themes
		themes = wx.StaticBox(self, label=mtexts.txts["Themes"])
		themesizer = wx.StaticBoxSizer(themes, wx.VERTICAL)
		self.themecb = wx.ComboBox(self, -1, mtexts.themeList[0], size=(100, -1), choices=mtexts.themeList, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		themesizer.Add(self.themecb, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
		vsizer_col.Add(themesizer, 0, wx.GROW|wx.RIGHT, 5)

		# AscMC-size
		ascmcsize = wx.StaticBox(self, label=mtexts.txts["AscMCWidth"])
		ascmcsizesizer = wx.StaticBoxSizer(ascmcsize, wx.VERTICAL)
		self.ascmcsizeslider = wx.Slider(self, -1, 5, 2, 5, size=(140,-1), style=wx.SL_LABELS)
		ascmcsizesizer.Add(self.ascmcsizeslider, 1, wx.ALIGN_CENTRE, 5)
		vsizer_col.Add(ascmcsizesizer, 0, wx.GROW|wx.RIGHT, 5)

		# Table-size
		tablesize = wx.StaticBox(self, label=mtexts.txts["TableSize"])
		tablesizesizer = wx.StaticBoxSizer(tablesize, wx.VERTICAL)
		self.sizeslider = wx.Slider(self, -1, 75, 50, 100, size=(140,-1), style=wx.SL_LABELS)
		tablesizesizer.Add(self.sizeslider, 1, wx.ALIGN_CENTRE, 5)
		vsizer_col.Add(tablesizesizer, 0, wx.GROW|wx.RIGHT, 5)

		# Show
		planetary = wx.StaticBox(self, label=mtexts.txts["ShowPlanetary"])
		planetarysizer = wx.StaticBoxSizer(planetary, wx.VERTICAL)
		self.planetarydayhour = wx.CheckBox(self, -1, mtexts.txts['PlanetaryHour'])
		planetarysizer.Add(self.planetarydayhour, 1, wx.ALL, 2)
		self.housesystem = wx.CheckBox(self, -1, mtexts.txts['Housesystem'])
		planetarysizer.Add(self.housesystem, 1, wx.ALL, 2)
		vsizer_col.Add(planetarysizer, 0, wx.GROW|wx.RIGHT|wx.TOP, 5)

		# Netbook
		netb = wx.StaticBox(self, label='')
		netbsizer = wx.StaticBoxSizer(netb, wx.VERTICAL)
		self.netbckb = wx.CheckBox(self, -1, mtexts.txts['Netbook'])
		netbsizer.Add(self.netbckb, 0, wx.ALL, 0)
		vsizer_col.Add(netbsizer, 1, wx.GROW|wx.RIGHT, 5)

		mhsizer.Add(vsizer_col, 0, wx.GROW|wx.LEFT, 5)
		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALL, 0)

		btnsizer = wx.StdDialogButtonSizer()
		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)

		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)
		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		
		# Conectamos el botón OK con nuestra nueva función de guardado
		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)

		self.SetSizer(mvsizer)
		mvsizer.Fit(self)
		btnOk.SetFocus()

	def onAspects(self, event):
		self.changeAspects(self.aspectsckb.GetValue())

	def changeAspects(self, enable):
		ar = [self.conjunctiockb, self.semisextilckb, self.semiquadratckb, self.sextilckb, self.quintileckb, self.quadratckb, self.trigonckb, self.sesquiquadratckb, self.biquintileckb, self.quinqunxckb, self.oppositiockb]
		for asp in ar:
			asp.Enable(enable)

	def onNodes(self, event):
		self.asps2nodesckb.Enable(self.shownodesckb.GetValue())

	def onLoF(self, event):
		self.asps2lofckb.Enable(self.lofckb.GetValue())

	def onNone(self, event):
		self.enableSubFixstars(False)

	def onFixStars(self, event):
		self.enableSubFixstars(True)

	def onDodec(self, event):
		self.enableSubFixstars(False)

	def onAntis(self, event):
		self.enableSubFixstars(False)

	def onCAntis(self, event):
		self.enableSubFixstars(False)

	def enableSubFixstars(self, enable):
		self.fixstarshcsckb.Enable(enable)
		self.fixstarslofckb.Enable(enable)
		self.fixstarsnodesckb.Enable(enable)

	def onUranus(self, event):
		if (not self.uranusckb.GetValue()):
			self.neptuneckb.SetValue(False)
			self.plutockb.SetValue(False)

	def onNeptune(self, event):
		if (self.neptuneckb.GetValue()):
			self.uranusckb.SetValue(True)
		else:
			self.plutockb.SetValue(False)

	def onPluto(self, event):
		if (self.plutockb.GetValue()):
			self.uranusckb.SetValue(True)
			self.neptuneckb.SetValue(True)

	def fill(self, opts):
		self.aspectsckb.SetValue(opts.aspects)
		self.conjunctiockb.SetValue(opts.aspect[chart.Chart.CONJUNCTIO])
		self.semisextilckb.SetValue(opts.aspect[chart.Chart.SEMISEXTIL])
		self.semiquadratckb.SetValue(opts.aspect[chart.Chart.SEMIQUADRAT])
		self.sextilckb.SetValue(opts.aspect[chart.Chart.SEXTIL])
		self.quintileckb.SetValue(opts.aspect[chart.Chart.QUINTILE])
		self.quadratckb.SetValue(opts.aspect[chart.Chart.QUADRAT])
		self.trigonckb.SetValue(opts.aspect[chart.Chart.TRIGON])
		self.sesquiquadratckb.SetValue(opts.aspect[chart.Chart.SESQUIQUADRAT])
		self.biquintileckb.SetValue(opts.aspect[chart.Chart.BIQUINTILE])
		self.quinqunxckb.SetValue(opts.aspect[chart.Chart.QUINQUNX])
		self.oppositiockb.SetValue(opts.aspect[chart.Chart.OPPOSITIO])
		self.symbolsckb.SetValue(opts.symbols)
		self.traditionalaspectsckb.SetValue(opts.traditionalaspects)
		self.housesckb.SetValue(opts.houses)
		self.positionsckb.SetValue(opts.positions)

		self.changeAspects(self.aspectsckb.GetValue())

		if (opts.bw):
			self.bwrb.SetValue(opts.bw)
		else:
			self.colorrb.SetValue(not opts.bw)

		self.themecb.SetStringSelection(mtexts.themeList[opts.theme])
		self.ascmcsizeslider.SetValue(opts.ascmcsize)
		self.sizeslider.SetValue(int(opts.tablesize*100)) # Cast a int para evitar problemas en Slider
		self.planetarydayhour.SetValue(opts.planetarydayhour)
		self.housesystem.SetValue(opts.housesystem)

		self.uranusckb.SetValue(opts.transcendental[chart.Chart.TRANSURANUS])
		self.neptuneckb.SetValue(opts.transcendental[chart.Chart.TRANSNEPTUNE])
		self.plutockb.SetValue(opts.transcendental[chart.Chart.TRANSPLUTO])

		self.shownodesckb.SetValue(opts.shownodes)
		self.asps2nodesckb.SetValue(opts.aspectstonodes)
		self.asps2nodesckb.Enable(self.shownodesckb.GetValue())

		self.intablesckb.SetValue(opts.intables)
		self.lofckb.SetValue(opts.showlof)
		self.asps2lofckb.SetValue(opts.showaspectstolof)
		self.asps2lofckb.Enable(self.lofckb.GetValue())

		self.termsckb.SetValue(opts.showterms)
		self.decansckb.SetValue(opts.showdecans)

		if opts.showfixstars == options.Options.NONE:
			self.nonerb.SetValue(True)
			self.enableSubFixstars(False)
		elif opts.showfixstars == options.Options.FIXSTARS:
			self.fixstarsrb.SetValue(True)
			self.enableSubFixstars(True)
		elif opts.showfixstars == options.Options.DODECATEMORIA:
			self.dodecsrb.SetValue(True)
			self.enableSubFixstars(False)
		elif opts.showfixstars == options.Options.ANTIS:
			self.antisrb.SetValue(True)
			self.enableSubFixstars(False)
		elif opts.showfixstars == options.Options.CANTIS:
			self.cantisrb.SetValue(True)
			self.enableSubFixstars(False)

		self.fixstarshcsckb.SetValue(opts.showfixstarshcs)
		self.fixstarslofckb.SetValue(opts.showfixstarslof)
		self.fixstarsnodesckb.SetValue(opts.showfixstarsnodes)
		self.topocentricckb.SetValue(opts.topocentric)
		self.tradfsckb.SetValue(opts.usetradfixstarnamespdlist)
		self.netbckb.SetValue(opts.netbook)

	def check(self, opts):
		changed = False

		# Aspectos
		if opts.aspects != self.aspectsckb.GetValue():
			opts.aspects = self.aspectsckb.GetValue()
			changed = True
		
		# Diccionario de aspectos (Conjuncion, Sextil, etc)
		asps_keys = [
			(chart.Chart.CONJUNCTIO, self.conjunctiockb),
			(chart.Chart.SEMISEXTIL, self.semisextilckb),
			(chart.Chart.SEMIQUADRAT, self.semiquadratckb),
			(chart.Chart.SEXTIL, self.sextilckb),
			(chart.Chart.QUINTILE, self.quintileckb),
			(chart.Chart.QUADRAT, self.quadratckb),
			(chart.Chart.TRIGON, self.trigonckb),
			(chart.Chart.SESQUIQUADRAT, self.sesquiquadratckb),
			(chart.Chart.BIQUINTILE, self.biquintileckb),
			(chart.Chart.QUINQUNX, self.quinqunxckb),
			(chart.Chart.OPPOSITIO, self.oppositiockb)
		]
		for key, control in asps_keys:
			if opts.aspect[key] != control.GetValue():
				opts.aspect[key] = control.GetValue()
				changed = True

		# Opciones generales
		if opts.symbols != self.symbolsckb.GetValue():
			opts.symbols = self.symbolsckb.GetValue()
			changed = True
		if opts.traditionalaspects != self.traditionalaspectsckb.GetValue():
			opts.traditionalaspects = self.traditionalaspectsckb.GetValue()
			changed = True
		if opts.houses != self.housesckb.GetValue():
			opts.houses = self.housesckb.GetValue()
			changed = True
		if opts.positions != self.positionsckb.GetValue():
			opts.positions = self.positionsckb.GetValue()
			changed = True
		if opts.intables != self.intablesckb.GetValue():
			opts.intables = self.intablesckb.GetValue()
			changed = True
		if opts.bw != self.bwrb.GetValue():
			opts.bw = self.bwrb.GetValue()
			changed = True

		# Sliders (Tratamiento de decimales Python 3)
		if opts.ascmcsize != self.ascmcsizeslider.GetValue():
			opts.ascmcsize = self.ascmcsizeslider.GetValue()
			changed = True

		val_tablesize = round(self.sizeslider.GetValue() / 100.0, 2)
		if round(opts.tablesize, 2) != val_tablesize:
			opts.tablesize = val_tablesize
			changed = True

		# Temas
		if self.themecb.GetCurrentSelection() != opts.theme:
			opts.theme = self.themecb.GetCurrentSelection()
			changed = True

		# Planetas Transaturnianos
		trans_keys = [
			(chart.Chart.TRANSURANUS, self.uranusckb),
			(chart.Chart.TRANSNEPTUNE, self.neptuneckb),
			(chart.Chart.TRANSPLUTO, self.plutockb)
		]
		for key, control in trans_keys:
			if opts.transcendental[key] != control.GetValue():
				opts.transcendental[key] = control.GetValue()
				changed = True

		# Nodos y Rueda de la Fortuna
		if opts.shownodes != self.shownodesckb.GetValue():
			opts.shownodes = self.shownodesckb.GetValue()
			changed = True
		if opts.aspectstonodes != self.asps2nodesckb.GetValue():
			opts.aspectstonodes = self.asps2nodesckb.GetValue()
			changed = True
		if opts.showlof != self.lofckb.GetValue():
			opts.showlof = self.lofckb.GetValue()
			changed = True
		if opts.showaspectstolof != self.asps2lofckb.GetValue():
			opts.showaspectstolof = self.asps2lofckb.GetValue()
			changed = True

		# Estrellas fijas y otros radio buttons
		new_fixstars = options.Options.NONE
		if self.fixstarsrb.GetValue(): new_fixstars = options.Options.FIXSTARS
		elif self.dodecsrb.GetValue(): new_fixstars = options.Options.DODECATEMORIA
		elif self.antisrb.GetValue(): new_fixstars = options.Options.ANTIS
		elif self.cantisrb.GetValue(): new_fixstars = options.Options.CANTIS

		if opts.showfixstars != new_fixstars:
			opts.showfixstars = new_fixstars
			changed = True

		# Otros
		if opts.showterms != self.termsckb.GetValue():
			opts.showterms = self.termsckb.GetValue()
			changed = True
		if opts.showdecans != self.decansckb.GetValue():
			opts.showdecans = self.decansckb.GetValue()
			changed = True
		if opts.topocentric != self.topocentricckb.GetValue():
			opts.topocentric = self.topocentricckb.GetValue()
			changed = True
		if opts.netbook != self.netbckb.GetValue():
			opts.netbook = self.netbckb.GetValue()
			changed = True

		return changed
		
	def onOK(self, event):
		parent = self.GetParent()
		opts = parent.options
		
		# 1. Guardamos los datos
		if self.check(opts):
			opts.save()
		
		# 2. SIMULAMOS EL CAMBIO DE TAMAÑO (Dispara el EVT_SIZE interno)
		w, h = parent.GetSize()
		parent.SetSize((w + 1, h + 1)) # Engordamos la ventana 1 píxel
		parent.SetSize((w, h))         # La devolvemos a su sitio
		
		# 3. Forzamos el repintado
		parent.Refresh()
		parent.Update()
		
		# 4. Cerramos
		self.EndModal(wx.ID_OK)


