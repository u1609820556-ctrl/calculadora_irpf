import streamlit as st
import plotly.graph_objects as go
from renta import calcular_renta_total
from datetime import datetime

st.set_page_config(
    page_title="TaxCalc Pro - Calculadora IRPF Profesional",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS (mismo diseño oscuro minimalista)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #1a1d29;
        --bg-medium: #252837;
        --text-light: #e2e8f0;
        --text-medium: #94a3b8;
        --accent: #3b82f6;
        --accent-hover: #2563eb;
    }
    
    .main {
        font-family: 'Inter', sans-serif;
        background: var(--bg-dark);
        color: var(--text-light);
    }
    
    .block-container {
        padding: 2rem;
        max-width: 1400px;
        background: var(--bg-dark);
    }
    
    .hero-header {
        background: var(--bg-medium);
        padding: 3rem 2rem;
        border-radius: 12px;
        text-align: center;
        color: var(--text-light);
        margin-bottom: 2rem;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .hero-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--text-light);
    }
    
    .hero-header p {
        font-size: 1.1rem;
        color: var(--text-medium);
    }
    
    [data-testid="stExpander"] {
        background: transparent !important;
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .streamlit-expanderHeader {
        background: var(--bg-medium) !important;
        color: var(--text-light) !important;
        border-radius: 8px;
        font-weight: 600;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(59, 130, 246, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-medium);
        padding: 1.5rem;
        border-radius: 0 0 8px 8px;
    }
    
    .seccion-titulo {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-light);
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .resultado-hero {
        background: var(--bg-medium);
        padding: 3rem;
        border-radius: 12px;
        text-align: center;
        color: var(--text-light);
        margin: 2rem 0;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .resultado-monto {
        font-size: 4rem;
        font-weight: 800;
        margin: 1rem 0;
        color: var(--text-light);
    }
    
    .resultado-badge {
        display: inline-block;
        padding: 0.75rem 2rem;
        background: var(--accent);
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
    }
    
    .stButton > button {
        background: var(--accent);
        color: white;
        border: none;
        padding: 0.875rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: var(--accent-hover);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.875rem 1.5rem;
        border-radius: 8px 8px 0 0;
        font-weight: 500;
        color: var(--text-medium);
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent);
        color: white;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-light);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: var(--text-medium);
    }
    
    [data-testid="metric-container"] {
        background: var(--bg-medium);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 1.5rem;
        background: var(--bg-medium);
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .progress-step {
        flex: 1;
        text-align: center;
        color: var(--text-medium);
        font-weight: 500;
        position: relative;
    }
    
    section[data-testid="stSidebar"] {
        background: var(--bg-medium);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-light);
    }
    
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background: var(--bg-dark) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        color: var(--text-light) !important;
        padding: 0.625rem !important;
    }
    
    .stNumberInput input:focus,
    .stTextInput input:focus,
    .stSelectbox select:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    label {
        color: var(--text-light) !important;
        font-weight: 500 !important;
    }
    
    .stAlert {
        background: var(--bg-medium) !important;
        border-radius: 8px !important;
        border-left: 3px solid var(--accent) !important;
        color: var(--text-light) !important;
        padding: 1rem !important;
    }
    
    .stCheckbox label, .stRadio label {
        color: var(--text-light) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    p, span, div {
        color: var(--text-light);
    }
    
    .caption, small {
        color: var(--text-medium) !important;
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares
def generar_html_pdf(resultado, datos):
    cuota_dif = resultado['cuota_diferencial']
    resumen = resultado['resumen']
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Inter', Arial, sans-serif; margin: 40px; background: #1a1d29; color: #e2e8f0; }}
            .header {{ background: #252837; color: #e2e8f0; padding: 40px; text-align: center; border-radius: 12px; }}
            .resultado {{ font-size: 52px; font-weight: 800; margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #252837; }}
            th, td {{ border-bottom: 1px solid rgba(59, 130, 246, 0.3); padding: 16px; color: #e2e8f0; }}
            th {{ background-color: #3b82f6; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💼 TaxCalc Pro - Informe {datetime.now().year}</h1>
            <div class="resultado">{cuota_dif['resultado']}: {cuota_dif['importe']:,.2f} €</div>
        </div>
        <table>
            <tr><th>Concepto</th><th>Importe</th></tr>
            <tr><td>Base Imponible</td><td>{resumen['base_imponible_general']:,.2f} €</td></tr>
            <tr><td>Cuota Líquida</td><td>{resultado['cuotas_liquidas']['total']:,.2f} €</td></tr>
            <tr><td>Retenciones</td><td>{cuota_dif['total_pagado']:,.2f} €</td></tr>
            <tr><td><b>RESULTADO</b></td><td><b>{cuota_dif['importe']:,.2f} €</b></td></tr>
        </table>
    </body>
    </html>
    """
    return html

def calcular_optimizaciones(datos, resultado):
    optimizaciones = []
    ahorro_total = 0
    resumen = resultado['resumen']
    tipo_medio = resumen['tipo_medio'] / 100
    
    if datos.get('plan_pensiones', 0) < 1500 and resumen['base_imponible_general'] > 15000:
        margen = 1500 - datos.get('plan_pensiones', 0)
        ahorro = margen * tipo_medio
        optimizaciones.append({
            'icono': '🏦',
            'titulo': 'Plan de Pensiones',
            'accion': f"Aportar {margen:,.0f} € más",
            'ahorro': ahorro
        })
        ahorro_total += ahorro
    
    if datos.get('donaciones', 0) < 150 and resumen['base_imponible_general'] > 20000:
        donacion_sugerida = 150 - datos.get('donaciones', 0)
        ahorro = donacion_sugerida * 0.80
        optimizaciones.append({
            'icono': '❤️',
            'titulo': 'Donaciones',
            'accion': f"Donar {donacion_sugerida:,.0f} €",
            'ahorro': ahorro
        })
        ahorro_total += ahorro
    
    return optimizaciones, ahorro_total

if 'historial_calculos' not in st.session_state:
    st.session_state.historial_calculos = []

# SIDEBAR
with st.sidebar:
    st.markdown("### 💼 TaxCalc Pro")
    st.caption("Calculadora IRPF Profesional")
    st.markdown("---")
    
    menu = st.radio(
        "Navegación",
        ["🏠 Calculadora", "📊 Simulador", "📈 Historial", "💡 Guía"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📌 Tips Rápidos")
    st.info("💡 Guarda certificados")
    st.info("✅ Revisa deducciones CCAA")
    st.info("⏰ Campaña: Abril-Junio")

# CONTENIDO PRINCIPAL
if menu == "🏠 Calculadora":
    st.markdown("""
    <div class="hero-header">
        <h1>💼 TaxCalc Pro</h1>
        <p>Calculadora profesional IRPF 2024 - Versión completa</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="progress-container">
        <div class="progress-step active">
            <div style="font-size: 1.75rem;">👤</div>
            <div style="font-weight: 600; margin-top: 0.5rem; font-size: 0.9rem;">Personales</div>
        </div>
        <div class="progress-step">
            <div style="font-size: 1.75rem;">💰</div>
            <div style="font-weight: 600; margin-top: 0.5rem; font-size: 0.9rem;">Ingresos</div>
        </div>
        <div class="progress-step">
            <div style="font-size: 1.75rem;">📉</div>
            <div style="font-weight: 600; margin-top: 0.5rem; font-size: 0.9rem;">Deducciones</div>
        </div>
        <div class="progress-step">
            <div style="font-size: 1.75rem;">🎯</div>
            <div style="font-weight: 600; margin-top: 0.5rem; font-size: 0.9rem;">Resultado</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # PASO 1: DATOS PERSONALES
    with st.expander("👤 PASO 1: Datos Personales", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            comunidad = st.selectbox(
                "📍 Comunidad Autónoma",
                ["Selecciona tu comunidad", "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias",
                 "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña",
                 "Comunidad Valenciana", "Extremadura", "Galicia", "Madrid",
                 "Murcia", "Navarra", "País Vasco", "La Rioja", "Ceuta", "Melilla"],
                help="Importante: cada comunidad tiene deducciones específicas"
            )
            
            estado_civil = st.selectbox(
                "💍 Estado civil",
                ["Selecciona", "Soltero/a", "Casado/a (declaración conjunta)",
                 "Casado/a (declaración individual)", "Viudo/a", "Divorciado/a"]
            )
            
            edad = st.number_input("🎂 Edad", min_value=18, max_value=100, value=30)

        with col2:
            discapacidad = st.checkbox("♿ Certificado de discapacidad")
            if discapacidad:
                grado_discapacidad = st.number_input("Grado (%)", min_value=33, max_value=100, value=33)
            else:
                grado_discapacidad = 0
            
            familia_numerosa = st.checkbox("👨‍👩‍👧‍👦 Familia numerosa")
            if familia_numerosa:
                familia_numerosa_especial = st.checkbox("Familia numerosa especial (≥5 hijos)")
            else:
                familia_numerosa_especial = False

        st.markdown("**👶 Descendientes:**")
        col3, col4, col5 = st.columns(3)
        with col3:
            hijos_menores_3 = st.number_input("Menores de 3 años", 0, 10, 0)
        with col4:
            hijos_mayores_3 = st.number_input("Mayores de 3 años", 0, 10, 0)
        with col5:
            hijos_con_discapacidad = st.number_input("Con discapacidad", 0, 10, 0)
        
        nacimiento_ultimo_ano = st.checkbox("👶 Nacimiento/adopción en el último año")
        
        st.markdown("**👴 Ascendientes a cargo:**")
        col6, col7 = st.columns(2)
        with col6:
            ascendientes_mayores_65 = st.number_input("Mayores de 65 años", 0, 5, 0)
        with col7:
            ascendientes_mayores_75 = st.number_input("Mayores de 75 años", 0, 5, 0)

    # PASO 2: INGRESOS
    with st.expander("💰 PASO 2: Ingresos"):
        # Trabajo por cuenta ajena
        st.markdown('<div class="seccion-titulo">💵 Rendimientos del Trabajo</div>', unsafe_allow_html=True)
        col8, col9 = st.columns(2)
        with col8:
            salario = st.number_input("Salario bruto anual (€)", 0.0, value=0.0, step=1000.0)
        with col9:
            retenciones = st.number_input("Retenciones IRPF (€)", 0.0, value=0.0, step=100.0,
                                         help="Total retenido en nómina")
        
        # Autónomos
        st.markdown('<div class="seccion-titulo">🏪 Actividades Económicas (Autónomos)</div>', unsafe_allow_html=True)
        es_autonomo = st.checkbox("💼 Soy autónomo o tengo actividad económica")
        
        if es_autonomo:
            col10, col11 = st.columns(2)
            with col10:
                regimen_autonomo = st.selectbox(
                    "Régimen fiscal",
                    ["estimacion_directa_simplificada", "estimacion_directa_normal", "estimacion_objetiva"]
                )
                ingresos_autonomo = st.number_input("Ingresos actividad (€)", 0.0, value=0.0, step=1000.0)
            with col11:
                gastos_autonomo = st.number_input("Gastos deducibles (€)", 0.0, value=0.0, step=500.0)
                pagos_fraccionados_autonomo = st.number_input("Pagos fraccionados (€)", 0.0, value=0.0, step=100.0,
                                                              help="Modelo 130/131")
        else:
            regimen_autonomo = None
            ingresos_autonomo = 0
            gastos_autonomo = 0
            pagos_fraccionados_autonomo = 0
        
        # Inmobiliarios
        st.markdown('<div class="seccion-titulo">🏠 Rendimientos Inmobiliarios</div>', unsafe_allow_html=True)
        
        alquiler_ingresos = st.number_input("Ingresos por alquiler (€)", 0.0, value=0.0, step=1000.0)
        
        if alquiler_ingresos > 0:
            st.caption("💡 Puedes detallar gastos o poner total:")
            col12, col13, col14 = st.columns(3)
            with col12:
                ibi = st.number_input("IBI (€)", 0.0, value=0.0, step=100.0)
                comunidad = st.number_input("Comunidad (€)", 0.0, value=0.0, step=50.0)
            with col13:
                seguro_hogar = st.number_input("Seguro (€)", 0.0, value=0.0, step=50.0)
                reparaciones = st.number_input("Reparaciones (€)", 0.0, value=0.0, step=100.0)
            with col14:
                intereses_hipoteca = st.number_input("Intereses hipoteca (€)", 0.0, value=0.0, step=500.0)
                alquiler_gastos = st.number_input("Otros gastos (€)", 0.0, value=0.0, step=100.0)
            
            valor_construccion_alquiler = st.number_input(
                "Valor construcción (para amortización 3%)", 0.0, value=0.0, step=10000.0,
                help="70% del valor de compra aprox"
            )
            
            arrendatario_menor_30 = st.checkbox("El inquilino tiene menos de 30 años (reducción 70%)")
        else:
            ibi = comunidad = seguro_hogar = reparaciones = 0
            intereses_hipoteca = alquiler_gastos = valor_construccion_alquiler = 0
            arrendatario_menor_30 = False
        
        # Segunda vivienda
        tiene_segunda_vivienda = st.checkbox("🏘️ Tengo segunda vivienda no alquilada")
        if tiene_segunda_vivienda:
            col15, col16 = st.columns(2)
            with col15:
                valor_catastral_segunda = st.number_input("Valor catastral (€)", 0.0, value=0.0, step=10000.0)
            with col16:
                valor_catastral_revisado = st.checkbox("Valor catastral revisado post-1994")
        else:
            valor_catastral_segunda = 0
            valor_catastral_revisado = False
        
        # Capital mobiliario
        st.markdown('<div class="seccion-titulo">📈 Capital Mobiliario y Ganancias</div>', unsafe_allow_html=True)
        col17, col18 = st.columns(2)
        with col17:
            dividendos = st.number_input("Dividendos (€)", 0.0, value=0.0, step=100.0)
            intereses = st.number_input("Intereses bancarios (€)", 0.0, value=0.0, step=50.0)
        with col18:
            ganancias = st.number_input("Ganancias patrimoniales (€)", 0.0, value=0.0, step=500.0,
                                       help="Venta acciones, criptos, inmuebles")
            perdidas_patrimoniales = st.number_input("Pérdidas patrimoniales (€)", 0.0, value=0.0, step=500.0)
        
        perdidas_pendientes_anos_anteriores = st.number_input(
            "Pérdidas pendientes de años anteriores (€)", 0.0, value=0.0, step=500.0,
            help="Pérdidas de hasta 4 años atrás sin compensar"
        )

    # PASO 3: DEDUCCIONES
    with st.expander("📉 PASO 3: Deducciones y Reducciones"):
        st.markdown('<div class="seccion-titulo">🏦 Reducciones de la Base</div>', unsafe_allow_html=True)
        col19, col20 = st.columns(2)
        with col19:
            plan_pensiones = st.number_input("Plan de pensiones (€)", 0.0, value=0.0, step=100.0,
                                            help="Máximo: 1.500€/año")
            if es_autonomo:
                mutualidad = st.number_input("Mutualidad alternativa (€)", 0.0, value=0.0, step=100.0)
            else:
                mutualidad = 0
        with col20:
            pensiones_compensatorias = st.number_input("Pensiones compensatorias (€)", 0.0, value=0.0, step=100.0,
                                                       help="A favor del cónyuge")
        
        st.markdown('<div class="seccion-titulo">✅ Deducciones Estatales</div>', unsafe_allow_html=True)
        
        vivienda_habitual = st.checkbox("🏠 Vivienda habitual (compra pre-2013)")
        if vivienda_habitual:
            vivienda_importe = st.number_input("Importe pagado hipoteca (€)", 0.0, value=0.0, step=100.0)
        else:
            vivienda_importe = 0
        
        col21, col22 = st.columns(2)
        with col21:
            donaciones = st.number_input("❤️ Donaciones (€)", 0.0, value=0.0, step=50.0)
            if donaciones > 0:
                donacion_plurianual = st.checkbox("Donación plurianual (3+ años)")
            else:
                donacion_plurianual = False
        
        with col22:
            maternidad = st.checkbox("👶 Madre trabajadora (hijos <3 años)")
        
        st.markdown('<div class="seccion-titulo">🏘️ Deducciones Autonómicas</div>', unsafe_allow_html=True)
        st.caption(f"Específicas de: {comunidad if comunidad != 'Selecciona tu comunidad' else 'selecciona comunidad'}")
        
        col23, col24 = st.columns(2)
        with col23:
            alquiler_vivienda_habitual_pagado = st.number_input(
                "Alquiler vivienda habitual pagado (€/año)", 0.0, value=0.0, step=100.0,
                help="Lo que TÚ pagas de alquiler"
            )
        with col24:
            gastos_guarderia = st.number_input("Gastos guardería (€)", 0.0, value=0.0, step=100.0)

    st.markdown("---")
    
    # BOTÓN CALCULAR
    if st.button("🚀 CALCULAR DECLARACIÓN COMPLETA"):
        if comunidad == "Selecciona tu comunidad":
            st.error("⚠️ Selecciona tu comunidad autónoma")
        elif estado_civil == "Selecciona":
            st.error("⚠️ Selecciona tu estado civil")
        else:
            datos = {
                'comunidad': comunidad,
                'estado_civil': estado_civil,
                'edad': edad,
                'discapacidad': discapacidad,
                'grado_discapacidad': grado_discapacidad,
                'familia_numerosa': familia_numerosa,
                'familia_numerosa_especial': familia_numerosa_especial,
                'hijos_menores_3': hijos_menores_3,
                'hijos_mayores_3': hijos_mayores_3,
                'hijos_con_discapacidad': hijos_con_discapacidad,
                'nacimiento_ultimo_ano': nacimiento_ultimo_ano,
                'ascendientes_mayores_65_a_cargo': ascendientes_mayores_65,
                'ascendientes_mayores_75_a_cargo': ascendientes_mayores_75,
                'salario': salario,
                'retenciones': retenciones,
                'es_autonomo': es_autonomo,
                'regimen_autonomo': regimen_autonomo,
                'ingresos_autonomo': ingresos_autonomo,
                'gastos_autonomo': gastos_autonomo,
                'pagos_fraccionados_autonomo': pagos_fraccionados_autonomo,
                'alquiler_ingresos': alquiler_ingresos,
                'ibi': ibi,
                'comunidad': comunidad,
                'seguro_hogar': seguro_hogar,
                'reparaciones': reparaciones,
                'intereses_hipoteca': intereses_hipoteca,
                'alquiler_gastos': alquiler_gastos,
                'valor_construccion_alquiler': valor_construccion_alquiler,
                'arrendatario_menor_30': arrendatario_menor_30,
                'tiene_segunda_vivienda': tiene_segunda_vivienda,
                'valor_catastral_segunda': valor_catastral_segunda,
                'valor_catastral_revisado': valor_catastral_revisado,
                'dividendos': dividendos,
                'intereses': intereses,
                'ganancias': ganancias,
                'perdidas_patrimoniales': perdidas_patrimoniales,
                'perdidas_pendientes_anos_anteriores': perdidas_pendientes_anos_anteriores,
                'plan_pensiones': plan_pensiones,
                'mutualidad': mutualidad,
                'pensiones_compensatorias': pensiones_compensatorias,
                'vivienda_habitual': vivienda_habitual,
                'vivienda_importe': vivienda_importe,
                'donaciones': donaciones,
                'donacion_plurianual': donacion_plurianual,
                'maternidad': maternidad,
                'alquiler_vivienda_habitual_pagado': alquiler_vivienda_habitual_pagado,
                'gastos_guarderia': gastos_guarderia
            }
            
            st.session_state['datos_calculados'] = datos
            
            with st.spinner('🔮 Calculando declaración completa...'):
                resultado = calcular_renta_total(datos)
                st.session_state['resultado_calculado'] = resultado
                st.session_state.historial_calculos.append({
                    'fecha': datetime.now(),
                    'datos': datos,
                    'resultado': resultado
                })
            
            cuota_dif = resultado['cuota_diferencial']
            simbolo = "💸" if cuota_dif['diferencial'] > 0 else "💰"
            
            st.markdown(f"""
            <div class="resultado-hero">
                <div style="font-size: 1.1rem; color: #94a3b8; margin-bottom: 0.5rem;">Tu declaración de la renta</div>
                <div class="resultado-monto">{cuota_dif['importe']:,.2f} €</div>
                <div class="resultado-badge">{simbolo} {cuota_dif['resultado']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Avisos importantes
            if resultado.get('avisos'):
                for aviso in resultado['avisos']:
                    st.warning(f"⚠️ {aviso}")
            
            # Optimizador
            st.markdown('<div class="seccion-titulo">💡 Optimizador Fiscal</div>', unsafe_allow_html=True)
            
            optimizaciones, ahorro_total = calcular_optimizaciones(datos, resultado)
            
            if len(optimizaciones) > 0:
                st.info(f"🎯 **Ahorro potencial detectado:** {ahorro_total:,.0f} €")
                for opt in optimizaciones:
                    st.success(f"{opt['icono']} **{opt['titulo']}:** {opt['accion']} - Ahorro: **{opt['ahorro']:,.0f} €**")
            else:
                st.success("✅ Excelente aprovechamiento de deducciones")
            
            # Exportar
            st.markdown("---")
            html_pdf = generar_html_pdf(resultado, datos)
            st.download_button(
                label="📄 Descargar Informe",
                data=html_pdf,
                file_name=f"TaxCalc_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html"
            )
            
            # Gráficos
            st.markdown('<div class="seccion-titulo">📊 Análisis Visual</div>', unsafe_allow_html=True)
            
            resumen = resultado['resumen']
            cuotas = resultado['cuotas_integras']
            
            tab1, tab2, tab3 = st.tabs(["📊 Resumen", "📈 Tramos", "💰 Desglose"])
            
            with tab1:
                fig = go.Figure()
                valores = [
                    resumen['base_imponible_general'] + resumen['base_imponible_ahorro'],
                    resultado['cuotas_liquidas']['total'],
                    resultado['deducciones']['total_estatal'] + resultado['deducciones']['total_autonomica'],
                    cuota_dif['total_pagado']
                ]
                
                fig.add_trace(go.Bar(
                    x=['Ingresos', 'Impuestos', 'Deducciones', 'Ya Pagado'],
                    y=valores,
                    marker_color=['#3b82f6', '#ef4444', '#10b981', '#94a3b8'],
                    text=[f"{v:,.0f} €" for v in valores],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0'),
                    showlegend=False,
                    yaxis=dict(gridcolor='rgba(59, 130, 246, 0.1)')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                if cuotas['estatal_general'] > 0:
                    tramos_data = []
                    for tramo in cuotas['desglose_estatal_general']:
                        tramos_data.append({
                            'Tramo': f"{tramo['base']:,.0f} €",
                            'Base': tramo['base'],
                            'Cuota': tramo['cuota']
                        })
                    
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(
                        name='Base',
                        x=[t['Tramo'] for t in tramos_data],
                        y=[t['Base'] for t in tramos_data],
                        marker_color='#3b82f6'
                    ))
                    
                    fig2.add_trace(go.Scatter(
                        name='Cuota',
                        x=[t['Tramo'] for t in tramos_data],
                        y=[t['Cuota'] for t in tramos_data],
                        mode='lines+markers',
                        line=dict(color='#ef4444', width=3),
                        yaxis='y2'
                    ))
                    
                    fig2.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#e2e8f0'),
                        yaxis=dict(gridcolor='rgba(59, 130, 246, 0.1)', title='Base (€)'),
                        yaxis2=dict(title='Cuota (€)', overlaying='y', side='right', showgrid=False)
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    col_i1, col_i2 = st.columns(2)
                    with col_i1:
                        st.info(f"📊 **Tipo Marginal:** {resumen['tipo_marginal']:.2f}%")
                    with col_i2:
                        st.info(f"✅ **Tipo Medio:** {resumen['tipo_medio']:.2f}%")
            
            with tab3:
                st.subheader("Desglose detallado de ingresos")
                
                # Trabajo
                rt = resultado['rendimiento_trabajo']
                if rt['bruto'] > 0:
                    st.markdown("**👔 Rendimientos del Trabajo**")
                    col_d1, col_d2, col_d3 = st.columns(3)
                    with col_d1:
                        st.metric("Bruto", f"{rt['bruto']:,.0f} €")
                    with col_d2:
                        st.metric("Reducción", f"-{rt['reduccion']:,.0f} €")
                    with col_d3:
                        st.metric("Neto", f"{rt['neto']:,.0f} €")
                
                # Autónomos
                if es_autonomo:
                    ra = resultado['rendimiento_actividades']
                    st.markdown("**🏪 Actividad Económica**")
                    col_d4, col_d5, col_d6 = st.columns(3)
                    with col_d4:
                        st.metric("Ingresos", f"{ra['ingresos']:,.0f} €")
                    with col_d5:
                        st.metric("Gastos", f"-{ra['gastos']:,.0f} €")
                    with col_d6:
                        st.metric("Neto", f"{ra['neto']:,.0f} €")
                
                # Alquileres
                rci = resultado['rendimiento_capital_inmobiliario']
                if rci['ingresos'] > 0:
                    st.markdown("**🏠 Rendimientos Inmobiliarios**")
                    col_d7, col_d8, col_d9 = st.columns(3)
                    with col_d7:
                        st.metric("Ingresos", f"{rci['ingresos']:,.0f} €")
                    with col_d8:
                        st.metric("Gastos", f"-{rci['gastos_totales']:,.0f} €")
                    with col_d9:
                        st.metric("Neto", f"{rci['neto_final']:,.0f} €")
                    
                    with st.expander("Ver gastos detallados"):
                        for concepto, valor in rci['gastos_detallados'].items():
                            if valor > 0:
                                st.write(f"• {concepto.replace('_', ' ').title()}: {valor:,.2f} €")
                
                # Ganancias
                gp = resultado['ganancias_patrimoniales']
                if gp['ganancias_brutas'] > 0 or gp['perdidas_ejercicio'] > 0:
                    st.markdown("**📈 Ganancias Patrimoniales**")
                    col_d10, col_d11, col_d12 = st.columns(3)
                    with col_d10:
                        st.metric("Ganancias", f"{gp['ganancias_brutas']:,.0f} €")
                    with col_d11:
                        st.metric("Pérdidas", f"-{gp['perdidas_ejercicio']:,.0f} €")
                    with col_d12:
                        st.metric("Neto", f"{gp['ganancias_final']:,.0f} €")
            
            # Métricas clave
            st.markdown('<div class="seccion-titulo">📋 Métricas Clave</div>', unsafe_allow_html=True)
            
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            
            with col_m1:
                st.metric("Base Imponible", f"{resumen['base_imponible_general']:,.0f} €")
            with col_m2:
                st.metric("Cuota Íntegra", f"{cuotas['total']:,.0f} €")
            with col_m3:
                deducciones_total = resultado['deducciones']['total_estatal'] + resultado['deducciones']['total_autonomica']
                st.metric("Deducciones", f"{deducciones_total:,.0f} €")
            with col_m4:
                st.metric("Ya Pagado", f"{cuota_dif['total_pagado']:,.0f} €")

elif menu == "📊 Simulador":
    st.markdown("""
    <div class="hero-header">
        <h1>📊 Simulador Interactivo</h1>
        <p>Compara escenarios fiscales</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'datos_calculados' not in st.session_state:
        st.info("⚠️ Primero calcula tu declaración en 'Calculadora'")
    else:
        datos_base = st.session_state['datos_calculados']
        resultado_base = st.session_state['resultado_calculado']
        cuota_base = resultado_base['cuota_diferencial']
        
        st.info(f"📌 **Escenario Base:** {cuota_base['resultado']} - **{cuota_base['importe']:,.2f} €**")
        
        st.markdown("---")
        st.subheader("🎛️ Ajusta parámetros")
        
        col_sim1, col_sim2 = st.columns(2)
        
        with col_sim1:
            st.markdown("### 💰 Ingresos")
            salario_sim = st.slider(
                "💵 Salario",
                0,
                max(int(datos_base.get('salario', 0) * 2), 100000),
                int(datos_base.get('salario', 0)),
                1000
            )
        
        with col_sim2:
            st.markdown("### 📉 Deducciones")
            pension_sim = st.slider("🏦 Plan pensiones", 0, 1500, int(datos_base.get('plan_pensiones', 0)), 100)
        
        if st.button("🔄 SIMULAR"):
            datos_sim = datos_base.copy()
            datos_sim['salario'] = salario_sim
            datos_sim['plan_pensiones'] = pension_sim
            
            with st.spinner('🔮 Simulando...'):
                resultado_sim = calcular_renta_total(datos_sim)
            
            cuota_sim = resultado_sim['cuota_diferencial']
            diferencia = cuota_sim['importe'] - cuota_base['importe']
            
            col_comp1, col_comp2, col_comp3 = st.columns(3)
            
            with col_comp1:
                st.metric("Base", f"{cuota_base['importe']:,.0f} €")
            with col_comp2:
                st.metric("Simulado", f"{cuota_sim['importe']:,.0f} €")
            with col_comp3:
                st.metric("Diferencia", f"{abs(diferencia):,.0f} €", delta=f"{diferencia:,.0f} €")

elif menu == "📈 Historial":
    st.markdown("""
    <div class="hero-header">
        <h1>📈 Historial</h1>
        <p>Tus cálculos anteriores</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.historial_calculos) == 0:
        st.info("🔍 Aún no has realizado cálculos")
    else:
        st.info(f"📊 {len(st.session_state.historial_calculos)} cálculo(s) guardado(s)")
        
        for calculo in reversed(st.session_state.historial_calculos):
            fecha = calculo['fecha'].strftime('%d/%m/%Y %H:%M')
            resultado = calculo['resultado']
            cuota = resultado['cuota_diferencial']
            
            with st.expander(f"🗓️ {fecha} - {cuota['resultado']}: {cuota['importe']:,.2f} €"):
                col_h1, col_h2, col_h3 = st.columns(3)
                with col_h1:
                    st.metric("Resultado", f"{cuota['importe']:,.2f} €")
                with col_h2:
                    st.metric("Base", f"{resultado['resumen']['base_imponible_general']:,.2f} €")
                with col_h3:
                    st.metric("Tipo Medio", f"{resultado['resumen']['tipo_medio']:.2f}%")

elif menu == "💡 Guía":
    st.markdown("""
    <div class="hero-header">
        <h1>💡 Guía Rápida</h1>
        <p>Conceptos clave del IRPF</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📚 Conceptos", "❓ FAQ"])
    
    with tab1:
        with st.expander("🔍 ¿Qué es el IRPF?"):
            st.write("""
            **Impuesto progresivo:**
            - 📊 A mayor renta, mayor %
            - 🏛️ 50% Estatal + 50% Autonómico
            - 🗓️ Declaración anual (abril-junio)
            """)
        
        with st.expander("⚖️ Tramos 2024"):
            st.write("""
            | Base Imponible | Tipo Total |
            |----------------|------------|
            | Hasta 12.450€  | 19% |
            | 12.450-20.200€ | 24% |
            | 20.200-35.200€ | 30% |
            | 35.200-60.000€ | 37% |
            | 60.000-300.000€| 45% |
            | >300.000€      | 47% |
            """)
        
        with st.expander("💡 Deducciones principales"):
            st.write("""
            **Estatales:**
            - 🏦 Plan pensiones: hasta 1.500€
            - ❤️ Donaciones: 80% primeros 150€
            - 👶 Maternidad: 1.200€/hijo <3 años
            
            **Autonómicas:** Varían según comunidad
            """)
    
    with tab2:
        with st.expander("❓ ¿Estoy obligado?"):
            st.write("""
            **SÍ si tienes:**
            - Trabajo >22.000€ (un pagador)
            - Trabajo >15.000€ (varios)
            - Capital >1.600€
            - Alquileres >1.000€
            """)
        
        with st.expander("❓ ¿Cuándo declaro?"):
            st.write("📅 Del 3 abril al 1 julio 2025")
        
        with st.expander("❓ ¿Qué documentos necesito?"):
            st.write("""
            ✅ Certificado retenciones trabajo
            ✅ Certificados bancarios
            ✅ Facturas alquiler (si aplica)
            ✅ Justificantes deducciones
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 2rem;'>
    <p style='font-weight: 600; margin-bottom: 0.5rem; color: #e2e8f0;'>💼 TaxCalc Pro</p>
    <p style='font-size: 0.875rem;'>Calculadora profesional IRPF 2024</p>
    <p style='font-size: 0.75rem; margin-top: 1rem;'>v3.0 Professional Edition</p>
</div>
""", unsafe_allow_html=True)