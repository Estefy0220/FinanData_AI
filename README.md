"""
FinanData AI - Dashboard comercial (Streamlit)
Análisis financiero automatizado para estudio de crédito de negocios.
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

PRIMARY = "#0757c9"

# Estilos CSS corregidos para alto contraste (modo oscuro y claro) y tipografía proporcional
st.markdown(
    """
    <style>
    .kpi-card {
        border-radius: 10px;
        padding: 12px 10px;
        color: white;
        box-shadow: 0 2px 7px rgba(0,0,0,.15);
        min-height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        opacity: .95;
        margin-bottom: 4px;
        text-transform: uppercase;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-value {
        font-size: 17px;
        font-weight: 800;
        word-break: break-all;
        line-height: 1.2;
    }
    .k1{background:#7050f6} .k2{background:#0878e8} .k3{background:#0ca5ba}
    .k4{background:#05c47a} .k5{background:#8b4df1} .k6{background:#0756c9}

    /* Corrección de contraste para texto en tarjetas e IA */
    .diag-box {
        background: #ffffff !important;
        color: #1e293b !important;
        border-left: 5px solid #1264d6;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,.1);
    }
    .diag-box * { color: #1e293b !important; }
    
    .ind-row { font-size: 14px; margin: 6px 0; color: #334155 !important; }
    
    .conclusion-box {
        background: #f1f5f9 !important;
        color: #0f172a !important;
        border-radius: 8px;
        padding: 14px;
        margin-top: 12px;
        font-size: 14px;
        border: 1px solid #cbd5e1;
    }
    .conclusion-box * { color: #0f172a !important; }

    .assistant-box {
        background: #f0f9ff !important;
        color: #0369a1 !important;
        border: 1px solid #bae6fd;
        border-radius: 9px;
        padding: 18px;
    }
    .assistant-box * { color: #0c4a6e !important; }

    .risk-card {
        background: #ffffff !important;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,.08);
    }
    .risk-low { border-left: 5px solid #10b981; }
    .risk-med { border-left: 5px solid #f59e0b; }
    .risk-high { border-left: 5px solid #ef4444; }
    .risk-title { font-size: 11px; font-weight: 700; color: #64748b !important; letter-spacing: 0.5px; }
    .risk-count { font-size: 26px; font-weight: 800; color: #0f172a !important; margin: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# FUNCIONES DE UTILIDAD
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

# ----------------------------------------------------------------------
# CÁLCULO DE INDICADORES
# ----------------------------------------------------------------------
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

def semaforo_endeudamiento(v):
    if v > 0.70: return "🔴", "Alto", "Una proporción elevada de los activos está financiada con deuda."
    if v > 0.50: return "🟠", "Moderado", "El nivel de deuda es considerable y debe vigilarse."
    return "🟢", "Adecuado", "La proporción de deuda sobre los activos es manejable."

def semaforo_cobertura(v):
    if v < 1: return "🔴", "Riesgo", "El flujo disponible no alcanza para cubrir completamente la cuota."
    if v < 1.30: return "🟠", "Ajustada", "El flujo cubre la cuota, pero con poco margen de holgura."
    return "🟢", "Adecuada", "El flujo disponible cubre la cuota con holgura suficiente."

def semaforo_margen(v):
    if v < 0.20: return "🔴", "Bajo", "El negocio tiene poca capacidad para absorber gastos adicionales."
    if v < 0.30: return "🟠", "Moderado", "El margen es aceptable, aunque con espacio limitado de maniobra."
    return "🟢", "Bueno", "El negocio conserva un margen saludable sobre sus ventas."

def semaforo_liquidez(v):
    if v < 1: return "🔴", "Atención", "Los activos corrientes no alcanzan para cubrir las obligaciones de corto plazo."
    if v < 1.20: return "🟠", "Ajustada", "La liquidez cubre lo corriente pero con poco colchón."
    return "🟢", "Adecuada", "Los activos corrientes cubren cómodamente las obligaciones de corto plazo."

def semaforo_utilidad(v):
    if v < 0: return "🔴", "Negativa", "El negocio no está generando excedente después de sus costos y gastos."
    return "🟢", "Positiva", "El negocio genera excedente después de costos y gastos."

def generar_diagnostico_cliente(row):
    e_i, e_l, e_t = semaforo_endeudamiento(row["endeudamiento"])
    c_i, c_l, c_t = semaforo_cobertura(row["cobertura"])
    m_i, m_l, m_t = semaforo_margen(row["margenBruto"])
    liq_i, liq_l, liq_t = semaforo_liquidez(row["liquidez"])
    u_i, u_l, u_t = semaforo_utilidad(row["utilidadNeta"])

    lineas = [
        f"<div class='ind-row'>{e_i} <strong>Endeudamiento:</strong> {percent(row['endeudamiento'])} → {e_l}. {e_t}</div>",
        f"<div class='ind-row'>{c_i} <strong>Cobertura:</strong> {row['cobertura']:.2f}x → {c_l}. {c_t}</div>",
        f"<div class='ind-row'>{m_i} <strong>Margen:</strong> {percent(row['margenBruto'])} → {m_l}. {m_t}</div>",
        f"<div class='ind-row'>{liq_i} <strong>Liquidez:</strong> {row['liquidez']:.2f}x → {liq_l}. {liq_t}</div>",
        f"<div class='ind-row'>{u_i} <strong>Utilidad neta:</strong> {money(row['utilidadNeta'])} → {u_l}. {u_t}</div>",
    ]
    return "".join(lineas)

def generar_conclusion(row):
    v = row["viabilidad"]
    if v == "VIABLE":
        return "El negocio presenta indicadores financieros sólidos. Se recomienda continuar el estudio de crédito validando soportes."
    if v == "VIABLE CON CONDICIONES":
        return "El negocio presenta un perfil aceptable con puntos de atención. Se recomienda ajustar monto o plazo."
    return "El negocio presenta capacidad de pago insuficiente o alto riesgo. No se recomienda aprobar en primera instancia."

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
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:10px;margin-bottom:10px;'>"
        f"<div style='width:32px;height:32px;background:{PRIMARY};color:white;border-radius:6px;"
        f"display:flex;align-items:center;justify-content:center;font-weight:800;'>F</div>"
        f"<span style='font-weight:700;font-size:18px;'>FinanData AI</span></div>",
        unsafe_allow_html=True,
    )
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
            if df_raw.empty:
                st.error("El archivo está vacío.")
            else:
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
# KPIS
# ----------------------------------------------------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (k1, "k1", "Total negocios", f"{len(datos)}"),
    (k2, "k2", "Ventas promedio", money(datos["ventas"].mean())),
    (k3, "k3", "Margen promedio", percent(datos["margenBruto"].mean())),
    (k4, "k4", "Utilidad neta", money(datos["utilidadNeta"].mean())),
    (k5, "k5", "Endeudamiento", percent(datos["endeudamiento"].mean())),
    (k6, "k6", "Cobertura", f"{datos['cobertura'].mean():.2f}x"),
]
for col, klass, label, value in kpis:
    with col:
        st.markdown(
            f"<div class='kpi-card {klass}'><div class='kpi-label'>{label}</div>"
            f"<div class='kpi-value'>{value}</div></div>",
            unsafe_allow_html=True,
        )

st.write("")

# ----------------------------------------------------------------------
# DIAGNÓSTICO Y RECOMENDACIÓN
# ----------------------------------------------------------------------
st.subheader("💡 Diagnóstico y recomendación financiera")

if cliente_idx is not None:
    fila = df.loc[cliente_idx]
    st.markdown(
        f"<div class='diag-box'>"
        f"<strong>Diagnóstico financiero — {nombre_cliente(fila)}</strong><br><br>"
        f"{generar_diagnostico_cliente(fila)}"
        f"<div class='conclusion-box'><strong>Conclusión:</strong><br>{generar_conclusion(fila)}"
        f"<br><br><strong>Recomendación comercial:</strong> {fila['recomendacion']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
else:
    viables = (datos["viabilidad"] == "VIABLE").sum()
    total = len(datos)
    alto = (datos["riesgo"] == "ALTO").sum()

    if total and alto / total >= 0.4:
        texto = ("Se identifica una concentración importante de negocios en riesgo alto. "
                 "Se recomienda fortalecer la validación de capacidad de pago antes de aprobar.")
    else:
        texto = (f"El análisis preliminar identifica {viables} negocios viables en primera instancia. "
                 f"La cobertura promedio es {datos['cobertura'].mean():.2f}x y el endeudamiento promedio "
                 f"es {percent(datos['endeudamiento'].mean())}.")

    st.markdown(f"<div class='diag-box'>{texto}</div>", unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------------------------
# DISTRIBUCIÓN DEL RIESGO
# ----------------------------------------------------------------------
st.subheader("Distribución del riesgo")
r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"<div class='risk-card risk-low'><div class='risk-title'>RIESGO BAJO</div><div class='risk-count'>{(datos['riesgo']=='BAJO').sum()}</div></div>", unsafe_allow_html=True)
with r2:
    st.markdown(f"<div class='risk-card risk-med'><div class='risk-title'>RIESGO MEDIO</div><div class='risk-count'>{(datos['riesgo']=='MEDIO').sum()}</div></div>", unsafe_allow_html=True)
with r3:
    st.markdown(f"<div class='risk-card risk-high'><div class='risk-title'>RIESGO ALTO</div><div class='risk-count'>{(datos['riesgo']=='ALTO').sum()}</div></div>", unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------------------------
# GRÁFICAS REVISADAS Y DINÁMICAS
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
# DETALLE DEL CLIENTE
# ----------------------------------------------------------------------
st.subheader("👤 Detalle del cliente")
if cliente_idx is None:
    st.caption("Selecciona un cliente individual arriba para explorar sus detalles.")
else:
    fila = df.loc[cliente_idx]
    ciudad = get_field(fila, ["Ciudad", "Municipio"], "-")
    actividad = get_field(fila, ["Actividad_Economica", "Actividad"], "-")
    d1, d2, d3, d4 = st.columns(4)
    campos = [
        ("CLIENTE", nombre_cliente(fila)), ("CIUDAD", ciudad), ("ACTIVIDAD", actividad),
        ("VENTAS MENSUALES", money(fila["ventas"])), ("UTILIDAD NETA", money(fila["utilidadNeta"])),
        ("MARGEN", percent(fila["margenBruto"])), ("ENDEUDAMIENTO", percent(fila["endeudamiento"])),
        ("LIQUIDEZ", f"{fila['liquidez']:.2f}x"), ("COBERTURA", f"{fila['cobertura']:.2f}x"),
        ("CAPITAL DE TRABAJO", money(fila["capitalTrabajo"])), ("RIESGO", fila["riesgo"]),
        ("VIABILIDAD", fila["viabilidad"]),
    ]
    cols = [d1, d2, d3, d4]
    for i, (label, value) in enumerate(campos):
        with cols[i % 4]:
            st.markdown(f"<small style='color:#64748b;'>{label}</small><br><strong>{value}</strong>", unsafe_allow_html=True)
            st.write("")

st.write("")

# ----------------------------------------------------------------------
# TABLA Y ASISTENTE IA
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
st.markdown(
    f"<div class='assistant-box'><h4>🤖 Asistente IA comercial</h4>"
    f"<p>El análisis identifica <strong>{bajo}</strong> negocios en riesgo bajo, <strong>{medio}</strong> "
    f"en riesgo medio y <strong>{alto}</strong> en riesgo alto. Se identifican <strong>{viables}</strong> "
    f"perfiles viables en primera instancia.</p></div>",
    unsafe_allow_html=True,
)
