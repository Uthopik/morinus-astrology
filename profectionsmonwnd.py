import wx
import os
import astrology
import planets
import houses
import chart
import fortune
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
#from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class ProfectionsMonWnd(commonwnd.CommonWnd):
	AGE, DATE, ASC, MC, SUN, MOON, FORTUNE, MERCURY, VENUS, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO = range(0, 15)

	def __init__(self, parent, age, pchrts, dates, options, mainfr, mainsigs, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, pchrts[0][0], options, id, size)
		
		self.age = age
		self.pcharts = pchrts
		self.dates = dates
		self.mainfr = mainfr
		self.mainsigs = mainsigs

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = len(dates)

		if self.mainsigs:
			self.COLUMN_NUM = 7
		else:
			self.COLUMN_NUM = 15
			if self.options.intables:
				if not self.options.transcendental[chart.Chart.TRANSURANUS]:
					self.COLUMN_NUM -= 1
				if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
					self.COLUMN_NUM -= 1
				if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
					self.COLUMN_NUM -= 1

		self.CELL_WIDTH = 3*self.FONT_SIZE
		self.BIG_CELL_WIDTH = 7*self.FONT_SIZE #Date
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.CELL_WIDTH+(self.COLUMN_NUM-1)*self.BIG_CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = ((self.COLUMN_NUM-1)*(self.BIG_CELL_WIDTH)+self.CELL_WIDTH)
		val = 0
		if len(self.dates) == 12:
			val = self.LINE_HEIGHT
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM*(self.LINE_HEIGHT))+val)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Pro']


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
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt_list = (mtexts.txts['Age'], mtexts.txts['Date'], mtexts.txts['Asc'], mtexts.txts['MC'], common.common.Planets[0], common.common.Planets[1], common.common.fortune, common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[7], common.common.Planets[8], common.common.Planets[9])
		arclrs = (txtclr, txtclr, txtclr, txtclr, self.options.clrindividual[0], self.options.clrindividual[1], self.options.clrindividual[11], self.options.clrindividual[2], self.options.clrindividual[3], self.options.clrindividual[4], self.options.clrindividual[5], self.options.clrindividual[6], self.options.clrindividual[7], self.options.clrindividual[8], self.options.clrindividual[9])

		cols = (self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)

		offs = 0
		for i in range(self.COLUMN_NUM):
			fnt = self.fntText
			if i > 3:
				fnt = self.fntMorinus
			tclr = (0, 0, 0)
			if not self.bw:
				if self.options.useplanetcolors:
					tclr = arclrs[i]
				else:
					if i > 3:
						tclr = self.options.clrperegrin

			# CORRECCIÓN: Títulos de cabecera
			bbox = draw.textbbox((0, 0), txt_list[i], font=fnt)
			w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
			clr = txtclr
			if i > 3:
				clr = tclr
			draw.text((BOR+offs+(cols[i]-w)//2, BOR+(self.TITLE_HEIGHT-h)//2), txt_list[i], fill=clr, font=fnt)
			offs += cols[i]

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY

		# Draw Age
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		txt_age = str(int(self.age)) 
		bbox_age = draw.textbbox((0, 0), txt_age, font=self.fntText)
		w_age, h_age = bbox_age[2]-bbox_age[0], bbox_age[3]-bbox_age[1]
		# Esto imprimirá solo "1975" (o el año que corresponda) sin decimales
		draw.text((x+(self.CELL_WIDTH-w_age)//2, y+(self.TABLE_HEIGHT-h_age)//2-self.LINE_HEIGHT//2), txt_age, fill=txtclr, font=self.fntText)

		agestart = agecont = self.age%12
		for i in range(self.LINE_NUM):
			if i < len(self.pcharts):
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, self.pcharts[int(agecont)], self.dates, i)
			else:
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, self.pcharts[int(agestart)], self.dates, i)
			agecont += 1
			if agecont > 11:
				agecont = 0

		y_end = BOR+self.TABLE_HEIGHT
		if len(self.dates) == 12:
			draw.line((x, y_end, x+self.TABLE_WIDTH, y_end), fill=tableclr)
			summa = 0
			for i in range(self.COLUMN_NUM):
				draw.line((x+summa+cols[i], y_end-self.LINE_HEIGHT, x+summa+cols[i], y_end), fill=tableclr)
				summa += cols[i]
		else:
			draw.line((x, y_end, x+self.TABLE_WIDTH, y_end), fill=tableclr)
			
		draw.line((BOR, BOR, BOR, BOR + 406), fill=tableclr)

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, clr, pcharts, dates, idx):
		# Línea horizontal inferior
		val = self.CELL_WIDTH
		draw.line((x+val, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		# Anchos de columna
		offs = (self.CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH, self.BIG_CELL_WIDTH)

		BOR = commonwnd.CommonWnd.BORDER
		draw.line((x, y, x, y+self.LINE_HEIGHT), fill=clr)
		
		summa = 0
		for i in range(self.COLUMN_NUM):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			tclr = (0, 0, 0)
			if not self.bw:
				tclr = self.options.clrtexts

			# ESTE BLOQUE AHORA SÍ ESTÁ DENTRO DEL BUCLE (3 niveles de tabulación)
			if i == ProfectionsMonWnd.DATE:
				anio = str(int(dates[idx][0]))
				mes = str(int(dates[idx][1])).zfill(2)
				dia = str(int(dates[idx][2])).zfill(2)
				txt_d = f"{anio}.{mes}.{dia}."
				
				bbox_d = draw.textbbox((0, 0), txt_d, font=self.fntText)
				w_d, h_d = bbox_d[2]-bbox_d[0], bbox_d[3]-bbox_d[1]
				draw.text((x+summa+(offs[i]-w_d)//2, y+(self.LINE_HEIGHT-h_d)//2), txt_d, fill=tclr, font=self.fntText)
			
			elif i != ProfectionsMonWnd.AGE:
				lon = 0.0
				if i == ProfectionsMonWnd.ASC: lon = pcharts[0].houses.ascmc[houses.Houses.ASC]
				elif i == ProfectionsMonWnd.MC: lon = pcharts[0].houses.ascmc[houses.Houses.MC]
				elif i == ProfectionsMonWnd.SUN: lon = pcharts[0].planets.planets[astrology.SE_SUN].data[planets.Planet.LONG]
				elif i == ProfectionsMonWnd.MOON: lon = pcharts[0].planets.planets[astrology.SE_MOON].data[planets.Planet.LONG]
				elif i == ProfectionsMonWnd.FORTUNE: lon = pcharts[0].fortune.fortune[fortune.Fortune.LON]
				elif i >= ProfectionsMonWnd.MERCURY: lon = pcharts[0].planets.planets[i-5].data[planets.Planet.LONG]
				
				if self.options.ayanamsha != 0:
					lon = util.normalize(lon - self.chart.ayanamsha)
				
				d, m, s = util.decToDeg(lon)
				sign_idx = int(d/chart.Chart.SIGN_DEG)
				pos_val = int(d%chart.Chart.SIGN_DEG)
				
				# Medición de componentes para centrado
				b_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp = b_sp[2]-b_sp[0]
				b_sg = draw.textbbox((0, 0), self.signs[sign_idx], font=self.fntMorinus)
				wsg, hsg = b_sg[2]-b_sg[0], b_sg[3]-b_sg[1]
				
				txt_p = (str(pos_val)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				b_p = draw.textbbox((0, 0), txt_p, font=self.fntText)
				w_p, h_p = b_p[2]-b_p[0], b_p[3]-b_p[1]
				
				offset = (offs[i]-(w_p+wsp+wsg))//2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h_p)//2), txt_p, fill=tclr, font=self.fntText)
				draw.text((x+summa+offset+w_p+wsp, y+(self.LINE_HEIGHT-hsg)//2), self.signs[sign_idx], fill=tclr, font=self.fntMorinus)

			summa += offs[i]





