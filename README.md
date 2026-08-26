"""
FinanData AI - Dashboard comercial (Streamlit)
Versión ajustada con componentes nativos para compatibilidad total con Modo Oscuro/Claro.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ----------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# FUNCIONES DE UTILIDAD Y CÁLCULOS
# ----------------------------------------------------------------------
def to_number(v):
    if pd.isna(v):
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(" ", "").replace("$", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def money(v):
    try:
        return f"${v:,.0f}".replace(",", ".")
    except Exception:
        return "$0"

def percent(v):
    return f"{v * 100:.1f}%"

def get_field(row, names, default=0):
    for name in names:
        if name in row and row[name] not in ("", None) and not pd.isna(row[name]):
            return row[name]
    return default

def calcular_indicadores(row):
    ventas = to_number(get_field(row, ["Ventas_Mensuales", "Ventas mensuales", "Ventas", "Ingresos_Mensuales", "Ingresos"]))
    costo = to_number(get_field(row, ["Costo_Ventas", "Costo de ventas", "Costos_Ventas", "Costo_Ventas_Mensual"]))
    gastos = to_number(get_field(row, ["Gastos_Operativos", "Gastos operativos", "Gastos_Operacion"]))
    financieros = to_number(get_field(row, ["Gastos_Financieros", "Gastos financieros"]))
    ac = to_number(get_field(row, ["Activos_Corrientes", "Activos corrientes"]))
    pc = to_number(get_field(row, ["Pasivos_Corrientes", "Pasivos corrientes"]))
    at = to_number(get_field(row, ["Activos_Totales", "Activos totales"]))
    pt = to_number(get_field(row, ["Pasivos_Totales", "Pasivos totales"]))
    cuota = to_number(get_field(row, ["Cuota_Mensual_Credito", "Cuota mensual credito", "Cuota_Mensual", "Cuota"]))

    utilidad_bruta = ventas - costo
    utilidad_neta = utilidad_bruta - gastos - (2 * financieros)
    flujo = utilidad_bruta - gastos

    return pd.Series({
        "ventas": ventas,
        "utilidadBruta": utilidad_bruta,
        "utilidadNeta": utilidad_neta,
        "margenBruto": (utilidad_bruta / ventas) if ventas else 0,
        "endeudamiento": (pt / at) if at else 0,
        "liquidez": (ac / pc) if pc else 0,
        "cobertura": (flujo / cuota) if cuota else 0,
        "capitalTrabajo": ac - pc,
    })

def clasificar_riesgo(row):
    p = 0
    mora = to_number(get_field(row, ["Dias_Mora_Max", "Días de mora", "Dias_Mora"]))
    hist = str(get_field(row, ["Historial_Pagos", "Historial de pagos"], "")).lower()

    if row["endeudamiento"] > 0.70: p += 3
    elif row["endeudamiento"] > 0.50: p += 1

    if row["cobertura"] < 1: p += 3
    elif row["cobertura"] < 1.30: p += 1

    if row["margenBruto"] < 0.20: p += 2
    elif row["margenBruto"] < 0.30: p += 1

    if row["utilidadNeta"] < 0: p += 2

    if mora > 30: p += 3
    elif mora > 15: p += 1

    if "malo" in hist or "incum" in hist: p += 3
    elif "regular" in hist: p += 1

    return "ALTO" if p >= 7 else ("MEDIO" if p >= 3 else "BAJO")

def evaluar_viabilidad(riesgo, row):
    if riesgo == "BAJO" and row["cobertura"] >= 1.30 and row["endeudamiento"] <= 0.50 and row["utilidadNeta"] >= 0:
        return "VIABLE"
    if riesgo == "MEDIO" and row["cobertura"] >= 1 and row["utilidadNeta"] >= 0:
        return "VIABLE CON CONDICIONES"
    return "NO VIABLE"

def generar_recomendacion(viabilidad):
    if viabilidad == "VIABLE":
        return "Continuar estudio y validar soportes, flujo de caja y capacidad de pago."
    if viabilidad == "VIABLE CON CONDICIONES":
        return "Solicitar soportes adicionales y evaluar monto/plazo según capacidad de pago."
    return "No recomendar aprobación en primera instancia. Revisar endeudamiento, capacidad de pago, rentabilidad e historial."

@st.cache_data(show_spinner=False)
def procesar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    indicadores = df.apply(calcular_indicadores, axis=1)
    df = pd.concat([df, indicadores], axis=1)
    df["riesgo"] = df.apply(clasificar_riesgo, axis=1)
    df["viabilidad"] = df.apply(lambda r: evaluar_viabilidad(r["riesgo"], r), axis=1)
    df["recomendacion"] = df["viabilidad"].apply(generar_recomendacion)
    return df

def nombre_cliente(row):
    for col in ["Cliente", "Nombre_Cliente", "Nombre cliente"]:
        if col in row and pd.notna(row[col]) and str(row[col]).strip():
            return str(row[col])
    return "Cliente"

# ----------------------------------------------------------------------
# BARRA LATERAL
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("FinanData AI")
    st.caption("Dashboard comercial · Análisis financiero")
    st.divider()

    archivo = st.file_uploader("📁 Cargar Excel", type=["xlsx", "xls", "csv"])

    if "clientes_df" not in st.session_state:
        st.session_state.clientes_df = None

    if archivo is not None:
        try:
            if archivo.name.lower().endswith(".csv"):
                df_raw = pd.read_csv(archivo)
            else:
                df_raw = pd.read_excel(archivo)
            if not df_raw.empty:
                st.session_state.clientes_df = procesar_dataframe(df_raw)
                st.success(f"Cargado: {archivo.name}")
        except Exception as e:
            st.error(f"Error al leer archivo: {e}")

df = st.session_state.get("clientes_df")

# ----------------------------------------------------------------------
# ENCABEZADO Y SELECTOR
# ----------------------------------------------------------------------
col_titulo, col_selector = st.columns([2, 1])
with col_titulo:
    st.title("Dashboard comercial")
    st.caption("Visualización y análisis financiero de negocios")

opciones_cliente = ["Todos los clientes"]
if df is not None:
    opciones_cliente += [f"{i} · {nombre_cliente(row)}" for i, row in df.iterrows()]

with col_selector:
    seleccion = st.selectbox("Cliente", opciones_cliente, label_visibility="collapsed")

if df is None:
    st.info("Por favor, carga un archivo Excel desde la barra lateral para continuar.")
    st.stop()

if seleccion == "Todos los clientes":
    datos = df
    cliente_idx = None
else:
    cliente_idx = int(seleccion.split(" · ")[0])
    datos = df.loc[[cliente_idx]]

# ----------------------------------------------------------------------
# KPIS NATIVOS (SIN PROBLEMAS DE LETRA BLANCA)
# ----------------------------------------------------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total negocios", f"{len(datos)}")
k2.metric("Ventas promedio", money(datos["ventas"].mean()))
k3.metric("Margen promedio", percent(datos["margenBruto"].mean()))
k4.metric("Utilidad neta", money(datos["utilidadNeta"].mean()))
k5.metric("Endeudamiento", percent(datos["endeudamiento"].mean()))
k6.metric("Cobertura", f"{datos['cobertura'].mean():.2f}x")

st.divider()

# ----------------------------------------------------------------------
# DIAGNÓSTICO Y RECOMENDACIÓN NATIVOS
# ----------------------------------------------------------------------
st.subheader("💡 Diagnóstico y recomendación financiera")

with st.container():
    if cliente_idx is not None:
        fila = df.loc[cliente_idx]
        st.markdown(f"### Diagnóstico financiero — **{nombre_cliente(fila)}**")
        
        c_diag1, c_diag2 = st.columns(2)
        with c_diag1:
            st.write(f"• **Endeudamiento:** {percent(fila['endeudamiento'])}")
            st.write(f"• **Cobertura:** {fila['cobertura']:.2f}x")
            st.write(f"• **Margen Bruto:** {percent(fila['margenBruto'])}")
        with c_diag2:
            st.write(f"• **Liquidez:** {fila['liquidez']:.2f}x")
            st.write(f"• **Utilidad Neta:** {money(fila['utilidadNeta'])}")
        
        st.info(f"**Recomendación Comercial:** {fila['recomendacion']}")
    else:
        viables = (datos["viabilidad"] == "VIABLE").sum()
        texto = (f"El análisis preliminar identifica **{viables}** negocios viables en primera instancia. "
                 f"La cobertura promedio es **{datos['cobertura'].mean():.2f}x** y el endeudamiento promedio "
                 f"es **{percent(datos['endeudamiento'].mean())}**. La clasificación es preliminar y debe "
                 f"complementarse con la política de crédito vigente.")
        st.info(texto)

st.write("")

# ----------------------------------------------------------------------
# DISTRIBUCIÓN DEL RIESGO NATIVA
# ----------------------------------------------------------------------
st.subheader("Distribución del riesgo")
r1, r2, r3 = st.columns(3)
with r1:
    st.success(f"**RIESGO BAJO**\n# {(datos['riesgo']=='BAJO').sum()}")
with r2:
    st.warning(f"**RIESGO MEDIO**\n# {(datos['riesgo']=='MEDIO').sum()}")
with r3:
    st.error(f"**RIESGO ALTO**\n# {(datos['riesgo']=='ALTO').sum()}")

st.write("")

# ----------------------------------------------------------------------
# GRÁFICAS DINÁMICAS (PLOTLY)
# ----------------------------------------------------------------------
g1, g2 = st.columns(2)

with g1:
    st.markdown("**Distribución del riesgo**")
    conteo = datos["riesgo"].value_counts().reindex(["BAJO", "MEDIO", "ALTO"]).fillna(0)
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Riesgo bajo", "Riesgo medio", "Riesgo alto"],
        values=conteo.values,
        marker_colors=["#10b981", "#f59e0b", "#ef4444"],
        hole=0.5,
    )])
    fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, legend=dict(orientation="h"))
    st.plotly_chart(fig_pie, use_container_width=True)

with g2:
    st.markdown("**Gráfica de Liquidez vs. Endeudamiento**")
    datos_scatter = datos.copy()
    datos_scatter["Nombre"] = datos_scatter.apply(nombre_cliente, axis=1)
    
    fig_scatter = px.scatter(
        datos_scatter,
        x="endeudamiento",
        y="liquidez",
        color="riesgo",
        hover_name="Nombre",
        color_discrete_map={"BAJO": "#10b981", "MEDIO": "#f59e0b", "ALTO": "#ef4444"},
        labels={"endeudamiento": "Endeudamiento (%)", "liquidez": "Liquidez (x)"}
    )
    fig_scatter.add_vline(x=0.5, line_dash="dash", line_color="gray", annotation_text="Max 50%")
    fig_scatter.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Min 1.0x")
    fig_scatter.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig_scatter, use_container_width=True)

g3, g4 = st.columns(2)

with g3:
    st.markdown("**Gráfica de DSCR / Cobertura de Deuda**")
    datos_dscr = datos.head(15).copy()
    datos_dscr["Nombre"] = datos_dscr.apply(nombre_cliente, axis=1)
    
    fig_dscr = px.bar(
        datos_dscr,
        x="cobertura",
        y="Nombre",
        orientation="h",
        color="cobertura",
        color_continuous_scale="Blues",
        labels={"cobertura": "Ratio Cobertura (x)", "Nombre": ""}
    )
    fig_dscr.add_vline(x=1.3, line_dash="dash", line_color="#ef4444", annotation_text="Objetivo 1.3x")
    fig_dscr.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, coloraxis_showscale=False)
    st.plotly_chart(fig_dscr, use_container_width=True)

with g4:
    st.markdown("**Ventas vs. Utilidad Neta**")
    datos_v_u = datos.copy()
    datos_v_u["Nombre"] = datos_v_u.apply(nombre_cliente, axis=1)
    
    fig_vu = px.scatter(
        datos_v_u,
        x="ventas",
        y="utilidadNeta",
        hover_name="Nombre",
        color_discrete_sequence=["#7050f6"],
        labels={"ventas": "Ventas Mensuales ($)", "utilidadNeta": "Utilidad Neta ($)"}
    )
    fig_vu.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig_vu, use_container_width=True)

st.write("")

# ----------------------------------------------------------------------
# TABLA Y ASISTENTE IA NATIVO
# ----------------------------------------------------------------------
st.subheader("⚠️ Señales y recomendación comercial")
tabla = datos.copy()
tabla["Cliente"] = tabla.apply(nombre_cliente, axis=1)
tabla_mostrar = tabla[["Cliente", "ventas", "margenBruto", "endeudamiento", "cobertura", "riesgo", "viabilidad", "recomendacion"]].copy()
tabla_mostrar["ventas"] = tabla_mostrar["ventas"].apply(money)
tabla_mostrar["margenBruto"] = tabla_mostrar["margenBruto"].apply(percent)
tabla_mostrar["endeudamiento"] = tabla_mostrar["endeudamiento"].apply(percent)
tabla_mostrar["cobertura"] = tabla_mostrar["cobertura"].apply(lambda x: f"{x:.2f}x")
tabla_mostrar.columns = ["Cliente", "Ventas", "Margen", "Endeudamiento", "Cobertura", "Riesgo", "Viabilidad", "Recomendación"]
st.dataframe(tabla_mostrar, use_container_width=True, hide_index=True)

st.write("")

bajo, medio, alto = (datos["riesgo"] == "BAJO").sum(), (datos["riesgo"] == "MEDIO").sum(), (datos["riesgo"] == "ALTO").sum()
viables = (datos["viabilidad"] == "VIABLE").sum()

st.success(
    f"🤖 **Asistente IA comercial**\n\n"
    f"El análisis identifica **{bajo}** negocios en riesgo bajo, **{medio}** en riesgo medio y **{alto}** en riesgo alto. "
    f"Se identifican **{viables}** perfiles viables en primera instancia. Estos resultados sirven como apoyo comercial y no reemplazan la decisión crediticia definitiva."
)
