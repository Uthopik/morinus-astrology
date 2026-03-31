import wx
import os
import astrology
import chart
import houses
import planets
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class AntisciaWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.ants = chrt.antiscia
		self.options = options		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 4
		self.SPACE = self.FONT_SIZE//2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE

		self.TITLE_HEIGHT = 2*self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0

		self.LINE_NUM = 15
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
			if not self.options.showlof:
				self.LINE_NUM -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 2

		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+self.LINE_NUM*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.clrs = [self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil]
		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, 3*self.FONT_SIZE//2)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Ant']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.bkgclr)
		draw = ImageDraw.Draw(img)

		BOR = commonwnd.CommonWnd.BORDER

		#Title
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		txt_header = (mtexts.txts['Antiscion'], mtexts.txts['Contraantiscion'])
		for i in range(len(txt_header)):
			l, t, r, b = draw.textbbox((0, 0), txt_header[i], font=self.fntText)
			w, h = r - l, b - t
			
			offs = 0
			if i == 1:
				offs = self.CELL_WIDTH # Desplazamiento para el segundo título
			
			# Dibujo del texto centrado
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH//2+offs+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2), txt_header[i], fill=txtclr, font=self.fntText)

		txt_sub = (mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Longitude'], mtexts.txts['Latitude'])
		for i in range(len(txt_sub)):
			l, t, r, b = draw.textbbox((0, 0), txt_sub[i], font=self.fntText)
			w, h = r - l, b - t
			
			# Dibujo del texto centrado en cada una de las 4 columnas
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)//2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)//2), txt_sub[i], fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		txts = (common.common.Planets[0], common.common.Planets[1], common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[7], common.common.Planets[8], common.common.Planets[9], common.common.Planets[10], common.common.Planets[11], common.common.fortune, '0', '1')
		data = ((self.ants.plantiscia[0].lon, 0.0, self.ants.plcontraant[0].lon, 0.0), (self.ants.plantiscia[1].lon, self.ants.plantiscia[1].lat, self.ants.plcontraant[1].lon, self.ants.plcontraant[1].lat), (self.ants.plantiscia[2].lon, self.ants.plantiscia[2].lat, self.ants.plcontraant[2].lon, self.ants.plcontraant[2].lat), (self.ants.plantiscia[3].lon, self.ants.plantiscia[3].lat, self.ants.plcontraant[3].lon, self.ants.plcontraant[3].lat), (self.ants.plantiscia[4].lon, self.ants.plantiscia[4].lat, self.ants.plcontraant[4].lon, self.ants.plcontraant[4].lat), (self.ants.plantiscia[5].lon, self.ants.plantiscia[5].lat, self.ants.plcontraant[5].lon, self.ants.plcontraant[5].lat), (self.ants.plantiscia[6].lon, self.ants.plantiscia[6].lat, self.ants.plcontraant[6].lon, self.ants.plcontraant[6].lat), (self.ants.plantiscia[7].lon, self.ants.plantiscia[7].lat, self.ants.plcontraant[7].lon, self.ants.plcontraant[7].lat), (self.ants.plantiscia[8].lon, self.ants.plantiscia[8].lat, self.ants.plcontraant[8].lon, self.ants.plcontraant[8].lat), (self.ants.plantiscia[9].lon, self.ants.plantiscia[9].lat, self.ants.plcontraant[9].lon, self.ants.plcontraant[9].lat), (self.ants.plantiscia[10].lon, self.ants.plantiscia[10].lat, self.ants.plcontraant[10].lon, self.ants.plcontraant[10].lat), (self.ants.plantiscia[11].lon, self.ants.plantiscia[11].lat, self.ants.plcontraant[11].lon, self.ants.plcontraant[11].lat), (self.ants.lofant.lon, self.ants.lofant.lat, self.ants.lofcontraant.lon, self.ants.lofcontraant.lat), (self.ants.ascmcant[0].lon, self.ants.ascmcant[0].lat, self.ants.ascmccontraant[0].lon, self.ants.ascmccontraant[0].lat), (self.ants.ascmcant[1].lon, self.ants.ascmcant[1].lat, self.ants.ascmccontraant[1].lon, self.ants.ascmccontraant[1].lat))
		i = 0
		for j in range(len(txts)):
			ascmc = False
			if j > 12:
				ascmc = True

			if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes) or (j == astrology.SE_TRUE_NODE and not self.options.shownodes) or (j== astrology.SE_TRUE_NODE+1 and not self.options.showlof)):
				continue
			self.drawline(draw, x, y+i*self.LINE_HEIGHT, txts[j], tableclr, data[j], j, ascmc)
			i += 1

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, txt, clr, data, idx, AscMC):
		# Línea horizontal inferior
		draw.line((x, y + self.LINE_HEIGHT, x + self.TABLE_WIDTH, y + self.LINE_HEIGHT), fill=clr)

		# Líneas verticales
		offs_cols = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(self.COLUMN_NUM + 1 + 1):
			draw.line((x + summa + offs_cols[i], y, x + summa + offs_cols[i], y + self.LINE_HEIGHT), fill=clr)
			summa += offs_cols[i]

		# Dibujar Símbolos (Planetas o Asc/MC)
		tclr = (0, 0, 0)
		if not self.bw:
			if not AscMC:
				objidx = idx
				if objidx >= len(common.common.Planets) - 1:
					objidx -= 1
				tclr = self.options.clrindividual[objidx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(objidx)]
			else:
				tclr = self.options.clrtexts
		else:
			tclr = clr

		fnt = self.fntSymbol if AscMC else self.fntMorinus
		l, t, r, b = draw.textbbox((0, 0), txt, font=fnt)
		w, h = r - l, b - t
		draw.text((x + (self.SMALL_CELL_WIDTH - w) // 2, y + (self.LINE_HEIGHT - h) // 2), txt, fill=tclr, font=fnt)

		# Dibujar Datos (Longitude y Latitude)
		data_offs = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(len(data)):
			d, m, s = util.decToDeg(data[i])

			if i == 0 or i == 2: # Columnas de Longitud
				if self.options.ayanamsha != 0:
					lona = util.normalize(data[i] + self.chart.ayanamsha)
					d, m, s = util.decToDeg(lona)

				sign = int(d / chart.Chart.SIGN_DEG)
				pos = d % chart.Chart.SIGN_DEG
				
				# Medidas para el espacio y el signo zodiacal
				l_sp, t_sp, r_sp, b_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp = r_sp - l_sp
				l_sg, t_sg, r_sg, b_sg = draw.textbbox((0, 0), self.signs[sign], font=self.fntMorinus)
				wsg, hsg = r_sg - l_sg, b_sg - t_sg
				
				txt_lon = (str(pos)).rjust(2) + self.deg_symbol + (str(m)).zfill(2) + "'" + (str(s)).zfill(2) + '"'
				l_t, t_t, r_t, b_t = draw.textbbox((0, 0), txt_lon, font=self.fntText)
				w, h = (r_t - l_t) + 12, b_t - t_t # +12 para respiro del signo
				
				offset = (data_offs[i] - (w + wsp + wsg)) // 2
				draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt_lon, fill=tclr, font=self.fntText)
				draw.text((x + self.SMALL_CELL_WIDTH + summa + offset + w + wsp, y + (self.LINE_HEIGHT - hsg) // 2), self.signs[sign], fill=tclr, font=self.fntMorinus)
			else: # Columnas de Latitud
				sign_char = '-' if data[i] < 0.0 else ''
				txt_lat = sign_char + (str(d)).rjust(2) + self.deg_symbol + (str(m)).zfill(2) + "'" + (str(s)).zfill(2) + '"'
				l_l, t_l, r_l, b_l = draw.textbbox((0, 0), txt_lat, font=self.fntText)
				w, h = r_l - l_l, b_l - t_l
				offset = (data_offs[i] - w) // 2
				draw.text((x + self.SMALL_CELL_WIDTH + summa + offset, y + (self.LINE_HEIGHT - h) // 2), txt_lat, fill=tclr, font=self.fntText)

			summa += data_offs[i]




