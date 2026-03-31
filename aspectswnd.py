import math
import wx
import os
import astrology
import planets
import houses
import chart
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import mtexts
import util


class AspectsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(2*18*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int(self.FONT_SIZE/4)
		self.XOFFSET = self.SPACE
		self.YOFFSET = int(self.SPACE//2)
		self.SQUARE_SIZE = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = 12

		self.HOUSESOFFS = 13
		self.COLUMN_NUM = 19 
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
				self.COLUMN_NUM -= 1 
				self.HOUSESOFFS -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
				self.COLUMN_NUM -= 1 
				self.HOUSESOFFS -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
				self.COLUMN_NUM -= 1 
				self.HOUSESOFFS -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 1
			if not self.options.houses:
				self.COLUMN_NUM -= 6 

		self.TABLE_HEIGHT = (self.LINE_NUM*(self.SQUARE_SIZE+self.SPACE))

		self.TABLE_WIDTH = (self.COLUMN_NUM*(self.SQUARE_SIZE+self.SPACE))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, int(4*self.FONT_SIZE/5))
		self.fntSymbol = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE//2))
		self.fntAspects = ImageFont.truetype(common.common.symbols, int(self.FONT_SIZE//2))
		self.fntText = ImageFont.truetype(common.common.abc, int(2*self.FONT_SIZE/3))
		self.fntText2 = ImageFont.truetype(common.common.abc, int(self.FONT_SIZE/3))
		self.fntText3 = ImageFont.truetype(common.common.abc, int(self.FONT_SIZE//2))
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)
		self.arsigndiff = (0, -1, -1, 2, -1, 3, 4, -1, -1, -1, 6)
		self.hidx = (1, 2, 3, 10, 11, 12)

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Asps']


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

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		# Columna lateral de Planetas
		x = BOR
		j_plan = 0
		num = len(common.common.Planets)-1
		for i in range(num):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue

			y = BOR+(j_plan+1)*(self.SQUARE_SIZE+self.SPACE)
			self.drawSquare(draw, x, y, tableclr)
			clr = (0,0,0)
			if not self.bw:
				if self.options.useplanetcolors:
					clr = self.options.clrindividual[i]
				else:
					dign = self.chart.dignity(i)
					clr = self.clrs[dign]
			
			l, t, r, b = draw.textbbox((0, 0), common.common.Planets[i], font=self.fntMorinus)
			w, h = r - l, b - t
			draw.text((x+(self.SQUARE_SIZE-w)//2, y+(self.SQUARE_SIZE-h)//2), common.common.Planets[i], fill=clr, font=self.fntMorinus)
			j_plan += 1

		# --- SECCIÓN AscMC (Cabecera y Aspectos) ---
		txt_ascmc = ('0', '1') # Glifos para 'Asc' y 'MC' en fntSymbol
		y_top = BOR
		for i in range(len(txt_ascmc)):		
			x_pos = BOR+(self.SQUARE_SIZE+self.SPACE)*(i+1)
			self.drawSquare(draw, x_pos, y_top, tableclr)
			
			# Medimos el texto del glifo
			l, t, r, b = draw.textbbox((0, 0), txt_ascmc[i], font=self.fntSymbol)
			w, h = r - l, b - t
			
			# CÁLCULO DE CENTRADO TEÓRICO
			center_y = int(y_top + (self.SQUARE_SIZE - h) // 2)
			
			# AJUSTE MANUAL: Subir 'Asc' y 'MC'
			# Subimos el texto restando un valor fijo (p.ej., el 15% del tamaño del cuadro).
			# Si aún lo ves bajo, sube este valor (ej. 0.20); si está muy alto, bájalo.
			# Este valor siempre será igual para esta tabla.
			OFFSET_VERTICAL_MANUAL = int(self.SQUARE_SIZE * 0.35)
			
			# Posición vertical definitiva (centro teórico - offset manual)
			y_definitiva = center_y - OFFSET_VERTICAL_MANUAL
			
			# Dibujamos con la nueva posición vertical
			draw.text((x_pos+(self.SQUARE_SIZE-w)//2, y_definitiva), txt_ascmc[i], fill=txtclr, font=self.fntSymbol)

		for i in range(len(self.chart.aspmatrixAscMC)):
			k = 0
			for j in range(len(self.chart.aspmatrixAscMC[i])):
				if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes)):
					continue
				x_cell = BOR+(i+1)*(self.SPACE+self.SQUARE_SIZE)
				y_cell = BOR+(k+1)*(self.SQUARE_SIZE+self.SPACE)
				self.drawSquare(draw, x_cell, y_cell, tableclr)
				
				# DEFINICIÓN DE showasp PARA AscMC (Soluciona el error)
				lon1 = self.chart.houses.ascmc[i]
				lon2 = self.chart.planets.planets[j].data[planets.Planet.LONG]
				showasp = self.isShowAsp(self.chart.aspmatrixAscMC[i][j].typ, lon1, lon2)

				if showasp:
					if self.isExact(self.chart.aspmatrixAscMC[i][j].exact, lon1, lon2):
						draw.rectangle(((x_cell+self.XOFFSET//2, y_cell+self.XOFFSET//2), (x_cell+self.SQUARE_SIZE-self.XOFFSET//2, y_cell+self.SQUARE_SIZE-self.XOFFSET//2-1)), fill=self.bkgclr, outline=tableclr)
					
					txt_asp = common.common.Aspects[self.chart.aspmatrixAscMC[i][j].typ]
					clr_asp = self.options.clraspect[self.chart.aspmatrixAscMC[i][j].typ] if not self.bw else (0,0,0)
					draw.text((x_cell+self.XOFFSET, y_cell+self.YOFFSET), txt_asp, fill=clr_asp, font=self.fntAspects)

				# Dibujo de Orbe (con limpieza de solapamiento)
				txt_num = str(self.chart.aspmatrixAscMC[i][j].aspdif) if showasp else str(self.chart.aspmatrixAscMC[i][j].dif)
				fnt_n = self.fntText3 if showasp else self.fntText2
				clr_n = (self.options.clraspect[self.chart.aspmatrixAscMC[i][j].typ] if showasp else txtclr) if not self.bw else (0,0,0)

				t_part = txt_num.partition('.')
				txt_num = t_part[0]+t_part[1]+t_part[2][0]
				l_n, t_n, r_n, b_n = draw.textbbox((0, 0), txt_num, font=fnt_n)
				w_n, h_n = r_n - l_n, b_n - t_n
				# Subida del 15%
				draw.text((x_cell+(self.SQUARE_SIZE-w_n)//2, y_cell+self.SQUARE_SIZE-h_n-self.YOFFSET-int(self.SQUARE_SIZE*0.15)), txt_num, fill=clr_n, font=fnt_n)
				k += 1

		# --- DIAGONAL DE PLANETAS ---
		x_diag = BOR+3*self.SQUARE_SIZE+3*self.SPACE
		y_start = BOR+(self.SQUARE_SIZE+self.SPACE)
		ii = 0
		for i in range(self.chart.planets.PLANETS_NUM-1):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			jj = 0
			for j in range(self.chart.planets.PLANETS_NUM-1):
				if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes)):
					continue
				
				if jj > ii:
					k_pos = x_diag+(self.SQUARE_SIZE+self.SPACE)*ii
					l_pos = y_start+(self.SQUARE_SIZE+self.SPACE)*jj
					self.drawSquare(draw, k_pos, l_pos, tableclr)
					
					lon1_p = self.chart.planets.planets[i].data[planets.Planet.LONG]
					lon2_p = self.chart.planets.planets[j].data[planets.Planet.LONG]
					showasp_p = self.isShowAsp(self.chart.aspmatrix[j][i].typ, lon1_p, lon2_p, j)
					
					if showasp_p:
						txt_asp = common.common.Aspects[self.chart.aspmatrix[j][i].typ]
						clr_asp = self.options.clraspect[self.chart.aspmatrix[j][i].typ] if not self.bw else (0,0,0)
						draw.text((k_pos+self.XOFFSET, l_pos+self.YOFFSET), txt_asp, fill=clr_asp, font=self.fntAspects)

					# Texto Orbe Planetas
					txt_d = str(self.chart.aspmatrix[j][i].aspdif) if showasp_p else str(self.chart.aspmatrix[j][i].dif)
					fnt_d = self.fntText3 if showasp_p else self.fntText2
					t_p = txt_d.partition('.')
					txt_d = t_p[0]+t_p[1]+t_p[2][0]
					l_d, t_d, r_d, b_d = draw.textbbox((0, 0), txt_d, font=fnt_d)
					draw.text((k_pos+(self.SQUARE_SIZE-(r_d-l_d))//2, l_pos+self.SQUARE_SIZE-(b_d-t_d)-self.YOFFSET-int(self.SQUARE_SIZE*0.15)), txt_d, fill=(0,0,0), font=fnt_d)
				jj += 1
			ii += 1

		# --- SECCIÓN CASAS ---
		if not self.options.intables or (self.options.intables and self.options.houses):
			x_h_base = BOR+self.HOUSESOFFS*(self.SQUARE_SIZE+self.SPACE)
			for i in range(len(self.hidx)):
				# Cabecera Casas
				self.drawSquare(draw, x_h_base+i*(self.SQUARE_SIZE+self.SPACE), BOR, tableclr)
				txt_h = common.common.Housenames2[self.hidx[i]-1]
				l, t, r, b = draw.textbbox((0, 0), txt_h, font=self.fntText)
				draw.text((x_h_base+i*(self.SQUARE_SIZE+self.SPACE)+(self.SQUARE_SIZE-(r-l))//2, BOR+(self.SQUARE_SIZE-(b-t))//2), txt_h, fill=(0,0,0), font=self.fntText)

				kk = 0
				for j in range(len(self.chart.aspmatrixH[i])):
					if self.options.intables and ((j == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (j == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (j == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (j == astrology.SE_MEAN_NODE and not self.options.shownodes)):
						continue
					
					k_h = x_h_base+i*(self.SQUARE_SIZE+self.SPACE)
					l_h = BOR+(kk+1)*(self.SQUARE_SIZE+self.SPACE)
					self.drawSquare(draw, k_h, l_h, tableclr)
					
					lon1_h = self.chart.houses.cusps[self.hidx[i]]
					lon2_h = self.chart.planets.planets[j].data[planets.Planet.LONG]
					showasp_h = self.isShowAsp(self.chart.aspmatrixH[i][j].typ, lon1_h, lon2_h)
					
					if showasp_h:
						txt_asp = common.common.Aspects[self.chart.aspmatrixH[i][j].typ]
						draw.text((k_h+self.XOFFSET, l_h+self.YOFFSET), txt_asp, fill=(0,0,0), font=self.fntAspects)

					txt_n = str(self.chart.aspmatrixH[i][j].aspdif) if showasp_h else str(self.chart.aspmatrixH[i][j].dif)
					fnt_n = self.fntText3 if showasp_h else self.fntText2
					t_p = txt_n.partition('.')
					txt_n = t_p[0]+t_p[1]+t_p[2][0]
					l_n, t_n, r_n, b_n = draw.textbbox((0, 0), txt_n, font=fnt_n)
					draw.text((k_h+(self.SQUARE_SIZE-(r_n-l_n))//2, l_h+self.SQUARE_SIZE-(b_n-t_n)-self.YOFFSET-int(self.SQUARE_SIZE*0.15)), txt_n, fill=(0,0,0), font=fnt_n)
					kk += 1

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawSquare(self, draw, x, y, tableclr):
		draw.line((x, y, x+self.SQUARE_SIZE, y), fill=tableclr)
		draw.line((x, y, x, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x, y+self.SQUARE_SIZE, x+self.SQUARE_SIZE, y+self.SQUARE_SIZE), fill=tableclr)
		draw.line((x+self.SQUARE_SIZE, y+self.SQUARE_SIZE, x+self.SQUARE_SIZE, y), fill=tableclr)


	def isShowAsp(self, typ, lon1, lon2, p = -1):
		res = False

		if typ != chart.Chart.NONE and (not self.options.intables or self.options.aspect[typ]):
			val = True
			#check traditional aspects
			if self.options.intables:
				if self.options.traditionalaspects:
					if not(typ == chart.Chart.CONJUNCTIO or typ == chart.Chart.SEXTIL or typ == chart.Chart.QUADRAT or typ == chart.Chart.TRIGON or typ == chart.Chart.OPPOSITIO):
						val = False
					else:
						lona1 = lon1
						lona2 = lon2
						if self.options.ayanamsha != 0:
							lona1 -= self.chart.ayanamsha
							lona1 = util.normalize(lona1)
							lona2 -= self.chart.ayanamsha
							lona2 = util.normalize(lona2)
						sign1 = int(lona1/chart.Chart.SIGN_DEG)
						sign2 = int(lona2/chart.Chart.SIGN_DEG)
						signdiff = math.fabs(sign1-sign2)
						#check pisces-aries transition
						if signdiff > chart.Chart.SIGN_NUM//2:
							signdiff = chart.Chart.SIGN_NUM-signdiff#!?
						if self.arsigndiff[typ] != signdiff:
							val = False

				if not self.options.aspectstonodes and p == astrology.SE_MEAN_NODE:
					val = False

			res = val

		return res


	def isExact(self, exact, lon1, lon2):
		res = False

		if self.options.intables and self.options.traditionalaspects:
			lona1 = lon1
			lona2 = lon2
			if self.options.ayanamsha != 0:
				lona1 -= self.chart.ayanamsha
				lona1 = util.normalize(lona1)
				lona2 -= self.chart.ayanamsha
				lona2 = util.normalize(lona2)
			deg1 = int(lona1%chart.Chart.SIGN_DEG)
			deg2 = int(lona2%chart.Chart.SIGN_DEG)
			if deg1 == deg2:
				res = True
		else:
			if exact:
				res = True

		return res



