import math
import astrology
import sweastrology
# Forzamos que, dentro de ESTE archivo, use tus funciones adaptadas
astrology.swe_houses_ex = sweastrology.swe_houses_ex_adaptado
astrology.swe_calc = sweastrology.swe_calc_adaptado
import chart
import util


class Houses:
	"""Calculates the cusps of the Houses"""

	HOUSE_NUM = 12
	hsystems = ('P', 'K', 'R', 'C', 'E', 'W', 'X', 'M', 'H', 'T', 'B', 'O')

	ASC, MC, ARMC, VERTEX, EQUASC, COASC, COASC2, POLARASC = range(0, 8)

	LON = 0
	LAT = 1
	RA = 2
	DECL = 3

	def __init__(self, tjd_ut, flag, geolat, geolon, hsys, obl, ayanopt, ayan):
		# 1. Sistema de casas
		self.hsys = hsys if hsys in Houses.hsystems else Houses.hsystems[0]

		# 2. SEGURIDAD DE ECLÍPTICA: Si es 0 o menor a 1, usamos 23.44
		try:
			val_obl = float(obl)
			if val_obl < 1.0:
				self.obl = 23.445  # Valor estándar J2000 aprox.
			else:
				self.obl = val_obl
		except:
			self.obl = 23.445

		# 3. LLAMADA A LA LIBRERÍA
		# Forzamos los tipos para que Swisseph no se confunda
		res = astrology.swe_houses_ex(float(tjd_ut), int(flag), float(geolat), float(geolon), ord(self.hsys))

		# --- EL CHIVATO ---
		#print("\n" + "="*50)
		#print(f"OBLICUIDAD USADA: {self.obl}")
		#print(f"RESULTADO SWISSEPH: {res[1][0:3]}...") 
		#print("="*50 + "\n")

		# 4. ASIGNACIÓN CORREGIDA
		# res[0] son las Cúspides (13 elementos)
		# res[1] son los Ángulos Asc/MC
		self.cusps = list(res[0]) 
		self.ascmc = list(res[1])

		# 5. CÁLCULO DE COORDENADAS (Asc/MC)
		# El Ascendente es el índice 0 de la lista ascmc
		# El MC es el índice 1 de la lista ascmc
		asc_deg = float(self.ascmc[0])
		mc_deg = float(self.ascmc[1])

		# Aquí usamos la oblicuidad que hemos validado arriba
		ascra, ascdecl, dist_a = astrology.swe_cotrans(asc_deg, 0.0, 1.0, -self.obl)				
		mcra, mcdecl, dist_m = astrology.swe_cotrans(mc_deg, 0.0, 1.0, -self.obl)
		self.ascmc2 = ((asc_deg, 0.0, ascra, ascdecl), (mc_deg, 0.0, mcra, mcdecl))

		# 6. GENERACIÓN DE CÚSPIDES PARA EL GRÁFICO
		self.cuspstmp = []
		# En houses.py, justo antes del bucle for i in range(1, 13):
		#print(f"DEBUG FINAL: self.cusps tiene {len(self.cusps)} casas.")
		for i in range(1, 13):
			# Usamos de nuevo nuestra obl validada
			lon_c, lat_c, d_c = astrology.swe_cotrans(float(self.cusps[i]), 0.0, 1.0, -self.obl)
			self.cuspstmp.append([lon_c, lat_c])
		
		self.cusps2 = tuple((c[0], c[1]) for c in self.cuspstmp)


	#Zodiacal
	def getHousePos(self, lon, opts, useorbs = False):
		for i in range(1, Houses.HOUSE_NUM):
			orb1 = 0.0
			orb2 = 0.0

			if useorbs:
				orb1 = opts.orbiscuspH
				orb2 = opts.orbiscuspH
				if i == 1 or i == 4 or i == 7 or i == 10:
					orb1 = opts.orbiscuspAscMC
				if i+1 == 4 or i+1 == 7 or i+1 == 10:
					orb2 = opts.orbiscuspAscMC

			cusp1 = util.normalize(self.cusps[i]-orb1)
			cusp2 = util.normalize(self.cusps[i+1]-orb2)

			pos = lon
			if cusp1 > 240.0 and cusp2 < 120.0: #Pisces-Aries check
				if pos > 240.0:#planet is in the Pisces-part
					cusp2 += 360.0
				else:
					cusp2 += 360.0
					pos += 360.0
					
			if cusp1 < pos and cusp2 > pos:
				if opts.traditionalaspects:
					pos = lon
					cusp1 = self.cusps[i]
					cusp2 = self.cusps[i+1]
					if cusp1 > 240.0 and cusp1 < 120.0: #Pisces-Aries check
						if pos > 240.0:#planet is in the Pisces-part
							cusp2 += 360.0
						else:
							cusp2 += 360.0
							pos += 360.0

					if cusp1 > pos:
						sign1 = int(lon/chart.Chart.SIGN_DEG)
						sign2 = int(self.cusps[i]/chart.Chart.SIGN_DEG)
						if sign1 != sign2:
							if i == 1:
								return 11
							else:
								return i-2

				return i-1

		#12-I
		orb1 = 0.0
		orb2 = 0.0

		if useorbs:
			orb1 = opts.orbiscuspH
			orb2 = opts.orbiscuspAscMC		

		cusp1 = util.normalize(self.cusps[12]-orb1)
		cusp2 = util.normalize(self.cusps[1]-orb2)

		pos = lon
		if cusp1 > 240.0 and cusp2 < 120.0: #Pisces-Aries check
			if pos > 240.0:#planet is in the Pisces-part
				cusp2 += 360.0
			else:
				cusp2 += 360.0
				pos += 360.0
					
		if cusp1 < pos and cusp2 > pos:
			if opts.traditionalaspects:
				pos = lon
				cusp1 = self.cusps[i]
				cusp2 = self.cusps[i+1]
				if cusp1 > 240.0 and cusp1 < 120.0: #Pisces-Aries check
					if pos > 240.0:#planet is in the Pisces-part
						cusp2 += 360.0
					else:
						cusp2 += 360.0
						pos += 360.0

				if cusp1 > pos:
					sign1 = int(lon/chart.Chart.SIGN_DEG)
					sign2 = int(self.cusps[i]/chart.Chart.SIGN_DEG)
					if sign1 != sign2:
						if i == 1:
							return 11
						else:
							return i-2

			return 11

		return 0


	def calcProfPos(self, prof):
		hcs = [self.cusps[0]]
		for i in range(1, Houses.HOUSE_NUM+1):
			hcs.append(util.normalize(self.cusps[i]+prof.offs))

		#to tuple (which is a read-only list)
		self.cusps = tuple(hcs)

		self.ascmc = (util.normalize(self.ascmc[Houses.ASC]+prof.offs), util.normalize(self.ascmc[Houses.MC]+prof.offs), self.ascmc[Houses.ARMC], self.ascmc[Houses.VERTEX], self.ascmc[Houses.EQUASC], self.ascmc[Houses.COASC], self.ascmc[Houses.COASC2], self.ascmc[Houses.POLARASC])

		ascra, ascdecl, dist = astrology.swe_cotrans(self.ascmc[Houses.ASC], 0.0, 1.0, -self.obl)
		mcra, mcdecl, dist = astrology.swe_cotrans(self.ascmc[Houses.MC], 0.0, 1.0, -self.obl)

		self.ascmc2 = ((self.ascmc[Houses.ASC], 0.0, ascra, ascdecl), (self.ascmc[Houses.MC], 0.0, mcra, mcdecl))








