"""
Motor de cálculo de IRPF - España 2024
Incluye: Escala estatal, mínimos personales y familiares, deducciones estatales y autonómicas
"""


def calcular_renta_total(datos):
    """
    Calcula la declaración de la renta completa
    
    Args:
        datos: dict con todos los campos del formulario
    
    Returns:
        dict con resultados detallados del cálculo
    """
    resultado = {
        'errores': [],
        'avisos': [],
        'datos_entrada': datos.copy()
    }

    # ===== PASO 1: RENDIMIENTOS DEL TRABAJO =====
    rendimiento_trabajo_bruto = datos['salario']
    
    # Reducción por obtención de rendimientos del trabajo (art. 20 LIRPF)
    reduccion_trabajo = calcular_reduccion_trabajo(rendimiento_trabajo_bruto, datos)
    rendimiento_trabajo_neto = max(0, rendimiento_trabajo_bruto - reduccion_trabajo)
    
    resultado['rendimiento_trabajo'] = {
        'bruto': rendimiento_trabajo_bruto,
        'reduccion': reduccion_trabajo,
        'neto': rendimiento_trabajo_neto
    }

    # ===== PASO 2: RENDIMIENTOS DEL CAPITAL INMOBILIARIO =====
    alquiler_bruto = datos['alquiler_ingresos']
    alquiler_gastos = datos['alquiler_gastos']
    alquiler_neto_previo = max(0, alquiler_bruto - alquiler_gastos)
    
    # Reducción del 60% para alquileres de vivienda (art. 23.2 LIRPF)
    reduccion_alquiler = alquiler_neto_previo * 0.60 if alquiler_bruto > 0 else 0
    rendimiento_capital_inmobiliario = max(0, alquiler_neto_previo - reduccion_alquiler)
    
    resultado['rendimiento_capital_inmobiliario'] = {
        'ingresos': alquiler_bruto,
        'gastos': alquiler_gastos,
        'neto_previo': alquiler_neto_previo,
        'reduccion_60': reduccion_alquiler,
        'neto_final': rendimiento_capital_inmobiliario
    }

    # ===== PASO 3: RENDIMIENTOS DEL CAPITAL MOBILIARIO =====
    rendimiento_capital_mobiliario = datos['dividendos']
    
    resultado['rendimiento_capital_mobiliario'] = {
        'total': rendimiento_capital_mobiliario
    }

    # ===== PASO 4: GANANCIAS PATRIMONIALES =====
    ganancias_patrimoniales = datos['ganancias']
    
    resultado['ganancias_patrimoniales'] = {
        'total': ganancias_patrimoniales
    }

    # ===== PASO 5: BASE IMPONIBLE GENERAL =====
    base_imponible_general = (
        rendimiento_trabajo_neto +
        rendimiento_capital_inmobiliario
    )

    # ===== PASO 6: BASE IMPONIBLE DEL AHORRO =====
    base_imponible_ahorro = (
        rendimiento_capital_mobiliario +
        ganancias_patrimoniales
    )

    # ===== PASO 7: REDUCCIONES DE LA BASE IMPONIBLE =====
    # Plan de pensiones (máximo 1.500€ general)
    plan_pensiones = min(datos['plan_pensiones'], 1500)
    
    base_imponible_general -= plan_pensiones
    base_imponible_general = max(0, base_imponible_general)

    resultado['reducciones_base'] = {
        'plan_pensiones': plan_pensiones
    }

    # ===== PASO 8: BASE LIQUIDABLE GENERAL =====
    base_liquidable_general = base_imponible_general

    # ===== PASO 9: MÍNIMO PERSONAL Y FAMILIAR =====
    minimo_personal_familiar = calcular_minimo_personal_familiar(datos)
    
    resultado['minimo_personal_familiar'] = minimo_personal_familiar

    # ===== PASO 10: BASE LIQUIDABLE SOMETIDA A GRAVAMEN =====
    base_gravamen_general = max(0, base_liquidable_general - minimo_personal_familiar['total'])

    # ===== PASO 11: CUOTA ÍNTEGRA ESTATAL Y AUTONÓMICA =====
    # Escala general estatal (50% del tipo)
    cuota_estatal_general, desglose_estatal = calcular_cuota_escala(
        base_gravamen_general,
        ESCALA_ESTATAL_GENERAL
    )

    # Escala general autonómica (50% del tipo) - usamos escala genérica
    cuota_autonomica_general, desglose_autonomico = calcular_cuota_escala(
        base_gravamen_general,
        ESCALA_AUTONOMICA_GENERICA
    )

    # Escala del ahorro (igual estatal y autonómica)
    cuota_estatal_ahorro, desglose_ahorro_est = calcular_cuota_escala(
        base_imponible_ahorro,
        ESCALA_AHORRO_ESTATAL
    )
    
    cuota_autonomica_ahorro, desglose_ahorro_aut = calcular_cuota_escala(
        base_imponible_ahorro,
        ESCALA_AHORRO_AUTONOMICA
    )

    cuota_integra_estatal = cuota_estatal_general + cuota_estatal_ahorro
    cuota_integra_autonomica = cuota_autonomica_general + cuota_autonomica_ahorro
    cuota_integra_total = cuota_integra_estatal + cuota_integra_autonomica

    resultado['cuotas_integras'] = {
        'estatal_general': cuota_estatal_general,
        'estatal_ahorro': cuota_estatal_ahorro,
        'estatal_total': cuota_integra_estatal,
        'autonomica_general': cuota_autonomica_general,
        'autonomica_ahorro': cuota_autonomica_ahorro,
        'autonomica_total': cuota_integra_autonomica,
        'total': cuota_integra_total,
        'desglose_estatal_general': desglose_estatal,
        'desglose_autonomico_general': desglose_autonomico,
        'desglose_ahorro_estatal': desglose_ahorro_est,
        'desglose_ahorro_autonomico': desglose_ahorro_aut
    }

    # ===== PASO 12: DEDUCCIONES DE LA CUOTA =====
    deducciones = calcular_deducciones(datos, cuota_integra_estatal, cuota_integra_autonomica)
    
    resultado['deducciones'] = deducciones

    # ===== PASO 13: CUOTA LÍQUIDA =====
    cuota_liquida_estatal = max(0, cuota_integra_estatal - deducciones['total_estatal'])
    cuota_liquida_autonomica = max(0, cuota_integra_autonomica - deducciones['total_autonomica'])
    cuota_liquida_total = cuota_liquida_estatal + cuota_liquida_autonomica

    resultado['cuotas_liquidas'] = {
        'estatal': cuota_liquida_estatal,
        'autonomica': cuota_liquida_autonomica,
        'total': cuota_liquida_total
    }

    # ===== PASO 14: CUOTA DIFERENCIAL =====
    retenciones = datos['retenciones']
    cuota_diferencial = cuota_liquida_total - retenciones

    resultado['cuota_diferencial'] = {
        'cuota_liquida': cuota_liquida_total,
        'retenciones': retenciones,
        'diferencial': cuota_diferencial,
        'resultado': 'A PAGAR' if cuota_diferencial > 0 else 'A DEVOLVER',
        'importe': abs(cuota_diferencial)
    }

    # ===== RESUMEN FINAL =====
    resultado['resumen'] = {
        'base_imponible_general': base_imponible_general,
        'base_imponible_ahorro': base_imponible_ahorro,
        'base_liquidable_general': base_liquidable_general,
        'base_gravamen_general': base_gravamen_general,
        'tipo_medio': (cuota_liquida_total / base_imponible_general * 100) if base_imponible_general > 0 else 0,
        'tipo_marginal': calcular_tipo_marginal(base_gravamen_general)
    }

    return resultado


def calcular_reduccion_trabajo(salario, datos):
    """Calcula la reducción por rendimientos del trabajo (art. 20 LIRPF)"""
    if salario == 0:
        return 0
    
    # Reducción general: 2.000€ si rendimientos ≤ 14.000€
    if salario <= 14000:
        return 2000
    elif salario < 19000:
        # Reducción decreciente entre 14.000€ y 19.000€
        return 2000 - ((salario - 14000) * 2000 / 5000)
    else:
        return 0


def calcular_minimo_personal_familiar(datos):
    """Calcula el mínimo personal y familiar (art. 56-58 LIRPF)"""
    resultado = {}
    
    # Mínimo del contribuyente (art. 56)
    edad = datos['edad']
    if edad < 65:
        minimo_contribuyente = 5550
    elif edad < 75:
        minimo_contribuyente = 6700
    else:
        minimo_contribuyente = 8100
    
    # Incremento por discapacidad
    if datos['discapacidad']:
        minimo_contribuyente += 3000
    
    resultado['contribuyente'] = minimo_contribuyente
    
    # Mínimo por descendientes (art. 58)
    hijos_menores = datos['hijos_menores_3']
    hijos_mayores = datos['hijos_mayores_3']
    total_hijos = hijos_menores + hijos_mayores
    
    minimo_descendientes = 0
    # Importes por cada hijo: 2.400€ (1º), 2.700€ (2º), 4.000€ (3º), 4.500€ (4º y siguientes)
    importes_hijos = [2400, 2700, 4000] + [4500] * max(0, total_hijos - 3)
    
    for i in range(total_hijos):
        minimo_descendientes += importes_hijos[i]
    
    # Incremento por menores de 3 años: 2.800€ adicionales por cada uno
    minimo_descendientes += hijos_menores * 2800
    
    resultado['descendientes'] = minimo_descendientes
    resultado['total_hijos'] = total_hijos
    resultado['total'] = minimo_contribuyente + minimo_descendientes
    
    return resultado


def calcular_deducciones(datos, cuota_estatal, cuota_autonomica):
    """Calcula las deducciones aplicables"""
    deducciones = {
        'vivienda_habitual': 0,
        'donaciones': 0,
        'maternidad': 0,
        'total_estatal': 0,
        'total_autonomica': 0
    }
    
    # Deducción por vivienda habitual (solo compras pre-2013)
    if datos['vivienda_habitual']:
        # 15% sobre máximo 9.040€ (deducción máxima 1.356€)
        base_deduccion = min(datos['vivienda_importe'], 9040)
        deducciones['vivienda_habitual'] = base_deduccion * 0.15
    
    # Deducción por donaciones
    if datos['donaciones'] > 0:
        # Simplificado: 80% primeros 150€, 35% resto (hasta 40% para donaciones plurianuales)
        if datos['donaciones'] <= 150:
            deducciones['donaciones'] = datos['donaciones'] * 0.80
        else:
            deducciones['donaciones'] = 150 * 0.80 + (datos['donaciones'] - 150) * 0.35
    
    # Deducción por maternidad (1.200€/año por hijo menor de 3 años)
    if datos['maternidad'] and datos['hijos_menores_3'] > 0:
        deducciones['maternidad'] = datos['hijos_menores_3'] * 1200
    
    # Las deducciones se reparten 50/50 entre estatal y autonómica (simplificado)
    total_deducciones = (
        deducciones['vivienda_habitual'] +
        deducciones['donaciones'] +
        deducciones['maternidad']
    )
    
    deducciones['total_estatal'] = min(total_deducciones * 0.5, cuota_estatal)
    deducciones['total_autonomica'] = min(total_deducciones * 0.5, cuota_autonomica)
    
    return deducciones


def calcular_cuota_escala(base, escala):
    """Calcula la cuota según una escala progresiva"""
    cuota = 0
    desglose = []
    base_restante = base
    tramo_previo = 0
    
    for limite, tipo in escala:
        if base_restante <= 0:
            break
        
        tramo_base = min(base_restante, limite - tramo_previo)
        if tramo_base <= 0:
            tramo_previo = limite
            continue
        
        cuota_tramo = tramo_base * tipo
        cuota += cuota_tramo
        
        desglose.append({
            'base': tramo_base,
            'tipo': tipo,
            'cuota': cuota_tramo
        })
        
        base_restante -= tramo_base
        tramo_previo = limite
    
    return cuota, desglose


def calcular_tipo_marginal(base):
    """Calcula el tipo marginal total (estatal + autonómico)"""
    # Buscamos en qué tramo está
    for limite, tipo_est in ESCALA_ESTATAL_GENERAL:
        if base <= limite:
            # Buscamos el tipo autonómico correspondiente
            for lim_aut, tipo_aut in ESCALA_AUTONOMICA_GENERICA:
                if base <= lim_aut:
                    return (tipo_est + tipo_aut) * 100
    return 47.0  # Tipo máximo


# ===== ESCALAS IMPOSITIVAS 2024 =====

# Escala ESTATAL general (50% del total)
ESCALA_ESTATAL_GENERAL = [
    (12450, 0.095),    # 9.5% (19% / 2)
    (20200, 0.12),     # 12% (24% / 2)
    (35200, 0.15),     # 15% (30% / 2)
    (60000, 0.185),    # 18.5% (37% / 2)
    (300000, 0.225),   # 22.5% (45% / 2)
    (float('inf'), 0.235)  # 23.5% (47% / 2)
]

# Escala AUTONÓMICA genérica (50% del total) - varía por CCAA
ESCALA_AUTONOMICA_GENERICA = [
    (12450, 0.095),
    (20200, 0.12),
    (35200, 0.15),
    (60000, 0.185),
    (300000, 0.225),
    (float('inf'), 0.235)
]

# Escala del AHORRO estatal (parte estatal)
ESCALA_AHORRO_ESTATAL = [
    (6000, 0.095),     # 9.5% (19% / 2)
    (50000, 0.105),    # 10.5% (21% / 2)
    (200000, 0.115),   # 11.5% (23% / 2)
    (300000, 0.13),    # 13% (26% / 2)
    (float('inf'), 0.145)  # 14.5% (29% / 2)
]

# Escala del AHORRO autonómica
ESCALA_AHORRO_AUTONOMICA = [
    (6000, 0.095),
    (50000, 0.105),
    (200000, 0.115),
    (300000, 0.13),
    (float('inf'), 0.145)
]
