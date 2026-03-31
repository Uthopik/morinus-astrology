import swisseph as swe
import os
import sys

# 1. CONFIGURACIÓN DE RUTA (SWEP/Ephem)
base_dir = os.path.dirname(os.path.abspath(__file__))
ruta_efem = os.path.join(base_dir, 'SWEP', 'Ephem')

if os.path.exists(ruta_efem):
    # Verificamos si hay archivos .se1 dentro para estar seguros
    archivos = os.listdir(ruta_efem)
    if any(f.endswith('.se1') for f in archivos):
        swe.set_ephe_path(ruta_efem)
        # Esto saldrá en tu terminal de Ubuntu para darte paz mental:
        sys.stderr.write(f"\n[OK] Motor Suizo conectado con éxito en: {ruta_efem}\n")
    else:
        sys.stderr.write(f"\n[ERROR] La carpeta {ruta_efem} está vacía o no tiene archivos .se1\n")
else:
    sys.stderr.write(f"\n[ERROR] No se encuentra la ruta: {ruta_efem}\n")

# 2. ADAPTADORES DE CÁLCULO
def swe_calc_ut_adaptado(jd, ipl, flag):
    try:
        # Forzamos los tipos para evitar errores de Python 3.13
        res = swe.calc_ut(float(jd), int(ipl), int(flag))
        # res[0] contiene (longitud, latitud, distancia, velocidad_lon, etc.)
        return [float(x) for x in res[0]], 0
    except Exception as e:
        return [0.0]*6, -1

# Morinus a veces llama a swe_calc directamente esperando (error, longitud)
def swe_calc_adaptado(jd, ipl, flag):
    data, err = swe_calc_ut_adaptado(jd, ipl, flag)
    return err, data[0] 

# 3. ADAPTADOR DE CASAS (Precisión en Ascendente/MC)
def swe_houses_ex_adaptado(jd, iflag, lat, lon, hsys):
    # Convertimos el sistema de casas a bytes (requerido por pyswisseph)
    if isinstance(hsys, int):
        hsys_byte = chr(hsys).encode('utf-8')
    else:
        hsys_byte = hsys.encode('utf-8')

    res = swe.houses_ex(float(jd), float(lat), float(lon), hsys_byte)
    
    # Morinus espera que el índice 0 de las cúspides esté vacío o sea 0.0
    cusp_list = [0.0] + list(res[0]) 
    ascmc_list = list(res[1])
    
    # Rellenamos hasta 10 elementos para evitar IndexError en Morinus
    while len(ascmc_list) < 10:
        ascmc_list.append(0.0)
    
    return (cusp_list, ascmc_list, ascmc_list)
    
def swe_rise_trans(jd, ipl, star, epheflag, rsmi, lon, lat, alt, press, temp):
    import sys
    try:
        # 1. Preparar los datos según tu manual
        tjdut = float(jd)
        
        # 'body' puede ser el ID del planeta o el nombre de la estrella
        body = star if (star and len(str(star).strip()) > 0) else int(ipl)
        
        rsmi_val = int(rsmi)
        geopos = (float(lon), float(lat), float(alt))
        atpress = float(press) if press else 0.0
        attemp = float(temp) if temp else 0.0
        flags = int(epheflag)

        # 2. LLAMADA SEGÚN TU DICCIONARIO:
        # rise_trans(tjdut, body, rsmi, geopos, atpress, attemp, flags)
        res = swe.rise_trans(tjdut, body, rsmi_val, geopos, atpress, attemp, flags)
        
        # 3. Extraer el resultado (el Julian Day del evento)
        # res[1] suele ser una lista [jd_resultado, ...] o el número directo
        if isinstance(res[1], (list, tuple)):
            jd_calc = float(res[1][0])
        else:
            jd_calc = float(res[1])
            
        return 0, jd_calc, ""

    except Exception as e:
        sys.stderr.write(f"\n[DEBUG] Fallo con manual: {str(e)}")
        # Si falla por los argumentos opcionales, probamos solo con 4:
        try:
            res = swe.rise_trans(tjdut, body, rsmi_val, geopos)
            jd_calc = float(res[1][0]) if isinstance(res[1], (list, tuple)) else float(res[1])
            return 0, jd_calc, ""
        except:
            return -1, float(jd), str(e)

def swe_cotrans(lon, lat, dist, obl):
    try:
        res = swe.cotrans(float(lon), float(lat), float(dist), float(obl))
        return [float(x) for x in res]
    except Exception as e:
        return [float(lon), float(lat), float(dist)]
        
# 1. Asegúrate de que revjul entregue la hora con precisión
def swe_revjul_adaptado(jd, cal):
    # pyswisseph devuelve (año, mes, día, hora_decimal)
    res = swe.revjul(float(jd), int(cal))
    return res[0], res[1], res[2], float(res[3])

# 2. Asegúrate de que sidtime0 (usado para el cálculo de casas) sea preciso
def swe_sidtime0_adaptado(jd, ecl, nut):
    res = swe.sidtime0(float(jd), float(ecl), float(nut))
    # res es una tupla, el primer elemento es el tiempo sidéreo
    return float(res[0])

# 4. MAPEO DE FUNCIONES (El puente)
swe_revjul = swe_revjul_adaptado
swe_sidtime0 = swe_sidtime0_adaptado
swe_rise_trans = swe_rise_trans
swe_cotrans = swe_cotrans
swe_calc_ut = swe_calc_ut_adaptado
swe_calc = swe_calc_adaptado
swe_houses_ex = swe_houses_ex_adaptado
swe_set_ephe_path = swe.set_ephe_path
swe_fixstar_ut = lambda star, jd, flag: (swe.fixstar_ut(star, jd, flag)[0], star, "")
swe_close = swe.close
swe_revjul = swe.revjul
swe_julday = swe.julday
swe_sidtime = swe.sidtime
swe_get_planet_name = swe.get_planet_name
swe_set_sid_mode = swe.set_sid_mode
swe_houses_armc = swe.houses_armc
swe_set_topo = swe.set_topo
swe_deltat = swe.deltat
swe_time_equ = lambda jd: (0, float(swe.time_equ(float(jd))), "")
swe_sidtime0 = lambda jd, ecl, nut: float(swe.sidtime0(float(jd), float(ecl), float(nut))[0])

# 5. CONSTANTES
SE_SUN = 0
SEFLG_SWIEPH = 2
SE_CALC_RISE = 1
SE_GREG_CAL = 1
SE_FLG_SPEED = 256
