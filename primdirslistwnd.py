import os
import math
import wx
from PIL import Image, ImageDraw, ImageFont
#from PIL import Image, ImageDraw, ImageFont
import common
import astrology
import chart
import houses
import fortune
import primdirs
import pdsinchart
import pdsinchartstepperdlg
import pdsinchartframe
import pdsinchartingressframe
import pdsinchartdlgopts
import fixstars
import mtexts
import util


class PrimDirsListWnd(wx.ScrolledWindow):
	SCROLL_RATE = 20
	BORDER = 20

	def __init__(self, parent, chrt, options, pds, mainfr, currpage, maxpage, fr, to, id = -1, size = wx.DefaultSize):
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

		self.parent = parent
		self.chart = chrt
		self.options = options
		self.bw = self.options.bw
		self.pds = pds
		self.mainfr = mainfr

		self.SetBackgroundColour(self.options.clrbackground)
		self.SetScrollRate(PrimDirsListWnd.SCROLL_RATE, PrimDirsListWnd.SCROLL_RATE)

		self.pmenu = wx.Menu()
		self.ID_SaveAsBitmap = wx.NewId()
		self.ID_SaveAsText = wx.NewId()
		self.ID_BlackAndWhite = wx.NewId()
		if chrt.htype == chart.Chart.RADIX:
			self.ID_PDsInChartInZod = wx.NewId()
			self.ID_PDsInChartInMun = wx.NewId()
			self.ID_PDsInChartIngress = wx.NewId()

		self.pmenu.Append(self.ID_SaveAsBitmap, mtexts.txts['SaveAsBmp'], mtexts.txts['SaveTable'])
		self.pmenu.Append(self.ID_SaveAsText, mtexts.txts['SaveAsText'], mtexts.txts['SavePDs'])
		mbw = self.pmenu.Append(self.ID_BlackAndWhite, mtexts.txts['BlackAndWhite'], mtexts.txts['TableBW'], wx.ITEM_CHECK)
		if chrt.htype == chart.Chart.RADIX:
			self.pmenu.Append(self.ID_PDsInChartInZod, mtexts.txts['PDsInChartInZod'], mtexts.txts['PDsInChartInZod'])
			self.pmenu.Append(self.ID_PDsInChartInMun, mtexts.txts['PDsInChartInMun'], mtexts.txts['PDsInChartInMun'])
			self.pmenu.Append(self.ID_PDsInChartIngress, mtexts.txts['PDsInChartIngress'], mtexts.txts['PDsInChartIngress'])
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_RIGHT_UP, self.onPopupMenu)
		self.Bind(wx.EVT_MENU, self.onSaveAsBitmap, id=self.ID_SaveAsBitmap)
		self.Bind(wx.EVT_MENU, self.onSaveAsText, id=self.ID_SaveAsText)
		self.Bind(wx.EVT_MENU, self.onBlackAndWhite, id=self.ID_BlackAndWhite)
		if chrt.htype == chart.Chart.RADIX:
			self.Bind(wx.EVT_MENU, self.onPDsInChartZod, id=self.ID_PDsInChartInZod)
			self.Bind(wx.EVT_MENU, self.onPDsInChartMun, id=self.ID_PDsInChartInMun)
			self.Bind(wx.EVT_MENU, self.onPDsInChartIngress, id=self.ID_PDsInChartIngress)

		if (self.bw):
			mbw.Check()

		self.FONT_SIZE = int(21*self.options.tablesize) #Change fontsize to change the size of the table!
		self.SPACE = int((self.FONT_SIZE//2))
		self.LINE_HEIGHT = (self.SPACE+self.FONT_SIZE+self.SPACE)
		self.LINE_NUM = parent.LINE_NUM #Per column
		self.COLUMN_NUM = 6

		self.currpage = currpage
		self.maxpage = maxpage
		self.fr = fr
		self.to = to

		self.SMALL_CELL_WIDTH = (4*self.FONT_SIZE)
		self.CELL_WIDTH = (6*self.FONT_SIZE)
		self.BIG_CELL_WIDTH = (8*self.FONT_SIZE)
		self.TABLE_WIDTH = (2*self.SMALL_CELL_WIDTH+3*self.CELL_WIDTH+self.BIG_CELL_WIDTH)
		self.SPACE_TITLEY = 4
		self.TITLE_CELL_HEIGHT = (2*self.LINE_HEIGHT)
		self.TABLE_HEIGHT = ((self.TITLE_CELL_HEIGHT)+(self.SPACE_TITLEY)+(self.LINE_NUM)*(self.LINE_HEIGHT))
		self.SPACE_BETWEEN_TABLESX = 4
		self.TITLE_CELL_WIDTH = (2*self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX+1)
		self.SECOND_TABLE_OFFSX = (self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX)
	
		self.WIDTH = (PrimDirsListWnd.BORDER+self.TITLE_CELL_WIDTH+PrimDirsListWnd.BORDER)
		self.HEIGHT = (PrimDirsListWnd.BORDER+self.TABLE_HEIGHT+PrimDirsListWnd.BORDER)

		self.SetVirtualSize((self.WIDTH, self.HEIGHT))

		self.fntMorinus = ImageFont.truetype(common.common.symbols, int(self.FONT_SIZE))
		self.fntSymbol = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE//2))
		self.fntAspects = ImageFont.truetype(common.common.symbols, int(3*self.FONT_SIZE/4))
		self.fntText = ImageFont.truetype(common.common.abc, self.FONT_SIZE)
		self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)

		self.drawBkg()
		self.curposx = None
		self.curposy = None


	def onPopupMenu(self, event):
		self.curposx, self.curposy = event.GetPosition()
		self.PopupMenu(self.pmenu, event.GetPosition())


	def onSaveAsBitmap(self, event):
		name = self.chart.name+mtexts.txts['PD']
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


	def onSaveAsText(self, event):
		if self.options.langid != 0:
			dlg = wx.MessageDialog(self, mtexts.txts['SwitchToEnglish'], mtexts.txts['Message'], wx.OK)
			dlg.ShowModal()
			return		

		name = self.chart.name+mtexts.txts['PD']
		dlg = wx.FileDialog(self, mtexts.txts['SaveAsText'], '', name, mtexts.txts['TXTFiles'], wx.FD_SAVE)
		if os.path.isdir(self.mainfr.fpathimgs):
			dlg.SetDirectory(self.mainfr.fpathimgs)
		else:
			dlg.SetDirectory(u'.')

		if dlg.ShowModal() == wx.ID_OK:
			dpath = dlg.GetDirectory()
			fpath = dlg.GetPath()
			if not fpath.endswith(u'.txt'):
				fpath+=u'.txt'
			#Check if fpath already exists!?
			if os.path.isfile(fpath):
 				dlg = wx.MessageDialog(self, mtexts.txts['FileExists'], mtexts.txts['Message'], wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)
			if dlg.ShowModal() == wx.ID_NO:
				return

			self.mainfr.fpathimgs = dpath
			self.pds.print2file(fpath)		


	def onBlackAndWhite(self, event):
		if (self.bw != event.IsChecked()):
			self.bw = event.IsChecked()
			self.drawBkg()
			self.Refresh()


	def onPDsInChartZod(self, event):
		valid, pdnum = self.getPDNum(event)

		if valid and self.pds.pds[pdnum].mundane:
 			dlg = wx.MessageDialog(self, mtexts.txts['NotAvailableWithPDSettings'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		return

		valid, y, m, d, ho, mi, se, t, pdtypetxt, pdkeytxt, direct, da, pdchart = self.calc(event, False)
		if not valid:
 			dlg = wx.MessageDialog(self, mtexts.txts['PDClickError'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		return

		txtdir = mtexts.txts['D']
		if not direct:
			txtdir = mtexts.txts['C']

		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		rw = pdsinchartframe.PDsInChartFrame(self.mainfr, txt, pdchart, self.chart, self.options)
		rw.Show(True)

		pdstepdlg = pdsinchartstepperdlg.PDsInChartStepperDlg(rw, self.chart, y, m, d, t, direct, da, self.options, False)
		pdstepdlg.CenterOnParent()
		pdstepdlg.Show(True)


	def onPDsInChartMun(self, event):
		valid, pdnum = self.getPDNum(event)

		if valid and not self.pds.pds[pdnum].mundane:# and "From the planets" in Options (Disable the Terrestrial-menuitem instead)
 			dlg = wx.MessageDialog(self, mtexts.txts['NotAvailableWithPDSettings'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		return

		valid, y, m, d, ho, mi, se, t, pdtypetxt, pdkeytxt, direct, da, pdchart = self.calc(event, True)
		if not valid:
 			dlg = wx.MessageDialog(self, mtexts.txts['PDClickError'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		return

		txtdir = mtexts.txts['D']
		if not direct:
			txtdir = mtexts.txts['C']

		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		rw = pdsinchartframe.PDsInChartFrame(self.mainfr, txt, pdchart, self.chart, self.options, 0, False)
		rw.Show(True)

		pdstepdlg = pdsinchartstepperdlg.PDsInChartStepperDlg(rw, self.chart, y, m, d, t, direct, da, self.options, True)
		pdstepdlg.CenterOnParent()
		pdstepdlg.Show(True)


	def onPDsInChartIngress(self, event):
		valid, pdnum = self.getPDNum(event)

		if valid and self.pds.pds[pdnum].mundane:
 			dlg = wx.MessageDialog(self, mtexts.txts['NotAvailableWithPDSettings'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		return

		valid, y, m, d, ho, mi, se, t, pdtypetxt, pdkeytxt, direct, da, pdchart = self.calc(event, False)
		if not valid:
 			dlg = wx.MessageDialog(self, mtexts.txts['PDClickError'], mtexts.txts['Message'], wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		return

		#create Ingress-chart
		cal = chart.Time.GREGORIAN
		if self.chart.time.cal == chart.Time.JULIAN:
			cal = chart.Time.JULIAN
		tim = chart.Time(y, m, d, ho, mi, se, self.chart.time.bc, cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
		ingchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)

		txtdir = mtexts.txts['D']
		if not direct:
			txtdir = mtexts.txts['C']

		txt = pdtypetxt+' '+pdkeytxt+' '+txtdir+' '+str(y)+'.'+str(m).zfill(2)+'.'+str(d).zfill(2)+' '+str(ho).zfill(2)+':'+str(mi).zfill(2)+':'+str(se).zfill(2)+'  '+str(da)
		rw = pdsinchartingressframe.PDsInChartIngressFrame(self.mainfr, txt, self.chart, pdchart, ingchart, self.options)
		rw.Show(True)

		pdstepdlg = pdsinchartstepperdlg.PDsInChartStepperDlg(rw, self.chart, y, m, d, t, direct, da, self.options, False)
		pdstepdlg.CenterOnParent()
		pdstepdlg.Show(True)


	def calc(self, event, terrestrial):
		valid, pdnum = self.getPDNum(event)

		if valid:
			y, m, d, t = astrology.swe_revjul(self.pds.pds[pdnum].time, 1)
			ho, mi, se = util.decToDeg(t)

			da = self.pds.pds[pdnum].arc
			if not self.pds.pds[pdnum].direct:
				da *= -1

			pdinch = pdsinchart.PDsInChart(self.chart, da) #self.yz, mz, dz, tz ==> chart
			pdh, pdm, pds = util.decToDeg(pdinch.tz)
			cal = chart.Time.GREGORIAN
			if self.chart.time.cal == chart.Time.JULIAN:
				cal = chart.Time.JULIAN
			tim = chart.Time(pdinch.yz, pdinch.mz, pdinch.dz, pdh, pdm, pds, self.chart.time.bc, cal, chart.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			if not terrestrial:
				if self.options.pdincharttyp == pdsinchartdlgopts.PDsInChartsDlgOpts.FROMMUNDANEPOS:
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)
					pdchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)
					#modify planets ...
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.planets.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.houses = houses.Houses(tim.jd, 0, pdchart.place.lat, pdchart.place.lon, 'R', pdchart.obl[0], self.options.ayanamsha, pdchart.ayanamsha)
						pdchart.planets.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])

					#modify lof
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.fortune.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.fortune.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])

				elif self.options.pdincharttyp == pdsinchartdlgopts.PDsInChartsDlgOpts.FROMZODIACALPOS:
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False, chart.Chart.YEAR, True)

					pdchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False, chart.Chart.YEAR, True)
					#modify planets ...
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.planets.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.houses = houses.Houses(tim.jd, 0, pdchart.place.lat, pdchart.place.lon, 'R', pdchart.obl[0], self.options.ayanamsha, pdchart.ayanamsha)
						pdchart.planets.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.planets.planets, self.chart.place.lat, self.chart.obl[0])

					#modify lof
					if self.options.primarydir == primdirs.PrimDirs.PLACIDIANSEMIARC or self.options.primarydir == primdirs.PrimDirs.PLACIDIANUNDERTHEPOLE:
						pdchart.fortune.calcMundaneProfPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
					else:
						pdchart.fortune.calcRegioPDsInChartsPos(pdchart.houses.ascmc2, pdchartpls.fortune, self.chart.place.lat, self.chart.obl[0])
	
				else:#Full Astronomical Procedure
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)

					pdchartpls = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)

					pdpls = pdchartpls.planets.planets
					if self.options.pdinchartsecmotion:
						pdpls = pdchart.planets.planets

					raequasc, declequasc, dist = astrology.swe_cotrans(pdchart.houses.ascmc[houses.Houses.EQUASC], 0.0, 1.0, -self.chart.obl[0])
					pdchart.planets.calcFullAstronomicalProc(da, self.chart.obl[0], pdpls, pdchart.place.lat, pdchart.houses.ascmc2, raequasc) #planets
					pdchart.fortune.calcFullAstronomicalProc(pdchartpls.fortune, da, self.chart.obl[0]) 

			else:
				if self.options.pdinchartterrsecmotion:
					pdchart = chart.Chart(self.chart.name, self.chart.male, tim, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)
				else:
					pdchart = chart.Chart(self.chart.name, self.chart.male, self.chart.time, self.chart.place, chart.Chart.PDINCHART, '', self.options, False)#, proftype, nolat)
					raequasc, declequasc, dist = astrology.swe_cotrans(pdchart.houses.ascmc[houses.Houses.EQUASC], 0.0, 1.0, -self.chart.obl[0])
					pdchart.planets.calcMundaneWithoutSM(da, self.chart.obl[0], pdchart.place.lat, pdchart.houses.ascmc2, raequasc)

				pdchart.fortune.recalcForMundaneChart(self.chart.fortune.fortune[fortune.Fortune.LON], self.chart.fortune.fortune[fortune.Fortune.LAT], self.chart.fortune.fortune[fortune.Fortune.RA], self.chart.fortune.fortune[fortune.Fortune.DECL], pdchart.houses.ascmc2, pdchart.raequasc, pdchart.obl[0], pdchart.place.lat)


			keytxt = mtexts.typeListDyn[self.options.pdkeyd]
			if not self.options.pdkeydyn:
				keytxt = mtexts.typeListStat[self.options.pdkeys]

			return True, y, m, d, ho, mi, se, t, mtexts.typeListDirs[self.options.primarydir], keytxt, self.pds.pds[pdnum].direct, math.fabs(da), pdchart

		else:
			return False, 2000, 1, 1, 1, 1, 1, 1.0, '', '', True, 0.0, None


	def getPDNum(self, event):
		xu, yu = self.GetScrollPixelsPerUnit()
		xs, ys = self.GetViewStart()
		yscrolledoffs = yu*ys
		xscrolledoffs = xu*xs
		x,y = self.curposx, self.curposy
		offs = PrimDirsListWnd.BORDER+self.TITLE_CELL_HEIGHT+self.SPACE_TITLEY

		self.SECOND_TABLE_OFFSX = (self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX)
		if (y+yscrolledoffs > offs and y+yscrolledoffs < offs+self.TABLE_HEIGHT) and ((x+xscrolledoffs > PrimDirsListWnd.BORDER and x+xscrolledoffs < PrimDirsListWnd.BORDER+self.TABLE_WIDTH) or (x+xscrolledoffs > PrimDirsListWnd.BORDER+self.SECOND_TABLE_OFFSX and x+xscrolledoffs < PrimDirsListWnd.BORDER+self.SECOND_TABLE_OFFSX+self.TABLE_WIDTH)):
			col = 0
			rownum = (y+yscrolledoffs-offs)/self.LINE_HEIGHT
			if x+xscrolledoffs > PrimDirsListWnd.BORDER and x+xscrolledoffs < PrimDirsListWnd.BORDER+self.TABLE_WIDTH:
				pass
			else:
				col = 1

			pdnum = (self.currpage-1)*2*self.LINE_NUM+self.LINE_NUM*col+rownum

			return pdnum < len(self.pds.pds), pdnum


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

		#Title
		BOR = PrimDirsListWnd.BORDER
		draw.rectangle(((BOR, BOR),(BOR+self.TITLE_CELL_WIDTH, BOR+self.TITLE_CELL_HEIGHT)), outline=(tableclr), fill=(self.bkgclr))
		dirtxt = mtexts.typeListDirs[self.options.primarydir]
		keytypetxt = mtexts.txts['DynamicKey']
		if not self.options.pdkeydyn:
			keytypetxt = mtexts.txts['StaticKey']
		keytxt = mtexts.typeListDyn[self.options.pdkeyd]
		if not self.options.pdkeydyn:
			keytxt = mtexts.typeListStat[self.options.pdkeys]

		clr = self.options.clrtexts
		if self.bw:
			clr = (0,0,0)
		txt = dirtxt+'   '+keytypetxt+': '+keytxt
		
		bbox = draw.textbbox((0, 0), txt, font=self.fntText)
		w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
		draw.text((BOR+(self.TITLE_CELL_WIDTH-w)//2, BOR+(self.LINE_HEIGHT-h)//2), txt, fill=clr, font=self.fntText)

		txt_page = str(self.currpage)+' / '+str(self.maxpage)
		draw.text((BOR+self.TITLE_CELL_WIDTH-self.TITLE_CELL_WIDTH/10, BOR+(self.LINE_HEIGHT-h)//2), txt_page, fill=clr, font=self.fntText)

		txt_cols = (mtexts.txts['MZ'], mtexts.txts['Prom'], mtexts.txts['DC'], mtexts.txts['Sig'], mtexts.txts['Arc'], mtexts.txts['Date'])
		widths = (self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.BIG_CELL_WIDTH)
		
		summa = 0
		for i in range(self.COLUMN_NUM):
			bbox = draw.textbbox((0, 0), txt_cols[i], font=self.fntText)
			wc, hc = bbox[2]-bbox[0], bbox[3]-bbox[1]
			draw.text((BOR+summa+(widths[i]-wc)//2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-hc)//2), txt_cols[i], fill=clr, font=self.fntText)
			summa += widths[i]
			
		summa = 0
		for i in range(self.COLUMN_NUM):
			bbox = draw.textbbox((0, 0), txt_cols[i], font=self.fntText)
			wc, hc = bbox[2]-bbox[0], bbox[3]-bbox[1]
			draw.text((self.SECOND_TABLE_OFFSX+BOR+summa+(widths[i]-wc)//2, BOR+self.LINE_HEIGHT+(self.LINE_HEIGHT-hc)//2), txt_cols[i], fill=clr, font=self.fntText)
			summa += widths[i]

		#Tables
		x = BOR
		y = BOR+self.TITLE_CELL_HEIGHT+self.SPACE_TITLEY
		draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
		rng = self.to-self.fr
		lim = rng
		leftovers = False
		if lim > self.LINE_NUM:
			lim = self.LINE_NUM
			leftovers = True
		idx = self.fr
		for i in range(lim):
			self.drawline(draw, x, y+i*self.LINE_HEIGHT, idx, tableclr)
			idx += 1
		if leftovers:
			x = BOR+self.TABLE_WIDTH+self.SPACE_BETWEEN_TABLESX
			y = BOR+self.TITLE_CELL_HEIGHT+self.SPACE_TITLEY
			draw.line((x, y, x+self.TABLE_WIDTH, y), fill=tableclr)
			lim = rng-self.LINE_NUM
			idx = self.fr+self.LINE_NUM
			for i in range(lim):
				self.drawline(draw, x, y+i*self.LINE_HEIGHT, idx, tableclr)
				idx += 1

		wxImg = wx.Image(img.size[0], img.size[1])
		wxImg.SetData(img.tobytes())
		self.buffer = wx.Bitmap(wxImg)


	def drawline(self, draw, x, y, idx, clr):
		draw.line((x, y+self.LINE_HEIGHT, x+self.TABLE_WIDTH, y+self.LINE_HEIGHT), fill=clr)
		offs = (0, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.SMALL_CELL_WIDTH, self.CELL_WIDTH, self.CELL_WIDTH, self.BIG_CELL_WIDTH)
		summa = 0
		txtclr = self.options.clrtexts
		if self.bw:
			txtclr = (0,0,0)

		for i in range(self.COLUMN_NUM+1):
			draw.line((x+summa+offs[i], y, x+summa+offs[i], y+self.LINE_HEIGHT), fill=clr)
			
			if i == 1: # M/Z
				mtxt = mtexts.txts['M']
				if not self.pds.pds[idx].mundane:
					mtxt = mtexts.txts['Z']
				bbox = draw.textbbox((0, 0), mtxt, font=self.fntText)
				wm, hm = bbox[2]-bbox[0], bbox[3]-bbox[1]
				draw.text((x+summa+(offs[i]-wm)//2, y+(self.LINE_HEIGHT-hm)//2), mtxt, fill=txtclr, font=self.fntText)

			elif i == 2: # Prom
				if self.pds.pds[idx].promasp == chart.Chart.MIDPOINT or self.pds.pds[idx].sigasp == chart.Chart.RAPTPAR or self.pds.pds[idx].sigasp == chart.Chart.RAPTCONTRAPAR:
					promtxt = common.common.Planets[self.pds.pds[idx].prom]
					prom2txt = common.common.Planets[self.pds.pds[idx].prom2]
					
					bp1 = draw.textbbox((0,0), promtxt, self.fntMorinus)
					wp, hp = bp1[2]-bp1[0], bp1[3]-bp1[1]
					bsp = draw.textbbox((0,0), ' ', self.fntText)
					wsp, hsp = bsp[2]-bsp[0], bsp[3]-bsp[1]
					bp2 = draw.textbbox((0,0), prom2txt, self.fntMorinus)
					wp2, hp2 = bp2[2]-bp2[0], bp2[3]-bp2[1]
					
					offset = (offs[i]-(wp+wsp+wp2))//2
					tclr1 = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].prom
							if objidx > astrology.SE_MEAN_NODE: objidx = astrology.SE_MEAN_NODE
							tclr1 = self.options.clrindividual[objidx]
						else:
							tclr1 = self.clrs[self.chart.dignity(self.pds.pds[idx].prom)]
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)//2), promtxt, fill=tclr1, font=self.fntMorinus)
					
					tclr2 = (0,0,0)
					if not self.bw:
						if self.options.useplanetcolors:
							objidx = self.pds.pds[idx].prom2
							if objidx > astrology.SE_MEAN_NODE: objidx = astrology.SE_MEAN_NODE
							tclr2 = self.options.clrindividual[objidx]
						else:
							tclr2 = self.clrs[self.chart.dignity(self.pds.pds[idx].prom2)]
					draw.text((x+summa+offset+wp+wsp, y+(self.LINE_HEIGHT-hp2)//2), prom2txt, fill=tclr2, font=self.fntMorinus)

				elif self.pds.pds[idx].prom >= primdirs.PrimDir.ANTISCION and self.pds.pds[idx].prom < primdirs.PrimDir.TERM:
					promasptxt = ''
					wspa = 0
					bsp = draw.textbbox((0,0), ' ', self.fntText)
					wsp, hsp = bsp[2]-bsp[0], bsp[3]-bsp[1]
					if self.pds.pds[idx].promasp != chart.Chart.CONJUNCTIO:
						promasptxt = common.common.Aspects[self.pds.pds[idx].promasp]
						wspa = wsp
					ba = draw.textbbox((0,0), promasptxt, self.fntAspects)
					wa, ha = ba[2]-ba[0], ba[3]-ba[1]
					
					anttxt = mtexts.txts['Antis']
					if self.pds.pds[idx].prom >= primdirs.PrimDir.CONTRAANT:
						anttxt = mtexts.txts['ContraAntis']
					bt = draw.textbbox((0,0), anttxt, self.fntText)
					wt, ht = bt[2]-bt[0], bt[3]-bt[1]

					promtxt, promfnt, tclr = '', self.fntMorinus, (0,0,0)
					if self.pds.pds[idx].prom in (primdirs.PrimDir.ANTISCIONLOF, primdirs.PrimDir.CONTRAANTLOF):
						promtxt, promfnt = common.common.fortune, self.fntMorinus
						if not self.bw: tclr = self.options.clrindividual[astrology.SE_MEAN_NODE+1] if self.options.useplanetcolors else self.options.clrperegrin
					elif self.pds.pds[idx].prom in (primdirs.PrimDir.ANTISCIONASC, primdirs.PrimDir.CONTRAANTASC, primdirs.PrimDir.ANTISCIONMC, primdirs.PrimDir.CONTRAANTMC):
						promtxt = mtexts.txts['Asc'] if self.pds.pds[idx].prom in (primdirs.PrimDir.ANTISCIONASC, primdirs.PrimDir.CONTRAANTASC) else mtexts.txts['MC']
						promfnt, tclr = self.fntText, txtclr
					else:
						antoffs = primdirs.PrimDir.ANTISCION if self.pds.pds[idx].prom < primdirs.PrimDir.CONTRAANT else primdirs.PrimDir.CONTRAANT
						promtxt = common.common.Planets[self.pds.pds[idx].prom-antoffs]
						if not self.bw:
							p_idx = self.pds.pds[idx].prom-antoffs
							if self.options.useplanetcolors:
								obj_c = p_idx if p_idx <= astrology.SE_MEAN_NODE else astrology.SE_MEAN_NODE if p_idx == astrology.SE_MEAN_NODE+1 else astrology.SE_MEAN_NODE+1
								tclr = self.options.clrindividual[obj_c]
							else: tclr = self.clrs[self.chart.dignity(p_idx)]
					
					bp = draw.textbbox((0,0), promtxt, promfnt)
					wp, hp = bp[2]-bp[0], bp[3]-bp[1]
					offset = (offs[i]-(wa+wspa+wt+wsp+wp))//2
					if promasptxt != '':
						clrasp = (0,0,0)
						if not self.bw: clrasp = self.options.clrperegrin if self.pds.pds[idx].promasp in (chart.Chart.PARALLEL, chart.Chart.CONTRAPARALLEL) else self.options.clraspect[self.pds.pds[idx].promasp]
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)//2), promasptxt, fill=clrasp, font=self.fntAspects)
					draw.text((x+summa+offset+wa+wspa, y+(self.LINE_HEIGHT-ht)//2), anttxt, fill=txtclr, font=self.fntText)
					draw.text((x+summa+offset+wa+wspa+wt+wsp, y+(self.LINE_HEIGHT-hp)//2), promtxt, fill=tclr, font=promfnt)

				elif self.pds.pds[idx].prom >= primdirs.PrimDir.TERM and self.pds.pds[idx].prom < primdirs.PrimDir.FIXSTAR:
					signs = common.common.Signs1 if self.options.signs else common.common.Signs2
					promtxt = signs[self.pds.pds[idx].prom-primdirs.PrimDir.TERM]
					prom2txt = common.common.Planets[self.pds.pds[idx].prom2]
					bp1 = draw.textbbox((0,0), promtxt, self.fntMorinus)
					wp, hp = bp1[2]-bp1[0], bp1[3]-bp1[1]
					bsp = draw.textbbox((0,0), ' ', self.fntText)
					wsp, hsp = bsp[2]-bsp[0], bsp[3]-bsp[1]
					bp2 = draw.textbbox((0,0), prom2txt, self.fntMorinus)
					wp2, hp2 = bp2[2]-bp2[0], bp2[3]-bp2[1]
					offset = (offs[i]-(wp+wsp+wp2))//2
					sclr = (0,0,0)
					if not self.bw: sclr = self.options.clrsigns
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)//2), promtxt, fill=sclr, font=self.fntMorinus)
					tclr = (0,0,0)
					if not self.bw:
						objidx = self.pds.pds[idx].prom2
						if objidx > astrology.SE_MEAN_NODE: objidx = astrology.SE_MEAN_NODE
						tclr = self.options.clrindividual[objidx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(objidx)]
					draw.text((x+summa+offset+wp+wsp, y+(self.LINE_HEIGHT-hp2)//2), prom2txt, fill=tclr, font=self.fntMorinus)

				elif self.pds.pds[idx].prom >= primdirs.PrimDir.FIXSTAR:
					promtxt = self.chart.fixstars.data[self.pds.pds[idx].prom-primdirs.PrimDir.FIXSTAR][fixstars.FixStars.NOMNAME]
					if self.options.usetradfixstarnamespdlist:
						tradname = self.chart.fixstars.data[self.pds.pds[idx].prom-primdirs.PrimDir.FIXSTAR][fixstars.FixStars.NAME].strip()
						if tradname != '': promtxt = tradname
					bb = draw.textbbox((0,0), promtxt, self.fntText)
					w, h = bb[2]-bb[0], bb[3]-bb[1]
					draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), promtxt, fill=txtclr, font=self.fntText)

				elif self.pds.pds[idx].prom == primdirs.PrimDir.LOF:
					lofclr = (0,0,0)
					if not self.bw: lofclr = self.options.clrindividual[astrology.SE_MEAN_NODE+1] if self.options.useplanetcolors else self.options.clrperegrin
					promtxt = common.common.fortune
					bp = draw.textbbox((0,0), promtxt, self.fntMorinus)
					wp, hp = bp[2]-bp[0], bp[3]-bp[1]
					draw.text((x+summa+(offs[i]-wp)//2, y+(self.LINE_HEIGHT-hp)//2), promtxt, fill=lofclr, font=self.fntMorinus)

				elif self.pds.pds[idx].prom == primdirs.PrimDir.CUSTOMERPD:
					promtxt = mtexts.txts['Customer2']
					bp = draw.textbbox((0,0), promtxt, self.fntText)
					wp, hp = bp[2]-bp[0], bp[3]-bp[1]
					draw.text((x+summa+(offs[i]-wp)//2, y+(self.LINE_HEIGHT-hp)//2), promtxt, fill=txtclr, font=self.fntText)

				elif self.pds.pds[idx].prom in (primdirs.PrimDir.ASC, primdirs.PrimDir.MC):
					promasptxt = common.common.Aspects[self.pds.pds[idx].promasp] if self.pds.pds[idx].promasp != chart.Chart.CONJUNCTIO else ''
					promtxt = mtexts.txts['Asc'] if self.pds.pds[idx].prom == primdirs.PrimDir.ASC else mtexts.txts['MC']
					ba, bs, bsp = draw.textbbox((0,0), promasptxt, self.fntAspects), draw.textbbox((0,0), promtxt, self.fntText), draw.textbbox((0,0), ' ', self.fntText)
					wa, ha, ws, hs, wsp = ba[2]-ba[0], ba[3]-ba[1], bs[2]-bs[0], bs[3]-bs[1], bsp[2]-bsp[0]
					offset = (offs[i]-(wa+wsp+ws))//2
					clrasp = (0,0,0)
					if not self.bw: clrasp = self.options.clrperegrin if self.pds.pds[idx].promasp in (chart.Chart.PARALLEL, chart.Chart.CONTRAPARALLEL) else self.options.clraspect[self.pds.pds[idx].promasp]
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)//2), promasptxt, fill=clrasp, font=self.fntAspects)
					draw.text((x+summa+offset+wa+wsp, y+(self.LINE_HEIGHT-hs)//2), promtxt, fill=txtclr, font=self.fntText)

				elif primdirs.PrimDir.HC2 <= self.pds.pds[idx].prom < primdirs.PrimDir.LOF:
					HCs = (mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC11'], mtexts.txts['HC12'])
					hctxt = HCs[self.pds.pds[idx].sig-primdirs.PrimDir.HC2]
					bs = draw.textbbox((0,0), hctxt, self.fntText)
					ws, hs = bs[2]-bs[0], bs[3]-bs[1]
					draw.text((x+summa+(offs[i]-ws)//2, y+(self.LINE_HEIGHT-hs)//2), hctxt, fill=txtclr, font=self.fntText)

				else:
					promtxt = common.common.Planets[self.pds.pds[idx].prom]
					promasptxt = common.common.Aspects[self.pds.pds[idx].promasp] if self.pds.pds[idx].promasp != chart.Chart.CONJUNCTIO else ''
					bp, ba, bsp = draw.textbbox((0,0), promtxt, self.fntMorinus), draw.textbbox((0,0), promasptxt, self.fntAspects), draw.textbbox((0,0), ' ', self.fntText)
					wp, hp, wa, ha, wsp = bp[2]-bp[0], bp[3]-bp[1], ba[2]-ba[0], ba[3]-ba[1], bsp[2]-bsp[0]
					wspa = wsp if promasptxt != '' else 0
					offset = (offs[i]-(wa+wspa+wp))//2
					if promasptxt != '':
						clrasp = (0,0,0)
						if not self.bw: clrasp = self.options.clrperegrin if self.pds.pds[idx].promasp in (chart.Chart.PARALLEL, chart.Chart.CONTRAPARALLEL) else self.options.clraspect[self.pds.pds[idx].promasp]
						draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)//2), promasptxt, fill=clrasp, font=self.fntAspects)
					tclr = (0,0,0)
					if not self.bw:
						objidx = self.pds.pds[idx].prom
						if objidx > astrology.SE_MEAN_NODE: objidx = astrology.SE_MEAN_NODE
						tclr = self.options.clrindividual[objidx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(objidx)]
					draw.text((x+summa+offset+wa+wspa, y+(self.LINE_HEIGHT-hp)//2), promtxt, fill=tclr, font=self.fntMorinus)

			elif i == 3: # D/C
				dirtxt = mtexts.txts['D'] if self.pds.pds[idx].direct else mtexts.txts['C']
				bb1, bsp, bb2 = draw.textbbox((0,0), dirtxt, self.fntText), draw.textbbox((0,0), ' ', self.fntText), draw.textbbox((0,0), '-', self.fntSymbol)
				w1, h1, wsp, w2, h2 = bb1[2]-bb1[0], bb1[3]-bb1[1], bsp[2]-bsp[0], bb2[2]-bb2[0], bb2[3]-bb2[1]
				offset = (offs[i]-(w1+wsp+w2))//2
				draw.text((x+summa+offset, y+(self.LINE_HEIGHT-h1)//2), dirtxt, fill=txtclr, font=self.fntText)
				draw.text((x+summa+offset+w1+wsp, y+(self.LINE_HEIGHT-h2)//2), '-', fill=txtclr, font=self.fntSymbol)

			elif i == 4: # Sig
				if self.pds.pds[idx].sigasp in (chart.Chart.PARALLEL, chart.Chart.CONTRAPARALLEL):
					partxt = 'X' if not (self.pds.pds[idx].parallelaxis == 0 and self.pds.pds[idx].sigasp == chart.Chart.CONTRAPARALLEL) else 'Y'
					sigtxt = common.common.Planets[self.pds.pds[idx].sig]
					angletxt = ('('+mtexts.txts['Asc']+')', '('+mtexts.txts['Dsc']+')', '('+mtexts.txts['MC']+')', '('+mtexts.txts['IC']+')')[self.pds.pds[idx].parallelaxis-primdirs.PrimDir.OFFSANGLES] if self.pds.pds[idx].parallelaxis != 0 else ''
					bp, bs, ba, bsp = draw.textbbox((0,0), partxt, self.fntAspects), draw.textbbox((0,0), sigtxt, self.fntMorinus), draw.textbbox((0,0), angletxt, self.fntText), draw.textbbox((0,0), ' ', self.fntText)
					wp, hp, ws, hs, wa, ha, wsp = bp[2]-bp[0], bp[3]-bp[1], bs[2]-bs[0], bs[3]-bs[1], ba[2]-ba[0], ba[3]-ba[1], bsp[2]-bsp[0]
					offset = (offs[i]-(wp+wsp+ws+wsp+wa))//2
					pclr = (0,0,0) if self.bw else self.options.clrperegrin
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hp)//2), partxt, fill=pclr, font=self.fntAspects)
					tclr = (0,0,0)
					if not self.bw:
						oidx = self.pds.pds[idx].sig
						if oidx > astrology.SE_MEAN_NODE: oidx = astrology.SE_MEAN_NODE
						tclr = self.options.clrindividual[oidx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(oidx)]
					draw.text((x+summa+offset+wp+wsp, y+(self.LINE_HEIGHT-hs)//2), sigtxt, fill=tclr, font=self.fntMorinus)
					draw.text((x+summa+offset+wp+wsp+ws+wsp, y+(self.LINE_HEIGHT-ha)//2), angletxt, fill=txtclr, font=self.fntText)

				elif self.pds.pds[idx].sigasp in (chart.Chart.RAPTPAR, chart.Chart.RAPTCONTRAPAR):
					rapttxt, partxt = 'R', 'X'
					angletxt = ('('+mtexts.txts['Asc']+')', '('+mtexts.txts['Dsc']+')', '('+mtexts.txts['MC']+')', '('+mtexts.txts['IC']+')')[self.pds.pds[idx].parallelaxis-primdirs.PrimDir.OFFSANGLES]
					br, bp, ba, bsp = draw.textbbox((0,0), rapttxt, self.fntText), draw.textbbox((0,0), partxt, self.fntAspects), draw.textbbox((0,0), angletxt, self.fntText), draw.textbbox((0,0), ' ', self.fntText)
					wr, hr, wp, hp, wa, ha, wsp = br[2]-br[0], br[3]-br[1], bp[2]-bp[0], bp[3]-bp[1], ba[2]-ba[0], ba[3]-ba[1], bsp[2]-bsp[0]
					offset = (offs[i]-(wr+wp+wsp+wsp+wa))//2
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-hr)//2), rapttxt, fill=txtclr, font=self.fntText)
					pclr = (0,0,0) if self.bw else self.options.clrperegrin
					draw.text((x+summa+offset+wr, y+(self.LINE_HEIGHT-hp)//2), partxt, fill=pclr, font=self.fntAspects)
					draw.text((x+summa+offset+wr+wp+wsp, y+(self.LINE_HEIGHT-ha)//2), angletxt, fill=txtclr, font=self.fntText)

				elif self.pds.pds[idx].sig == primdirs.PrimDir.LOF:
					sigtxt = common.common.fortune
					bp = draw.textbbox((0,0), sigtxt, self.fntMorinus)
					wp, hp, extra = bp[2]-bp[0], bp[3]-bp[1], 0
					if self.pds.pds[idx].mundane:
						sigasptxt = common.common.Aspects[self.pds.pds[idx].sigasp]
						ba, bsp = draw.textbbox((0,0), sigasptxt, self.fntAspects), draw.textbbox((0,0), ' ', self.fntText)
						wa, ha, wsp = ba[2]-ba[0], ba[3]-ba[1], bsp[2]-bsp[0]
						extra = wa+wsp
						clrasp = (0,0,0) if self.bw else self.options.clraspect[self.pds.pds[idx].sigasp]
						draw.text((x+summa+(offs[i]-(wp+extra))//2, y+(self.LINE_HEIGHT-ha)//2), sigasptxt, fill=clrasp, font=self.fntAspects)
					lofclr = (0,0,0)
					if not self.bw: lofclr = self.options.clrindividual[astrology.SE_MEAN_NODE+1] if self.options.useplanetcolors else self.options.clrperegrin
					draw.text((x+summa+(offs[i]-(wp+extra))//2+extra, y+(self.LINE_HEIGHT-hp)//2), sigtxt, fill=lofclr, font=self.fntMorinus)

				elif self.pds.pds[idx].sig == primdirs.PrimDir.SYZ:
					sigtxt = mtexts.txts['Syzygy']
					bb = draw.textbbox((0,0), sigtxt, self.fntText)
					w, h = bb[2]-bb[0], bb[3]-bb[1]
					draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), sigtxt, fill=txtclr, font=self.fntText)

				elif self.pds.pds[idx].sig == primdirs.PrimDir.CUSTOMERPD:
					sigtxt = mtexts.txts['User2']
					bb = draw.textbbox((0,0), sigtxt, self.fntText)
					w, h = bb[2]-bb[0], bb[3]-bb[1]
					draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), sigtxt, fill=txtclr, font=self.fntText)

				elif primdirs.PrimDir.OFFSANGLES <= self.pds.pds[idx].sig < primdirs.PrimDir.LOF:
					if self.pds.pds[idx].sig <= primdirs.PrimDir.IC:
						txt_a = (mtexts.txts['Asc'], mtexts.txts['Dsc'], mtexts.txts['MC'], mtexts.txts['IC'])[self.pds.pds[idx].sig-primdirs.PrimDir.OFFSANGLES]
						bb = draw.textbbox((0,0), txt_a, self.fntText)
						w, h = bb[2]-bb[0], bb[3]-bb[1]
						draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt_a, fill=txtclr, font=self.fntText)
					else:
						txt_h = (mtexts.txts['HC2'], mtexts.txts['HC3'], mtexts.txts['HC5'], mtexts.txts['HC6'], mtexts.txts['HC8'], mtexts.txts['HC9'], mtexts.txts['HC11'], mtexts.txts['HC12'])[self.pds.pds[idx].sig-primdirs.PrimDir.HC2]
						bb = draw.textbbox((0,0), txt_h, self.fntText)
						w, h = bb[2]-bb[0], bb[3]-bb[1]
						draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt_h, fill=txtclr, font=self.fntText)

				else:
					sigasptxt = common.common.Aspects[self.pds.pds[idx].sigasp] if self.pds.pds[idx].sigasp != chart.Chart.CONJUNCTIO else ''
					sigtxt = common.common.Planets[self.pds.pds[idx].sig]
					ba, bs, bsp = draw.textbbox((0,0), sigasptxt, self.fntAspects), draw.textbbox((0,0), sigtxt, self.fntMorinus), draw.textbbox((0,0), ' ', self.fntText)
					wa, ha, ws, hs, wsp = ba[2]-ba[0], ba[3]-ba[1], bs[2]-bs[0], bs[3]-bs[1], bsp[2]-bsp[0]
					wspa = wsp if sigasptxt != '' else 0
					offset = (offs[i]-(wa+wspa+ws))//2
					clrasp = (0,0,0) if self.bw else self.options.clraspect[self.pds.pds[idx].sigasp]
					draw.text((x+summa+offset, y+(self.LINE_HEIGHT-ha)//2), sigasptxt, fill=clrasp, font=self.fntAspects)
					tclr = (0,0,0)
					if not self.bw:
						oidx = self.pds.pds[idx].sig
						if oidx > astrology.SE_MEAN_NODE: oidx = astrology.SE_MEAN_NODE
						tclr = self.options.clrindividual[oidx] if self.options.useplanetcolors else self.clrs[self.chart.dignity(oidx)]
					draw.text((x+summa+offset+wa+wspa, y+(self.LINE_HEIGHT-hs)//2), sigtxt, fill=tclr, font=self.fntMorinus)

			elif i == 5: # Arc
				arctxt = str((int(self.pds.pds[idx].arc*1000))/1000.0)
				bb = draw.textbbox((0,0), arctxt, self.fntText)
				w, h = bb[2]-bb[0], bb[3]-bb[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), arctxt, fill=txtclr, font=self.fntText)

			elif i == 6: # Date
				year, month, day, h_rev = astrology.swe_revjul(self.pds.pds[idx].time, 1)
				txt_d = str(year).rjust(4)+'.'+str(month).zfill(2)+'.'+str(day).zfill(2)
				bb = draw.textbbox((0,0), txt_d, self.fntText)
				w, h = bb[2]-bb[0], bb[3]-bb[1]
				draw.text((x+summa+(offs[i]-w)//2, y+(self.LINE_HEIGHT-h)//2), txt_d, fill=txtclr, font=self.fntText)

			summa += offs[i]




 
