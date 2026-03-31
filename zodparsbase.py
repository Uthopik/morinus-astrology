import chart
import math
import util
import astrology # <--- IMPORTANTE: Conexión a la centralita
import sweastrology # <--- IMPORTANTE: Conexión a tu aduana

class Points:
	def __init__(self, valid, points):
		self.valid = valid
		self.pts = points

class ZodParsBase:
	"""Computes zodiacal parallels (abstract)"""

	def __init__(self, obl):
		# Usamos un try/except para capturar cualquier fallo de tipo
		try:
			f_obl = float(obl)
			if f_obl <= 0.0:
				# Si el dato viene mal, pedimos el VOTO real a tu sweastrology
				import sweastrology
				self.obl = sweastrology.swe_calc_ut_adaptado(0, -1, 0)[0]
				if self.obl <= 0.0:
					self.obl = 23.441587
			else:
				self.obl = f_obl
		except:
			self.obl = 23.441587

	def getEclPoints(self, lon, decl, onEcl):
		'''Calculates points of the Ecliptic from declination'''
		PARALLEL = chart.Chart.PARALLEL
		CONTRAPARALLEL = chart.Chart.CONTRAPARALLEL

		origdecl = decl

		# PROTECCIÓN DE DIVISIÓN POR CERO
		if math.sin(math.radians(self.obl)) == 0:
			self.obl = 23.441587

		if decl < 0.0:
			decl *= -1

		if decl > self.obl:
			return Points(False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))

		if onEcl:
			if decl == self.obl:
				lon += 180.0
				lon = util.normalize(lon)
				return Points(True, ((lon, CONTRAPARALLEL), (-1.0, PARALLEL)))
			else:
				lon1 = lon+180.0
				lon1 = util.normalize(lon1)
				lon2 = 360.0-lon1
				lon3 = util.normalize(lon2+180.0)
				return Points(True, ((lon1, CONTRAPARALLEL), (lon2, PARALLEL), (lon3, CONTRAPARALLEL)))
		else:
			# Aquí es donde fallaba la división originalmente
			# Al haber asegurado que self.obl != 0, ya es seguro
			div_val = math.sin(math.radians(self.obl))
			
			if decl == self.obl:
				lon1 = math.degrees(math.asin(math.sin(math.radians(origdecl))/div_val))
				lon1 = util.normalize(lon1)
				lon2 = util.normalize(lon1+180.0)
				return Points(True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL)))
			else:
				lon1 = math.degrees(math.asin(math.sin(math.radians(origdecl))/div_val))
				lon1 = util.normalize(lon1)
				lon2 = util.normalize(lon1+180.0)
				lon3 = 360.0-lon2
				lon4 = util.normalize(lon3+180.0)
				return Points(True, ((lon1, PARALLEL), (lon2, CONTRAPARALLEL), (lon3, PARALLEL), (lon4, CONTRAPARALLEL)))

		return Points(False, ((-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL), (-1.0, PARALLEL)))



