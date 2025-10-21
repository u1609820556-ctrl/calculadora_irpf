import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from renta import calcular_renta_total

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
    .resultado-monto {
        font-size: 48px;
        font-weight: bold;
        margin: 20px 0;
    }
    .pagar {
        color: #ff6b6b;
    }
    .devolver {
        color: #51cf66;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
<div class="main-header">
    <h1>🧾 Calculadora de IRPF - España 2024</h1>
    <p>Calcula tu declaración de la renta de forma fácil y visual</p>
</div>
""", unsafe_allow_html=True)

# Información inicial
with st.expander("ℹ️ ¿Cómo funciona esta calculadora?"):
    st.write("""
    Esta calculadora te ayuda a estimar tu declaración de la renta aplicando:
    - ✅ Escalas impositivas estatales y autonómicas 2024
    - ✅ Mínimos personales y familiares
    - ✅ Deducciones por hijos, vivienda, donaciones y maternidad
    - ✅ Reducción del 60% en alquileres de vivienda
    - ✅ Cálculo real con retenciones (saber si pagas o devuelves)
    - ✅ **NUEVO:** Gráficos interactivos y visualización profesional
    
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
        
        # Calcular
        with st.spinner('Calculando tu declaración...'):
            resultado = calcular_renta_total(datos)
        
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
        
        # GRÁFICO 2: Tramos Progresivos (solo si hay impuestos)
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
            
            # Barras de base imponible por tramo
            fig_tramos.add_trace(go.Bar(
                name='Base en cada tramo',
                x=[t['Tramo'] for t in tramos_data],
                y=[t['Base'] for t in tramos_data],
                marker_color='#4dabf7',
                text=[f"{t['Base']:,.0f} €" for t in tramos_data],
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Base: %{y:,.2f} €<extra></extra>'
            ))
            
            # Línea de cuota resultante
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
        
        # === RECOMENDACIONES ===
        with st.expander("💡 Ver recomendaciones personalizadas"):
            if plan_pensiones < 1500 and resumen['base_imponible_general'] > 20000:
                st.success(f"🏦 **Plan de pensiones:** Aún puedes aportar hasta {1500 - plan_pensiones:.0f} € más y ahorrar en impuestos.")
            
            if alquiler_ingresos > 0 and alquiler_gastos == 0:
                st.warning("🏠 **Gastos de alquiler:** Revisa si tienes gastos deducibles (IBI, comunidad, seguros...).")
            
            if hijos_menores_3 > 0 and not maternidad:
                st.info(f"👶 **Deducción por maternidad:** Si eres madre trabajadora, podrías deducir {hijos_menores_3 * 1200:.0f} € adicionales.")
            
            st.write("""
            **Consejos generales:**
            - Guarda todos los certificados de retenciones
            - Conserva justificantes de donaciones y gastos deducibles
            - Consulta las deducciones específicas de tu comunidad
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>⚠️ Esta calculadora es orientativa. Para casos complejos, consulta con un asesor fiscal profesional.</p>
    <p>📅 Cálculos basados en normativa IRPF 2024</p>
</div>
""", unsafe_allow_html=True)