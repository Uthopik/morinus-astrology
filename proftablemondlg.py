import wx
import chart
import mtexts
import util

class ProfTableMonDlg(wx.Dialog):

	def __init__(self, parent):
		# CAMBIO: Inicialización directa. Eliminamos 'pre' y usamos self.
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['MonthlyProfections'].capitalize(), 
						  style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_EX_CONTEXTHELP)

		# main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		# main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		# Significator Selection
		self.sselection = wx.StaticBox(self, label='')
		selectionsizer = wx.StaticBoxSizer(self.sselection, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.steps12rb = wx.RadioButton(self, -1, mtexts.txts['Steps12'], style=wx.RB_GROUP)
		vsizer.Add(self.steps12rb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		
		self.steps13rb = wx.RadioButton(self, -1, mtexts.txts['Steps13'])
		vsizer.Add(self.steps13rb, 0, wx.ALIGN_LEFT|wx.TOP, 2)

		selectionsizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		mvsizer.Add(selectionsizer, 0, wx.GROW|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, 5)

		btnsizer = wx.StdDialogButtonSizer()

		btnOk = wx.Button(self, wx.ID_OK, mtexts.txts['Ok'])
		btnOk.SetHelpText(mtexts.txts['HelpOk'])
		btnOk.SetDefault()
		btnsizer.AddButton(btnOk)

		btn = wx.Button(self, wx.ID_CANCEL, mtexts.txts['Cancel'])
		btn.SetHelpText(mtexts.txts['HelpCancel'])
		btnsizer.AddButton(btn)

		btnsizer.Realize()

		mvsizer.Add(btnsizer, 0, wx.GROW|wx.ALL, 10)
		self.SetSizer(mvsizer)
		mvsizer.Fit(self)

	def initialize(self):
		self.steps12rb.SetValue(True)



