import os
import wx
import astrology
import planets
import chart
import arabicparts
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class ArabicPartsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)
		
		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		lengthparts = 0
		if chrt.parts.parts != None:
			lengthparts = len(chrt.parts.parts)
		self.LINE_NUM = 1+lengthparts
		self.COLUMN_NUM = 4

		self.CELL_WIDTH = 12*self.FONT_SIZE
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_WIDTH = (self.COLUMN_NUM*(self.CELL_WIDTH))
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT))
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
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
		return mtexts.txts['Ara']


	def drawBkg(self):
		# --- AJUSTES DE ESTILO ---
		SUBIR_TEXTO = -4  
		SUBIR_SIMBOLO = -5
		# -------------------------

		if self.bw:
			self.bkgclr = (255,255,255)
		else:
			self.bkgclr = self.options.clrbackground

		self.SetBackgroundColour(self.bkgclr)
		tableclr = (0,0,0) if self.bw else self.options.clrtable
		img = Image.new('RGB', (int(self.WIDTH), int(self.HEIGHT)), self.bkgclr)
		draw = ImageDraw.Draw(img)
		BOR = commonwnd.CommonWnd.BORDER
		txtclr = (0,0,0) if self.bw else self.options.clrtexts

		# Títulos de las columnas (Basado en tu imagen de Windows)
		draw.rectangle(((BOR, BOR),(BOR+self.TABLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=tableclr, fill=self.bkgclr)
		
		# Ajustamos los nombres de las columnas para que coincidan con Windows
		headers = ["#", mtexts.txts['Name'], mtexts.txts['Formula'], mtexts.txts['Longitude'], "Dodecatemorion", "Declination", "Almuten"]
		
		# Nota: Las "offs" (anchos de columna) deben estar bien definidos en el __init__ 
		# para que quepan todas estas columnas nuevas.
		
		# Parts: Dibujamos Lot of Fortune primero
		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		self.drawlinelof(draw, x, y, mtexts.txts['LotOfFortune'], self.chart.fortune.fortune, tableclr, SUBIR_TEXTO, SUBIR_SIMBOLO)

		# Dibujamos el resto de las Partes Arábigas
		if self.chart.parts.parts != None:
			for i in range(len(self.chart.parts.parts)):
				y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_HEIGHT)*(i+1)
				self.drawline(draw, x, y, self.chart.parts.parts, tableclr, i, SUBIR_TEXTO, SUBIR_SIMBOLO)

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawlinelof(self, draw, x, y, name, data, clr, SUBIR_TEXTO, SUBIR_SIMBOLO):
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		txtclr = (0,0,0)
		if not self.bw: txtclr = self.options.clrtexts

		for i in range(self.COLUMN_NUM+1+1):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == 1:
				bbox = draw.textbbox((0, 0), name, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), name, fill=txtclr, font=self.fntText)
			elif i == 2:
				# ... (Lógica de la fórmula se mantiene igual) ...
				formula = u''
				if self.options.lotoffortune == chart.Chart.LFMOONSUN:
					formula = mtexts.txts['AC']+u' + '+mtexts.txts['MO']+u' - '+mtexts.txts['SU']
				# [Se omiten los otros elif de fórmula por brevedad, no cambian]
				bbox = draw.textbbox((0, 0), formula, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), formula, fill=txtclr, font=self.fntText)
			elif i == 3:
				lon = data[i-3]
				if self.options.ayanamsha != 0:
					lon = util.normalize(lon-self.chart.ayanamsha)
				d,m,s = util.decToDeg(lon)
				sign = int(d/chart.Chart.SIGN_DEG)
				pos = int(d%chart.Chart.SIGN_DEG)
				
				txtsign = self.signs[sign]
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				
				bbox_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp = bbox_sp[2] - bbox_sp[0]
				bbox_sg = draw.textbbox((0, 0), txtsign, font=self.fntMorinus)
				wsg = bbox_sg[2] - bbox_sg[0]
				bbox_t = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox_t[2] - bbox_t[0], bbox_t[3] - bbox_t[1]
				
				offset = (offs[i]-(w+wsp+wsg))//2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), txt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-h)//2 + SUBIR_SIMBOLO), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i == 4:
				self.drawDegWinner(draw, x+summa, y, 3, True, self.chart.almutens.essentials.degwinner, txtclr, SUBIR_TEXTO, SUBIR_SIMBOLO)
			summa += offs[i]


	def drawline(self, draw, x, y, data, clr, idx, SUBIR_TEXTO, SUBIR_SIMBOLO):
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)
		offs = (0, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		txtclr = (0,0,0)
		if not self.bw: txtclr = self.options.clrtexts

		for i in range(self.COLUMN_NUM+1+1):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == arabicparts.ArabicParts.NAME:
				name = data[idx][i]
				bbox = draw.textbbox((0, 0), name, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i+1]-w)//2, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), name, fill=txtclr, font=self.fntText)
			elif i == arabicparts.ArabicParts.FORMULA:
				# ... (Lógica de obtención de A, B, C igual) ...
				formula = mtexts.partstxts[data[idx][1][0]]+u' + '+mtexts.partstxts[data[idx][1][1]]+u' - '+mtexts.partstxts[data[idx][1][2]]
				bbox = draw.textbbox((0, 0), formula, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+self.CELL_WIDTH+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), formula, fill=txtclr, font=self.fntText)
			elif i == arabicparts.ArabicParts.LONG:
				lon = data[idx][i]
				if self.options.ayanamsha != 0:
					lon = util.normalize(lon-self.chart.ayanamsha)
				d,m,s = util.decToDeg(lon)
				sign = int(d/chart.Chart.SIGN_DEG)
				pos = int(d%chart.Chart.SIGN_DEG)
				
				txtsign = self.signs[sign]
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				
				wsp = draw.textbbox((0, 0), ' ', font=self.fntText)[2]
				wsg = draw.textbbox((0, 0), txtsign, font=self.fntMorinus)[2]
				bbox_t = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox_t[2] - bbox_t[0], bbox_t[3] - bbox_t[1]
				
				offset = (offs[i]-(w+wsp+wsg))//2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), txt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-h)//2 + SUBIR_SIMBOLO), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i == arabicparts.ArabicParts.DEGWINNER:
				self.drawDegWinner2(draw, x+summa, y, data[idx][i], txtclr, SUBIR_TEXTO, SUBIR_SIMBOLO)
			summa += offs[i]

	def drawDegWinner(self, draw, x, y, i, onlyone, degwinner, txtclr, SUBIR_TEXTO, SUBIR_SIMBOLO):
		aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]] # planetid, score, width
		subnum = len(degwinner[0])
		mwidth = 0 # <--- Aquí se inicializa
		
		# Primero calculamos el ancho total (mwidth)
		for j in range(subnum):
			pid = degwinner[i][j][0]
			if pid != -1:
				ptxt = common.common.Planets[pid]
				# CORRECCIÓN textbbox
				bbox_pl = draw.textbbox((0, 0), ptxt, font=self.fntMorinus)
				wpl = bbox_pl[2] - bbox_pl[0]
				
				sco = degwinner[i][0][1]
				txt = '('+str(sco)+')'
				bbox_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w = bbox_txt[2] - bbox_txt[0]
				
				bbox_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp = bbox_sp[2] - bbox_sp[0]
				
				aux[j][0] = pid
				aux[j][1] = sco
				aux[j][2] = wpl+wsp+w
				if mwidth != 0:
					mwidth += wsp
				mwidth += wpl+wsp+w
			else:
				break
			
		# Ahora dibujamos usando ese mwidth
		for j in range(subnum):
			if aux[j][0] != -1:
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[aux[j][0]]
					else:
						dign = self.chart.dignity(aux[j][0])
						clr = self.clrs[dign]
				
				pltxt = common.common.Planets[aux[j][0]]
				bbox_pl = draw.textbbox((0, 0), pltxt, font=self.fntMorinus)
				wpl, hpl = bbox_pl[2] - bbox_pl[0], bbox_pl[3] - bbox_pl[1]
				
				txt = '('+str(aux[j][1])+')'
				bbox_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp = bbox_sp[2] - bbox_sp[0]
				bbox_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox_txt[2] - bbox_txt[0], bbox_txt[3] - bbox_txt[1]
				
				prev = 0
				for p in range(j):
					prev += aux[p][2] + wsp # Corregido aux[p]

				offs = i
				if onlyone:
					offs = 0
				
				draw.text((x+(self.CELL_WIDTH-(mwidth))//2+prev, y+offs*self.LINE_HEIGHT+(self.LINE_HEIGHT-hpl)//2 + SUBIR_SIMBOLO), pltxt, fill=clr, font=self.fntMorinus)
				draw.text((x+(self.CELL_WIDTH-(mwidth))//2+prev+wpl+wsp, y+offs*self.LINE_HEIGHT+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), txt, fill=txtclr, font=self.fntText)

	def drawDegWinner2(self, draw, x, y, degwinner, txtclr, SUBIR_TEXTO, SUBIR_SIMBOLO):
		aux = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
		subnum = len(degwinner)
		mwidth = 0
		
		for j in range(subnum):
			pid = degwinner[j][0]
			if pid != -1:
				ptxt = common.common.Planets[pid]
				wpl = draw.textbbox((0, 0), ptxt, font=self.fntMorinus)[2]
				sco = degwinner[0][1]
				txt = '('+str(sco)+')'
				w = draw.textbbox((0, 0), txt, font=self.fntText)[2]
				wsp = draw.textbbox((0, 0), ' ', font=self.fntText)[2]
				aux[j][0] = pid
				aux[j][1] = sco
				aux[j][2] = wpl+wsp+w
				if mwidth != 0:
					mwidth += wsp
				mwidth += wpl+wsp+w
			else:
				break
			
		for j in range(subnum):
			if aux[j][0] != -1:
				clr = (0, 0, 0)
				if not self.bw:
					if self.options.useplanetcolors:
						clr = self.options.clrindividual[aux[j][0]]
					else:
						dign = self.chart.dignity(aux[j][0])
						clr = self.clrs[dign]
				
				pltxt = common.common.Planets[aux[j][0]]
				bbox_pl = draw.textbbox((0, 0), pltxt, font=self.fntMorinus)
				wpl, hpl = bbox_pl[2] - bbox_pl[0], bbox_pl[3] - bbox_pl[1]
				
				txt = '('+str(aux[j][1])+')'
				wsp = draw.textbbox((0, 0), ' ', font=self.fntText)[2]
				bbox_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox_txt[2] - bbox_txt[0], bbox_txt[3] - bbox_txt[1]
				
				prev = 0
				for p in range(j):
					prev += aux[p][2] + wsp

				draw.text((x+(self.CELL_WIDTH-(mwidth))//2+prev, y+(self.LINE_HEIGHT-hpl)//2 + SUBIR_SIMBOLO), pltxt, fill=clr, font=self.fntMorinus)
				draw.text((x+(self.CELL_WIDTH-(mwidth))//2+prev+wpl+wsp, y+(self.LINE_HEIGHT-h)//2 + SUBIR_TEXTO), txt, fill=txtclr, font=self.fntText)








