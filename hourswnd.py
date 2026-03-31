import wx
import os
from PIL import Image, ImageDraw, ImageFont
import astrology
import chart
import common
import commonwnd
import hours
import util
import mtexts


class HoursWnd(commonwnd.CommonWnd):
	HOURSPERHALFDAY = 12

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int(self.FONT_SIZE//2)
		self.COLUMN_NUM = 2
		self.LINE_NUM = HoursWnd.HOURSPERHALFDAY #Planets
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.SMALL_CELL_WIDTH = 2*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.TITLE_HEIGHT = 3*self.LINE_HEIGHT
		self.TITLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*self.CELL_WIDTH)
		self.SPACE_TITLEY = 0
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.COLUMN_NUM*self.CELL_WIDTH)
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)	

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Hrs']


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
		lon = int(self.chart.place.deglon+self.chart.place.minlon/60.0)
		if not self.chart.place.east:
			lon *= -1
		offs = int(lon*4.0/1440.0)
		adj = (1.0/24.0) if self.chart.time.daylightsaving else 0.0
		jdlocal = self.chart.time.jd + offs + adj
		jy, jm, jd, jh = astrology.swe_revjul(jdlocal, 1)
		hh, mm, ss = util.decToDeg(jh)

		txt = mtexts.txts['LocalBirthTime']+': '+str(hh)+':'+str(mm).zfill(2)+':'+str(ss).zfill(2)
		# CORRECCIÓN 1: Local Birth Time
		bbox = draw.textbbox((0, 0), txt, font=self.fntText)
		w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
		draw.text((BOR+(self.TITLE_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)

		if self.chart.time.ph != None:
			adj = (1.0/24.0) if self.chart.time.daylightsaving else 0.0

			rh, rm, rs = self.chart.time.ph.revTime(self.chart.time.ph.risetime + adj)
			sh, sm, ss = self.chart.time.ph.revTime(self.chart.time.ph.settime + adj)
			
			if self.chart.time.ph.daytime:
				txt1 = mtexts.txts['RiseTime']+': '+str(rh)+':'+str(rm).zfill(2)+':'+str(rs).zfill(2)
				txt2 = mtexts.txts['SetTime']+': '+str(sh)+':'+str(sm).zfill(2)+':'+str(ss).zfill(2)
			else:
				txt2 = mtexts.txts['RiseTime']+': '+str(rh)+':'+str(rm).zfill(2)+':'+str(rs).zfill(2)
				txt1 = mtexts.txts['SetTime']+': '+str(sh)+':'+str(sm).zfill(2)+':'+str(ss).zfill(2)

			# CORRECCIÓN 2: Rise/Set Time 1
			bbox1 = draw.textbbox((0, 0), txt1, font=self.fntText)
			w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
			draw.text((BOR+(self.TITLE_WIDTH-w1)//2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h1)//2), txt1, fill=txtclr, font=self.fntText)
			
			# CORRECCIÓN 3: Rise/Set Time 2
			bbox2 = draw.textbbox((0, 0), txt2, font=self.fntText)
			w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
			draw.text((BOR+(self.TITLE_WIDTH-w2)//2, BOR+2*self.LINE_HEIGHT+(self.LINE_HEIGHT-h2)//2), txt2, fill=txtclr, font=self.fntText)

			x = BOR
			y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

			self.begtime = 0.0
			if self.chart.time.ph.daytime:
				self.begtime = self.chart.time.ph.risetime
			else:
				self.begtime = self.chart.time.ph.settime
			for i in range(int(HoursWnd.HOURSPERHALFDAY)):
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, i)

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, clr, idx):
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		
		hr = 0
		endtime = 0.0
		if self.chart.time.ph.daytime:
			endtime = self.chart.time.ph.risetime+self.chart.time.ph.hrlen*(idx+1)
			hr = idx
		else:
			endtime = self.chart.time.ph.settime+self.chart.time.ph.hrlen*(idx+1)
			hr = idx+int(HoursWnd.HOURSPERHALFDAY)

		planetaryhour = hours.PlanetaryHours.PHs[self.chart.time.ph.weekday][hr]

		summa = 0
		for i in range(self.COLUMN_NUM+1+1):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			if i == 1:
				tclr = (0,0,0)
				if not self.bw:
					if self.options.useplanetcolors:
						tclr = self.options.clrindividual[planetaryhour]
					else:
						dign = self.chart.dignity(planetaryhour)
						tclr = self.clrs[dign]

				txtpl = common.common.Planets[planetaryhour] 
				# CORRECCIÓN 4: Símbolo del Planeta (fntMorinus)
				bbox_pl = draw.textbbox((0, 0), txtpl, font=self.fntMorinus)
				w_pl, h_pl = bbox_pl[2] - bbox_pl[0], bbox_pl[3] - bbox_pl[1]
				draw.text((x+summa+(offs[i]-w_pl)//2, y+(self.LINE_HEIGHT-h_pl)//2), txtpl, fill=tclr, font=self.fntMorinus)
			
			elif i > 1:
				t_temp = self.begtime if i == 2 else endtime
				offset = (1.0 / 24.0) if self.chart.time.daylightsaving else 0.0
				h_ast, m_ast, s_ast = self.chart.time.ph.revTime(t_temp + offset)

				txt = str(h_ast)+':'+str(m_ast).zfill(2)+':'+str(s_ast).zfill(2)
				
				# CORRECCIÓN 5: Texto de la hora (fntText)
				bbox_txt = draw.textbbox((0, 0), txt, font=self.fntText)
				w_txt, h_txt = bbox_txt[2] - bbox_txt[0], bbox_txt[3] - bbox_txt[1]
				draw.text((x+summa+(offs[i]-w_txt)//2, y+(self.LINE_HEIGHT-h_txt)//2), txt, fill=txtclr, font=self.fntText)

				if i == 3: # El relevo se hace al final de la fila
					self.begtime = endtime

			summa += offs[i]








