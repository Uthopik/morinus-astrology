import wx
import string
import mtexts


class IntValidator(wx.Validator):
	def __init__(self, minim=None, maxim=None):
		wx.Validator.__init__(self)
		self.minim = minim
		self.maxim = maxim
		self.Bind(wx.EVT_CHAR, self.OnChar)

	def Clone(self):
 		return IntValidator(self.minim, self.maxim)

	def TransferToWindow(self):
		return True

	def TransferFromWindow(self):
		return True

	def Validate(self, win):
		tc = self.GetWindow()
		val = tc.GetValue()

		if (val == ''):
			dlgm = wx.MessageDialog(None, mtexts.txts['NumFieldsCannotBeEmpty'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()		
			dlgm.Destroy()
			return False

		if ((self.minim != None and int(val) < self.minim) or (self.maxim != None and int(val) > self.maxim)):
			dlgm = wx.MessageDialog(None, mtexts.txts['RangeError'], mtexts.txts['Error'], wx.OK|wx.ICON_EXCLAMATION)
			dlgm.ShowModal()
			dlgm.Destroy()
			return False	

		return True

	def OnChar(self, event):
		key = event.GetKeyCode() # Usamos el método oficial GetKeyCode()

		# 1. Permitir teclas de control (Retroceso, Suprimir, Tab, Flechas, etc.)
		# En wxPython moderno, las teclas de control tienen códigos bajos o especiales
		if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
			event.Skip()
			return

		# 2. Permitir solo números (0-9)
		if chr(key) in string.digits:
			event.Skip()
			return

		# 3. Bloquear todo lo demás con un pitido (si no está en silencio)
		if not wx.Validator.IsSilent():
			wx.Bell()

		# No llamamos a event.Skip(), así que la letra "no entra" en el cuadro de texto
		return


