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


class DodecatemoriaWnd(commonwnd.CommonWnd):

	def __init__(self, parent, chrt, options, mainfr, id = -1, size = wx.DefaultSize):
		commonwnd.CommonWnd.__init__(self, parent, chrt, options, id, size)

		self.parent = parent
		self.ants = chrt.antiscia
		self.options = options		
		self.mainfr = mainfr
		self.bw = self.options.bw

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.COLUMN_NUM = 2
		self.SPACE = int(self.FONT_SIZE//2)
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
		self.fntMorinus = ImageFont.truetype(common.common.symbols, int(self.FONT_SIZE))
		self.fntSymbol = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE//2))
		self.fntText = ImageFont.truetype(common.common.abc, int(self.FONT_SIZE))
		self.signs = common.common.Signs1
		if not self.options.signs:
			self.signs = common.common.Signs2
		self.deg_symbol = u'\u00b0'

		self.drawBkg()


	def getExt(self):
		return mtexts.txts['Dodecatemorion']


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
		txt_header = (mtexts.txts['Dodecatemorion'], "")
		for i in range(len(txt_header)):
			# Reemplazo de textsize por textbbox
			bbox = draw.textbbox((0, 0), txt_header[i], font=self.fntText)
			w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
			
			offs = 0
			if i == 1:
				offs = self.CELL_WIDTH
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH//2+offs+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2), txt_header[i], fill=txtclr, font=self.fntText)

		txt_cols = (mtexts.txts['Longitude'], mtexts.txts['Latitude'])
		for i in range(len(txt_cols)):
			bbox = draw.textbbox((0, 0), txt_cols[i], font=self.fntText)
			w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
			draw.text((BOR+self.SMALL_CELL_WIDTH+self.CELL_WIDTH*i+(self.CELL_WIDTH-w)//2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-h)//2), txt_cols[i], fill=txtclr, font=self.fntText)

		x = BOR
		y = BOR+self.TITLE_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)

		txts = (common.common.Planets[0], common.common.Planets[1], common.common.Planets[2], common.common.Planets[3], common.common.Planets[4], common.common.Planets[5], common.common.Planets[6], common.common.Planets[7], common.common.Planets[8], common.common.Planets[9], common.common.Planets[10], common.common.Planets[11], common.common.fortune, '0', '1')

		data = ((self.ants.pldodecatemoria[0].lon, 0.0), (self.ants.pldodecatemoria[1].lon, 0.0), (self.ants.pldodecatemoria[2].lon, 0.0), (self.ants.pldodecatemoria[3].lon, 0.0), (self.ants.pldodecatemoria[4].lon, 0.0), (self.ants.pldodecatemoria[5].lon, 0.0), (self.ants.pldodecatemoria[6].lon, 0.0), (self.ants.pldodecatemoria[7].lon, 0.0), (self.ants.pldodecatemoria[8].lon, 0.0), (self.ants.pldodecatemoria[9].lon, 0.0), (self.ants.pldodecatemoria[10].lon, self.ants.pldodecatemoria[10].lat), (self.ants.pldodecatemoria[11].lon, self.ants.pldodecatemoria[11].lat), (self.ants.lofdodec.lon, self.ants.lofdodec.lat), (self.ants.ascmcdodec[0].lon, self.ants.ascmcdodec[0].lat), (self.ants.ascmcdodec[1].lon, self.ants.ascmcdodec[1].lat))

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
		#bottom horizontal line
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)

		#vertical lines
		offs_v = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)

		summa = 0
		for i in range(self.COLUMN_NUM+1+1):
			draw.line((x+summa+offs_v[i], y, x+summa+offs_v[i], y+self.LINE_HEIGHT), fill=clr)
			summa += offs_v[i]

		#draw symbols
		clr_draw = (0,0,0)
		if not self.bw:
			if not AscMC:
				objidx = idx
				if objidx >= len(common.common.Planets)-1:
					objidx -= 1
				if self.options.useplanetcolors:
					clr_draw = self.options.clrindividual[objidx]
				else:
					clr_draw = self.clrs[self.chart.dignity(objidx)]
			else:
				clr_draw = self.options.clrtexts

		fnt = self.fntMorinus
		if AscMC:
			fnt = self.fntSymbol
		
		bbox = draw.textbbox((0, 0), txt, font=fnt)
		w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
		offset = (self.SMALL_CELL_WIDTH-w)//2
		draw.text((x+offset, y+(self.LINE_HEIGHT-h)//2), txt, fill=clr_draw, font=fnt)

		#data
		offs_d = (self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH)
		summa = 0
		for i in range(len(data)):
			d,m,s = util.decToDeg(data[i])

			if i == 0 or i == 2:
				if self.options.ayanamsha != 0:
					lona = data[i]+self.chart.ayanamsha
					lona = util.normalize(lona)
					d,m,s = util.decToDeg(lona)

				sign = d/chart.Chart.SIGN_DEG
				pos = d%chart.Chart.SIGN_DEG
				
				bbox_sp = draw.textbbox((0, 0), ' ', self.fntText)
				wsp, hsp = bbox_sp[2]-bbox_sp[0], bbox_sp[3]-bbox_sp[1]
				
				bbox_sg = draw.textbbox((0, 0), self.signs[int(sign)], self.fntMorinus)
				wsg, hsg = bbox_sg[2]-bbox_sg[0], bbox_sg[3]-bbox_sg[1]
				
				txt_val = (str(pos)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				bbox_v = draw.textbbox((0, 0), txt_val, self.fntText)
				wv, hv = bbox_v[2]-bbox_v[0], bbox_v[3]-bbox_v[1]
				
				offset = (offs_d[i]-(wv+wsp+wsg))//2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, y+(self.LINE_HEIGHT-hv)//2), txt_val, fill=clr_draw, font=self.fntText)
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset+wv+wsp, y+(self.LINE_HEIGHT-hsg)//2), self.signs[int(sign)], fill=clr_draw, font=self.fntMorinus)
			else:
				sign_str = ''
				if data[i] < 0.0:
					sign_str = '-'
				txt_lat = sign_str+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
				
				bbox_l = draw.textbbox((0, 0), txt_lat, self.fntText)
				wl, hl = bbox_l[2]-bbox_l[0], bbox_l[3]-bbox_l[1]
				
				offset = (offs_d[i]-wl)//2
				draw.text((x+self.SMALL_CELL_WIDTH+summa+offset, y+(self.LINE_HEIGHT-hl)//2), txt_lat, fill=clr_draw, font=self.fntText)

			summa += offs_d[i]




