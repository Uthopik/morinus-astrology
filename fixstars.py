import astrology

class FixStars:
	"""Calculates the positions of the fixstars"""

	NAME = 0
	NOMNAME = 1
	LON = 2
	LAT = 3
	RA = 4
	DECL = 5

	def __init__(self, tjd_ut, flag, names, obl):
		
		self.data = []

		i = 0
		for k in names.keys():
			self.data.append(['', '', 0.0, 0.0, 0.0, 0.0])
			
			linea_cruda = k.strip()
			
			# 1. Extraemos el código de 5 letras (nomnam) para la búsqueda
			if ',' in linea_cruda:
				nomnam = linea_cruda.split(',')[1].strip()[:5].strip()
			else:
				nomnam = linea_cruda[:5].strip()

			# --- BUSCADOR RELATIVO EN LINUX ---
			# Intentamos encontrar el nombre real en el archivo .cat
			nombre_final = linea_cruda.split(',')[0].strip() # Por defecto el original
			
			try:
				# Usamos ruta relativa (ajusta 'swep/ephe/' según tu estructura real)
				ruta_cat = 'SWEP/Ephem/fixstars.cat' 
				
				with open(ruta_cat, 'r') as f:
					for fila in f:
						# Buscamos la cadena exacta del código (ej: 'atTau')
						if nomnam in fila:
							# Cortamos todo lo que hay ANTES de la primera coma
							nombre_final = fila.split(',')[0].strip()
							break 
			except Exception:
				# Si no encuentra el archivo, mantiene el nombre que ya tenía
				pass
			# ----------------------------------

			# 2. CÁLCULO (Mantenemos tu línea que funciona para Long/Lat)
			dat, serr, *sobras = astrology.swe_fixstar_ut(',' + nomnam, tjd_ut, flag)

			# 3. ASIGNACIÓN
			self.data[i][FixStars.NAME] = nombre_final
			self.data[i][FixStars.NOMNAME] = nomnam
			self.data[i][FixStars.LON] = dat[0]
			self.data[i][FixStars.LAT] = dat[1]
			
			# --- CÁLCULO TRIGONOMÉTRICO DIRECTO ---
			import math
			
			l_rad = math.radians(dat[0])
			b_rad = math.radians(dat[1])
			e_rad = math.radians(23.43929) # Oblicuidad fija para asegurar el cambio

			# Declinación: sin(delta) = sin(b)*cos(e) + cos(b)*sin(e)*sin(l)
			sin_delta = math.sin(b_rad) * math.cos(e_rad) + math.cos(b_rad) * math.sin(e_rad) * math.sin(l_rad)
			self.data[i][FixStars.DECL] = math.degrees(math.asin(sin_delta))

			# Rectascensión: tan(alpha) = (sin(l)*cos(e) - tan(b)*sin(e)) / cos(l)
			num = math.sin(l_rad) * math.cos(e_rad) - math.tan(b_rad) * math.sin(e_rad)
			den = math.cos(l_rad)
			ra_grados = math.degrees(math.atan2(num, den))
			
			if ra_grados < 0: 
				ra_grados += 360
			
			self.data[i][FixStars.RA] = ra_grados

			i += 1

		self.sort()


	def sort(self):
		num = len(self.data)
		self.mixed = []
			
		for i in range(num):
			self.mixed.append(i)

		for i in range(num):
			for j in range(num-1):
				if (self.data[j][FixStars.LON] > self.data[j+1][FixStars.LON]):
					tmp = self.data[j][:]
					self.data[j] = self.data[j+1][:]
					self.data[j+1] = tmp[:]
					tmp = self.mixed[j]
					self.mixed[j] = self.mixed[j+1]
					self.mixed[j+1] = tmp






