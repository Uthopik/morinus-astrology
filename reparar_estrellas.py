import pickle
import os

# 1. Definimos la ruta del archivo (ajusta la carpeta si es necesario)
ruta_opt = 'Opts/fixedstars.opt'

# 2. La lista de estrellas que quieres recuperar (Nombre: True)
# Usamos los códigos técnicos (nomnam) que Morinus entiende
estrellas = {
    'beCet': True, 'gaPeg': True, 'alAnd': True, 'beAnd': True, 'beAri': True, 
    'alAri': True, 'alCet': True, 'gaEri': True, 'bePer': True, 'etTau': True, 
    'alPer': True, 'gaTau': True, 'alTau': True, 'beOri': True, 'gaOri': True, 
    'alAur': True, 'beTau': True, 'epOri': True, 'zeOri': True, 'zeTau': True, 
    'alUMi': True, 'alOri': True, 'beAur': True, 'beCMa': True, 'gaGem': True, 
    'alCMa': True, 'alCar': True, 'alGem': True, 'epCMa': True
}

# 3. Creamos la carpeta Opts si no existe
if not os.path.exists('Opts'):
    os.makedirs('Opts')

# 4. Escribimos el archivo en el formato binario que Morinus espera
try:
    with open(ruta_opt, 'wb') as f:
        pickle.dump(estrellas, f, protocol=4) # Protocolo compatible con Python moderno
    print(f"¡Éxito! El archivo {ruta_opt} ha sido regenerado con sus 29 estrellas.")
except Exception as e:
    print(f"Error al crear el archivo: {e}")
