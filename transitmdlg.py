import wx
import intvalidator
import options
import rangechecker
import util
import mtexts

#---------------------------------------------------------------------------
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)
#---------------------------------------------------------------------------

class TransitMonthDlg(wx.Dialog):
	def __init__(self, parent, time):
		# CAMBIO: Inicialización directa. Eliminamos 'pre' que no existía.
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Transit'].capitalize(), 
						  style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_EX_CONTEXTHELP)
		
		# Ya no necesitamos ni pre.Create ni self.PostCreate(pre)

		# main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		# Time
		rnge = 3000
		checker = rangechecker.RangeChecker()
		if checker.isExtended():
			rnge = 5000
		
		# Nota: En Linux wx.StaticBox necesita el parent correcto
		self.stime = wx.StaticBox(self, label='')
		timesizer = wx.StaticBoxSizer(self.stime, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		fgsizer = wx.FlexGridSizer(1, 2, 0, 0)
		
		label = wx.StaticText(self, -1, mtexts.txts['Year']+':')
		vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		vsizer.Add(self.year, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(self, -1, mtexts.txts['Month']+':')
		vsizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		
		self.month = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(1, 12), size=(50,-1))
		vsizer.Add(self.month, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT, 0)
		fgsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		
		self.month.SetHelpText(mtexts.txts['HelpMonth'])
		self.month.SetMaxLength(2)

		timesizer.Add(fgsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		mvsizer.Add(timesizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		# Initialize
		self.year.SetValue(str(time.year))
		self.month.SetValue(str(time.month))

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

		self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
		self.Bind(wx.EVT_CLOSE, self.onCancel)

	def onOK(self, event):
		# stime es un StaticBox, no necesita Validate() directamente, 
		# pero mantenemos la estructura por si acaso.
		if self.Validate():
			if util.checkDate(int(self.year.GetValue()), int(self.month.GetValue()), 1):
				self.EndModal(wx.ID_OK) # EndModal es mejor para Diálogos
			else:
				dlgm = wx.MessageDialog(None, mtexts.txts['InvalidDate']+' ('+self.year.GetValue()+'.'+self.month.GetValue()+'.)', mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
				dlgm.ShowModal()		
				dlgm.Destroy()

	def onCancel(self, event):
		self.EndModal(wx.ID_CANCEL)


