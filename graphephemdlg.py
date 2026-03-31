import datetime
import wx
import intvalidator
import rangechecker
import util
import mtexts


#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class GraphEphemDlg(wx.Dialog):
	def __init__(self, parent):
		# 1. Llamada correcta a la clase base (sustituye al lío del 'pre')
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Ephemeris'], 
						  pos=wx.DefaultPosition, size=wx.DefaultSize, 
						  style=wx.DEFAULT_DIALOG_STYLE)

		self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)

		# Main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		# Main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		#Time
		rnge = 3000
		checker = rangechecker.RangeChecker()
		if checker.isExtended():
			rnge = 5000
		self.syear =wx.StaticBox(self, label=mtexts.txts['Year'])
		yearsizer = wx.StaticBoxSizer(self.syear, wx.VERTICAL)
		self.year = wx.TextCtrl(self, -1, '', validator=intvalidator.IntValidator(0, rnge), size=(50,-1))
		yearsizer.Add(self.year, 0, wx.GROW|wx.ALL, 5)
		if checker.isExtended():
			self.year.SetHelpText(mtexts.txts['HelpYear'])
		else:
			self.year.SetHelpText(mtexts.txts['HelpYear2'])
		self.year.SetMaxLength(4)

		mhsizer.Add(yearsizer, 1, wx.GROW|wx.ALL, 5)
		mvsizer.Add(mhsizer, 0, wx.GROW|wx.ALL, 5)

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

		now = datetime.datetime.now()
		self.year.SetValue(str(now.year))







