import wx
import chart
import intvalidator
import rangechecker
import mtexts
import util

class ProfTableDlg(wx.Dialog):

	def __init__(self, parent):
		# CAMBIO: Inicialización directa y limpia. 
		# Quitamos toda la lógica de 'pre' que no funcionaba.
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Profections'].capitalize(), 
						  style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_EX_CONTEXTHELP)

		# main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)
		# main horizontal sizer
		mhsizer = wx.BoxSizer(wx.HORIZONTAL)

		# Significator Selection
		# En Linux, pasar 'self' al StaticBox es fundamental
		self.sselection = wx.StaticBox(self, label='')
		selectionsizer = wx.StaticBoxSizer(self.sselection, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		
		self.mainrb = wx.RadioButton(self, -1, mtexts.txts['ProfsMainSignificatorsOnly'], style=wx.RB_GROUP)
		vsizer.Add(self.mainrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)
		
		self.allrb = wx.RadioButton(self, -1, mtexts.txts['ProfsAll'])
		vsizer.Add(self.allrb, 0, wx.ALIGN_LEFT|wx.TOP, 2)

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
		self.mainrb.SetValue(True)



