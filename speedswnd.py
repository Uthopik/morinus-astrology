import wx
import os
import astrology
import planets
import chart
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import util
import mtexts

class SpeedsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize)
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = planets.Planets.PLANETS_NUM 
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 1

		# CAMBIO 1: Ahora son 4 columnas de datos (Long, %, Lat, AU)
		self.COLUMN_NUM = 4

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
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
		self.deg_symbol = u'\u00b0'

		# IMPORTANTE: Definir bkgclr ANTES de llamar a drawBkg
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.drawBkg()

	def getExt(self):
		return mtexts.txts['Spe']

	def drawBkg(self):
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

		# --- TÍTULOS (Ahora con 4 elementos: Long, %, Lat, AU) ---
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt_headers = (mtexts.txts['InLong'], '%', mtexts.txts['InLat'], mtexts.txts['InAU'])

		for i in range(len(txt_headers)):
			l, t, r, b = draw.textbbox((0, 0), txt_headers[i], font=self.fntText)
			w, h = r - l, b - t
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)//2, BOR+(self.TITLE_HEIGHT-h)//2 - 2), txt_headers[i], fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		ii = 0
		for i in range(len(common.common.Planets)-1):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			self.drawline(draw, x, y+ii*self.LINE_HEIGHT, tableclr, i)
			ii += 1

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)

	def drawline(self, draw, x, y, clr, idx):
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		# CAMBIO 2: Añadimos un CELL_WIDTH más a offs para la 5ª columna
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		summa = 0
		for i in range(len(offs)):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == 0: 
				summa += offs[i]
				continue

			tclr = (0, 0, 0)
			if not self.bw:
				objidx = idx
				if objidx > astrology.SE_MEAN_NODE: objidx = astrology.SE_MEAN_NODE
				tclr = self.options.clrindividual[objidx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(idx)]

			# COLUMNA 1: Planeta
			if i == 1:
				txt_p = common.common.Planets[idx]
				l, t, r, b = draw.textbbox((0, 0), txt_p, font=self.fntMorinus)
				w, h = r - l, b - t
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2 - 3), txt_p, fill=tclr, font=self.fntMorinus)
			
			# COLUMNA 2: Longitude
			elif i == 2:
				data = self.chart.planets.planets[idx].data[planets.Planet.SPLON]
				self._draw_speed_val(draw, x+summa, y, offs[i], data, tclr)

			# COLUMNA 3: % (Calculado)
			elif i == 3:
				try:
					cur = self.chart.planets.planets[idx].data[planets.Planet.SPLON]
					mean = self.chart.planets.planets[idx].data[planets.Planet.SPLON + 3]
					perc = str(int(abs(cur/mean)*100)) + "%" if mean != 0 else "0%"
				except:
					perc = "---"
				l, t, r, b = draw.textbbox((0, 0), perc, font=self.fntText)
				draw.text((x+summa+(offs[i]-(r-l))//2, y+(self.LINE_HEIGHT-(b-t))//2 - 2), perc, fill=tclr, font=self.fntText)

			# COLUMNA 4: Latitude
			elif i == 4:
				data = self.chart.planets.planets[idx].data[planets.Planet.SPLAT]
				self._draw_speed_val(draw, x+summa, y, offs[i], data, tclr)

			# COLUMNA 5: AU
			elif i == 5:
				data = self.chart.planets.planets[idx].data[planets.Planet.SPLAT + 1]
				self._draw_speed_val(draw, x+summa, y, offs[i], data, tclr)

			summa += offs[i]

	def _draw_speed_val(self, draw, x_pos, y_pos, cell_w, data, color):
		d, m, s = util.decToDeg(data)
		sgn = '-' if data < 0.0 else ''
		txt = sgn+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
		l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
		draw.text((x_pos+(cell_w-(r-l))//2, y_pos+(self.LINE_HEIGHT-(b-t))//2 - 2), txt, fill=color, font=self.fntText)





