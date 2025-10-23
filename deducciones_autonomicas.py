"""
Deducciones autonómicas IRPF 2024 - España
Fuente: BOE y normativa de cada comunidad autónoma
Última actualización: 2024
"""

# ESCALAS AUTONÓMICAS REALES (parte autonómica del IRPF - 50%)
ESCALAS_AUTONOMICAS = {
    "Andalucía": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (130000, 0.225),
        (175000, 0.24),
        (float('inf'), 0.245)
    ],
    
    "Aragón": [
        (12450, 0.10),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.20),
        (float('inf'), 0.22)
    ],
    
    "Asturias": [
        (12450, 0.09),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.23)
    ],
    
    "Baleares": [
        (12450, 0.09),
        (20200, 0.115),
        (35200, 0.15),
        (60000, 0.195),
        (140000, 0.22),
        (float('inf'), 0.235)
    ],
    
    "Canarias": [
        (12450, 0.085),
        (20200, 0.115),
        (35200, 0.145),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Cantabria": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Castilla y León": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Castilla-La Mancha": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Cataluña": [
        (12450, 0.12),
        (20200, 0.14),
        (35200, 0.165),
        (60000, 0.215),
        (90000, 0.235),
        (120000, 0.245),
        (175000, 0.255),
        (float('inf'), 0.26)
    ],
    
    "Comunidad Valenciana": [
        (12450, 0.10),
        (20200, 0.12),
        (35200, 0.145),
        (60000, 0.185),
        (135000, 0.225),
        (float('inf'), 0.2475)
    ],
    
    "Extremadura": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Galicia": [
        (12450, 0.095),
        (20200, 0.115),
        (35200, 0.145),
        (60000, 0.185),
        (float('inf'), 0.215)
    ],
    
    "Madrid": [
        (12450, 0.09),
        (17707, 0.11),
        (33007, 0.135),
        (float('inf'), 0.215)
    ],
    
    "Murcia": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Navarra": [
        # Navarra tiene sistema foral propio - escala diferente
        (15500, 0.11),
        (20500, 0.14),
        (35500, 0.19),
        (60000, 0.23),
        (150000, 0.30),
        (250000, 0.35),
        (float('inf'), 0.40)
    ],
    
    "País Vasco": [
        # País Vasco tiene sistema foral propio - escala diferente
        (15000, 0.11),
        (20000, 0.13),
        (35000, 0.18),
        (60000, 0.23),
        (float('inf'), 0.25)
    ],
    
    "La Rioja": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Ceuta": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ],
    
    "Melilla": [
        (12450, 0.095),
        (20200, 0.12),
        (35200, 0.15),
        (60000, 0.185),
        (float('inf'), 0.225)
    ]
}


# DEDUCCIONES ESPECÍFICAS POR COMUNIDAD
DEDUCCIONES_ESPECIFICAS = {
    "Andalucía": {
        "nacimiento_adopcion": {"condiciones": "por cada hijo", "importe": 50},
        "familia_numerosa": {"general": 100, "especial": 200},
        "discapacidad_a_cargo": 100,
        "vivienda_habitual_menores_35": {"limite": 9040, "porcentaje": 0.02},
        "alquiler_menores_35": {"limite": 600, "porcentaje": 0.15}
    },
    
    "Aragón": {
        "nacimiento_tercer_hijo": 500,
        "adopcion_internacional": 600,
        "familia_numerosa": 200,
        "cuidado_menores_3": 200,
        "mayores_75_convivencia": 150
    },
    
    "Asturias": {
        "nacimiento_adopcion": {"primer_hijo": 500, "segundo": 1000, "tercero": 1500},
        "familia_monoparental": 300,
        "alquiler_vivienda_habitual": {"limite": 600, "porcentaje": 0.10}
    },
    
    "Baleares": {
        "nacimiento_adopcion": {"primer_hijo": 200, "segundo": 400, "tercero_mas": 600},
        "familia_numerosa": 300,
        "gastos_escolares": {"limite": 120, "porcentaje": 0.15}
    },
    
    "Canarias": {
        "familia_numerosa": {"general": 200, "especial": 400},
        "nacimiento_adopcion": 150,
        "gastos_guarderia": {"limite": 1000, "porcentaje": 0.15},
        "discapacidad": 300
    },
    
    "Cantabria": {
        "familia_numerosa": 150,
        "nacimiento_adopcion": {"primer_hijo": 100, "segundo_mas": 150},
        "cuidado_menores_3": {"limite": 600, "porcentaje": 0.15}
    },
    
    "Castilla y León": {
        "familia_numerosa": 500,
        "nacimiento_adopcion": {"primer_hijo": 710, "segundo": 1475, "tercero_mas": 2351},
        "cuidado_menores_4": {"limite": 322, "porcentaje": 0.30}
    },
    
    "Castilla-La Mancha": {
        "familia_numerosa": 300,
        "nacimiento_segundo_hijo": 300,
        "gastos_escolares": {"limite": 100, "porcentaje": 0.15}
    },
    
    "Cataluña": {
        "nacimiento_adopcion": {"primer_hijo": 300, "segundo": 600, "tercero_mas": 900},
        "alquiler_vivienda_habitual": {"limite": 600, "porcentaje": 0.10},
        "rehabilitacion_vivienda": {"limite": 9040, "porcentaje": 0.01},
        "donaciones_entidades_catalanas": {"hasta_150": 0.25, "resto": 0.10}
    },
    
    "Comunidad Valenciana": {
        "nacimiento_adopcion": {"primer_hijo": 270, "segundo": 297, "tercero_mas": 442},
        "familia_numerosa": 300,
        "discapacidad_a_cargo": {"33_65": 238, "mas_65": 366},
        "cantidades_satisfechas_hijos": {"limite": 100, "porcentaje": 0.05}
    },
    
    "Extremadura": {
        "nacimiento_adopcion": 300,
        "familia_numerosa": 300,
        "cuidado_menores_3": 250,
        "alquiler_menores_36": {"limite": 500, "porcentaje": 0.10}
    },
    
    "Galicia": {
        "nacimiento_adopcion": {"primer_hijo": 360, "segundo": 720, "tercero_mas": 1200},
        "familia_numerosa": {"general": 250, "especial": 600},
        "discapacidad": 300,
        "alquiler_menores_35": {"limite": 600, "porcentaje": 0.10}
    },
    
    "Madrid": {
        "nacimiento_adopcion": {"uno": 600, "dos_mas": 750},
        "cuidado_menores_3": {"limite": 1000, "porcentaje": 0.30},
        "alquiler_menores_35": {"limite": 1000, "porcentaje": 0.30}
    },
    
    "Murcia": {
        "nacimiento_adopcion": {"primer_hijo": 100, "segundo": 200, "tercero": 300, "cuarto_mas": 400},
        "familia_numerosa": 150,
        "gastos_guarderia": {"limite": 330, "porcentaje": 0.15},
        "inversion_vivienda_habitual": {"menores_35": 300}
    },
    
    "Navarra": {
        # Deducciones propias del régimen foral
        "familia_numerosa": 400,
        "personas_mayores_65": 150,
        "discapacidad": {"33_65": 500, "mas_65": 1000},
        "alquiler_vivienda": {"limite": 1200, "porcentaje": 0.15}
    },
    
    "País Vasco": {
        # Deducciones propias del régimen foral (cada territorio histórico puede variar)
        "familia_numerosa": {"general": 500, "especial": 1000},
        "menores_a_cargo": 250,
        "vivienda_habitual": {"limite": 1800, "porcentaje": 0.18}
    },
    
    "La Rioja": {
        "nacimiento_adopcion": {"primer_hijo": 150, "segundo": 180, "tercero_mas": 210},
        "familia_numerosa": 180,
        "cuidado_ascendientes": 180
    },
    
    "Ceuta": {
        "bonificacion_general": {"porcentaje": 0.50},  # 50% de bonificación en cuota autonómica
        "familia_numerosa": 200
    },
    
    "Melilla": {
        "bonificacion_general": {"porcentaje": 0.50},  # 50% de bonificación en cuota autonómica
        "familia_numerosa": 200
    }
}


def obtener_escala_autonomica(comunidad):
    """
    Devuelve la escala autonómica específica de la comunidad
    
    Args:
        comunidad (str): Nombre de la comunidad autónoma
        
    Returns:
        list: Lista de tuplas (límite, tipo) para la escala autonómica
    """
    return ESCALAS_AUTONOMICAS.get(comunidad, ESCALAS_AUTONOMICAS["Madrid"])  # Madrid por defecto


def obtener_deducciones_autonomicas(comunidad):
    """
    Devuelve las deducciones específicas de la comunidad
    
    Args:
        comunidad (str): Nombre de la comunidad autónoma
        
    Returns:
        dict: Diccionario con las deducciones específicas
    """
    return DEDUCCIONES_ESPECIFICAS.get(comunidad, {})


def calcular_deduccion_nacimiento(comunidad, numero_hijo):
    """
    Calcula la deducción por nacimiento/adopción según comunidad y número de hijo
    
    Args:
        comunidad (str): Comunidad autónoma
        numero_hijo (int): Número de hijo (1, 2, 3...)
        
    Returns:
        float: Importe de la deducción
    """
    deducciones = obtener_deducciones_autonomicas(comunidad)
    
    if "nacimiento_adopcion" in deducciones:
        nac = deducciones["nacimiento_adopcion"]
        
        if isinstance(nac, dict):
            if numero_hijo == 1:
                return nac.get("primer_hijo", 0)
            elif numero_hijo == 2:
                return nac.get("segundo", nac.get("segundo_hijo", 0))
            else:
                return nac.get("tercero_mas", nac.get("tercer_hijo", 0))
        else:
            return nac
    
    return 0


def calcular_deduccion_familia_numerosa(comunidad, tipo="general"):
    """
    Calcula la deducción por familia numerosa
    
    Args:
        comunidad (str): Comunidad autónoma
        tipo (str): "general" o "especial"
        
    Returns:
        float: Importe de la deducción
    """
    deducciones = obtener_deducciones_autonomicas(comunidad)
    
    if "familia_numerosa" in deducciones:
        fn = deducciones["familia_numerosa"]
        
        if isinstance(fn, dict):
            return fn.get(tipo, 0)
        else:
            return fn
    
    return 0


def calcular_deduccion_alquiler(comunidad, alquiler_pagado, edad):
    """
    Calcula la deducción por alquiler de vivienda habitual
    
    Args:
        comunidad (str): Comunidad autónoma
        alquiler_pagado (float): Cantidad pagada en alquiler anual
        edad (int): Edad del contribuyente
        
    Returns:
        float: Importe de la deducción
    """
    deducciones = obtener_deducciones_autonomicas(comunidad)
    
    # Buscar deducciones de alquiler (diferentes nombres según CCAA)
    for key in ["alquiler_vivienda_habitual", "alquiler_menores_35", "alquiler_menores_36", "alquiler_vivienda"]:
        if key in deducciones:
            alq = deducciones[key]
            
            # Verificar requisito de edad si existe
            if "menores" in key and edad >= 35:
                continue
            
            if isinstance(alq, dict):
                limite = alq.get("limite", float('inf'))
                porcentaje = alq.get("porcentaje", 0)
                base = min(alquiler_pagado, limite)
                return base * porcentaje
    
    return 0


# Notas importantes para el desarrollador:
"""
IMPORTANTE: ACTUALIZACIÓN ANUAL REQUERIDA

Este archivo debe actualizarse cada año (enero) consultando:
1. BOE - Ley de Presupuestos Generales del Estado
2. BOE autonómico de cada comunidad
3. Webs oficiales de Hacienda autonómica

FUENTES OFICIALES:
- Estatal: https://www.boe.es
- Autonómicas: Cada comunidad publica en su BOJA/DOGC/BOCM/etc.
- AEAT: https://sede.agenciatributaria.gob.es

CAMBIOS FRECUENTES:
- Límites de tramos (ajuste por inflación)
- Nuevas deducciones por políticas familiares
- Modificaciones en porcentajes

VALIDACIÓN:
Contrastar siempre con casos reales y el simulador oficial:
https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/
"""
