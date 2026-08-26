"""

FinanData AI - Dashboard comercial (Streamlit)

Análisis financiero automatizado para estudio de crédito de negocios.

Réplica funcional del dashboard HTML original + diagnóstico explicado por indicador.

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



st.markdown(

    """

    <style>

    .kpi-card{border-radius:10px;padding:14px 16px;color:white;box-shadow:0 2px 7px rgba(0,0,0,.08);}

    .kpi-label{font-size:12px;font-weight:600;opacity:.9;margin-bottom:6px;}

    .kpi-value{font-size:22px;font-weight:800;}

    .k1{background:#7050f6}.k2{background:#0878e8}.k3{background:#0ca5ba}

    .k4{background:#05c47a}.k5{background:#8b4df1}.k6{background:#0756c9}

    .diag-box{background:#fff;border-left:5px solid #1264d6;border-radius:8px;

              padding:16px 18px;box-shadow:0 2px 7px rgba(0,0,0,.05);}

    .ind-row{font-size:14px;margin:4px 0;}

    .conclusion-box{background:#f7f9fc;border-radius:8px;padding:14px;margin-top:10px;font-size:14px;}

    .assistant-box{background:linear-gradient(135deg,#eef5ff,#f8fbff);

                    border:1px solid #dceafe;border-radius:9px;padding:18px;}

    .risk-low{border-left:4px solid #10b981;padding:10px 14px;border-radius:8px;background:#fff;}

    .risk-med{border-left:4px solid #f59e0b;padding:10px 14px;border-radius:8px;background:#fff;}

    .risk-high{border-left:4px solid #ef4444;padding:10px 14px;border-radius:8px;background:#fff;}

    </style>

    """,

    unsafe_allow_html=True,

)



# ----------------------------------------------------------------------

# FUNCIONES DE UTILIDAD (equivalentes a num(), money(), percent(), get())

# ----------------------------------------------------------------------

def to_number(v):

    """Convierte strings con formato colombiano ($, puntos de miles, coma decimal) a float."""

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

# CÁLCULO DE INDICADORES (equivalente a indicadores(), clasificar(), viabilidad(), recomendacion())

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

    utilidad_neta = utilidad_bruta - gastos - (2 * financieros)  # replica el cálculo del original

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



    if row["endeudamiento"] > 0.70:

        p += 3

    elif row["endeudamiento"] > 0.50:

        p += 1



    if row["cobertura"] < 1:

        p += 3

    elif row["cobertura"] < 1.30:

        p += 1



    if row["margenBruto"] < 0.20:

        p += 2

    elif row["margenBruto"] < 0.30:

        p += 1



    if row["utilidadNeta"] < 0:

        p += 2



    if mora > 30:

        p += 3

    elif mora > 15:

        p += 1



    if "malo" in hist or "incum" in hist:

        p += 3

    elif "regular" in hist:

        p += 1



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





# ----------------------------------------------------------------------

# DIAGNÓSTICO EXPLICADO POR INDICADOR (nueva funcionalidad solicitada)

# ----------------------------------------------------------------------

def semaforo_endeudamiento(v):

    if v > 0.70:

        return "🔴", "Alto", "Una proporción elevada de los activos está financiada con deuda."

    if v > 0.50:

        return "🟠", "Moderado", "El nivel de deuda es considerable y debe vigilarse."

    return "🟢", "Adecuado", "La proporción de deuda sobre los activos es manejable."





def semaforo_cobertura(v):

    if v < 1:

        return "🔴", "Riesgo", "El flujo disponible no alcanza para cubrir completamente la cuota."

    if v < 1.30:

        return "🟠", "Ajustada", "El flujo cubre la cuota, pero con poco margen de holgura."

    return "🟢", "Adecuada", "El flujo disponible cubre la cuota con holgura suficiente."





def semaforo_margen(v):

    if v < 0.20:

        return "🔴", "Bajo", "El negocio tiene poca capacidad para absorber gastos adicionales."

    if v < 0.30:

        return "🟠", "Moderado", "El margen es aceptable, aunque con espacio limitado de maniobra."

    return "🟢", "Bueno", "El negocio conserva un margen saludable sobre sus ventas."





def semaforo_liquidez(v):

    if v < 1:

        return "🔴", "Atención", "Los activos corrientes no alcanzan para cubrir totalmente las obligaciones de corto plazo."

    if v < 1.20:

        return "🟠", "Ajustada", "La liquidez cubre lo corriente pero con poco colchón."

    return "🟢", "Adecuada", "Los activos corrientes cubren cómodamente las obligaciones de corto plazo."





def semaforo_utilidad(v):

    if v < 0:

        return "🔴", "Negativa", "El negocio no está generando excedente después de sus costos y gastos."

    return "🟢", "Positiva", "El negocio genera excedente después de costos y gastos."





def generar_diagnostico_cliente(row):

    """Construye el bloque de diagnóstico financiero explicado, indicador por indicador."""

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

        return (f"El negocio presenta indicadores financieros sólidos y consistentes. "

                f"Por esta razón, se recomienda continuar con el estudio de crédito, validando soportes "

                f"documentales y comportamiento de pago histórico.")

    if v == "VIABLE CON CONDICIONES":

        return (f"El negocio presenta un perfil aceptable pero con puntos de atención. "

                f"Se recomienda solicitar información adicional y ajustar monto o plazo según la capacidad "

                f"de pago real antes de continuar el estudio.")

    return (f"El negocio presenta una capacidad de pago insuficiente y/o un nivel de riesgo elevado. "

            f"Por estos indicadores, no se recomienda aprobar en primera instancia. Se recomienda solicitar "

            f"información adicional y revisar la estructura de obligaciones antes de continuar con el estudio.")





# ----------------------------------------------------------------------

# PROCESAMIENTO DE DATOS CARGADOS

# ----------------------------------------------------------------------

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

            return row[col]

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

    st.caption("Dashboard comercial · Análisis financiero de negocios")

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

                st.error("El archivo no contiene registros.")

            else:

                st.session_state.clientes_df = procesar_dataframe(df_raw)

                st.success(f"Archivo cargado: {archivo.name}")

        except Exception as e:

            st.error(f"No fue posible leer el archivo: {e}")



    st.divider()

    with st.expander("ℹ️ ¿Cómo interpretar los indicadores?"):

        st.markdown(

            """

            - **Endeudamiento** = Pasivos totales / Activos totales. Menor a 50% es sano; sobre 70% es alto.

            - **Cobertura** = Flujo disponible / Cuota del crédito. Debe ser mayor a 1.3x para tener holgura.

            - **Margen bruto** = (Ventas − Costo de ventas) / Ventas. Refleja la rentabilidad del negocio.

            - **Liquidez** = Activos corrientes / Pasivos corrientes. Mayor a 1x indica capacidad de cubrir el corto plazo.

            - **Utilidad neta** = Utilidad bruta − Gastos operativos − Gastos financieros. Debe ser positiva.



            Estos indicadores combinados determinan el **riesgo** (bajo/medio/alto) y la **viabilidad**

            (viable / viable con condiciones / no viable) de cada negocio.

            """

        )



df = st.session_state.get("clientes_df")



# ----------------------------------------------------------------------

# ENCABEZADO Y SELECTOR DE CLIENTE

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

    st.info("Carga un archivo Excel desde la barra lateral para comenzar el análisis. "

            "Puedes usar el archivo de ejemplo `datos/ejemplo_100_negocios.xlsx`.")

    st.stop()



if seleccion == "Todos los clientes":

    datos = df

    cliente_idx = None

else:

    cliente_idx = int(seleccion.split(" · ")[0])

    datos = df.loc[[cliente_idx]]



# ----------------------------------------------------------------------

# KPIs

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

# DIAGNÓSTICO Y RECOMENDACIÓN FINANCIERA (AMPLIADO)

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

    bajo = (datos["riesgo"] == "BAJO").sum()

    medio = (datos["riesgo"] == "MEDIO").sum()

    alto = (datos["riesgo"] == "ALTO").sum()

    viables = (datos["viabilidad"] == "VIABLE").sum()

    total = len(datos)



    if total and alto / total >= 0.4:

        texto = ("Se identifica una concentración importante de negocios en riesgo alto. "

                 "Se recomienda fortalecer la validación de capacidad de pago, endeudamiento y "

                 "comportamiento de pago antes de continuar con las aprobaciones.")

    else:

        texto = (f"El análisis preliminar identifica {viables} negocios viables en primera instancia. "

                  f"La cobertura promedio es {datos['cobertura'].mean():.2f}x y el endeudamiento promedio "

                  f"es {percent(datos['endeudamiento'].mean())}. La clasificación es preliminar y debe "

                  f"complementarse con la política de crédito vigente.")



    st.markdown(f"<div class='diag-box'>{texto}</div>", unsafe_allow_html=True)



st.write("")



# ----------------------------------------------------------------------

# DISTRIBUCIÓN DEL RIESGO

# ----------------------------------------------------------------------

st.subheader("Distribución del riesgo")

r1, r2, r3 = st.columns(3)

with r1:

    st.markdown(f"<div class='risk-low'><small>RIESGO BAJO</small><h2>{(df['riesgo']=='BAJO').sum()}</h2></div>", unsafe_allow_html=True)

with r2:

    st.markdown(f"<div class='risk-med'><small>RIESGO MEDIO</small><h2>{(df['riesgo']=='MEDIO').sum()}</h2></div>", unsafe_allow_html=True)

with r3:

    st.markdown(f"<div class='risk-high'><small>RIESGO ALTO</small><h2>{(df['riesgo']=='ALTO').sum()}</h2></div>", unsafe_allow_html=True)



st.write("")



# ----------------------------------------------------------------------

# GRÁFICAS

# ----------------------------------------------------------------------

g1, g2 = st.columns(2)



with g1:

    st.markdown("**Distribución del riesgo**")

    conteo = df["riesgo"].value_counts().reindex(["BAJO", "MEDIO", "ALTO"]).fillna(0)

    fig = go.Figure(data=[go.Pie(

        labels=["Riesgo bajo", "Riesgo medio", "Riesgo alto"],

        values=conteo.values,

        marker_colors=["#10b981", "#f59e0b", "#ef4444"],

        hole=0.5,

    )])

    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, legend=dict(orientation="h"))

    st.plotly_chart(fig, use_container_width=True)



with g2:

    st.markdown("**Ventas promedio por actividad**")

    col_act = "Actividad_Economica" if "Actividad_Economica" in df.columns else (

        "Actividad" if "Actividad" in df.columns else None)

    if col_act:

        grp = df.groupby(col_act)["ventas"].mean().sort_values()

        fig2 = px.bar(grp, x=grp.values, y=grp.index, orientation="h",

                      labels={"x": "Ventas promedio", "y": ""}, color_discrete_sequence=["#0878e8"])

        fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)

        st.plotly_chart(fig2, use_container_width=True)

    else:

        st.caption("No se encontró columna de actividad económica en el archivo.")



g3, g4 = st.columns(2)



with g3:

    st.markdown("**Ventas vs. utilidad neta**")

    fig3 = px.scatter(datos.head(100), x="ventas", y="utilidadNeta",

                       color_discrete_sequence=["#7050f6"],

                       labels={"ventas": "Ventas", "utilidadNeta": "Utilidad neta"})

    fig3.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)

    st.plotly_chart(fig3, use_container_width=True)



with g4:

    st.markdown("**Endeudamiento y cobertura (primeros 20)**")

    d20 = df.head(20).copy()

    d20["endeudamiento_pct"] = d20["endeudamiento"] * 100

    d20["etiqueta"] = d20.apply(nombre_cliente, axis=1)

    fig4 = go.Figure()

    fig4.add_trace(go.Bar(x=d20["etiqueta"], y=d20["endeudamiento_pct"], name="Endeudamiento %", marker_color="#8b4df1"))

    fig4.add_trace(go.Bar(x=d20["etiqueta"], y=d20["cobertura"], name="Cobertura", marker_color="#0ca5ba"))

    fig4.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300, barmode="group",

                        legend=dict(orientation="h"))

    st.plotly_chart(fig4, use_container_width=True)



st.write("")



# ----------------------------------------------------------------------

# DETALLE DEL CLIENTE

# ----------------------------------------------------------------------

st.subheader("👤 Detalle del cliente")

if cliente_idx is None:

    st.caption("Selecciona un cliente en el menú superior para visualizar su información.")

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

            st.markdown(f"<small style='color:#778399;'>{label}</small><br><strong>{value}</strong>", unsafe_allow_html=True)

            st.write("")



st.write("")



# ----------------------------------------------------------------------

# TABLA DE SEÑALES Y RECOMENDACIÓN

# ----------------------------------------------------------------------

st.subheader("⚠️ Señales y recomendación comercial")

tabla = df.copy()

tabla["Cliente"] = tabla.apply(nombre_cliente, axis=1)

tabla_mostrar = tabla[["Cliente", "ventas", "margenBruto", "endeudamiento", "cobertura", "riesgo", "viabilidad", "recomendacion"]].copy()

tabla_mostrar["ventas"] = tabla_mostrar["ventas"].apply(money)

tabla_mostrar["margenBruto"] = tabla_mostrar["margenBruto"].apply(percent)

tabla_mostrar["endeudamiento"] = tabla_mostrar["endeudamiento"].apply(percent)

tabla_mostrar["cobertura"] = tabla_mostrar["cobertura"].apply(lambda x: f"{x:.2f}x")

tabla_mostrar.columns = ["Cliente", "Ventas", "Margen", "Endeudamiento", "Cobertura", "Riesgo", "Viabilidad", "Recomendación"]

st.dataframe(tabla_mostrar, use_container_width=True, hide_index=True)



st.write("")



# ----------------------------------------------------------------------

# ASISTENTE IA COMERCIAL

# ----------------------------------------------------------------------

bajo, medio, alto = (df["riesgo"] == "BAJO").sum(), (df["riesgo"] == "MEDIO").sum(), (df["riesgo"] == "ALTO").sum()

viables = (df["viabilidad"] == "VIABLE").sum()

st.markdown(

    f"<div class='assistant-box'><h4>🤖 Asistente IA comercial</h4>"

    f"<p>El análisis identifica <strong>{bajo}</strong> negocios en riesgo bajo, <strong>{medio}</strong> "

    f"en riesgo medio y <strong>{alto}</strong> en riesgo alto. Se identifican <strong>{viables}</strong> "

    f"perfiles viables en primera instancia. Estos resultados sirven como apoyo comercial y no reemplazan "

    f"la decisión crediticia definitiva.</p></div>",

    unsafe_allow_html=True,

) 

