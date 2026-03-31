import wx
import os
import astrology
import chart
import planets
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class MidPointsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = self.FONT_SIZE/2
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.YOFFSET = self.LINE_HEIGHT
		self.TABLE_HEIGHT = (30*(self.LINE_HEIGHT)+4*self.YOFFSET)

		self.SMALL_CELL_WIDTH = 5*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.XOFFSET = self.SMALL_CELL_WIDTH
		self.TABLE_WIDTH = (3*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH)+3*self.XOFFSET)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = [self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil]
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2

		self.deg_symbol = u'\u00b0'

		#X,Y
		LN = 12
		BOR = commonwnd.CommonWnd.BORDER
		self.ar = [[BOR, BOR], [BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET, BOR], [BOR+2*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET), BOR], [BOR, BOR+LN*self.LINE_HEIGHT+self.YOFFSET], [BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET, BOR+LN*self.LINE_HEIGHT+self.YOFFSET], [BOR+2*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET), BOR+LN*self.LINE_HEIGHT+self.YOFFSET], [BOR, BOR+(LN+9)*self.LINE_HEIGHT+2*self.YOFFSET], [BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET, BOR+(LN+9)*self.LINE_HEIGHT+2*self.YOFFSET], [BOR+2*(self.SMALL_CELL_WIDTH+self.CELL_WIDTH+self.XOFFSET), BOR+(LN+9)*self.LINE_HEIGHT+2*self.YOFFSET], [BOR, BOR+(LN+15)*self.LINE_HEIGHT+3*self.YOFFSET]]

		if self.options.intables:
			leng = len(self.ar)
			for i in range(3, leng):
				if not self.options.transcendental[chart.Chart.TRANSURANUS]:
					self.ar[i][1] -= self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= self.LINE_HEIGHT
				if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
					self.ar[i][1] -= self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= self.LINE_HEIGHT
				if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
					self.ar[i][1] -= self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= self.LINE_HEIGHT
				if not self.options.shownodes:
					self.ar[i][1] -= 2*self.LINE_HEIGHT
					if i >= 6:
						self.ar[i][1] -= 2*self.LINE_HEIGHT

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Mid']


	def drawBkg(self):
		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)

		tableclr = self.options.clrtable
		if self.bw:
			tableclr = (0,0,0)

		txtclr = self.options.clrtexts
		if self.bw:
			txtclr = (0,0,0)

		img = Image.new('RGB', (int(self.WIDTH), int(self.HEIGHT)), self.bkgclr)
		draw = ImageDraw.Draw(img)

		# --- CABECERAS "Longitude" ---
		txt_head = mtexts.txts['Longitude']
		# Usamos textbbox para precisión
		l_h, t_h, r_h, b_h = draw.textbbox((0, 0), txt_head, font=self.fntText)
		w_head, h_head = r_h - l_h, b_h - t_h
		
		num = len(self.ar)
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]: num -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]: num -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]: num -= 1
			if not self.options.shownodes: num -= 1

		for i in range(num):
			x = self.ar[i][0]+self.SMALL_CELL_WIDTH
			y = self.ar[i][1]
			draw.line((x, y, x+self.CELL_WIDTH, y), fill=tableclr)
			draw.line((x, y, x, y+self.LINE_HEIGHT), fill=tableclr)
			draw.line((x+self.CELL_WIDTH, y, x+self.CELL_WIDTH, y+self.LINE_HEIGHT), fill=tableclr)
			draw.line((x-self.SMALL_CELL_WIDTH, y+self.LINE_HEIGHT, x+self.CELL_WIDTH, y+self.LINE_HEIGHT), fill=tableclr)
			
			# Centrado y pequeña elevación manual (-2 píxeles aprox)
			draw.text((x+(self.CELL_WIDTH-w_head)/2, y+(self.LINE_HEIGHT-h_head)/2 - 2), txt_head, fill=txtclr, font=self.fntText)

		artmp = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
		arln = [0]
		for i in range(len(artmp)):
			arln.append(arln[i]+artmp[i])

		# --- FILAS DE MIDPOINTS ---
		for i in range(num):
			ln = 1
			for j in range(arln[i], arln[i+1]):		
				if self.options.intables and ((self.chart.midpoints.mids[j].p2 == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (self.chart.midpoints.mids[j].p2 == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (self.chart.midpoints.mids[j].p2 == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (self.chart.midpoints.mids[j].p2 == astrology.SE_MEAN_NODE and not self.options.shownodes) or (self.chart.midpoints.mids[j].p2 == astrology.SE_TRUE_NODE and not self.options.shownodes)):
					continue
				
				# Medimos el separador
				l_s, t_s, r_s, b_s = draw.textbbox((0, 0), ' - ', font=self.fntText)
				wsp, hsp = r_s - l_s, b_s - t_s
				
				p1 = common.common.Planets[self.chart.midpoints.mids[j].p1]
				p2 = common.common.Planets[self.chart.midpoints.mids[j].p2]
				
				# Medimos planetas
				l1, t1, r1, b1 = draw.textbbox((0, 0), p1, font=self.fntMorinus)
				wpl1 = r1 - l1
				l2, t2, r2, b2 = draw.textbbox((0, 0), p2, font=self.fntMorinus)
				wpl2 = r2 - l2
				
				# Colores
				clr1 = (0,0,0)
				clr2 = (0,0,0)
				if not self.bw:
					objidx1 = self.chart.midpoints.mids[j].p1
					objidx2 = self.chart.midpoints.mids[j].p2
					if objidx1 >= planets.Planets.PLANETS_NUM-1: objidx1 -= 1
					if objidx2 >= planets.Planets.PLANETS_NUM-1: objidx2 -= 1
					if self.options.useplanetcolors:
						clr1 = self.options.clrindividual[objidx1]
						clr2 = self.options.clrindividual[objidx2]
					else:
						clr1 = self.clrs[self.chart.dignity(self.chart.midpoints.mids[j].p1)]
						clr2 = self.clrs[self.chart.dignity(self.chart.midpoints.mids[j].p2)]

				# Dibujar P1 - P2 (Subimos 2px la Y para que no pise la línea inferior)
				y_row = self.ar[i][1]+self.LINE_HEIGHT*ln
				pos_y_txt = y_row+(self.LINE_HEIGHT-hsp)/2 - 2
				
				start_x = self.ar[i][0]+(self.SMALL_CELL_WIDTH-(wpl1+wsp+wpl2))/2
				draw.text((start_x, pos_y_txt), p1, fill=clr1, font=self.fntMorinus)
				draw.text((start_x+wpl1, pos_y_txt), ' - ', fill=txtclr, font=self.fntText)
				draw.text((start_x+wpl1+wsp, pos_y_txt), p2, fill=clr2, font=self.fntMorinus)

				# Datos de Longitud
				lona = self.chart.midpoints.mids[j].m
				if self.options.ayanamsha != 0:
					lona = util.normalize(lona - self.chart.ayanamsha)
				
				d, m, s = util.decToDeg(lona)
				sign = int(lona/chart.Chart.SIGN_DEG)
				pos = int(lona%chart.Chart.SIGN_DEG)
				
				txt_val = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				
				l_v, t_v, r_v, b_v = draw.textbbox((0, 0), txt_val, font=self.fntText)
				w_val = r_v - l_v
				l_sig, t_sig, r_sig, b_sig = draw.textbbox((0, 0), self.signs[sign], font=self.fntMorinus)
				w_sig = r_sig - l_sig
				
				# Espacio entre número y signo
				l_spc, t_spc, r_spc, b_spc = draw.textbbox((0, 0), ' ', font=self.fntText)
				w_space = r_spc - l_spc
				
				offs = (self.CELL_WIDTH-(w_val+w_space+w_sig))/2
				draw.text((self.ar[i][0]+self.SMALL_CELL_WIDTH+offs, pos_y_txt), txt_val, fill=txtclr, font=self.fntText)
				draw.text((self.ar[i][0]+self.SMALL_CELL_WIDTH+offs+w_val+w_space, pos_y_txt), self.signs[sign], fill=txtclr, font=self.fntMorinus)

				# Líneas de la celda
				x_box = self.ar[i][0]
				draw.line((x_box, y_row+self.LINE_HEIGHT, x_box+self.SMALL_CELL_WIDTH+self.CELL_WIDTH, y_row+self.LINE_HEIGHT), fill=tableclr)
				draw.line((x_box, y_row+self.LINE_HEIGHT, x_box, y_row), fill=tableclr)
				draw.line((x_box+self.SMALL_CELL_WIDTH, y_row+self.LINE_HEIGHT, x_box+self.SMALL_CELL_WIDTH, y_row), fill=tableclr)
				draw.line((x_box+self.SMALL_CELL_WIDTH+self.CELL_WIDTH, y_row+self.LINE_HEIGHT, x_box+self.SMALL_CELL_WIDTH+self.CELL_WIDTH, y_row), fill=tableclr)

				ln += 1

		# Render final
		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)





