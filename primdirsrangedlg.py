import wx
import mtexts

#---------------------------------------------------------------------------
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)
#---------------------------------------------------------------------------

class PrimDirsRangeDlg(wx.Dialog):
	def __init__(self, parent):
		# CAMBIO: Inicialización directa. Eliminamos 'pre' y usamos self.
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['PrimaryDirs'], 
						  style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_EX_CONTEXTHELP)

		# main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		# main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		# Range
		srange = wx.StaticBox(self, label=mtexts.txts["Age"])
		rangesizer = wx.StaticBoxSizer(srange, wx.VERTICAL)
		self.range25rb = wx.RadioButton(self, -1, '0-25', style=wx.RB_GROUP)
		rangesizer.Add(self.range25rb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)
		self.range50rb = wx.RadioButton(self, -1, '25-50')
		rangesizer.Add(self.range50rb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)
		self.range75rb = wx.RadioButton(self, -1, '50-75')
		rangesizer.Add(self.range75rb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)
		self.range100rb = wx.RadioButton(self, -1, '75-100')
		rangesizer.Add(self.range100rb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)
		self.rangeallrb = wx.RadioButton(self, -1, '0-100')
		rangesizer.Add(self.rangeallrb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)

		mhsizer.Add(rangesizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.RIGHT|wx.LEFT, 2)

		# Direction
		sdir = wx.StaticBox(self, label='')
		dirsizer = wx.StaticBoxSizer(sdir, wx.VERTICAL)
		self.directrb = wx.RadioButton(self, -1, mtexts.txts['Direct'], style=wx.RB_GROUP)
		dirsizer.Add(self.directrb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)
		self.converserb = wx.RadioButton(self, -1, mtexts.txts['Converse'])
		dirsizer.Add(self.converserb, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5)
		self.bothrb = wx.RadioButton(self, -1, mtexts.txts['Both'])
		dirsizer.Add(self.bothrb, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mhsizer.Add(dirsizer, 1, wx.GROW|wx.ALIGN_LEFT|wx.LEFT, 0)
		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)

		btnsizer = wx.StdDialogButtonSizer()

		if wx.Platform != '__WXMSW__':
			btn = wx.ContextHelpButton(self)
			btnsizer.AddButton(btn)
        
		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnsizer.AddButton(btnOk)
		btnOk.SetHelpText(mtexts.txts['HelpOk'])
		btnOk.SetDefault()

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btnsizer.AddButton(btn)
		btn.SetHelpText(mtexts.txts['HelpCancel'])

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

		btnOk.SetFocus()







