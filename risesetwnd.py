import wx
import os
import astrology
import planets
import riseset
import chart
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class RiseSetWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.plnum = planets.Planets.PLANETS_NUM-2
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.plnum -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.plnum -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.plnum -= 1
			if not self.options.shownodes:
				self.plnum -= 1
		self.LINE_NUM = self.plnum

		self.COLUMN_NUM = 4

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 6*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM*(self.LINE_HEIGHT)))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
#		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Rise']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		img = Image.new('RGB', (int(self.WIDTH), int(self.HEIGHT)), self.bkgclr)
		draw = ImageDraw.Draw(img)

		BOR = commonwnd.CommonWnd.BORDER

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		# --- TÍTULOS (Rise, MC, Set, IC) ---
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt_headers = (mtexts.txts['Rise'], mtexts.txts['MC'], mtexts.txts['Set'], mtexts.txts['IC'])

		for i in range(len(txt_headers)):
			l, t, r, b = draw.textbbox((0, 0), txt_headers[i], font=self.fntText)
			w, h = r - l, b - t
			# Elevamos la cabecera 2 píxeles
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)/2, BOR+(self.TITLE_HEIGHT-h)/2 - 2), txt_headers[i], fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		num = len(common.common.Planets)-2 # Sin Nodos
		realnum = 0
		for i in range(num):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO])):
				continue
			# Llamamos a drawline que ahora usa el nuevo sistema de centrado
			self.drawline(draw, x, y+realnum*self.LINE_HEIGHT, tableclr, i)
			realnum += 1

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, clr, idx):
		# Línea horizontal inferior
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		# Definición de anchos de columna
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		
		for i in range(self.COLUMN_NUM+2): # +2 para cubrir todas las columnas
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			tclr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					tclr = self.options.clrindividual[idx]
				else:
					dign = self.chart.dignity(idx)
					tclr = self.clrs[dign]

			# Dibujar Planeta (Columna 1)
			if i == 1:
				txt_p = common.common.Planets[idx]
				l, t, r, b = draw.textbbox((0, 0), txt_p, font=self.fntMorinus)
				w, h = r - l, b - t
				# Elevación manual de 3px para los glifos de planetas
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2 - 3), txt_p, fill=tclr, font=self.fntMorinus)
			
			# Dibujar Tiempos (Columnas 2 a 5)
			elif i > 1:
				h_val, m_val, s_val = util.decToDeg(self.chart.riseset.times[idx][i-2])
				txt_time = (str(h_val)).zfill(2)+':'+(str(m_val)).zfill(2)+':'+(str(s_val)).zfill(2)
				l, t, r, b = draw.textbbox((0, 0), txt_time, font=self.fntText)
				w, h = r - l, b - t
				# Elevación manual de 2px para los números
				draw.text((x+summa+(offs[i]-w)/2, y+(self.LINE_HEIGHT-h)/2 - 2), txt_time, fill=tclr, font=self.fntText)

			summa += offs[i]





