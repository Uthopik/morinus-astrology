import os
import wx
import astrology
import planets
import chart
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class MunPosWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = planets.Planets.PLANETS_NUM-1 
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 1
		self.COLUMN_NUM = 1

		self.SPACE_ARABIANY = self.LINE_HEIGHT
		self.LINE_NUM_ARABIAN = 1
		self.COLUMN_NUM_ARABIAN = 4

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.TITLE_WIDTH_ARABIAN = (self.COLUMN_NUM_ARABIAN+1)*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
		self.TABLE_WIDTH_ARABIAN = self.TABLE_WIDTH
		self.TABLE_HEIGHT_ARABIAN = 0
		if not self.options.intables or (self.options.intables and self.options.showlof):
			self.TABLE_WIDTH_ARABIAN = (self.CELL_WIDTH+self.COLUMN_NUM_ARABIAN*(self.CELL_WIDTH))
			self.TABLE_HEIGHT_ARABIAN = (self.SPACE_ARABIANY+self.LINE_NUM_ARABIAN*self.LINE_HEIGHT)
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT)+self.TABLE_HEIGHT_ARABIAN)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH_ARABIAN+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Mun']


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

		#Title
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt = mtexts.txts['HousePercent']
		l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
		w, h = r - l, b - t
		draw.text((BOR+self.SMALL_CELL_WIDTH+(self.CELL_WIDTH-w)//2, BOR+(self.TITLE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		ii = 0
		for i in range(len(common.common.Planets)-1):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			self.drawline(draw, x, y+ii*self.LINE_HEIGHT, tableclr, i)
			ii += 1

		#Arabian Parts
		if not self.options.intables or (self.options.intables and self.options.showlof):
			x = BOR
			y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT)+self.SPACE_ARABIANY
			draw.rectangle(((x,y),(x+self.TITLE_WIDTH_ARABIAN, y+self.LINE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
			self.drawlinelof(draw, x, y, mtexts.txts['MLoF'], self.chart.munfortune.mfortune, tableclr, 0)

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(self.COLUMN_NUM+1+1):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			tclr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					tclr = self.options.clrindividual[idx]
				else:
					dign = self.chart.dignity(idx)
					tclr = self.clrs[dign]

			if i == 1:
				txt = common.common.Planets[idx]
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntMorinus)
				w, h = r - l, b - t
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt, fill=tclr, font=self.fntMorinus)
			elif i != 0:
				p_lon = float(self.chart.planets.planets[idx].data[0])
				p_lat = float(self.chart.planets.planets[idx].data[1])
				armc = float(self.chart.houses.ascmc[1])
				lat_lugar = float(self.chart.place.lat)
				obliq = float(self.chart.obl)
				hsys_byte = str(self.chart.houses.hsys).encode()
				xpin = [p_lon, p_lat]

				ret = astrology.swe.house_pos(armc, lat_lugar, obliq, xpin, hsys_byte)

				txt = str(round(ret, 2))
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				draw.text((int(x+summa+(offs[i]-w)//2), int(y+(self.LINE_HEIGHT-h)//2)), txt, fill=tclr, font=self.fntText)

			summa += offs[i]


	def drawlinelof(self, draw, x, y, name, data, clr, idx):
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH_ARABIAN, y+self.LINE_HEIGHT), fill=clr)
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		for i in range(self.COLUMN_NUM_ARABIAN+1+1):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)
			d, m, s = 0, 0, 0
			if i > 1:
				d,m,s = util.decToDeg(data[i-2])

			if i == 1: # Nombre "Mundane Fortuna"
				l, t, r, b = draw.textbbox((0, 0), name, font=self.fntText)
				w, h = r - l, b - t
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), name, fill=txtclr, font=self.fntText)
			elif i == 2: # Longitud con signo
				val_fortuna = data[i-2]
				if self.options.ayanamsha != 0:
					val_fortuna = util.normalize(val_fortuna - self.chart.ayanamsha)
				d, m, s = util.decToDeg(val_fortuna)
				sign = int(val_fortuna / 30.0)
				pos = d % 30
				txtsign = self.signs[sign]
				
				l_sp, t_sp, r_sp, b_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp = r_sp - l_sp
				l_sg, t_sg, r_sg, b_sg = draw.textbbox((0, 0), txtsign, font=self.fntMorinus)
				wsg, hsg = r_sg - l_sg, b_sg - t_sg
				
				txt = (str(pos)).rjust(2) + self.deg_symbol + (str(m)).zfill(2) + "'" + (str(s)).zfill(2) + '"'
				l_t, t_t, r_t, b_t = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = (r_t - l_t) + 12, b_t - t_t # +12 para separación

				offset = (offs[i] - (w + wsp + wsg)) // 2
				draw.text((int(x+summa+offset), int(y+(self.LINE_HEIGHT-h)//2)), txt, fill=txtclr, font=self.fntText)
				draw.text((int(x+summa+offset+w+wsp), int(y+(self.LINE_HEIGHT-hsg)//2)), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i in (3, 4, 5): # Latitud, RA, Dec
				if i == 4 and self.options.intime:
					d_t, m_t, s_t = util.decToDeg(data[i-2]/15.0)
					txt = (str(d_t)).rjust(2)+':'+(str(m_t)).zfill(2)+":"+(str(s_t)).zfill(2)
				else:
					sgn_char = '-' if data[i-2] < 0.0 else ''
					txt = sgn_char+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)

			summa += offs[i]




