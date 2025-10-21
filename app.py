import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from renta import calcular_renta_total
from io import BytesIO
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Calculadora IRPF España 2024",
    page_icon="🧾",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .resultado-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .optimizador-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .ahorro-potencial {
        font-size: 36px;
        font-weight: bold;
        color: #51cf66;
    }
</style>
""", unsafe_allow_html=True)

# Función para generar HTML del PDF
def generar_html_pdf(resultado, datos):
    """Genera HTML formateado para exportar como PDF"""
    cuota_dif = resultado['cuota_diferencial']
    resumen = resultado['resumen']
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .resultado {{ font-size: 48px; font-weight: bold; margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #667eea; color: white; }}
            .seccion {{ margin-top: 30px; page-break-inside: avoid; }}
            h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧾 Declaración de la Renta {datetime.now().year}</h1>
            <div class="resultado">
                {cuota_dif['resultado']}: {cuota_dif['importe']:,.2f} €
            </div>
            <p>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <div class="seccion">
            <h2>📊 Resumen Ejecutivo</h2>
            <table>
                <tr><th>Concepto</th><th>Importe</th></tr>
                <tr><td>Base Imponible General</td><td>{resumen['base_imponible_general']:,.2f} €</td></tr>
                <tr><td>Base Imponible Ahorro</td><td>{resumen['base_imponible_ahorro']:,.2f} €</td></tr>
                <tr><td>Cuota Íntegra</td><td>{resultado['cuotas_integras']['total']:,.2f} €</td></tr>
                <tr><td>Deducciones</td><td>{resultado['deducciones']['total_estatal'] + resultado['deducciones']['total_autonomica']:,.2f} €</td></tr>
                <tr><td>Cuota Líquida</td><td>{resultado['cuotas_liquidas']['total']:,.2f} €</td></tr>
                <tr><td>Retenciones Practicadas</td><td>{cuota_dif['retenciones']:,.2f} €</td></tr>
                <tr style="background: #f0f0f0; font-weight: bold;">
                    <td>RESULTADO FINAL</td>
                    <td>{cuota_dif['resultado']}: {cuota_dif['importe']:,.2f} €</td>
                </tr>
            </table>
        </div>
        
        <div class="seccion">
            <h2>💡 Tipos Impositivos</h2>
            <p><strong>Tipo Medio Efectivo:</strong> {resumen['tipo_medio']:.2f}%</p>
            <p><strong>Tipo Marginal:</strong> {resumen['tipo_marginal']:.2f}%</p>
        </div>
        
        <div class="seccion">
            <h2>👤 Datos Personales</h2>
            <table>
                <tr><td>Comunidad Autónoma</td><td>{datos['comunidad']}</td></tr>
                <tr><td>Estado Civil</td><td>{datos['estado_civil']}</td></tr>
                <tr><td>Edad</td><td>{datos['edad']} años</td></tr>
                <tr><td>Hijos menores de 3 años</td><td>{datos['hijos_menores_3']}</td></tr>
                <tr><td>Hijos mayores de 3 años</td><td>{datos['hijos_mayores_3']}</td></tr>
            </table>
        </div>
        
        <div class="seccion">
            <h2>💰 Desglose de Ingresos</h2>
            <table>
                <tr><th>Concepto</th><th>Importe</th></tr>
                <tr><td>Salario Bruto</td><td>{resultado['rendimiento_trabajo']['bruto']:,.2f} €</td></tr>
                <tr><td>Rendimiento Trabajo Neto</td><td>{resultado['rendimiento_trabajo']['neto']:,.2f} €</td></tr>
                <tr><td>Rendimiento Capital Inmobiliario</td><td>{resultado['rendimiento_capital_inmobiliario']['neto_final']:,.2f} €</td></tr>
                <tr><td>Rendimiento Capital Mobiliario</td><td>{resultado['rendimiento_capital_mobiliario']['total']:,.2f} €</td></tr>
                <tr><td>Ganancias Patrimoniales</td><td>{resultado['ganancias_patrimoniales']['total']:,.2f} €</td></tr>
            </table>
        </div>
        
        <div class="seccion">
            <h2>🧮 Cálculo por Tramos (Parte Estatal)</h2>
            <table>
                <tr><th>Base del Tramo</th><th>Tipo</th><th>Cuota</th></tr>
    """
    
    for tramo in resultado['cuotas_integras']['desglose_estatal_general']:
        html += f"""
                <tr>
                    <td>{tramo['base']:,.2f} €</td>
                    <td>{tramo['tipo']*100:.2f}%</td>
                    <td>{tramo['cuota']:,.2f} €</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="seccion" style="margin-top: 50px; text-align: center; color: #666; font-size: 12px;">
            <p>⚠️ Esta calculadora es orientativa. Para casos complejos, consulta con un asesor fiscal profesional.</p>
            <p>📅 Cálculos basados en normativa IRPF 2024</p>
        </div>
    </body>
    </html>
    """
    return html

# Función para optimizar fiscalmente
def calcular_optimizaciones(datos, resultado):
    """Analiza y sugiere optimizaciones fiscales"""
    optimizaciones = []
    ahorro_total = 0
    resumen = resultado['resumen']
    tipo_medio = resumen['tipo_medio'] / 100
    
    # 1. Plan de pensiones
    if datos['plan_pensiones'] < 1500 and resumen['base_imponible_general'] > 15000:
        margen = 1500 - datos['plan_pensiones']
        ahorro = margen * tipo_medio
        optimizaciones.append({
            'tipo': '🏦 Plan de Pensiones',
            'accion': f"Aportar {margen:,.0f} € más",
            'ahorro': ahorro,
            'detalle': f"Aprovecha el límite máximo de 1.500€/año. Por cada 100€ que aportes, ahorras {tipo_medio*100:.1f}€ en impuestos."
        })
        ahorro_total += ahorro
    
    # 2. Donaciones
    if datos['donaciones'] == 0 and resumen['base_imponible_general'] > 20000:
        donacion_sugerida = 150
        ahorro = donacion_sugerida * 0.80  # 80% primeros 150€
        optimizaciones.append({
            'tipo': '❤️ Donaciones',
            'accion': f"Donar {donacion_sugerida}€ a ONGs",
            'ahorro': ahorro,
            'detalle': "Los primeros 150€ en donaciones tienen una deducción del 80%. Ayudas y ahorras impuestos."
        })
        ahorro_total += ahorro
    
    # 3. Gastos alquiler
    if datos['alquiler_ingresos'] > 0 and datos['alquiler_gastos'] < datos['alquiler_ingresos'] * 0.2:
        gasto_estimado = datos['alquiler_ingresos'] * 0.25
        ahorro_base = (gasto_estimado - datos['alquiler_gastos']) * 0.4  # 40% de lo que no se reduce al 60%
        ahorro = ahorro_base * tipo_medio
        optimizaciones.append({
            'tipo': '🏠 Gastos de Alquiler',
            'accion': f"Revisar gastos deducibles",
            'ahorro': ahorro,
            'detalle': "IBI, comunidad, seguros, reparaciones... El 60% del rendimiento neto está exento. Asegúrate de incluir todos los gastos."
        })
        ahorro_total += ahorro
    
    # 4. Maternidad
    if datos['hijos_menores_3'] > 0 and not datos['maternidad'] and datos['salario'] > 0:
        ahorro = datos['hijos_menores_3'] * 1200
        optimizaciones.append({
            'tipo': '👶 Deducción por Maternidad',
            'accion': "Activar deducción maternal",
            'ahorro': ahorro,
            'detalle': f"Si eres madre trabajadora con hijos menores de 3 años, puedes deducir 1.200€ por cada hijo."
        })
        ahorro_total += ahorro
    
    # 5. Vivienda habitual (si aplica)
    if not datos['vivienda_habitual'] and resumen['base_imponible_general'] > 25000:
        optimizaciones.append({
            'tipo': '🏠 Vivienda Habitual',
            'accion': "Verificar si aplica deducción",
            'ahorro': 0,
            'detalle': "Si compraste tu vivienda antes de 2013, podrías deducir hasta 1.356€/año. Verifica tus fechas."
        })
    
    return optimizaciones, ahorro_total

# Título principal
st.markdown("""
<div class="main-header">
    <h1>🧾 Calculadora de IRPF - España 2024</h1>
    <p>Calcula, simula y optimiza tu declaración de la renta</p>
</div>
""", unsafe_allow_html=True)

# Tabs para organizar funcionalidades
tab1, tab2 = st.tabs(["📝 Calculadora Principal", "🎯 Simulador Interactivo"])

with tab1:
    # Información inicial
    with st.expander("ℹ️ ¿Cómo funciona esta calculadora?"):
        st.write("""
        Esta calculadora te ayuda a estimar tu declaración de la renta aplicando:
        - ✅ Escalas impositivas estatales y autonómicas 2024
        - ✅ Mínimos personales y familiares
        - ✅ Deducciones por hijos, vivienda, donaciones y maternidad
        - ✅ Reducción del 60% en alquileres de vivienda
        - ✅ Cálculo real con retenciones (saber si pagas o devuelves)
        - ✅ **Gráficos interactivos** y visualización profesional
        - ✅ **Optimizador fiscal** que detecta ahorros potenciales
        - ✅ **Exportar PDF** con tu informe completo
        
        **⚠️ Nota:** Esta es una herramienta orientativa. Para casos complejos, consulta con un asesor fiscal.
        """)

    # Formulario en columnas
    st.markdown("---")
    st.header("📝 Introduce tus datos")

    # === DATOS PERSONALES ===
    st.subheader("👤 Datos Personales")
    col1, col2 = st.columns(2)

    with col1:
        comunidad = st.selectbox(
            "📍 Comunidad Autónoma",
            ["Selecciona tu comunidad", "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias",
             "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña",
             "Comunidad Valenciana", "Extremadura", "Galicia", "Madrid",
             "Murcia", "Navarra", "País Vasco", "La Rioja", "Ceuta", "Melilla"]
        )
        
        estado_civil = st.selectbox(
            "💍 Estado civil",
            ["Selecciona", "Soltero/a", "Casado/a (declaración conjunta)",
             "Casado/a (declaración individual)", "Viudo/a", "Divorciado/a"]
        )

    with col2:
        edad = st.number_input("🎂 Edad", min_value=18, max_value=100, value=30)
        discapacidad = st.checkbox("♿ Tengo certificado de discapacidad (≥33%)")

    st.write("**👶 Hijos a cargo:**")
    col3, col4 = st.columns(2)
    with col3:
        hijos_menores_3 = st.number_input("Menores de 3 años", min_value=0, max_value=10, value=0)
    with col4:
        hijos_mayores_3 = st.number_input("Mayores de 3 años", min_value=0, max_value=10, value=0)

    st.markdown("---")

    # === INGRESOS ===
    st.subheader("💰 Ingresos del Trabajo")
    col5, col6 = st.columns(2)

    with col5:
        salario = st.number_input("💵 Salario bruto anual (€)", min_value=0.0, value=0.0, step=1000.0)
    with col6:
        retenciones = st.number_input("🧾 Retenciones IRPF practicadas (€)", min_value=0.0, value=0.0, step=100.0,
                                      help="Mira tu nómina o certificado de la empresa")

    st.subheader("🏠 Rendimientos del Capital Inmobiliario")
    col7, col8 = st.columns(2)

    with col7:
        alquiler_ingresos = st.number_input("💶 Ingresos brutos por alquiler (€)", min_value=0.0, value=0.0, step=1000.0)
    with col8:
        alquiler_gastos = st.number_input("🔧 Gastos deducibles del alquiler (€)", min_value=0.0, value=0.0, step=100.0,
                                          help="IBI, comunidad, reparaciones, intereses...")

    st.subheader("📈 Otros Ingresos")
    col9, col10 = st.columns(2)

    with col9:
        dividendos = st.number_input("💹 Dividendos e intereses (€)", min_value=0.0, value=0.0, step=100.0)
    with col10:
        ganancias = st.number_input("📊 Ganancias patrimoniales (€)", min_value=0.0, value=0.0, step=1000.0,
                                    help="Venta de acciones, criptos, inmuebles...")

    st.markdown("---")

    # === DEDUCCIONES ===
    st.subheader("📉 Deducciones y Reducciones")

    plan_pensiones = st.number_input("🏦 Aportaciones a planes de pensiones (€)", min_value=0.0, value=0.0, step=100.0,
                                     help="Máximo deducible: 1.500€/año")

    vivienda_habitual = st.checkbox("🏠 Compré vivienda habitual antes de 2013 (deducción estatal)")
    vivienda_importe = 0.0
    if vivienda_habitual:
        vivienda_importe = st.number_input("Cantidad pagada por hipoteca (€)", min_value=0.0, value=0.0, step=100.0)

    donaciones = st.number_input("❤️ Donaciones (€)", min_value=0.0, value=0.0, step=50.0,
                                 help="A ONGs, fundaciones, iglesia...")

    maternidad = st.checkbox("👶 Madre trabajadora con hijos menores de 3 años (deducción 1.200€/hijo)")

    st.markdown("---")

    # === BOTÓN DE CÁLCULO ===
    if st.button("🧮 CALCULAR DECLARACIÓN", type="primary", use_container_width=True):
        
        # Validaciones
        if comunidad == "Selecciona tu comunidad":
            st.error("⚠️ Por favor, selecciona tu comunidad autónoma")
        elif estado_civil == "Selecciona":
            st.error("⚠️ Por favor, selecciona tu estado civil")
        else:
            # Preparar datos
            datos = {
                'comunidad': comunidad,
                'estado_civil': estado_civil,
                'edad': edad,
                'discapacidad': discapacidad,
                'hijos_menores_3': hijos_menores_3,
                'hijos_mayores_3': hijos_mayores_3,
                'salario': salario,
                'retenciones': retenciones,
                'alquiler_ingresos': alquiler_ingresos,
                'alquiler_gastos': alquiler_gastos,
                'dividendos': dividendos,
                'ganancias': ganancias,
                'plan_pensiones': plan_pensiones,
                'vivienda_habitual': vivienda_habitual,
                'vivienda_importe': vivienda_importe,
                'donaciones': donaciones,
                'maternidad': maternidad
            }
            
            # Guardar en session_state para el simulador
            st.session_state['datos_calculados'] = datos
            
            # Calcular
            with st.spinner('Calculando tu declaración...'):
                resultado = calcular_renta_total(datos)
                st.session_state['resultado_calculado'] = resultado
            
            cuota_dif = resultado['cuota_diferencial']
            
            # RESULTADO PRINCIPAL
            color_clase = "pagar" if cuota_dif['diferencial'] > 0 else "devolver"
            simbolo = "💸" if cuota_dif['diferencial'] > 0 else "💰"
            
            st.markdown(f"""
            <div class="resultado-box">
                <h1>{simbolo} RESULTADO DE TU DECLARACIÓN</h1>
                <div class="resultado-monto {color_clase}">{cuota_dif['importe']:,.2f} €</div>
                <h2>{cuota_dif['resultado']}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # === OPTIMIZADOR FISCAL ===
            st.header("💡 Optimizador Fiscal Inteligente")
            
            optimizaciones, ahorro_total = calcular_optimizaciones(datos, resultado)
            
            if len(optimizaciones) > 0:
                st.markdown(f"""
                <div class="optimizador-box">
                    <h2>🎯 ¡Puedes ahorrar hasta <span class="ahorro-potencial">{ahorro_total:,.2f} €</span>!</h2>
                    <p>Hemos detectado {len(optimizaciones)} oportunidades de optimización fiscal</p>
                </div>
                """, unsafe_allow_html=True)
                
                for opt in optimizaciones:
                    with st.expander(f"{opt['tipo']} - Ahorro: {opt['ahorro']:,.2f} €"):
                        st.write(f"**Acción sugerida:** {opt['accion']}")
                        st.write(f"**Detalle:** {opt['detalle']}")
                        if opt['ahorro'] > 0:
                            st.success(f"💰 Ahorro estimado: **{opt['ahorro']:,.2f} €**")
            else:
                st.success("✅ ¡Excelente! Estás aprovechando bien las deducciones disponibles.")
            
            # === BOTÓN EXPORTAR PDF ===
            st.markdown("---")
            html_pdf = generar_html_pdf(resultado, datos)
            
            st.download_button(
                label="📄 Descargar Informe Completo (HTML)",
                data=html_pdf,
                file_name=f"declaracion_renta_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
            
            st.info("💡 **Tip:** Abre el archivo HTML descargado en tu navegador y usa Ctrl+P para guardarlo como PDF")
            
            # === GRÁFICOS INTERACTIVOS ===
            st.header("📊 Visualización Interactiva")
            
            resumen = resultado['resumen']
            cuotas = resultado['cuotas_integras']
            
            # GRÁFICO 1: Comparativa Ingresos vs Impuestos vs Deducciones
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                st.subheader("💰 Desglose General")
                
                fig_barras = go.Figure()
                
                fig_barras.add_trace(go.Bar(
                    name='Ingresos Totales',
                    x=['Tu Situación'],
                    y=[resumen['base_imponible_general'] + resumen['base_imponible_ahorro']],
                    marker_color='#51cf66',
                    text=[f"{resumen['base_imponible_general'] + resumen['base_imponible_ahorro']:,.0f} €"],
                    textposition='auto',
                ))
                
                fig_barras.add_trace(go.Bar(
                    name='Impuestos',
                    x=['Tu Situación'],
                    y=[resultado['cuotas_liquidas']['total']],
                    marker_color='#ff6b6b',
                    text=[f"{resultado['cuotas_liquidas']['total']:,.0f} €"],
                    textposition='auto',
                ))
                
                fig_barras.add_trace(go.Bar(
                    name='Deducciones',
                    x=['Tu Situación'],
                    y=[resultado['deducciones']['total_estatal'] + resultado['deducciones']['total_autonomica']],
                    marker_color='#4dabf7',
                    text=[f"{resultado['deducciones']['total_estatal'] + resultado['deducciones']['total_autonomica']:,.0f} €"],
                    textposition='auto',
                ))
                
                fig_barras.update_layout(
                    barmode='group',
                    height=400,
                    showlegend=True,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_barras, use_container_width=True)
            
            with col_graf2:
                st.subheader("🥧 Distribución de Impuestos")
                
                fig_pastel = go.Figure(data=[go.Pie(
                    labels=['Cuota Estatal', 'Cuota Autonómica', 'Retenciones Ya Pagadas'],
                    values=[
                        cuotas['estatal_total'],
                        cuotas['autonomica_total'],
                        cuota_dif['retenciones']
                    ],
                    marker=dict(colors=['#667eea', '#764ba2', '#51cf66']),
                    hole=0.4,
                    textinfo='label+percent+value',
                    texttemplate='%{label}<br>%{value:,.0f} €<br>(%{percent})',
                )])
                
                fig_pastel.update_layout(
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_pastel, use_container_width=True)
            
            # GRÁFICO 2: Tramos Progresivos
            if cuotas['estatal_general'] > 0:
                st.subheader("📈 Tu Progresión por Tramos Impositivos")
                
                tramos_data = []
                for tramo in cuotas['desglose_estatal_general']:
                    tramos_data.append({
                        'Tramo': f"{tramo['base']:,.0f} €",
                        'Tipo': f"{tramo['tipo']*100:.1f}%",
                        'Base': tramo['base'],
                        'Cuota': tramo['cuota']
                    })
                
                fig_tramos = go.Figure()
                
                fig_tramos.add_trace(go.Bar(
                    name='Base en cada tramo',
                    x=[t['Tramo'] for t in tramos_data],
                    y=[t['Base'] for t in tramos_data],
                    marker_color='#4dabf7',
                    text=[f"{t['Base']:,.0f} €" for t in tramos_data],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Base: %{y:,.2f} €<extra></extra>'
                ))
                
                fig_tramos.add_trace(go.Scatter(
                    name='Impuesto en cada tramo',
                    x=[t['Tramo'] for t in tramos_data],
                    y=[t['Cuota'] for t in tramos_data],
                    mode='lines+markers+text',
                    line=dict(color='#ff6b6b', width=3),
                    marker=dict(size=10),
                    text=[f"{t['Cuota']:,.0f} €" for t in tramos_data],
                    textposition='top center',
                    yaxis='y2',
                    hovertemplate='<b>%{x}</b><br>Impuesto: %{y:,.2f} €<extra></extra>'
                ))
                
                fig_tramos.update_layout(
                    height=400,
                    xaxis_title="Tramos",
                    yaxis_title="Base Imponible (€)",
                    yaxis2=dict(
                        title="Cuota Impuesto (€)",
                        overlaying='y',
                        side='right'
                    ),
                    hovermode='x unified',
                    showlegend=True
                )
                
                st.plotly_chart(fig_tramos, use_container_width=True)
                
                st.info(f"""
                💡 **Interpretación:** 
                - Las barras azules muestran cuánto de tu base imponible cae en cada tramo
                - La línea roja muestra el impuesto que pagas en cada tramo
                - Tu tipo marginal (último tramo) es **{resumen['tipo_marginal']:.2f}%**
                - Tu tipo medio efectivo es **{resumen['tipo_medio']:.2f}%**
                """)
            
            # === RESUMEN EJECUTIVO ===
            st.header("📋 Resumen Ejecutivo")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric("Base Imponible General", f"{resumen['base_imponible_general']:,.2f} €")
                st.metric("Base Imponible Ahorro", f"{resumen['base_imponible_ahorro']:,.2f} €")
            
            with col_res2:
                st.metric("Cuota Íntegra", f"{resultado['cuotas_integras']['total']:,.2f} €")
                st.metric("Deducciones", f"{resultado['deducciones']['total_estatal'] + resultado['deducciones']['total_autonomica']:,.2f} €")
            
            with col_res3:
                st.metric("Cuota Líquida", f"{resultado['cuotas_liquidas']['total']:,.2f} €")
                st.metric("Retenciones", f"{cuota_dif['retenciones']:,.2f} €")
            
            # Tipos impositivos
            st.info(f"""
            📌 **Tu tipo medio efectivo:** {resumen['tipo_medio']:.2f}%  
            📌 **Tu tipo marginal:** {resumen['tipo_marginal']:.2f}%
            
            *El tipo medio es el porcentaje real que pagas. El tipo marginal es lo que pagas por cada euro adicional.*
            """)
            
            # === DESGLOSE DETALLADO ===
            with st.expander("💰 Ver desglose detallado de ingresos"):
                rt = resultado['rendimiento_trabajo']
                if rt['bruto'] > 0:
                    st.subheader("👔 Rendimientos del Trabajo")
                    st.write(f"- Salario bruto: **{rt['bruto']:,.2f} €**")
                    st.write(f"- Reducción por trabajo: **-{rt['reduccion']:,.2f} €**")
                    st.write(f"- **Rendimiento neto: {rt['neto']:,.2f} €**")
                
                rci = resultado['rendimiento_capital_inmobiliario']
                if rci['ingresos'] > 0:
                    st.subheader("🏠 Rendimientos Alquileres")
                    st.write(f"- Ingresos: **{rci['ingresos']:,.2f} €**")
                    st.write(f"- Gastos: **-{rci['gastos']:,.2f} €**")
                    st.write(f"- Reducción 60%: **-{rci['reduccion_60']:,.2f} €**")
                    st.write(f"- **Rendimiento neto: {rci['neto_final']:,.2f} €**")
            
            # === MÍNIMO PERSONAL Y FAMILIAR ===
            with st.expander("👨‍👩‍👧‍👦 Ver mínimo personal y familiar"):
                mpf = resultado['minimo_personal_familiar']
                st.info("El mínimo personal y familiar es la cantidad que NO tributa porque se considera mínimo vital.")
                st.write(f"- Mínimo del contribuyente: **{mpf['contribuyente']:,.2f} €**")
                if mpf['descendientes'] > 0:
                    st.write(f"- Mínimo por {mpf['total_hijos']} hijo(s): **{mpf['descendientes']:,.2f} €**")
                st.write(f"- **Total exento: {mpf['total']:,.2f} €**")

# TAB 2: SIMULADOR INTERACTIVO
with tab2:
    st.header("🎯 Simulador Interactivo 'Qué pasaría si...'")
    
    st.info("""
    **¿Cómo funciona?**  
    Primero calcula tu declaración en la pestaña principal. Luego vuelve aquí para simular diferentes escenarios 
    y ver cómo afectan cambios en tu salario, deducciones o situación familiar.
    """)
    
    if 'datos_calculados' not in st.session_state or 'resultado_calculado' not in st.session_state:
        st.warning("⚠️ Primero calcula tu declaración en la pestaña 'Calculadora Principal'")
    else:
        datos_base = st.session_state['datos_calculados']
        resultado_base = st.session_state['resultado_calculado']
        
        st.success(f"""
        **Escenario Base (tu situación actual):**  
        Resultado: **{resultado_base['cuota_diferencial']['resultado']}** - **{resultado_base['cuota_diferencial']['importe']:,.2f} €**
        """)
        
        st.markdown("---")
        st.subheader("🔧 Ajusta los parámetros para simular")
        
        col_sim1, col_sim2 = st.columns(2)
        
        with col_sim1:
            st.write("**💰 Ingresos**")
            salario_sim = st.slider(
                "Salario anual (€)",
                min_value=0,
                max_value=int(datos_base['salario'] * 2) if datos_base['salario'] > 0 else 100000,
                value=int(datos_base['salario']),
                step=1000
            )
            
            alquiler_sim = st.slider(
                "Ingresos por alquiler (€)",
                min_value=0,
                max_value=int(datos_base['alquiler_ingresos'] * 2) if datos_base['alquiler_ingresos'] > 0 else 50000,
                value=int(datos_base['alquiler_ingresos']),
                step=1000
            )
        
        with col_sim2:
            st.write("**📉 Deducciones**")
            pension_sim = st.slider(
                "Plan de pensiones (€)",
                min_value=0,
                max_value=1500,
                value=int(datos_base['plan_pensiones']),
                step=100
            )
            
            donaciones_sim = st.slider(
                "Donaciones (€)",
                min_value=0,
                max_value=5000,
                value=int(datos_base['donaciones']),
                step=50
            )
        
        st.markdown("---")
        
        if st.button("🔄 SIMULAR NUEVO ESCENARIO", type="primary", use_container_width=True):
            # Crear datos simulados
            datos_sim = datos_base.copy()
            datos_sim['salario'] = salario_sim
            datos_sim['alquiler_ingresos'] = alquiler_sim
            datos_sim['plan_pensiones'] = pension_sim
            datos_sim['donaciones'] = donaciones_sim
            
            # Calcular nuevo escenario
            with st.spinner('Simulando nuevo escenario...'):
                resultado_sim = calcular_renta_total(datos_sim)
            
            cuota_base = resultado_base['cuota_diferencial']
            cuota_sim = resultado_sim['cuota_diferencial']
            
            # COMPARACIÓN LADO A LADO
            st.header("📊 Comparación de Escenarios")
            
            col_comp1, col_comp2, col_comp3 = st.columns(3)
            
            with col_comp1:
                st.markdown("### 📌 Escenario BASE")
                st.metric("Resultado", f"{cuota_base['importe']:,.2f} €")
                st.write(f"**{cuota_base['resultado']}**")
            
            with col_comp2:
                st.markdown("### 🔮 Escenario SIMULADO")
                st.metric("Resultado", f"{cuota_sim['importe']:,.2f} €")
                st.write(f"**{cuota_sim['resultado']}**")
            
            with col_comp3:
                st.markdown("### 📈 DIFERENCIA")
                diferencia = cuota_sim['importe'] - cuota_base['importe']
                color_delta = "normal" if diferencia < 0 else "inverse"
                st.metric(
                    "Cambio",
                    f"{abs(diferencia):,.2f} €",
                    delta=f"{diferencia:,.2f} €",
                    delta_color=color_delta
                )
                
                if diferencia < 0:
                    st.success(f"✅ Ahorrarías {abs(diferencia):,.2f} €")
                elif diferencia > 0:
                    st.error(f"⚠️ Pagarías {diferencia:,.2f} € más")
                else:
                    st.info("Sin cambios")
            
            # GRÁFICO COMPARATIVO
            st.subheader("📊 Comparativa Visual")
            
            fig_comp = go.Figure()
            
            fig_comp.add_trace(go.Bar(
                name='Escenario Base',
                x=['Ingresos', 'Impuestos', 'Deducciones'],
                y=[
                    resultado_base['resumen']['base_imponible_general'],
                    resultado_base['cuotas_liquidas']['total'],
                    resultado_base['deducciones']['total_estatal'] + resultado_base['deducciones']['total_autonomica']
                ],
                marker_color='#667eea'
            ))
            
            fig_comp.add_trace(go.Bar(
                name='Escenario Simulado',
                x=['Ingresos', 'Impuestos', 'Deducciones'],
                y=[
                    resultado_sim['resumen']['base_imponible_general'],
                    resultado_sim['cuotas_liquidas']['total'],
                    resultado_sim['deducciones']['total_estatal'] + resultado_sim['deducciones']['total_autonomica']
                ],
                marker_color='#51cf66'
            ))
            
            fig_comp.update_layout(
                barmode='group',
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # DETALLES DE CAMBIOS
            with st.expander("🔍 Ver detalles de los cambios"):
                st.write("**Cambios en tus datos:**")
                if salario_sim != datos_base['salario']:
                    st.write(f"- Salario: {datos_base['salario']:,.0f} € → {salario_sim:,.0f} € ({salario_sim - datos_base['salario']:+,.0f} €)")
                if alquiler_sim != datos_base['alquiler_ingresos']:
                    st.write(f"- Alquiler: {datos_base['alquiler_ingresos']:,.0f} € → {alquiler_sim:,.0f} € ({alquiler_sim - datos_base['alquiler_ingresos']:+,.0f} €)")
                if pension_sim != datos_base['plan_pensiones']:
                    st.write(f"- Plan pensiones: {datos_base['plan_pensiones']:,.0f} € → {pension_sim:,.0f} € ({pension_sim - datos_base['plan_pensiones']:+,.0f} €)")
                if donaciones_sim != datos_base['donaciones']:
                    st.write(f"- Donaciones: {datos_base['donaciones']:,.0f} € → {donaciones_sim:,.0f} € ({donaciones_sim - datos_base['donaciones']:+,.0f} €)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>⚠️ Esta calculadora es orientativa. Para casos complejos, consulta con un asesor fiscal profesional.</p>
    <p>📅 Cálculos basados en normativa IRPF 2024</p>
    <p>🚀 Versión 2.0 - Con simulador, optimizador y exportación</p>
</div>
""", unsafe_allow_html=True)