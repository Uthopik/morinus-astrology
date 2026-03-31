import wx
import os
import astrology
import chart
import houses
import planets
import primdirs
import common
from PIL import Image, ImageDraw, ImageFont
#from PIL import Image, ImageDraw, ImageFont
import util
import mtexts

from math import sin, asin, cos, radians, degrees, tan


class PositionsWnd(wx.ScrolledWindow):
	BORDER = 20
	SCROLL_RATE = 20

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		wx.ScrolledWindow.__init__(self, parent, id, wx.DefaultPosition, size=size, style=wx.SUNKEN_BORDER)

		self.parent = parent
		self.chart = chrt
		self.options = options		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.parent.mbw.Check(self.bw)

		self.speculum = 0
		if self.options.primarydir == primdirs.PrimDirs.REGIOMONTAN or self.options.primarydir == primdirs.PrimDirs.CAMPANIAN:
			self.speculum = 1

		column_num = 0
		for i in range(len(self.options.speculums[self.speculum])):
			if self.options.speculums[self.speculum][i] == True:
				column_num += 1

		BOR = PositionsWnd.BORDER

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = column_num
		self.SPACE = int(self.FONT_SIZE/2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE

		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.COLUMN_NUM*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.SPACE_ASCPLANETSY = self.LINE_HEIGHT
		self.SPACE_PLANETSHCSY = self.LINE_HEIGHT

		self.LINE_NUM = 19
		if self.options.intables:
			if not self.options.transcendental[chart.Chart.TRANSURANUS]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSNEPTUNE]:
				self.LINE_NUM -= 1
			if not self.options.transcendental[chart.Chart.TRANSPLUTO]:
				self.LINE_NUM -= 1
			if not self.options.shownodes:
				self.LINE_NUM -= 1
			if not self.options.houses:
				self.LINE_NUM -= 6
				self.SPACE_PLANETSHCSY = 0

		self.TABLE_HEIGHT = ((self.TITLE_HEIGHT)+(self.LINE_NUM)*(self.LINE_HEIGHT)+self.SPACE_TITLEY+self.SPACE_ASCPLANETSY+self.SPACE_PLANETSHCSY)
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*(self.CELL_WIDTH))
	
		self.RETRYOFFS = int(3*self.FONT_SIZE/5)

		self.WIDTH = (BOR+self.TABLE_WIDTH+BOR)
		self.HEIGHT = (BOR+self.TABLE_HEIGHT+BOR)

		self.SetBackgroundColour(self.options.clrbackground)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))
		self.SetScrollRate(PositionsWnd.SCROLL_RATE, PositionsWnd.SCROLL_RATE)

		self.fntMorinus = ImageFont.truetype(common.common.symbols, int(self.FONT_SIZE))
		self.fntSymbol = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE/2))
		self.fntText = ImageFont.truetype(common.common.abc, int(self.FONT_SIZE))
		self.fntRText = ImageFont.truetype(common.common.abc, int(self.FONT_SIZE*3/4))
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)


	def onPopupMenu(self, event):
		self.parent.onPopupMenu(event)


	def onSaveAsBitmap(self, event):
		name = self.chart.name+mtexts.txts['Pos']
		dlg = wx.FileDialog(self, mtexts.txts['SaveAsBmp'], '', name, mtexts.txts['BMPFiles'], wx.FD_SAVE)
		if os.path.isdir(self.mainfr.fpathimgs):
			dlg.SetDirectory(self.mainfr.fpathimgs)
		else:
			dlg.SetDirectory(u'.')

		if (dlg.ShowModal() == wx.ID_OK):
			dpath = dlg.GetDirectory()
			fpath = dlg.GetPath()
			if (not fpath.endswith(u'.bmp')):
				fpath+=u'.bmp'
			#Check if fpath already exists!?
			if (os.path.isfile(fpath)):
 				dlgm = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
			if (dlgm.ShowModal() == wx.ID_NO):
				dlgm.Destroy()
				dlg.Destroy()
				return
				dlgm.Destroy()

			self.mainfr.fpathimgs = dpath
			self.buffer.SaveFile(fpath, wx.BITMAP_TYPE_BMP)

		dlg.Destroy()


	def onBlackAndWhite(self, event):
		if self.bw != event.IsChecked():
			self.bw = event.IsChecked()
			self.drawBkg()
			self.Refresh()


	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)


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

		BOR = PositionsWnd.BORDER

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		#Title
		draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR),(BOR+self.SMALL_CELL_WIDTH+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		txt = ((mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Rectascension'], mtexts.txts['Declination'], mtexts.txts['AscDiffLat'], mtexts.txts['Semiarcus'], mtexts.txts['Meridiandist'], mtexts.txts['Horizondist'], mtexts.txts['TemporalHour'], mtexts.txts['HourlyDist'], mtexts.txts['PMP'], mtexts.txts['AscDiffPole'], mtexts.txts['PoleHeight'], mtexts.txts['AODO']), (mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Rectascension'], mtexts.txts['Declination'], mtexts.txts['Meridiandist'], mtexts.txts['Horizondist'], mtexts.txts['ZD'], mtexts.txts['Pole'], mtexts.txts['Q'], mtexts.txts['WReg'], mtexts.txts['CMP'], mtexts.txts['RMP'], mtexts.txts['AZM'], mtexts.txts['ELV']))
# ########################################
# Roberto change - V 7.1.0
# ########################################

		j = 0
		for i in range(len(txt[self.speculum])):
			if self.options.speculums[self.speculum][i]:
				l, t, r, b = draw.textbbox((0, 0), txt[self.speculum][i], font=self.fntText)
				w, h = r - l, b - t
				draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*j+(self.CELL_WIDTH-w)/2, BOR+(self.LINE_HEIGHT-h)/2), txt[self.speculum][i], fill=txtclr, font=self.fntText)
				j += 1

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		#AscMC - REPARACIÓN DE DECLINACIÓN AC/MC
		txts = ('0', '1')
		lons = [self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]]
		
		# Necesitamos eps aquí también. Si ya lo calculaste abajo, muévelo arriba.
		# Si no, usamos este cálculo rápido:
		try:
			res = astrology.swe_calc_ut(self.chart.time.jd, astrology.SE_ECL_NUT, 0)
			eps = radians(res[1][0]) if (isinstance(res, tuple) and len(res) > 1) else radians(23.44)
		except:
			eps = radians(23.44)

		if self.options.ayanamsha != 0:
			for i in range(len(txts)):
				lons[i] -= self.chart.ayanamsha
				lons[i] = util.normalize(lons[i])

		# Calculamos declinaciones reales: sin(dec) = sin(eps) * sin(lon)
		decl_ac = degrees(asin(sin(eps) * sin(radians(self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LON]))))
		decl_mc = degrees(asin(sin(eps) * sin(radians(self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LON]))))

		# Ahora montamos data con los valores calculados en el último lugar de cada tupla
		data = (
			(lons[0], self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.LAT], self.chart.houses.ascmc2[houses.Houses.ASC][houses.Houses.RA], decl_ac), 
			(lons[1], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.LAT], self.chart.houses.ascmc2[houses.Houses.MC][houses.Houses.RA], decl_mc)
		)

		for i in range(len(txts)):
			self.drawanglesline(draw, x, y+i*self.LINE_HEIGHT, tableclr, txts[i], data[i], True)

		#Planets
		y = y+len(txts)*self.LINE_HEIGHT+self.SPACE_ASCPLANETSY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
		lons = []
		num = len(common.common.Planets)-1
		realnum = 0
		for i in range(num):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			lons.append(self.chart.planets.planets[i].data[planets.Planet.LONG])
			realnum += 1

		if self.options.ayanamsha != 0:
			for i in range(len(lons)):
				lons[i] -= self.chart.ayanamsha
				lons[i] = util.normalize(lons[i])
		j = 0
		for i in range(num):
			if self.options.intables and ((i == astrology.SE_URANUS and not self.options.transcendental[chart.Chart.TRANSURANUS]) or (i == astrology.SE_NEPTUNE and not self.options.transcendental[chart.Chart.TRANSNEPTUNE]) or (i == astrology.SE_PLUTO and not self.options.transcendental[chart.Chart.TRANSPLUTO]) or (i == astrology.SE_MEAN_NODE and not self.options.shownodes)):
				continue
			if self.speculum == 0:
				self.drawplacidianline(draw, x, y+j*self.LINE_HEIGHT, tableclr, common.common.Planets[i], self.chart.planets.planets[i].speculums[self.speculum], lons[j], i, self.chart.planets.planets[i].data[planets.Planet.SPLON])
			else:
				self.drawregiomontanline(draw, x, y+j*self.LINE_HEIGHT, tableclr, common.common.Planets[i], self.chart.planets.planets[i].speculums[self.speculum], lons[j], i, self.chart.planets.planets[i].data[planets.Planet.SPLON])
			j += 1

		#Houses - REPARACIÓN DE DECLINACIÓN
		if not self.options.intables or (self.options.intables and self.options.houses):
			hidx = (1, 2, 3, 10, 11, 12)
			lons = [self.chart.houses.cusps[hidx[0]], self.chart.houses.cusps[hidx[1]], self.chart.houses.cusps[hidx[2]], self.chart.houses.cusps[hidx[3]], self.chart.houses.cusps[hidx[4]], self.chart.houses.cusps[hidx[5]]]
			
			# 1. Obtenemos la Oblicuidad (eps) de forma segura
			try:
				res = astrology.swe_calc_ut(self.chart.time.jd, astrology.SE_ECL_NUT, 0)
				# Si res es una tupla, el dato está en la segunda posición
				if isinstance(res, tuple) and len(res) > 1:
					eps = radians(res[1][0])
				else:
					eps = radians(23.44) # Valor estándar si falla la extracción
			except:
				eps = radians(23.44)

			# 2. Definimos la función de cálculo trigonométrico
			def get_decl(lon_deg):
				lon_rad = radians(lon_deg)
				# Fórmula: sen(Dec) = sen(Eps) * sen(Long)
				return degrees(asin(sin(eps) * sin(lon_rad)))

			if self.options.ayanamsha != 0 and self.options.hsys != 'W':
				for i in range(len(hidx)):
					lons[i] -= self.chart.ayanamsha
					lons[i] = util.normalize(lons[i])

			# 3. Rellenamos la tabla con la declinación calculada
			data = []
			for i in range(len(hidx)):
				idx = hidx[i]-1
				lon_real = lons[i]
				# Aquí calculamos la declinación real en lugar de poner 0.0
				decl_calc = get_decl(self.chart.houses.cusps[hidx[i]])
				ra_real = self.chart.houses.cusps2[idx][0]
				data.append((lon_real, 0.0, ra_real, decl_calc))

			y = y+realnum*self.LINE_HEIGHT+self.SPACE_PLANETSHCSY
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
			for i in range(len(hidx)):
				self.drawanglesline(draw, x, y+i*self.LINE_HEIGHT, tableclr, common.common.Housenames2[hidx[i]-1], data[i])

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawanglesline(self, draw, x, y, clr, txt, data, AscMC=False):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		SPEC = 2
		j = 0
		summa = 0
		for i in range(len(self.options.speculums[self.speculum])+1+1):#+1 is the leftmost column
			if i >= SPEC and not self.options.speculums[self.speculum][i-SPEC]:
				continue

			draw.line((x+summa+offs[j], y, x+summa+offs[j], y+self.LINE_HEIGHT), fill=clr)

			j += 1
			summa += offs[i]

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts

		#draw symbols
		fnt = self.fntSymbol
		if not AscMC:
			fnt = self.fntText
		l, t, r, b = draw.textbbox((0, 0), txt, font=fnt)
		w, h = r - l, b - t
		offset = int((self.SMALL_CELL_WIDTH-w)/2)
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)/2), txt, fill=txtclr, font=fnt)

		#data
		offs = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		j = 0
		summa = 0
		for i in range(planets.Planet.DECL+1):
			if not self.options.speculums[self.speculum][i]:
				continue

			d,m,s = util.decToDeg(data[i])

			if i == planets.Planet.LONG:
				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				l1, t1, r1, b1 = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp, hsp = r1 - l1, b1 - t1
				ls, ts, rs, bs = draw.textbbox((0, 0), self.signs[int(sign)], font=self.fntMorinus)
				wsg, hsg = rs - ls, bs - ts
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				# Medimos los números primero (txt) con un margen de +12
				l_txt, t_txt, r_txt, b_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = (r_txt - l_txt) + 12, b_txt - t_txt

				# Luego medimos el signo
				ls, ts, rs, bs = draw.textbbox((0, 0), self.signs[int(sign)], font=self.fntMorinus)
				wsg, hsg = rs - ls, bs - ts
				offset = int((offs[i]-(w+wsp+wsg))/2)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=txtclr, font=self.fntText)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset+w+wsp, int(y+(self.LINE_HEIGHT-hsg)/2)), self.signs[int(sign)], fill=txtclr, font=self.fntMorinus)
			elif i == planets.Planet.LAT or i == planets.Planet.DECL:
				sign = ''
				if data[i] < 0.0:
					sign = '-'
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = (offs[i]-w)/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=txtclr, font=self.fntText)
			elif i == planets.Planet.RA:
				txt = (str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if self.options.intime:
					# Convertimos d, m y s a enteros nada más nacer
					d, m, s = [int(x) for x in util.decToDeg(data[i]/15.0)]
					txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
				else:
					txt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = (offs[i]-w)/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=txtclr, font=self.fntText)

			j += 1
			summa += offs[i]


	def drawplacidianline(self, draw, x, y, clr, txt, data, ayanlon, idxpl=0, speed=0.0):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		SPEC = 2
		j = 0
		summa = 0
		for i in range(len(self.options.speculums[self.speculum])+1+1):#+1 is the leftmost column
			if i >= SPEC and not self.options.speculums[self.speculum][i-SPEC]:
				continue

			draw.line((x+summa+offs[j], y, x+summa+offs[j], y+self.LINE_HEIGHT), fill=clr)

			j += 1
			summa += offs[i]

		#draw symbols
		clrpl = (0,0,0)
		if not self.bw:
			if self.options.useplanetcolors:
				clrpl = self.options.clrindividual[idxpl]
			else:
				dign = self.chart.dignity(idxpl)
				clrpl = self.clrs[dign]

		fnt = self.fntMorinus
		l, t, r, b = draw.textbbox((0, 0), txt, font=fnt)
		w, h = r - l, b - t
		offset = int((self.SMALL_CELL_WIDTH-w)/2)
		draw.text((x+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=fnt)
		if speed <= 0.0:
			t = 'R'
			if speed == 0.0:
				t = 'S'
			draw.text((x+offset+w, int(y+(self.LINE_HEIGHT-h)/2)+self.RETRYOFFS), t, fill=clrpl, font=self.fntRText)

		#data
		offs = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		j = 0
		summa = 0
		for i in range(len(self.options.speculums[self.speculum])):
			if not self.options.speculums[self.speculum][i]:
				continue

			d,m,s = util.decToDeg(data[i])

			if i == planets.Planet.LONG:
				if self.options.ayanamsha != 0:
					d,m,s = util.decToDeg(ayanlon)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				l_sp, t_sp, r_sp, b_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp, hsp = r_sp - l_sp, b_sp - t_sp
				l_sg, t_sg, r_sg, b_sg = draw.textbbox((0, 0), self.signs[int(sign)], font=self.fntMorinus)
				wsg, hsg = r_sg - l_sg, b_sg - t_sg
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l_txt, t_txt, r_txt, b_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = (r_txt - l_txt) + 12, b_txt - t_txt
				offset = (offs[i]-(w+wsp+wsg))/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset+w+wsp, int(y+(self.LINE_HEIGHT-hsg)/2)), self.signs[int(sign)], fill=clrpl, font=self.fntMorinus)
			elif i == planets.Planet.LAT or i == planets.Planet.DECL or i == planets.Planet.ADLAT:
				sign = ''
				if data[i] < 0.0:
					sign = '-'
				if i == planets.Planet.LAT and idxpl == 0:#Sun's latitude is always zero
					d, m, s = 0, 0, 0
					sign = ''
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = int((offs[i]-w)/2)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)
			elif i == planets.Planet.RA or i == planets.Planet.PMP or i == planets.Planet.ADPH or i == planets.Planet.POH:
				txt = (str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if i == planets.Planet.RA:
					if self.options.intime:
					# Convertimos d, m y s a enteros nada más nacer
						d, m, s = [int(x) for x in util.decToDeg(data[i]/15.0)]
						txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
					else:
						txt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = (offs[i]-w)/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)
			elif i == planets.Planet.SA or i == planets.Planet.MD or i == planets.Planet.HD or i == planets.Planet.TH or i == planets.Planet.HOD or i == planets.Planet.AODO:
				sign = ''
				if i == planets.Planet.SA or i == planets.Planet.TH or i == planets.Planet.HOD:
					sign = 'D'
					if data[i] < 0.0:
						sign = 'N'
				elif i == planets.Planet.MD:
					sign = 'M'
					if data[i] < 0.0:
						sign = 'I'
				elif i == planets.Planet.HD:
					sign = 'A'
					if data[i] < 0.0:
						sign = 'D'
				elif i == planets.Planet.AODO:
					sign = 'A'
					if data[i] < 0.0:
						sign = 'D'
				txt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = int((offs[i]-w)/2)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)

			j += 1
			summa += offs[i]


	def drawregiomontanline(self, draw, x, y, clr, txt, data, ayanlon, idxpl=0, speed=0.0):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
# ########################################
# Roberto change - V 7.1.0
# ########################################

		SPEC = 2
		j = 0
		summa = 0
		for i in range(len(self.options.speculums[self.speculum])+1+1):#+1 is the leftmost column
			if i >= SPEC and not self.options.speculums[self.speculum][i-SPEC]:
				continue

			draw.line((x+summa+offs[j], y, x+summa+offs[j], y+self.LINE_HEIGHT), fill=clr)

			j += 1
			summa += offs[i]

		#draw symbols
		clrpl = (0,0,0)
		if not self.bw:
			if self.options.useplanetcolors:
				clrpl = self.options.clrindividual[idxpl]
			else:
				dign = self.chart.dignity(idxpl)
				clrpl = self.clrs[dign]

		fnt = self.fntMorinus
		l, t, r, b = draw.textbbox((0, 0), txt, font=fnt)
		w, h = r - l, b - t
		offset = int((self.SMALL_CELL_WIDTH - w) / 2)
		draw.text((x + offset, int(y + (self.LINE_HEIGHT - h) / 2)), txt, fill=clrpl, font=fnt)
		if speed <= 0.0:
			t = 'R'
			if speed == 0.0:
				t = 'S'
			draw.text((x+offset+w, int(y+(self.LINE_HEIGHT-h)/2+self.RETRYOFFS)), t, fill=clrpl, font=self.fntRText)

		#data
		offs = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
# ########################################
# Roberto change - V 7.1.0
# ########################################

		j = 0
		summa = 0
		for i in range(len(self.options.speculums[self.speculum])):
			if not self.options.speculums[self.speculum][i]:
				continue

			d,m,s = util.decToDeg(data[i])

			if i == planets.Planet.LONG:
				if self.options.ayanamsha != 0:
					d,m,s = util.decToDeg(ayanlon)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				l_sp, t_sp, r_sp, b_sp = draw.textbbox((0, 0), ' ', font=self.fntText)
				wsp, hsp = r_sp - l_sp, b_sp - t_sp
				l_sg, t_sg, r_sg, b_sg = draw.textbbox((0, 0), self.signs[sign], font=self.fntMorinus)
				wsg, hsg = r_sg - l_sg, b_sg - t_sg
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l_txt, t_txt, r_txt, b_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = (r_txt - l_txt) + 12, b_txt - t_txt
				offset = int((offs[i]-(w+wsp+wsg))/2)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset+w+wsp, int(y+(self.LINE_HEIGHT-hsg)/2)), self.signs[sign], fill=clrpl, font=self.fntMorinus)
			elif i == planets.Planet.LAT or i == planets.Planet.DECL or i == planets.Planet.Q or i == planets.Planet.ELV:
# ########################################
# Roberto change - V 7.1.0
# ########################################
				sign = ''
				if data[i] < 0.0:
					sign = '-'
				if i == planets.Planet.LAT and idxpl == 0:#Sun's latitude is always zero
					d, m, s = 0, 0, 0
					sign = ''
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = int((offs[i]-w)/2)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)
			elif i == planets.Planet.RA or i == planets.Planet.ZD or i == planets.Planet.POLE or i == planets.Planet.W or i == planets.Planet.CMP or i == planets.Planet.RMP or i == planets.Planet.AZM or i == planets.Planet.ELV:
# ######################################## ???
# Roberto change - V 7.1.0
# ########################################
				sign = ''
				if i == planets.Planet.ZD:
					sign = 'Z'
					if data[i] < 0.0:
						sign = 'N'

				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if i == planets.Planet.RA:
					if self.options.intime:
						d,m,s = util.decToDeg(data[i]/15.0)
						txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
					else:
						txt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = (offs[i]-w)/2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)
			elif i == planets.Planet.RMD or i == planets.Planet.RHD:
				sign = ''
				if i == planets.Planet.RMD:
					sign = 'M'
					if data[i] < 0.0:
						sign = 'I'
				else:
					sign = 'A'
					if data[i] < 0.0:
						sign = 'D'

				txt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				l, t, r, b = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = r - l, b - t
				offset = int((offs[i]-w)/2)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, int(y+(self.LINE_HEIGHT-h)/2)), txt, fill=clrpl, font=self.fntText)

			j += 1
			summa += offs[i]






