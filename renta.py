"""
Motor de cálculo de IRPF - España 2024 (VERSIÓN PROFESIONAL)
Incluye: Escalas autonómicas reales, autónomos, imputación rentas, 
         deducciones completas, compensación pérdidas
"""

from deducciones_autonomicas import (
    obtener_escala_autonomica,
    obtener_deducciones_autonomicas,
    calcular_deduccion_nacimiento,
    calcular_deduccion_familia_numerosa,
    calcular_deduccion_alquiler
)


def calcular_renta_total(datos):
    """
    Calcula la declaración de la renta completa con todas las mejoras
    
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
    rendimiento_trabajo_bruto = datos.get('salario', 0)
    
    # Reducción por obtención de rendimientos del trabajo (art. 20 LIRPF)
    reduccion_trabajo = calcular_reduccion_trabajo(rendimiento_trabajo_bruto, datos)
    rendimiento_trabajo_neto = max(0, rendimiento_trabajo_bruto - reduccion_trabajo)
    
    resultado['rendimiento_trabajo'] = {
        'bruto': rendimiento_trabajo_bruto,
        'reduccion': reduccion_trabajo,
        'neto': rendimiento_trabajo_neto
    }

    # ===== PASO 1B: RENDIMIENTOS DE ACTIVIDADES ECONÓMICAS (AUTÓNOMOS) =====
    rendimiento_actividades = 0
    if datos.get('es_autonomo', False):
        ingresos_autonomo = datos.get('ingresos_autonomo', 0)
        gastos_autonomo = datos.get('gastos_autonomo', 0)
        
        # Rendimiento neto = ingresos - gastos
        rendimiento_neto_actividad = max(0, ingresos_autonomo - gastos_autonomo)
        
        # Reducción adicional por actividades económicas (gastos difícil justificación)
        if datos.get('regimen_autonomo') == 'estimacion_directa_simplificada':
            # 5% adicional en simplificada (máximo 2.000€)
            reduccion_adicional = min(rendimiento_neto_actividad * 0.05, 2000)
            rendimiento_actividades = max(0, rendimiento_neto_actividad - reduccion_adicional)
        else:
            rendimiento_actividades = rendimiento_neto_actividad
        
        resultado['rendimiento_actividades'] = {
            'ingresos': ingresos_autonomo,
            'gastos': gastos_autonomo,
            'neto': rendimiento_actividades
        }
    else:
        resultado['rendimiento_actividades'] = {
            'ingresos': 0,
            'gastos': 0,
            'neto': 0
        }

    # ===== PASO 2: RENDIMIENTOS DEL CAPITAL INMOBILIARIO =====
    alquiler_bruto = datos.get('alquiler_ingresos', 0)
    alquiler_gastos = datos.get('alquiler_gastos', 0)
    
    # Gastos deducibles detallados
    gastos_detallados = {
        'ibi': datos.get('ibi', 0),
        'comunidad': datos.get('comunidad', 0),
        'seguro': datos.get('seguro_hogar', 0),
        'reparaciones': datos.get('reparaciones', 0),
        'intereses_hipoteca': datos.get('intereses_hipoteca', 0),
        'amortizacion': calcular_amortizacion_inmueble(datos),
        'otros': alquiler_gastos
    }
    
    total_gastos_alquiler = sum(gastos_detallados.values())
    alquiler_neto_previo = max(0, alquiler_bruto - total_gastos_alquiler)
    
    # Reducción del 60% para alquileres de vivienda (art. 23.2 LIRPF)
    # Si arrendatario es menor de 30 años: 70% (nueva normativa)
    porcentaje_reduccion = 0.70 if datos.get('arrendatario_menor_30', False) else 0.60
    reduccion_alquiler = alquiler_neto_previo * porcentaje_reduccion if alquiler_bruto > 0 else 0
    rendimiento_capital_inmobiliario = max(0, alquiler_neto_previo - reduccion_alquiler)
    
    resultado['rendimiento_capital_inmobiliario'] = {
        'ingresos': alquiler_bruto,
        'gastos_detallados': gastos_detallados,
        'gastos_totales': total_gastos_alquiler,
        'neto_previo': alquiler_neto_previo,
        'reduccion_porcentaje': porcentaje_reduccion,
        'reduccion_importe': reduccion_alquiler,
        'neto_final': rendimiento_capital_inmobiliario
    }

    # ===== PASO 2B: IMPUTACIÓN DE RENTAS INMOBILIARIAS =====
    # Segunda vivienda no alquilada: 1,1% o 2% del valor catastral
    imputacion_rentas = 0
    if datos.get('tiene_segunda_vivienda', False):
        valor_catastral = datos.get('valor_catastral_segunda', 0)
        porcentaje = 0.02 if datos.get('valor_catastral_revisado', False) else 0.011
        imputacion_rentas = valor_catastral * porcentaje
        
        resultado['imputacion_rentas'] = {
            'valor_catastral': valor_catastral,
            'porcentaje': porcentaje * 100,
            'importe': imputacion_rentas
        }

    # ===== PASO 3: RENDIMIENTOS DEL CAPITAL MOBILIARIO =====
    rendimiento_capital_mobiliario = datos.get('dividendos', 0) + datos.get('intereses', 0)
    
    resultado['rendimiento_capital_mobiliario'] = {
        'dividendos': datos.get('dividendos', 0),
        'intereses': datos.get('intereses', 0),
        'total': rendimiento_capital_mobiliario
    }

    # ===== PASO 4: GANANCIAS Y PÉRDIDAS PATRIMONIALES =====
    ganancias_brutas = datos.get('ganancias', 0)
    perdidas = datos.get('perdidas_patrimoniales', 0)
    
    # Compensación de pérdidas (art. 49 LIRPF)
    # Las pérdidas se compensan primero con ganancias del mismo año
    ganancias_netas = max(0, ganancias_brutas - perdidas)
    perdidas_pendientes = max(0, perdidas - ganancias_brutas)
    
    # Pérdidas de años anteriores pendientes de compensar
    perdidas_anos_anteriores = datos.get('perdidas_pendientes_anos_anteriores', 0)
    ganancias_tras_compensacion = max(0, ganancias_netas - perdidas_anos_anteriores)
    perdidas_pendientes_futuro = max(0, perdidas_pendientes + (perdidas_anos_anteriores - ganancias_netas))
    
    resultado['ganancias_patrimoniales'] = {
        'ganancias_brutas': ganancias_brutas,
        'perdidas_ejercicio': perdidas,
        'ganancias_netas': ganancias_netas,
        'perdidas_anos_anteriores': perdidas_anos_anteriores,
        'ganancias_final': ganancias_tras_compensacion,
        'perdidas_pendientes_compensar': perdidas_pendientes_futuro
    }
    
    if perdidas_pendientes_futuro > 0:
        resultado['avisos'].append(
            f"Tienes {perdidas_pendientes_futuro:,.2f}€ en pérdidas pendientes de compensar en ejercicios futuros (hasta 4 años)"
        )

    # ===== PASO 5: BASE IMPONIBLE GENERAL =====
    base_imponible_general = (
        rendimiento_trabajo_neto +
        rendimiento_actividades +
        rendimiento_capital_inmobiliario +
        imputacion_rentas
    )

    # ===== PASO 6: BASE IMPONIBLE DEL AHORRO =====
    base_imponible_ahorro = (
        rendimiento_capital_mobiliario +
        ganancias_tras_compensacion
    )

    # ===== PASO 7: REDUCCIONES DE LA BASE IMPONIBLE =====
    reducciones_totales = 0
    
    # 7.1 Plan de pensiones (máximo 1.500€ general)
    plan_pensiones = min(datos.get('plan_pensiones', 0), 1500)
    reducciones_totales += plan_pensiones
    
    # 7.2 Aportaciones a mutualidades (autónomos)
    if datos.get('es_autonomo', False):
        mutualidad = min(datos.get('mutualidad', 0), 1500)
        reducciones_totales += mutualidad
    else:
        mutualidad = 0
    
    # 7.3 Pensiones compensatorias
    pensiones_compensatorias = datos.get('pensiones_compensatorias', 0)
    reducciones_totales += pensiones_compensatorias
    
    base_imponible_general -= reducciones_totales
    base_imponible_general = max(0, base_imponible_general)

    resultado['reducciones_base'] = {
        'plan_pensiones': plan_pensiones,
        'mutualidad': mutualidad,
        'pensiones_compensatorias': pensiones_compensatorias,
        'total': reducciones_totales
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

    # Escala general autonómica REAL según comunidad
    escala_autonomica = obtener_escala_autonomica(datos.get('comunidad', 'Madrid'))
    cuota_autonomica_general, desglose_autonomico = calcular_cuota_escala(
        base_gravamen_general,
        escala_autonomica
    )

    # Escala del ahorro
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
    deducciones = calcular_deducciones_completas(datos, cuota_integra_estatal, cuota_integra_autonomica)
    
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
    retenciones = datos.get('retenciones', 0)
    pagos_fraccionados = datos.get('pagos_fraccionados_autonomo', 0) if datos.get('es_autonomo', False) else 0
    total_pagado = retenciones + pagos_fraccionados
    
    cuota_diferencial = cuota_liquida_total - total_pagado

    resultado['cuota_diferencial'] = {
        'cuota_liquida': cuota_liquida_total,
        'retenciones': retenciones,
        'pagos_fraccionados': pagos_fraccionados,
        'total_pagado': total_pagado,
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
        'tipo_medio': (cuota_liquida_total / (base_imponible_general + base_imponible_ahorro) * 100) if (base_imponible_general + base_imponible_ahorro) > 0 else 0,
        'tipo_marginal': calcular_tipo_marginal(base_gravamen_general, escala_autonomica)
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


def calcular_amortizacion_inmueble(datos):
    """
    Calcula la amortización del inmueble alquilado (3% anual sobre construcción)
    """
    if datos.get('alquiler_ingresos', 0) == 0:
        return 0
    
    valor_construccion = datos.get('valor_construccion_alquiler', 0)
    if valor_construccion == 0:
        # Si no se especifica, estimamos 70% del valor total como construcción
        valor_total = datos.get('valor_compra_inmueble', 0)
        valor_construccion = valor_total * 0.70
    
    return valor_construccion * 0.03  # 3% anual


def calcular_minimo_personal_familiar(datos):
    """Calcula el mínimo personal y familiar (art. 56-58 LIRPF)"""
    resultado = {}
    
    # Mínimo del contribuyente (art. 56)
    edad = datos.get('edad', 30)
    if edad < 65:
        minimo_contribuyente = 5550
    elif edad < 75:
        minimo_contribuyente = 6700
    else:
        minimo_contribuyente = 8100
    
    # Incremento por discapacidad
    if datos.get('discapacidad', False):
        grado_discapacidad = datos.get('grado_discapacidad', 33)
        if grado_discapacidad >= 65:
            minimo_contribuyente += 9000
        else:
            minimo_contribuyente += 3000
    
    resultado['contribuyente'] = minimo_contribuyente
    
    # Mínimo por descendientes (art. 58)
    hijos_menores = datos.get('hijos_menores_3', 0)
    hijos_mayores = datos.get('hijos_mayores_3', 0)
    total_hijos = hijos_menores + hijos_mayores
    
    minimo_descendientes = 0
    # Importes por cada hijo: 2.400€ (1º), 2.700€ (2º), 4.000€ (3º), 4.500€ (4º y siguientes)
    importes_hijos = [2400, 2700, 4000] + [4500] * max(0, total_hijos - 3)
    
    for i in range(total_hijos):
        minimo_descendientes += importes_hijos[i]
    
    # Incremento por menores de 3 años: 2.800€ adicionales por cada uno
    minimo_descendientes += hijos_menores * 2800
    
    # Incremento si descendiente con discapacidad
    hijos_con_discapacidad = datos.get('hijos_con_discapacidad', 0)
    minimo_descendientes += hijos_con_discapacidad * 3000
    
    resultado['descendientes'] = minimo_descendientes
    resultado['total_hijos'] = total_hijos
    
    # Mínimo por ascendientes
    ascendientes_mayores_65 = datos.get('ascendientes_mayores_65_a_cargo', 0)
    ascendientes_mayores_75 = datos.get('ascendientes_mayores_75_a_cargo', 0)
    minimo_ascendientes = ascendientes_mayores_65 * 1150 + ascendientes_mayores_75 * 1400
    resultado['ascendientes'] = minimo_ascendientes
    
    resultado['total'] = minimo_contribuyente + minimo_descendientes + minimo_ascendientes
    
    return resultado


def calcular_deducciones_completas(datos, cuota_estatal, cuota_autonomica):
    """Calcula TODAS las deducciones aplicables (estatales + autonómicas)"""
    deducciones = {
        # Estatales
        'vivienda_habitual': 0,
        'donaciones': 0,
        'maternidad': 0,
        'familia_numerosa_estatal': 0,
        
        # Autonómicas
        'nacimiento_adopcion': 0,
        'familia_numerosa_autonomica': 0,
        'alquiler_vivienda_habitual': 0,
        'cuidado_menores': 0,
        'discapacidad_a_cargo': 0,
        'otras_autonomicas': 0,
        
        'total_estatal': 0,
        'total_autonomica': 0
    }
    
    # === DEDUCCIONES ESTATALES ===
    
    # 1. Vivienda habitual (solo compras pre-2013)
    if datos.get('vivienda_habitual', False):
        base_deduccion = min(datos.get('vivienda_importe', 0), 9040)
        deducciones['vivienda_habitual'] = base_deduccion * 0.15
    
    # 2. Donaciones
    if datos.get('donaciones', 0) > 0:
        donacion = datos.get('donaciones', 0)
        if donacion <= 150:
            deducciones['donaciones'] = donacion * 0.80
        else:
            # Verificar si es plurianual (3+ años consecutivos)
            es_plurianual = datos.get('donacion_plurianual', False)
            porcentaje_resto = 0.40 if es_plurianual else 0.35
            deducciones['donaciones'] = 150 * 0.80 + (donacion - 150) * porcentaje_resto
    
    # 3. Maternidad (1.200€/año por hijo menor de 3 años)
    if datos.get('maternidad', False) and datos.get('hijos_menores_3', 0) > 0:
        deducciones['maternidad'] = datos.get('hijos_menores_3', 0) * 1200
    
    # 4. Familia numerosa estatal (1.200€)
    if datos.get('familia_numerosa', False):
        deducciones['familia_numerosa_estatal'] = 1200
    
    # === DEDUCCIONES AUTONÓMICAS ===
    comunidad = datos.get('comunidad', 'Madrid')
    
    # 5. Nacimiento/Adopción
    if datos.get('nacimiento_ultimo_ano', False):
        numero_hijo = datos.get('hijos_menores_3', 0) + datos.get('hijos_mayores_3', 0)
        deducciones['nacimiento_adopcion'] = calcular_deduccion_nacimiento(comunidad, numero_hijo)
    
    # 6. Familia numerosa autonómica
    if datos.get('familia_numerosa', False):
        tipo_fn = "especial" if datos.get('familia_numerosa_especial', False) else "general"
        deducciones['familia_numerosa_autonomica'] = calcular_deduccion_familia_numerosa(comunidad, tipo_fn)
    
    # 7. Alquiler vivienda habitual (autonómica)
    if datos.get('alquiler_vivienda_habitual_pagado', 0) > 0:
        deducciones['alquiler_vivienda_habitual'] = calcular_deduccion_alquiler(
            comunidad,
            datos.get('alquiler_vivienda_habitual_pagado', 0),
            datos.get('edad', 30)
        )
    
    # 8. Cuidado de menores (guarderías)
    gastos_guarderia = datos.get('gastos_guarderia', 0)
    if gastos_guarderia > 0:
        deducciones_ccaa = obtener_deducciones_autonomicas(comunidad)
        if 'gastos_guarderia' in deducciones_ccaa:
            gg = deducciones_ccaa['gastos_guarderia']
            limite = gg.get('limite', float('inf'))
            porcentaje = gg.get('porcentaje', 0)
            base = min(gastos_guarderia, limite)
            deducciones['cuidado_menores'] = base * porcentaje
    
    # Sumar estatales
    deducciones['total_estatal'] = (
        deducciones['vivienda_habitual'] +
        deducciones['donaciones'] +
        deducciones['maternidad'] +
        deducciones['familia_numerosa_estatal']
    )
    
    # Sumar autonómicas
    deducciones['total_autonomica'] = (
        deducciones['nacimiento_adopcion'] +
        deducciones['familia_numerosa_autonomica'] +
        deducciones['alquiler_vivienda_habitual'] +
        deducciones['cuidado_menores'] +
        deducciones['discapacidad_a_cargo'] +
        deducciones['otras_autonomicas']
    )
    
    # Limitar a cuotas
    deducciones['total_estatal'] = min(deducciones['total_estatal'], cuota_estatal)
    deducciones['total_autonomica'] = min(deducciones['total_autonomica'], cuota_autonomica)
    
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


def calcular_tipo_marginal(base, escala_autonomica):
    """Calcula el tipo marginal total (estatal + autonómico)"""
    # Buscamos en qué tramo está
    for limite, tipo_est in ESCALA_ESTATAL_GENERAL:
        if base <= limite:
            # Buscamos el tipo autonómico correspondiente
            for lim_aut, tipo_aut in escala_autonomica:
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
