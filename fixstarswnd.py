import wx
import os
import chart
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
import fixstars
import util
import mtexts


class FixStarsWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.mainfr = mainfr

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int(self.FONT_SIZE//2)
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = len(self.chart.fixstars.data)
		self.SMALL_CELL_WIDTH = 3*self.FONT_SIZE
		self.BIG_CELL_WIDTH = 10*self.FONT_SIZE
		self.CELL_WIDTH = 8*self.FONT_SIZE
		self.COLUMN_NUM = 6
		self.TITLE_HEIGHT = self.LINE_HEIGHT
		self.TITLE_WIDTH = self.BIG_CELL_WIDTH+(self.COLUMN_NUM-1)*self.CELL_WIDTH
		self.SPACE_TITLEY = 0
		self.TABLE_HEIGHT = (self.TITLE_HEIGHT+self.SPACE_TITLEY+(self.LINE_NUM)*(self.LINE_HEIGHT))
		self.TABLE_WIDTH = (self.SMALL_CELL_WIDTH+self.BIG_CELL_WIDTH+(self.COLUMN_NUM-1)*self.CELL_WIDTH)
		self.WIDTH = (commonwnd.CommonWnd.BORDER+self.TABLE_WIDTH+commonwnd.CommonWnd.BORDER)
		self.HEIGHT = (commonwnd.CommonWnd.BORDER+self.TABLE_HEIGHT+commonwnd.CommonWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, self.FONT_SIZE)
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Fix']


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
		txt = (mtexts.txts['Name'], mtexts.txts['Nomencl']+'.', mtexts.txts['Longitude'], mtexts.txts['Latitude'], mtexts.txts['Rectascension'], mtexts.txts['Declination'])

		summa = 0
		offs = (self.BIG_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		for i in range(len(txt)):
			bbox = draw.textbbox((0, 0), txt[i], font=self.fntText)
			w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
			draw.text((BOR+self.SMALL_CELL_WIDTH+summa+(offs[i]-w)//2, BOR+(self.TITLE_HEIGHT-h)//2), txt[i], fill=txtclr, font=self.fntText)
			summa += offs[i]

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		for i in range(len(self.chart.fixstars.data)):
			self.drawline(draw, x, y+i*self.LINE_HEIGHT, tableclr, i)

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, clr, idx):
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs = (0, self.SMALL_CELL_WIDTH, self.BIG_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		OFFS = 2
		BOR = commonwnd.CommonWnd.BORDER
		summa = 0
		txtclr = (0,0,0)
		if not self.bw:
			txtclr = self.options.clrtexts
		for i in range(self.COLUMN_NUM+OFFS):#+1 is the leftmost column
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)

			d, m, s = 0, 0, 0
			if i >= fixstars.FixStars.LON+OFFS:
				d,m,s = util.decToDeg(self.chart.fixstars.data[idx][i-OFFS])

			if i == 1:
				txt = str(idx+1)+'.'
				bbox = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)
			elif i == fixstars.FixStars.NAME+OFFS or i == fixstars.FixStars.NOMNAME+OFFS:
				trad_name = self.chart.fixstars.data[idx][fixstars.FixStars.NAME]
				tech_name = self.chart.fixstars.data[idx][fixstars.FixStars.NOMNAME]
				
				if i == fixstars.FixStars.NAME+OFFS:
					txt = trad_name if trad_name != "" else tech_name
				else:
					txt = tech_name if tech_name != "" else trad_name
				
				bbox = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)
			elif i == fixstars.FixStars.LON+OFFS:
				if self.options.ayanamsha != 0:
					lona = self.chart.fixstars.data[idx][i-OFFS]-self.chart.ayanamsha
					lona = util.normalize(lona)
					d,m,s = util.decToDeg(lona)
				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				
				# Cálculo de espacios y anchos con bbox
				bbox_sp = draw.textbbox((0,0), ' ', font=self.fntText)
				wsp, hsp = bbox_sp[2]-bbox_sp[0], bbox_sp[3]-bbox_sp[1]
				
				txtsign = self.signs[int(sign)]
				bbox_sg = draw.textbbox((0,0), txtsign, font=self.fntMorinus)
				wsg, hsg = bbox_sg[2]-bbox_sg[0], bbox_sg[3]-bbox_sg[1]
				
				txt = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				bbox_txt = draw.textbbox((0,0), txt, font=self.fntText)
				w, h = bbox_txt[2]-bbox_txt[0], bbox_txt[3]-bbox_txt[1]
				
				offset = (offs[i]-(w+wsp+wsg))//2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w+wsp, y+(self.LINE_HEIGHT-h)//2), txtsign, fill=txtclr, font=self.fntMorinus)
			elif i == fixstars.FixStars.LAT+OFFS or i == fixstars.FixStars.DECL+OFFS:
				sign = ''
				if self.chart.fixstars.data[idx][i-2] < 0.0:
					sign = '-'
				txt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				bbox = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)
			elif i == fixstars.FixStars.RA+OFFS:
				txt = str(d)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				if self.options.intime:
					d,m,s = util.decToDeg( self.chart.fixstars.data[idx][i-2]/15.0)
					txt = (str(d)).rjust(2)+':'+(str(m)).zfill(2)+":"+(str(s)).zfill(2)
				bbox = draw.textbbox((0, 0), txt, font=self.fntText)
				w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt, fill=txtclr, font=self.fntText)

			summa += offs[i]



