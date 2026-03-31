import wx
import mtexts

# ##################################
# Roberto V 7.3.0
# All texts txtsxxx -> txts
# ##################################

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------


class FirdariaDlg(wx.Dialog):
	def __init__(self, parent):
		# Inicialización directa y moderna
		wx.Dialog.__init__(self, parent, -1, mtexts.txts['Firdaria'], style=wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_EX_CONTEXTHELP)

		#main vertical sizer
		mvsizer = wx.BoxSizer(wx.VERTICAL)

		#Time
		sfirdaria =wx.StaticBox(self, label=mtexts.txts['Nocturnal'])
		firdariasizer = wx.StaticBoxSizer(sfirdaria, wx.VERTICAL)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		self.bonrb = wx.RadioButton(self, -1, mtexts.txts['Bonatus'], style=wx.RB_GROUP)
		vsizer.Add(self.bonrb, 0, wx.ALIGN_LEFT, 5)
		self.birrb = wx.RadioButton(self, -1, mtexts.txts['AlBiruni'])
		vsizer.Add(self.birrb, 0, wx.ALIGN_LEFT, 5)

		firdariasizer.Add(vsizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		mvsizer.Add(firdariasizer, 0, wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

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


	def fill(self, opts):
		if opts.isfirbonatti:
			self.bonrb.SetValue(True)
		else:
			self.birrb.SetValue(True)


	def check(self, opts):
		changed = self.bonrb.GetValue() != opts.isfirbonatti

		if changed:
			opts.isfirbonatti = self.bonrb.GetValue()

		return changed





