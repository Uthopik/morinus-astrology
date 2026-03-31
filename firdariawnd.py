from datetime import datetime, timedelta
# ##################################
# Elias V 7.3.0
import astrology
# ##################################
import wx
import planets
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
#from PIL import Image, ImageDraw, ImageFont
import mtexts

# ##################################
# Roberto V 7.3.0
# *** SOME *** texts txtsxxx -> txts
# ##################################

class FirdariaWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, opts, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, opts, id, size)

		self.parent = parent
		self.fird = chrt.firdaria
		self.options = opts		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 1
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)

		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.CELL_WIDTH = 12*self.FONT_SIZE
		self.BIG_CELL_WIDTH = 20*self.FONT_SIZE

		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = (self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH)
		self.SPACE_TITLEY = 0

		self.EXTRA_PERIODS = 3 #Three more planetary periods after year 75
# ##################################
# Roberto V 7.3.0		
		self.LINE_NUM = (planets.Planets.PLANETS_NUM + self.EXTRA_PERIODS)*6 #(planets.Planets.PLANETS_NUM+1)+2 #+2 is the number of the Nodes of the Moon
# ##################################
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+self.LINE_NUM*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH)
	
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))
# ##################################
# Elias V 8.0.0		
		self.clrs = [self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil]
# ##################################
		self.fntMorinus = ImageFont.truetype(common.common.symbols, int(self.FONT_SIZE))
		self.fntSymbol = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE//2))
		self.fntText = ImageFont.truetype(common.common.abc, int(self.FONT_SIZE))

		self.drawBkg()


	def getExt(self):
# ##################################
# Roberto V 7.3.0		
		#return mtexts.txtsabbrevs['Fir']
		return mtexts.txts['Firdaria']
# ##################################

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
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_WIDTH, BOR+self.TITLE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))

		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		txt = mtexts.txts['Firdaria']
		if self.fird.isdaily:
			txt += ' ('+mtexts.txts['Diurnal']+')'
		else:
			if self.options.isfirbonatti:
				txt += ' ('+mtexts.txts['Nocturnal']+': '+mtexts.txts['Bonatus']+')'
			else:
				txt += ' ('+mtexts.txts['Nocturnal']+': '+mtexts.txts['AlBiruni']+')'
	
		bbox = draw.textbbox((0, 0), txt, font=self.fntText)
		w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
		draw.text((BOR+(self.BIG_CELL_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)

		plstxts = (common.common.Planets[0], common.common.Planets[1], common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[10], common.common.Planets[11])

		if self.fird.isdaily:
			planetaryyears = self.fird.dailyplanetaryyears
		else:
			if self.options.isfirbonatti:
				planetaryyears = self.fird.nightlyplanetaryyearsbonatti
			else:
				planetaryyears = self.fird.nightlyplanetaryyearsalbiruni

		ln = 0
		starting = self.fird.startdate
		for index in range(len(planetaryyears) + self.EXTRA_PERIODS):
			aindex = index % len(planetaryyears)
			planet, years = planetaryyears[aindex]
			ending = datetime(starting.year + years, starting.month, starting.day)

			planetseliascorrection=[6,5,4,0,3,2,1,7,8]
			txt = plstxts[planetseliascorrection[planet]]
			
			# Definir color ANTES de dibujar
			clr = (0,0,0)
			if not self.bw:
				objidx = planetseliascorrection[planet]
				if self.options.useplanetcolors:
					if planetseliascorrection[planet] > astrology.SE_SATURN:
						objidx = 10 
					clr = self.options.clrindividual[objidx]
				else:
					dign = self.chart.dignity(objidx)
					clr = self.clrs[dign]

			# Dibujo de rectángulos
			draw.rectangle(((BOR, BOR+(ln+1)*self.LINE_HEIGHT),(BOR+self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH, BOR+(ln+2)*self.LINE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
			draw.line((BOR+self.SMALL_CELL_WIDTH, BOR+(ln+1)*self.LINE_HEIGHT, BOR+self.SMALL_CELL_WIDTH, BOR+(ln+2)*self.LINE_HEIGHT), fill=tableclr)
			
			# Texto del Planeta
			bbox_p = draw.textbbox((0, 0), txt, font=self.fntMorinus)
			w, h = bbox_p[2]-bbox_p[0], bbox_p[3]-bbox_p[1]
			draw.text((BOR+(self.SMALL_CELL_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2+(ln+1)*self.LINE_HEIGHT), txt, fill=clr, font=self.fntMorinus)
			
			# Texto de Fechas
			ending2 = ending+timedelta(days=-1)
			txt_date = str(starting.year)+'.'+str(starting.month).zfill(2)+'.'+str(starting.day).zfill(2)+' - '+str(ending2.year)+'.'+str(ending2.month).zfill(2)+'.'+str(ending2.day).zfill(2)+' ('+str(years)+' '+'Years'+')'
			bbox_d = draw.textbbox((0, 0), txt_date, font=self.fntText)
			wd, hd = bbox_d[2]-bbox_d[0], bbox_d[3]-bbox_d[1]
			draw.text((BOR+self.SMALL_CELL_WIDTH+(self.BIG_CELL_WIDTH-wd)//2, BOR+(self.LINE_HEIGHT-hd)//2+(ln+1)*self.LINE_HEIGHT), txt_date, fill=txtclr, font=self.fntText)

			ln += 1
			ln = self.displaySubPeriods(draw, planetaryyears, aindex, starting, ending, plstxts, ln, BOR, txtclr, tableclr)
			starting = ending

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def displaySubPeriods(self, draw, planetaryyears, index, starting, ending, plstxts, ln, BOR, txtclr, tableclr):
		if self.fird.isNode(index):
			return ln

		subperiodstart = starting
		try:
			secs = (ending - starting).total_seconds()
		except:
			secs = (ending - starting).seconds + (ending - starting).microseconds / 1E6 + (ending - starting).days * 86400		

		for i in range(7):
			planet, years = planetaryyears[index]
			subperiodends = subperiodstart + timedelta(seconds = secs / 7) 

			planetseliascorrection=[6,5,4,0,3,2,1,7,8]
			txt = plstxts[planetseliascorrection[planet]]
			
			# Definir color ANTES de dibujar
			clr = (0,0,0)
			if not self.bw:
				objidx = planetseliascorrection[planet]
				if self.options.useplanetcolors:
					if planetseliascorrection[planet] > astrology.SE_SATURN:
						objidx = 10 
					clr = self.options.clrindividual[objidx]
				else:
					dign = self.chart.dignity(objidx)
					clr = self.clrs[dign]

			# Dibujo de rectángulos
			draw.rectangle(((BOR+self.SMALL_CELL_WIDTH, BOR+(ln+i+1)*self.LINE_HEIGHT),(BOR+2*self.SMALL_CELL_WIDTH+self.CELL_WIDTH, BOR+(ln+i+2)*self.LINE_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
			draw.line((BOR+2*self.SMALL_CELL_WIDTH, BOR+(ln+i+1)*self.LINE_HEIGHT, BOR+2*self.SMALL_CELL_WIDTH, BOR+(ln+i+2)*self.LINE_HEIGHT), fill=tableclr)
			
			# Texto del Planeta (Subperiodo)
			bbox_sp = draw.textbbox((0, 0), txt, font=self.fntMorinus)
			w, h = bbox_sp[2]-bbox_sp[0], bbox_sp[3]-bbox_sp[1]
			draw.text((BOR+self.SMALL_CELL_WIDTH+(self.SMALL_CELL_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2+(ln+i+1)*self.LINE_HEIGHT), txt, fill=clr, font=self.fntMorinus)
			
			# Texto de Fecha (Subperiodo)
			txt_sdate = str(subperiodstart.year)+'.'+str(subperiodstart.month).zfill(2)+'.'+str(subperiodstart.day).zfill(2)
			bbox_sd = draw.textbbox((0, 0), txt_sdate, font=self.fntText)
			ws, hs = bbox_sd[2]-bbox_sd[0], bbox_sd[3]-bbox_sd[1]
			draw.text((BOR+2*self.SMALL_CELL_WIDTH+(self.CELL_WIDTH-ws)//2, BOR+(self.LINE_HEIGHT-hs)//2+(ln+i+1)*self.LINE_HEIGHT), txt_sdate, fill=txtclr, font=self.fntText)
			
			subperiodstart = subperiodends
			index = self.fird.nextIndex(index)

		return ln+i+1


