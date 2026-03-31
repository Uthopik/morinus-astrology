import wx
import os
import astrology
import houses
import planets
import chart
import fortune
import common
import commonwnd
from PIL import Image, ImageDraw, ImageFont
#from PIL import Image, ImageDraw, ImageFont
import util
import mtexts


class SquareChart:
    SMALL_SIZE = 400
    MEDIUM_SIZE = 600

    def __init__(self, chrt, size, opts, bw):
        self.chart = chrt
        self.options = opts
        self.w, self.h = size
        self.bw = bw
        self.buffer = wx.Bitmap(self.w, self.h)
        # self.bdc = wx.BufferedDC(None, self.buffer) # En versiones modernas se prefiere:
        self.bdc = wx.MemoryDC(self.buffer)
        
        self.chartsize = min(self.w, self.h)
        self.maxradius = int(self.chartsize/2)
        self.center = wx.Point(int(self.w/2), int(self.h/2))

        self.symbolSize = int(self.maxradius/16)
        self.smallSize = int(self.maxradius/18)
        self.fontSize = self.symbolSize
        
        # Corrección de carga de fuentes (asegurando que common.common.symbols sea un path válido)
        self.fntMorinus = ImageFont.truetype(common.common.symbols, int(self.symbolSize+1))
        self.fntMorinusSmall = ImageFont.truetype(common.common.symbols, int(self.smallSize+1))
        self.fntText = ImageFont.truetype(common.common.abc, int(self.fontSize+1))
        self.fntTextSmall = ImageFont.truetype(common.common.abc, int(1+3*self.fontSize/4))
        self.fntTextSmaller = ImageFont.truetype(common.common.abc, int(1+self.fontSize/2))
        
        self.signs = common.common.Signs1
        if not self.options.signs:
            self.signs = common.common.Signs2
        self.deg_symbol = u'\u00b0'

        self.SPACE = int(self.fontSize/5)
        self.LINE_HEIGHT = (self.SPACE+self.fontSize+self.SPACE)

        self.clrs = (self.options.clrdomicil, self.options.clrexal, self.options.clrperegrin, self.options.clrcasus, self.options.clrexil)
        self.hsystem = {'P':mtexts.txts['HSPlacidus'], 'K':mtexts.txts['HSKoch'], 'R':mtexts.txts['HSRegiomontanus'], 'C':mtexts.txts['HSCampanus'], 'E':mtexts.txts['HSEqual'], 'W':mtexts.txts['HSWholeSign'], 'X':mtexts.txts['HSAxial'], 'M':mtexts.txts['HSMorinus'], 'H':mtexts.txts['HSHorizontal'], 'T':mtexts.txts['HSPagePolich'], 'B':mtexts.txts['HSAlcabitus'], 'O':mtexts.txts['HSPorphyrius']}

    def drawChart(self):
        frameclr = (0,0,0)
        bkgclr = (255,255,255)
        posclr = (0,0,0)
        txtclr = (0,0,0)
        signsclr = (0,0,0)
        
        if not self.bw:
            bkgclr = self.options.clrbackground
            frameclr = self.options.clrframe
            posclr = self.options.clrpositions
            txtclr = self.options.clrtexts
            signsclr = self.options.clrsigns

        # Preparar fondo
        self.bdc.SetBackground(wx.Brush(bkgclr))
        self.bdc.SetBrush(wx.Brush(bkgclr))
        self.bdc.Clear()

        (cx, cy) = self.center.Get()
        radius = int(self.maxradius * 0.90)

        # --- DIBUJO DE LÍNEAS (Estructura Medieval) ---
        w_line = 4
        if self.chartsize <= SquareChart.SMALL_SIZE: w_line = 2
        elif self.chartsize <= SquareChart.MEDIUM_SIZE: w_line = 3

        pen = wx.Pen(frameclr, w_line)
        self.bdc.SetPen(pen)
        
        # 1. Cuadrado Exterior
        self.bdc.DrawRectangle(int(cx-radius), int(cy-radius), int(2*radius), int(2*radius))

        # Líneas internas más finas
        self.bdc.SetPen(wx.Pen(frameclr, max(1, w_line-1)))

        # 2. Rombo (Diagonales que conectan los puntos medios)
        self.bdc.DrawLine(int(cx), int(cy-radius), int(cx-radius), int(cy))
        self.bdc.DrawLine(int(cx-radius), int(cy), int(cx), int(cy+radius))
        self.bdc.DrawLine(int(cx), int(cy+radius), int(cx+radius), int(cy))
        self.bdc.DrawLine(int(cx+radius), int(cy), int(cx), int(cy-radius))

        # 3. Líneas de las esquinas hacia el centro
        self.bdc.DrawLine(int(cx-radius), int(cy-radius), int(cx-radius//2), int(cy-radius//2))
        self.bdc.DrawLine(int(cx-radius), int(cy+radius), int(cx-radius//2), int(cy+radius//2))
        self.bdc.DrawLine(int(cx+radius), int(cy+radius), int(cx+radius//2), int(cy+radius//2))
        self.bdc.DrawLine(int(cx+radius), int(cy-radius), int(cx+radius//2), int(cy-radius//2))
        
        # 4. Cuadrado Interior
        self.bdc.DrawRectangle(int(cx-radius//2), int(cy-radius//2), int(radius + 1), int(radius + 1))

        # --- FINALIZAR DIBUJO WX Y PASAR A PIL ---
        del self.bdc # Obligatorio en Linux para volcar el dibujo al bitmap

        wxImag = self.buffer.ConvertToImage()
        img = Image.new('RGB', (wxImag.GetWidth(), wxImag.GetHeight()))
        img.frombytes(bytes(wxImag.GetData()))
        draw = ImageDraw.Draw(img)

        # --- TEXTOS CENTRALES CORREGIDOS ---
        # Anclamos el texto al cuadrado interior: margen izquierdo y superior
        tx = int(cx - radius//2 + self.SPACE * 2)
        ty = int(cy - radius//2 + self.SPACE * 2)

        # Ajuste si hay horas planetarias para que no se salga por abajo
        if self.chart.time.ph != None:
            ty = int(cy - radius//2 + self.SPACE)

        datetxt = f"{self.chart.time.origyear}.{common.common.months[self.chart.time.origmonth-1]}.{str(self.chart.time.origday).zfill(2)}"
        if self.chart.time.cal == chart.Time.JULIAN:
            datetxt += ' ' + mtexts.txts['J']

        zonetxts = (mtexts.txts['ZN'], mtexts.txts['UT'], mtexts.txts['LC'], mtexts.txts['LC'])
        timetxt = f"{str(self.chart.time.hour).zfill(2)}:{str(self.chart.time.minute).zfill(2)}:{str(self.chart.time.second).zfill(2)} {zonetxts[self.chart.time.zt]}"
        placetxt = self.chart.place.place
        coordtxt = f"{str(self.chart.place.deglon).zfill(2)}{self.deg_symbol}{str(self.chart.place.minlon).zfill(2)}'{(mtexts.txts['E'] if self.chart.place.east else mtexts.txts['W'])}  {str(self.chart.place.deglat).zfill(2)}{self.deg_symbol}{str(self.chart.place.minlat).zfill(2)}'{(mtexts.txts['N'] if self.chart.place.north else mtexts.txts['S'])}"

        draw.text((tx, ty), datetxt, fill=txtclr, font=self.fntText)
        draw.text((tx, ty + self.LINE_HEIGHT), timetxt, fill=txtclr, font=self.fntText)
        draw.text((tx, ty + 2*self.LINE_HEIGHT), placetxt, fill=txtclr, font=self.fntText)
        draw.text((tx, ty + 3*self.LINE_HEIGHT), coordtxt, fill=txtclr, font=self.fntText)
        draw.text((tx, ty + 4*self.LINE_HEIGHT), self.chart.name, fill=txtclr, font=self.fntText)
        draw.text((tx, ty + 5*self.LINE_HEIGHT), mtexts.typeList[self.chart.htype], fill=txtclr, font=self.fntText)
        draw.text((tx, ty + 6*self.LINE_HEIGHT), self.hsystem[self.options.hsys], fill=txtclr, font=self.fntText)

        if self.chart.time.ph != None:
            ar_planets = (1, 4, 2, 5, 3, 6, 0)
            day_planet = common.common.Planets[ar_planets[self.chart.time.ph.weekday]]
            draw.text((tx, ty + 7*self.LINE_HEIGHT), day_planet, fill=txtclr, font=self.fntMorinus)
            bbox_sym = draw.textbbox((0, 0), day_planet, font=self.fntMorinus)
            draw.text((tx + (bbox_sym[2]-bbox_sym[0]) + 5, ty + 7*self.LINE_HEIGHT), mtexts.txts['Day'], fill=txtclr, font=self.fntText)
            
            hour_planet = common.common.Planets[self.chart.time.ph.planetaryhour]
            draw.text((tx, ty + 8*self.LINE_HEIGHT), hour_planet, fill=txtclr, font=self.fntMorinus)
            bbox_sym2 = draw.textbbox((0, 0), hour_planet, font=self.fntMorinus)
            draw.text((tx + (bbox_sym2[2]-bbox_sym2[0]) + 5, ty + 8*self.LINE_HEIGHT), mtexts.txts['Hour'], fill=txtclr, font=self.fntText)

        # --- CÁLCULO DE CASAS Y PLANETAS ---
        ar = (((cx-3*radius//4-3*self.fontSize//2, cy-radius//3+self.fontSize), (cx-3*radius//4-self.fontSize//2, cy-radius//3), (cx-3*radius//4+self.fontSize//2, cy-radius//3-self.fontSize//2)), ((cx-3*radius//4-self.fontSize, cy+radius//3-3*self.fontSize), (cx-3*radius//4, cy+radius//3-2*self.fontSize-self.fontSize//4), (cx-3*radius//4+self.fontSize, cy+radius//3-self.fontSize)), ((cx-3*radius//4-5*self.fontSize//2, cy+3*radius//4+4*self.fontSize//5), (cx-3*radius//4-3*self.fontSize//2, cy+3*radius//4-self.fontSize//5), (cx-3*radius//4-self.fontSize//2, cy+3*radius//4-4*self.fontSize//5)), ((cx-radius//4-2*self.fontSize, cy+3*radius//4-self.fontSize), (cx-radius//4-self.fontSize, cy+3*radius//4-self.fontSize//4), (cx-radius//4, cy+3*radius//4+self.fontSize)), ((cx+radius//4-5*self.fontSize//2, cy+3*radius//4+4*self.fontSize//5), (cx+radius//4-3*self.fontSize//2, cy+3*radius//4-self.fontSize//5), (cx+radius//4-self.fontSize//2, cy+3*radius//4-4*self.fontSize//5)), ((cx+3*radius//4-2*self.fontSize, cy+3*radius//4-self.fontSize), (cx+3*radius//4-self.fontSize, cy+3*radius//4-self.fontSize//4), (cx+3*radius//4, cy+3*radius//4+self.fontSize)), ((cx+3*radius//4-3*self.fontSize//4, cy+radius//3-self.fontSize//2), (cx+3*radius//4+self.fontSize//4, cy+radius//3-3*self.fontSize//2), (cx+3*radius//4+5*self.fontSize//4, cy+radius//3-9*self.fontSize//4)), ((cx+3*radius//4-3*self.fontSize//2, cy-radius//3+self.fontSize), (cx+3*radius//4-self.fontSize//4, cy-radius//3+7*self.fontSize//4), (cx+3*radius//4+3*self.fontSize//4, cy-radius//3+11*self.fontSize//4)), ((cx+3*radius//4-self.fontSize, cy-3*radius//4+self.fontSize), (cx+3*radius//4, cy-3*radius//4), (cx+3*radius//4+self.fontSize, cy-3*radius//4-3*self.fontSize//4)), ((cx+radius//4-self.fontSize//4, cy-3*radius//4-self.fontSize), (cx+radius//4+3*self.fontSize//4, cy-3*radius//4-self.fontSize//4), (cx+radius//4+7*self.fontSize//4, cy-3*radius//4+self.fontSize)), ((cx-radius//4-self.fontSize, cy-3*radius//4+self.fontSize), (cx-radius//4, cy-3*radius//4), (cx-radius//4+self.fontSize, cy-3*radius//4-3*self.fontSize//4)), ((cx-3*radius//4, cy-3*radius//4-self.fontSize), (cx-3*radius//4+self.fontSize, cy-3*radius//4), (cx-3*radius//4+2*self.fontSize, cy-3*radius//4+5*self.fontSize//4)))
        arpl = ((cx-3*radius//4-3*self.fontSize//4, cy-self.fontSize//2), (cx-radius+self.fontSize//2, cy+radius//2-self.fontSize//2), (cx-3*radius//4+self.fontSize, cy+3*radius//4+self.fontSize), (cx-radius//5+self.fontSize, cy+radius//2+2*self.fontSize), (cx+radius//2-5*self.fontSize//2, cy+3*radius//4+self.fontSize), (cx+2*radius//3+self.fontSize//2, cy+radius//2-self.fontSize//2), (cx+radius//2+self.fontSize//2, cy-self.fontSize//2), (cx+2*radius//3+self.fontSize//2, cy-radius//2-self.fontSize//2), (cx+radius//2-2*self.fontSize, cy-radius+2*self.fontSize), (cx-radius//6+self.fontSize, cy-3*radius//4+self.fontSize//2), (cx-3*radius//4+2*self.fontSize, cy-radius+2*self.fontSize), (cx-radius+self.fontSize//2, cy-radius//2-self.fontSize//2))

        lh = int(self.fontSize)
        lhoffs = [0.0] * 12

        for i in range(12):
            lon = self.chart.houses.cusps[i+1]
            if self.options.ayanamsha != 0 and self.options.hsys != 'W':
                lon = util.normalize(lon - self.chart.ayanamsha)

            d, m, s = util.decToDeg(lon)
            sign = int(d // 30)
            pos = int(d % 30)

            draw.text((int(ar[i][0][0]), int(ar[i][0][1])), str(pos).rjust(2) + self.deg_symbol, fill=posclr, font=self.fntTextSmall)
            draw.text((int(ar[i][1][0]), int(ar[i][1][1])), self.signs[sign], fill=signsclr, font=self.fntMorinusSmall)
            draw.text((int(ar[i][2][0]), int(ar[i][2][1])), str(m).zfill(2) + "'", fill=posclr, font=self.fntTextSmaller)

            order, mixed = self.getPlanetsInHouse(i)
            num = len(order)
            if num > 1: lhoffs[i] -= (lh * (num - 1)) // 2

            for j in range(num):
                idxpl = mixed[j]
                lon_p = order[j]
                if self.options.ayanamsha != 0: lon_p = util.normalize(lon_p - self.chart.ayanamsha)
                dp, mp, sp = util.decToDeg(lon_p)
                px, py = arpl[i][0], arpl[i][1]
                
                pl_sym = common.common.Planets[idxpl] if idxpl < planets.Planets.PLANETS_NUM else common.common.fortune
                
                clrpl = (0,0,0)
                if not self.bw:
                    if self.options.useplanetcolors:
                        objidx = idxpl
                        if objidx == planets.Planets.PLANETS_NUM-1: objidx = astrology.SE_MEAN_NODE
                        elif objidx > planets.Planets.PLANETS_NUM-1: objidx = astrology.SE_MEAN_NODE+1
                        clrpl = self.options.clrindividual[objidx]
                    else:
                        if idxpl < planets.Planets.PLANETS_NUM:
                            clrpl = self.clrs[self.chart.dignity(idxpl)]
                        else: clrpl = self.options.clrperegrin

                draw.text((px, py+lhoffs[i]), pl_sym, fill=clrpl, font=self.fntMorinusSmall)
                
                bbox_pl = draw.textbbox((0, 0), pl_sym, font=self.fntMorinusSmall)
                wpl = bbox_pl[2]-bbox_pl[0]
                
                sign_p = int(dp // 30)
                pos_p = int(dp % 30)
                txtdeg = str(pos_p).zfill(2) + self.deg_symbol
                
                draw.text((px+wpl+5, py+lhoffs[i]), txtdeg, fill=clrpl, font=self.fntTextSmall)
                lhoffs[i] += lh

        wxImg = wx.Image(img.size[0], img.size[1])
        wxImg.SetData(img.tobytes())
        self.buffer = wx.Bitmap(wxImg)
        return self.buffer

    def getPlanetsInHouse(self, hnum):
        inhouse, mixed = [], []
        for i in range (planets.Planets.PLANETS_NUM+1):
            if i in (astrology.SE_URANUS, astrology.SE_NEPTUNE, astrology.SE_PLUTO): continue
            lon = self.chart.planets.planets[i].data[planets.Planet.LONG] if i < planets.Planets.PLANETS_NUM else self.chart.fortune.fortune[fortune.Fortune.LON]
            if self.options.ayanamsha != 0 and self.options.hsys == 'W':
                lon = util.normalize(lon - self.chart.ayanamsha)
            if self.chart.houses.getHousePos(lon, self.options) == hnum:
                inhouse.append(lon)
                mixed.append(i)
        
        # Ordenar planetas por longitud dentro de la casa
        for j in range(len(inhouse)):
            for i in range(len(inhouse)-1):
                if inhouse[i] > inhouse[i+1]:
                    inhouse[i], inhouse[i+1] = inhouse[i+1], inhouse[i]
                    mixed[i], mixed[i+1] = mixed[i+1], mixed[i]
        
        if 5 <= hnum <= 10:
            inhouse.reverse(); mixed.reverse()
        return tuple(inhouse), tuple(mixed)
		




