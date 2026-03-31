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


class ZodParsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.pars = chrt.zodpars.pars
		self.options = options		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 4
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE

		self.TITLE_HEIGHT = 2*self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0

		self.LINE_NUM = len(self.pars)
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+self.LINE_NUM*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntSymbol = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE//2))
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Par']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = (0,0,0) if self.bw else self.options.clrtable
		txtclr = (0,0,0) if self.bw else self.options.clrtexts

		img = Image.new('RGB', (int(self.WIDTH), int(self.HEIGHT)), self.bkgclr)
		draw = ImageDraw.Draw(img)
		BOR = commonwnd.CommonWnd.BORDER

		# --- CABECERA (TÍTULOS) ---
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.TABLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)

		# Título superior: "Zodiacal Parallels"
		txt_main = mtexts.txts['ZodPars']
		l, t, r, b = draw.textbbox((0, 0), txt_main, font=self.fntText)
		draw.text((BOR+self.SMALL_CELL_WIDTH + (self.TITLE_WIDTH-(r-l))//2, BOR+(self.LINE_HEIGHT-(b-t))//2), txt_main, fill=txtclr, font=self.fntText)

		draw.line((BOR+self.SMALL_CELL_WIDTH, BOR+self.LINE_HEIGHT, BOR+self.TABLE_WIDTH, BOR+self.LINE_HEIGHT), fill=tableclr)

		# Subtítulos: "Parallel" y "ContraParallel"
		subtitles = (mtexts.txts['Parallel'], mtexts.txts['ContraParallel'])
		for i in range(2):
			l, t, r, b = draw.textbbox((0, 0), subtitles[i], font=self.fntText)
			center_x = BOR + self.SMALL_CELL_WIDTH + (i * self.CELL_WIDTH * 2) + (self.CELL_WIDTH * 2 - (r-l))//2
			draw.text((center_x, BOR + self.LINE_HEIGHT + (self.LINE_HEIGHT-(b-t))//2), subtitles[i], fill=txtclr, font=self.fntText)

		draw.line((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*2, BOR+self.LINE_HEIGHT, BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*2, BOR+self.TITLE_HEIGHT), fill=tableclr)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		# --- DIBUJO DE FILAS (CORREGIDO PARA EVITAR INDEXERROR) ---
		ii = 0
		# Recorremos el rango de planetas estándar (0 a 9)
		for i in range(len(common.common.Planets)-1):
			# 1. Verificamos si el planeta debe mostrarse según las opciones
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO])):
				continue
			
			# 2. Verificamos si hay datos para este planeta en self.pars
			# (Usamos try por si la lista es más corta de lo esperado)
			try:
				data_pts = self.pars[i].pts
				self.drawline(draw, x, y+ii*self.LINE_HEIGHT, i, data_pts, tableclr)
				ii += 1
			except IndexError:
				continue
		wxImg = wx.Image(img.size[0], img.size[1]); wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)

	def drawline(self, draw, x, y, idx, data, clr):
		# --- 1. DIBUJO DE ESTRUCTURA Y GLIFO (IGUAL QUE SIEMPRE) ---
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(len(offs)):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)
			summa += offs[i]

		tclr = (0,0,0)
		if not self.bw:
			tclr = self.options.clrindividual[idx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(idx)]

		txt_p = common.common.Planets[idx]
		l, t, r, b = draw.textbbox((0, 0), txt_p, font=self.fntMorinus)
		draw.text((x+(self.SMALL_CELL_WIDTH-(r-l))//2, y+(self.LINE_HEIGHT-(b-t))//2 - 3), txt_p, fill=tclr, font=self.fntMorinus)

		# --- 2. EL MAPA DE MANIPULACIÓN (TU CUADRO DE MANDOS) ---
		# Vals contiene los datos que Python calcula (0, 1, 2, 3)
		vals = [d[0] for d in data if d[0] != -1.0]
		
		# Aquí defines el orden de las columnas [Col 1, Col 2, Col 3, Col 4]
		# Si pones un número que no existe (ej. el 3 cuando solo hay 3 datos), 
		# la celda saldrá vacía automáticamente.
		mapeo = {
			astrology.SE_SUN:      [1, 3, 0, 2], # El Sol: prueba este orden para el hueco dinámico
			astrology.SE_MOON:     [0, 2, 1, 3], 
			astrology.SE_MERCURY:  [0, 2, 1, 3],
			astrology.SE_VENUS:    [0, 2, 1, 3],
			astrology.SE_MARS:     [0, 2, 1, 3],
			astrology.SE_JUPITER:  [0, 2, 1, 3],
			astrology.SE_SATURN:   [0, 2, 1, 3],
			astrology.SE_URANUS:   [0, 2, 1, 3],
			astrology.SE_NEPTUNE:  [0, 2, 1, 3],
			astrology.SE_PLUTO:    [0, 2, 1, 3],
		}

		# Obtenemos el orden deseado para este planeta específico
		orden = mapeo.get(idx, [0, 1, 2, 3])
		ordered_data = [None, None, None, None]
		
		# Rellenamos basándonos en tu mapa
		for i in range(4):
			pos_buscada = orden[i]
			if pos_buscada is not None and pos_buscada < len(vals):
				ordered_data[i] = vals[pos_buscada]

		# --- 3. DIBUJO DE LOS DATOS REORDENADOS ---
		summa = self.SMALL_CELL_WIDTH
		for i in range(4):
			val = ordered_data[i]
			if val is not None:
				if self.options.ayanamsha != 0:
					val = util.normalize(val - self.chart.ayanamsha)

				d, m, s = util.decToDeg(val)
				sign = int(d / 30)
				pos = int(d % 30)
				
				txt_deg = f"{pos:2d}{self.deg_symbol}{m:02d}'{s:02d}\""
				txt_sign = self.signs[sign]
				
				l1, t1, r1, b1 = draw.textbbox((0, 0), txt_deg, font=self.fntText)
				l2, t2, r2, b2 = draw.textbbox((0, 0), txt_sign, font=self.fntMorinus)
				tw = (r1-l1) + 4 + (r2-l2)
				sx = x + summa + (self.CELL_WIDTH - tw) // 2
				
				draw.text((sx, y + (self.LINE_HEIGHT-(b1-t1))//2 - 2), txt_deg, fill=tclr, font=self.fntText)
				draw.text((sx + (r1-l1) + 4, y + (self.LINE_HEIGHT-(b2-t2))//2 - 4), txt_sign, fill=tclr, font=self.fntMorinus)
			
			summa += self.CELL_WIDTH




