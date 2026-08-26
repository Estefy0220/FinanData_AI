"""
FinanData AI - Dashboard comercial
Análisis financiero automatizado para estudio preliminar de crédito.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from html import escape


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PALETA DE COLORES
# ============================================================

PRIMARY = "#0757C9"
BLUE = "#0878E8"
PURPLE = "#7050F6"
PURPLE_2 = "#8B4DF1"
TEAL = "#0CA5BA"
GREEN = "#05C47A"
DARK_BLUE = "#0756C9"

RISK_LOW = "#05C47A"
RISK_MEDIUM = "#F59E0B"
RISK_HIGH = "#EF4444"

BACKGROUND = "#F4F7FB"
TEXT = "#25344A"
MUTED = "#667085"


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {BACKGROUND};
    }}

    .main-title {{
        color: {TEXT};
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 2px;
    }}

    .main-subtitle {{
        color: #667085;
        font-size: 14px;
        margin-bottom: 18px;
    }}

    .kpi-card {{
        border-radius: 10px;
        padding: 14px;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,.08);
        min-height: 95px;
        height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
    }}

    .kpi-label {{
        font-size: 12px;
        font-weight: 600;
        opacity: .94;
        margin-bottom: 8px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .kpi-value {{
        font-size: 20px;
        font-weight: 800;
        line-height: 1.05;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .k1 {{
        background: {PURPLE};
    }}

    .k2 {{
        background: {BLUE};
    }}

    .k3 {{
        background: {TEAL};
    }}

    .k4 {{
        background: {GREEN};
    }}

    .k5 {{
        background: {PURPLE_2};
    }}

    .k6 {{
        background: {DARK_BLUE};
    }}

    .info-box {{
        background: white;
        border-left: 5px solid {PRIMARY};
        border-radius: 9px;
        padding: 15px 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 7px rgba(0,0,0,.05);
    }}

    .info-title {{
        font-size: 15px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 10px;
    }}

    .info-text {{
        color: #475467;
        font-size: 13px;
        line-height: 1.55;
    }}

    .diag-box {{
        background: white;
        border-left: 5px solid {PRIMARY};
        border-radius: 9px;
        padding: 17px 19px;
        box-shadow: 0 2px 7px rgba(0,0,0,.06);
        color: {TEXT};
    }}

    .diag-title {{
        font-size: 16px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 13px;
    }}

    .diag-row {{
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 13px;
        line-height: 1.5;
        margin: 9px 0;
        color: #344054;
    }}

    .diag-icon {{
        width: 18px;
        min-width: 18px;
    }}

    .diag-text {{
        flex: 1;
    }}

    .conclusion-box {{
        background: #F4F6F9;
        border-radius: 8px;
        padding: 14px 15px;
        margin-top: 15px;
        color: #344054;
        font-size: 13px;
        line-height: 1.5;
    }}

    .conclusion-title {{
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .assistant-box {{
        background: linear-gradient(
            135deg,
            #EEF5FF,
            #F8FBFF
        );
        border: 1px solid #DCEAFE;
        border-radius: 10px;
        padding: 18px;
        color: #344054;
    }}

    .assistant-title {{
        font-size: 16px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 8px;
    }}

    .assistant-text {{
        font-size: 13px;
        line-height: 1.55;
    }}

    .risk-card {{
        background: white;
        border-radius: 9px;
        padding: 13px 16px;
        box-shadow: 0 2px 7px rgba(0,0,0,.05);
    }}

    .risk-low {{
        border-left: 5px solid {RISK_LOW};
    }}

    .risk-medium {{
        border-left: 5px solid {RISK_MEDIUM};
    }}

    .risk-high {{
        border-left: 5px solid {RISK_HIGH};
    }}

    .risk-number {{
        font-size: 26px;
        font-weight: 800;
        color: {TEXT};
        margin-top: 4px;
    }}

    .chart-description {{
        color: {MUTED};
        font-size: 12px;
        margin-bottom: 8px;
    }}

    .section-title {{
        color: {TEXT};
        font-weight: 750;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def to_number(value):
    """
    Convierte números en formatos colombianos:
    1.500.000
    1,500,000
    $1.500.000
    25%
    """

    if pd.isna(value):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if text == "":
        return 0.0

    text = (
        text
        .replace("$", "")
        .replace("%", "")
        .replace(" ", "")
    )

    if "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")

    elif "," in text:
        text = text.replace(",", ".")

    elif text.count(".") > 1:
        text = text.replace(".", "")

    try:
        return float(text)

    except ValueError:
        return 0.0


def money(value):
    try:
        return f"${value:,.0f}".replace(",", ".")
    except Exception:
        return "$0"


def percent(value):
    try:
        return f"{value * 100:.1f}%"
    except Exception:
        return "0.0%"


def safe_text(value):
    return escape(str(value))


def get_field(row, names, default=0):

    for name in names:

        if name in row:

            value = row[name]

            if (
                value is not None
                and value != ""
                and not pd.isna(value)
            ):
                return value

    return default


# ============================================================
# PREPARAR DATAFRAME
# ============================================================

def preparar_dataframe_base(df):

    df = df.copy()

    columnas_requeridas = [
        "ID_Cliente",
        "Cliente",
        "Ciudad",
        "Actividad_Economica",
        "Ventas_Mensuales",
        "Costo_Ventas",
        "Gastos_Operativos",
        "Gastos_Financieros",
        "Activos_Corrientes",
        "Pasivos_Corrientes",
        "Activos_Totales",
        "Pasivos_Totales",
        "Patrimonio",
        "Cuota_Mensual_Credito",
        "Antiguedad_Negocio_Anios",
        "Historial_Pagos",
        "Dias_Mora_Max",
        "Tiene_Centrales",
    ]

    # Si existe Tiene_Centrales, conservar hasta esa columna
    columnas = list(df.columns)

    indice_centrales = None

    for i, columna in enumerate(columnas):

        nombre = (
            str(columna)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if (
            "tiene" in nombre
            and "central" in nombre
        ):
            indice_centrales = i
            break

    if indice_centrales is not None:

        df = df.iloc[
            :,
            :indice_centrales + 1
        ]

    return df


# ============================================================
# CÁLCULO DE INDICADORES
# ============================================================

def calcular_indicadores(row):

    ventas = to_number(
        get_field(
            row,
            [
                "Ventas_Mensuales",
                "Ventas mensuales",
                "Ventas",
                "Ingresos_Mensuales",
                "Ingresos",
            ],
        )
    )

    costo = to_number(
        get_field(
            row,
            [
                "Costo_Ventas",
                "Costo de ventas",
                "Costos_Ventas",
            ],
        )
    )

    gastos = to_number(
        get_field(
            row,
            [
                "Gastos_Operativos",
                "Gastos operativos",
                "Gastos_Operacion",
                "Gastos_Operacionales",
            ],
        )
    )

    financieros = to_number(
        get_field(
            row,
            [
                "Gastos_Financieros",
                "Gastos financieros",
            ],
        )
    )

    activos_corrientes = to_number(
        get_field(
            row,
            [
                "Activos_Corrientes",
                "Activos corrientes",
            ],
        )
    )

    pasivos_corrientes = to_number(
        get_field(
            row,
            [
                "Pasivos_Corrientes",
                "Pasivos corrientes",
            ],
        )
    )

    activos_totales = to_number(
        get_field(
            row,
            [
                "Activos_Totales",
                "Activos totales",
            ],
        )
    )

    pasivos_totales = to_number(
        get_field(
            row,
            [
                "Pasivos_Totales",
                "Pasivos totales",
            ],
        )
    )

    cuota = to_number(
        get_field(
            row,
            [
                "Cuota_Mensual_Credito",
                "Cuota mensual credito",
                "Cuota_Mensual",
                "Cuota",
            ],
        )
    )

    utilidad_bruta = ventas - costo

    margen_bruto = (
        utilidad_bruta / ventas
        if ventas != 0
        else 0
    )

    utilidad_neta = (
        utilidad_bruta
        - gastos
        - financieros
    )

    margen_neto = (
        utilidad_neta / ventas
        if ventas != 0
        else 0
    )

    capital_trabajo = (
        activos_corrientes
        - pasivos_corrientes
    )

    endeudamiento = (
        pasivos_totales / activos_totales
        if activos_totales != 0
        else 0
    )

    liquidez = (
        activos_corrientes / pasivos_corrientes
        if pasivos_corrientes != 0
        else 0
    )

    flujo = (
        utilidad_bruta
        - gastos
    )

    cobertura = (
        flujo / cuota
        if cuota != 0
        else 0
    )

    apalancamiento = (
        pasivos_totales /
        max(activos_totales - pasivos_totales, 1)
        if activos_totales != 0
        else 0
    )

    return pd.Series(
        {
            "ventas": ventas,
            "costoVentas": costo,
            "gastosOperativos": gastos,
            "gastosFinancieros": financieros,
            "activosCorrientes": activos_corrientes,
            "pasivosCorrientes": pasivos_corrientes,
            "activosTotales": activos_totales,
            "pasivosTotales": pasivos_totales,
            "cuotaCredito": cuota,
            "utilidadBruta": utilidad_bruta,
            "margenBruto": margen_bruto,
            "utilidadNeta": utilidad_neta,
            "margenNeto": margen_neto,
            "capitalTrabajo": capital_trabajo,
            "endeudamiento": endeudamiento,
            "liquidez": liquidez,
            "cobertura": cobertura,
            "apalancamiento": apalancamiento,
        }
    )


# ============================================================
# RIESGO
# ============================================================

def clasificar_riesgo(row):

    puntos = 0

    mora = to_number(
        get_field(
            row,
            [
                "Dias_Mora_Max",
                "Días de mora",
                "Dias_Mora",
            ],
            0,
        )
    )

    historial = str(
        get_field(
            row,
            [
                "Historial_Pagos",
                "Historial de pagos",
                "Historial_Pago",
            ],
            "",
        )
    ).lower()

    # Endeudamiento
    if row["endeudamiento"] > 0.70:
        puntos += 3

    elif row["endeudamiento"] > 0.50:
        puntos += 1

    # Cobertura
    if row["cobertura"] < 1:
        puntos += 3

    elif row["cobertura"] < 1.30:
        puntos += 1

    # Margen
    if row["margenBruto"] < 0.20:
        puntos += 2

    elif row["margenBruto"] < 0.30:
        puntos += 1

    # Utilidad
    if row["utilidadNeta"] < 0:
        puntos += 2

    # Mora
    if mora > 30:
        puntos += 3

    elif mora > 15:
        puntos += 1

    # Historial
    if (
        "malo" in historial
        or "incum" in historial
    ):
        puntos += 3

    elif "regular" in historial:
        puntos += 1

    if puntos >= 7:
        return "ALTO"

    if puntos >= 3:
        return "MEDIO"

    return "BAJO"


# ============================================================
# VIABILIDAD
# ============================================================

def evaluar_viabilidad(riesgo, row):

    if (
        riesgo == "BAJO"
        and row["cobertura"] >= 1.30
        and row["endeudamiento"] <= 0.50
        and row["utilidadNeta"] >= 0
    ):
        return "VIABLE"

    if (
        riesgo == "MEDIO"
        and row["cobertura"] >= 1
        and row["utilidadNeta"] >= 0
    ):
        return "VIABLE CON CONDICIONES"

    return "NO VIABLE"


# ============================================================
# RECOMENDACIÓN
# ============================================================

def generar_recomendacion(viabilidad):

    if viabilidad == "VIABLE":

        return (
            "Continuar estudio y validar soportes, "
            "flujo de caja y capacidad de pago."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "Solicitar soportes adicionales y evaluar "
            "monto y plazo según capacidad de pago."
        )

    return (
        "No recomendar aprobación en primera instancia. "
        "Revisar endeudamiento, capacidad de pago, "
        "rentabilidad e historial."
    )


# ============================================================
# SEMÁFOROS
# ============================================================

def semaforo_endeudamiento(v):

    if v > 0.70:

        return (
            "🔴",
            "Alto",
            "Una proporción elevada de los activos está financiada con deuda."
        )

    if v > 0.50:

        return (
            "🟠",
            "Moderado",
            "El nivel de deuda es considerable y debe vigilarse."
        )

    return (
        "🟢",
        "Adecuado",
        "La proporción de deuda sobre los activos es manejable."
    )


def semaforo_cobertura(v):

    if v < 1:

        return (
            "🔴",
            "Riesgo",
            "El flujo disponible no alcanza para cubrir completamente la cuota."
        )

    if v < 1.30:

        return (
            "🟠",
            "Ajustada",
            "El flujo cubre la cuota, pero con poco margen."
        )

    return (
        "🟢",
        "Adecuada",
        "El flujo disponible cubre la cuota con holgura."
    )


def semaforo_margen(v):

    if v < 0.20:

        return (
            "🔴",
            "Bajo",
            "El negocio tiene poca capacidad para absorber gastos adicionales."
        )

    if v < 0.30:

        return (
            "🟠",
            "Moderado",
            "El margen es aceptable, aunque limitado."
        )

    return (
        "🟢",
        "Bueno",
        "El negocio conserva un margen saludable sobre sus ventas."
    )


def semaforo_liquidez(v):

    if v < 1:

        return (
            "🔴",
            "Atención",
            "Los activos corrientes no cubren totalmente las obligaciones de corto plazo."
        )

    if v < 1.20:

        return (
            "🟠",
            "Ajustada",
            "La liquidez cubre lo corriente pero con poco colchón."
        )

    return (
        "🟢",
        "Adecuada",
        "Los activos corrientes cubren cómodamente las obligaciones."
    )


def semaforo_utilidad(v):

    if v < 0:

        return (
            "🔴",
            "Negativa",
            "El negocio no genera excedente después de costos y gastos."
        )

    return (
        "🟢",
        "Positiva",
        "El negocio genera excedente después de costos y gastos."
    )


# ============================================================
# CLIENTE
# ============================================================

def nombre_cliente(row):

    campos = [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
        "Nombre",
        "Razón_Social",
        "Razon_Social",
    ]

    for campo in campos:

        if campo in row:

            valor = row[campo]

            if (
                pd.notna(valor)
                and str(valor).strip()
            ):
                return valor

    return "Cliente"


# ============================================================
# CONCLUSIÓN
# ============================================================

def generar_conclusion(row):

    viabilidad = row["viabilidad"]

    if viabilidad == "VIABLE":

        return (
            "El negocio presenta indicadores financieros sólidos "
            "y consistentes. Se recomienda continuar con el estudio "
            "de crédito, validando soportes documentales y "
            "comportamiento histórico de pago."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "El negocio presenta un perfil aceptable pero con "
            "puntos de atención. Se recomienda solicitar información "
            "adicional y ajustar monto o plazo según la capacidad "
            "de pago real."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente "
        "y/o un nivel de riesgo elevado. No se recomienda aprobar "
        "en primera instancia. Se debe revisar la estructura de "
        "obligaciones y solicitar información adicional."
    )


# ============================================================
# DIAGNÓSTICO
# ============================================================

def generar_diagnostico_cliente(row):

    e_i, e_l, e_t = semaforo_endeudamiento(
        row["endeudamiento"]
    )

    c_i, c_l, c_t = semaforo_cobertura(
        row["cobertura"]
    )

    m_i, m_l, m_t = semaforo_margen(
        row["margenBruto"]
    )

    liq_i, liq_l, liq_t = semaforo_liquidez(
        row["liquidez"]
    )

    u_i, u_l, u_t = semaforo_utilidad(
        row["utilidadNeta"]
    )

    return f"""
    <div class="diag-box">

        <div class="diag-title">
            Diagnóstico financiero — {safe_text(nombre_cliente(row))}
        </div>

        <div class="diag-row">
            <span class="diag-icon">{e_i}</span>
            <span class="diag-text">
                <strong>Endeudamiento:</strong>
                {percent(row["endeudamiento"])}
                → {e_l}.
                {e_t}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{c_i}</span>
            <span class="diag-text">
                <strong>Cobertura:</strong>
                {row["cobertura"]:.2f}x
                → {c_l}.
                {c_t}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{m_i}</span>
            <span class="diag-text">
                <strong>Margen bruto:</strong>
                {percent(row["margenBruto"])}
                → {m_l}.
                {m_t}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{liq_i}</span>
            <span class="diag-text">
                <strong>Liquidez:</strong>
                {row["liquidez"]:.2f}x
                → {liq_l}.
                {liq_t}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{u_i}</span>
            <span class="diag-text">
                <strong>Utilidad neta:</strong>
                {money(row["utilidadNeta"])}
                → {u_l}.
                {u_t}
            </span>
        </div>

        <div class="conclusion-box">

            <div class="conclusion-title">
                Conclusión
            </div>

            <div>
                {safe_text(generar_conclusion(row))}
            </div>

            <div style="margin-top:10px;">
                <strong>Recomendación comercial:</strong>
                {safe_text(row["recomendacion"])}
            </div>

        </div>

    </div>
    """


# ============================================================
# PROCESAMIENTO
# ============================================================

@st.cache_data(show_spinner=False)
def procesar_dataframe(df):

    df = preparar_dataframe_base(df)

    indicadores = df.apply(
        calcular_indicadores,
        axis=1
    )

    df = pd.concat(
        [
            df,
            indicadores
        ],
        axis=1
    )

    df["riesgo"] = df.apply(
        clasificar_riesgo,
        axis=1
    )

    df["viabilidad"] = df.apply(
        lambda r: evaluar_viabilidad(
            r["riesgo"],
            r
        ),
        axis=1
    )

    df["recomendacion"] = (
        df["viabilidad"]
        .apply(generar_recomendacion)
    )

    return df


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            margin-bottom:10px;
        ">

            <div style="
                width:32px;
                height:32px;
                background:{PRIMARY};
                color:white;
                border-radius:6px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:800;
            ">
                F
            </div>

            <span style="
                font-weight:700;
                font-size:18px;
            ">
                FinanData AI
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Dashboard comercial · Análisis financiero de negocios"
    )

    st.divider()

    # ========================================================
    # CARGAR ARCHIVO
    # ========================================================

    archivo = st.file_uploader(
        "📁 Cargar Excel",
        type=["xlsx", "xls", "csv"],
        key="archivo_excel"
    )

    if "clientes_df" not in st.session_state:
        st.session_state.clientes_df = None

    if archivo is not None:

        try:

            if archivo.name.lower().endswith(".csv"):

                df_raw = pd.read_csv(archivo)

            else:

                df_raw = pd.read_excel(archivo)

            if df_raw.empty:

                st.error(
                    "El archivo no contiene registros."
                )

            else:

                st.session_state.clientes_df = (
                    procesar_dataframe(df_raw)
                )

                st.success(
                    f"Archivo cargado: {archivo.name}"
                )

        except Exception as error:

            st.error(
                f"No fue posible leer el archivo: {error}"
            )

    st.divider()

    # ========================================================
    # INFORMACIÓN REQUERIDA
    # ========================================================

    with st.expander(
        "📋 Información requerida para el análisis",
        expanded=True
    ):

        st.markdown(
            """
            El archivo Excel debe contener **una sola hoja**
            con la información base de cada negocio.

            **Columnas requeridas:**

            - `ID_Cliente`
            - `Cliente`
            - `Ciudad`
            - `Actividad_Economica`
            - `Ventas_Mensuales`
            - `Costo_Ventas`
            - `Gastos_Operativos`
            - `Gastos_Financieros`
            - `Activos_Corrientes`
            - `Pasivos_Corrientes`
            - `Activos_Totales`
            - `Pasivos_Totales`
            - `Patrimonio`
            - `Cuota_Mensual_Credito`
            - `Antiguedad_Negocio_Anios`
            - `Historial_Pagos`
            - `Dias_Mora_Max`
            - `Tiene_Centrales`

            **Recomendación:** mantener los nombres de las
            columnas exactamente como aparecen arriba.

            Los valores financieros deben estar expresados
            en pesos colombianos. El sistema calcula
            automáticamente los indicadores financieros,
            nivel de riesgo, viabilidad y recomendación comercial.
            """
        )

    # ========================================================
    # INTERPRETACIÓN
    # ========================================================

    with st.expander(
        "ℹ️ ¿Cómo interpretar los indicadores?"
    ):

        st.markdown(
            """
            **Endeudamiento**

            Pasivos totales / Activos totales.

            - Menor o igual a 50% → nivel manejable.
            - Entre 50% y 70% → requiere atención.
            - Superior a 70% → nivel alto.

            **Cobertura / DSCR**

            Flujo disponible / Cuota mensual del crédito.

            - Menor a 1.00x → no cubre la cuota.
            - Entre 1.00x y 1.30x → cobertura ajustada.
            - Superior o igual a 1.30x → mayor holgura.

            **Margen bruto**

            (Ventas - Costo de ventas) / Ventas.

            **Liquidez**

            Activos corrientes / Pasivos corrientes.

            - Menor a 1.00x → atención.
            - Entre 1.00x y 1.20x → ajustada.
            - Superior a 1.20x → adecuada.

            **Utilidad neta**

            Utilidad bruta - Gastos operativos -
            Gastos financieros.

            Estos indicadores se analizan conjuntamente para
            determinar el nivel preliminar de riesgo y viabilidad.
            """
        )


# ============================================================
# DATAFRAME
# ============================================================

df = st.session_state.get(
    "clientes_df"
)


# ============================================================
# ENCABEZADO
# ============================================================

col_titulo, col_selector = st.columns(
    [2.2, 1]
)

with col_titulo:

    st.markdown(
        '<div class="main-title">Dashboard comercial</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Visualización y análisis financiero de negocios'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# SELECTOR CLIENTE
# ============================================================

opciones_cliente = [
    "Todos los clientes"
]

if df is not None:

    opciones_cliente += [
        f"{i} · {nombre_cliente(row)}"
        for i, row in df.iterrows()
    ]

with col_selector:

    seleccion = st.selectbox(
        "Cliente",
        opciones_cliente,
        label_visibility="collapsed",
        key="selector_cliente"
    )


# ============================================================
# SIN ARCHIVO
# ============================================================

if df is None:

    st.info(
        "📁 Carga un archivo Excel desde la barra lateral "
        "para comenzar el análisis."
    )

    st.stop()


# ============================================================
# FILTRAR
# ============================================================

if seleccion == "Todos los clientes":

    datos = df
    cliente_idx = None

else:

    cliente_idx = int(
        seleccion.split(" · ")[0]
    )

    datos = df.loc[
        [cliente_idx]
    ]


# ============================================================
# KPIs
# ============================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)

kpis = [
    (
        k1,
        "k1",
        "Total negocios",
        f"{len(datos)}"
    ),
    (
        k2,
        "k2",
        "Ventas promedio",
        money(datos["ventas"].mean())
    ),
    (
        k3,
        "k3",
        "Margen promedio",
        percent(datos["margenBruto"].mean())
    ),
    (
        k4,
        "k4",
        "Utilidad neta",
        money(datos["utilidadNeta"].mean())
    ),
    (
        k5,
        "k5",
        "Endeudamiento",
        percent(datos["endeudamiento"].mean())
    ),
    (
        k6,
        "k6",
        "Cobertura",
        f"{datos['cobertura'].mean():.2f}x"
    )
]

for columna, clase, etiqueta, valor in kpis:

    with columna:

        st.markdown(
            f"""
            <div class="kpi-card {clase}">

                <div class="kpi-label">
                    {safe_text(etiqueta)}
                </div>

                <div class="kpi-value">
                    {safe_text(valor)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


st.write("")


# ============================================================
# DIAGNÓSTICO
# ============================================================

st.markdown(
    '<h3 class="section-title">'
    '💡 Diagnóstico y recomendación financiera'
    '</h3>',
    unsafe_allow_html=True
)


if cliente_idx is not None:

    fila = df.loc[cliente_idx]

    st.markdown(
        generar_diagnostico_cliente(fila),
        unsafe_allow_html=True
    )

else:

    bajo = (
        datos["riesgo"] == "BAJO"
    ).sum()

    medio = (
        datos["riesgo"] == "MEDIO"
    ).sum()

    alto = (
        datos["riesgo"] == "ALTO"
    ).sum()

    viables = (
        datos["viabilidad"] == "VIABLE"
    ).sum()

    total = len(datos)

    if total and alto / total >= 0.40:

        texto = (
            "Se identifica una concentración importante de negocios "
            "en riesgo alto. Se recomienda fortalecer la validación "
            "de capacidad de pago, endeudamiento y comportamiento "
            "de pago antes de continuar con las aprobaciones."
        )

    else:

        texto = (
            f"El análisis preliminar identifica {viables} negocios "
            f"viables en primera instancia. La cobertura promedio "
            f"es {datos['cobertura'].mean():.2f}x y el endeudamiento "
            f"promedio es {percent(datos['endeudamiento'].mean())}. "
            "La clasificación es preliminar y debe complementarse "
            "con la política de crédito vigente."
        )

    st.markdown(
        f"""
        <div class="diag-box">

            <div class="diag-title">
                Diagnóstico general de cartera
            </div>

            <div class="diag-row">

                <span class="diag-icon">
                    📊
                </span>

                <span class="diag-text">
                    {safe_text(texto)}
                </span>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# DISTRIBUCIÓN DEL RIESGO
# ============================================================

st.markdown(
    '<h3 class="section-title">Distribución del riesgo</h3>',
    unsafe_allow_html=True
)

r1, r2, r3 = st.columns(3)


with r1:

    st.markdown(
        f"""
        <div class="risk-card risk-low">

            <small>RIESGO BAJO</small>

            <div class="risk-number">
                {(df["riesgo"] == "BAJO").sum()}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with r2:

    st.markdown(
        f"""
        <div class="risk-card risk-medium">

            <small>RIESGO MEDIO</small>

            <div class="risk-number">
                {(df["riesgo"] == "MEDIO").sum()}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with r3:

    st.markdown(
        f"""
        <div class="risk-card risk-high">

            <small>RIESGO ALTO</small>

            <div class="risk-number">
                {(df["riesgo"] == "ALTO").sum()}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# GRÁFICAS
# ============================================================

g1, g2 = st.columns(2)


# ============================================================
# GRÁFICA 1 - RIESGO
# ============================================================

with g1:

    st.markdown("**Distribución del riesgo**")

    conteo = (
        df["riesgo"]
        .value_counts()
        .reindex(
            [
                "BAJO",
                "MEDIO",
                "ALTO"
            ]
        )
        .fillna(0)
    )

    fig_riesgo = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Riesgo bajo",
                    "Riesgo medio",
                    "Riesgo alto"
                ],
                values=conteo.values,
                hole=0.52,
                marker=dict(
                    colors=[
                        RISK_LOW,
                        RISK_MEDIUM,
                        RISK_HIGH
                    ]
                ),
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Negocios: %{value}<br>"
                    "Participación: %{percent}"
                    "<extra></extra>"
                )
            )
        ]
    )

    fig_riesgo.update_layout(
        margin=dict(
            t=20,
            b=10,
            l=10,
            r=10
        ),
        height=330,
        legend=dict(
            orientation="h"
        )
    )

    st.plotly_chart(
        fig_riesgo,
        use_container_width=True
    )


# ============================================================
# GRÁFICA 2 - LIQUIDEZ VS ENDEUDAMIENTO
# ============================================================

with g2:

    st.markdown(
        "**Liquidez vs. Endeudamiento**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Relación entre capacidad de cubrir obligaciones
            de corto plazo y nivel de deuda.
        </div>
        """,
        unsafe_allow_html=True
    )

    chart_data = datos.copy()

    chart_data["Cliente_Display"] = (
        chart_data.apply(
            nombre_cliente,
            axis=1
        )
    )

    chart_data["Endeudamiento_%"] = (
        chart_data["endeudamiento"] * 100
    )

    chart_data["Liquidez_x"] = (
        chart_data["liquidez"]
    )

    fig_liquidez = px.scatter(
        chart_data,
        x="Endeudamiento_%",
        y="Liquidez_x",
        color="riesgo",
        color_discrete_map={
            "BAJO": RISK_LOW,
            "MEDIO": RISK_MEDIUM,
            "ALTO": RISK_HIGH
        },
        hover_name="Cliente_Display",
        hover_data={
            "Endeudamiento_%": ":.1f",
            "Liquidez_x": ":.2f",
            "riesgo": True
        },
        labels={
            "Endeudamiento_%": "Endeudamiento (%)",
            "Liquidez_x": "Liquidez (x)",
            "riesgo": "Riesgo"
        }
    )

    fig_liquidez.add_vline(
        x=50,
        line_dash="dash",
        line_color=PURPLE,
        annotation_text="50%"
    )

    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color=RISK_HIGH,
        annotation_text="70%"
    )

    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color=RISK_HIGH,
        annotation_text="1.00x"
    )

    fig_liquidez.update_traces(
        marker=dict(
            size=13,
            line=dict(
                width=1,
                color="white"
            )
        )
    )

    fig_liquidez.update_layout(
        margin=dict(
            t=25,
            b=10,
            l=10,
            r=10
        ),
        height=330,
        legend=dict(
            orientation="h"
        )
    )

    st.plotly_chart(
        fig_liquidez,
        use_container_width=True
    )


# ============================================================
# DSCR
# ============================================================

g3, g4 = st.columns(2)


# ============================================================
# GRÁFICA 3 - DSCR
# ============================================================

with g3:

    st.markdown(
        "**DSCR / Cobertura de deuda**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Capacidad del flujo disponible para cubrir
            la cuota mensual del crédito.
        </div>
        """,
        unsafe_allow_html=True
    )

    dscr_data = datos.copy()

    dscr_data["Cliente_Display"] = (
        dscr_data.apply(
            nombre_cliente,
            axis=1
        )
    )

    fig_dscr = px.bar(
        dscr_data,
        x="Cliente_Display",
        y="cobertura",
        color="riesgo",
        color_discrete_map={
            "BAJO": RISK_LOW,
            "MEDIO": RISK_MEDIUM,
            "ALTO": RISK_HIGH
        },
        hover_name="Cliente_Display",
        hover_data={
            "cobertura": ":.2f",
            "riesgo": True
        },
        labels={
            "Cliente_Display": "Cliente",
            "cobertura": "DSCR / Cobertura (x)",
            "riesgo": "Riesgo"
        }
    )

    fig_dscr.add_hline(
        y=1,
        line_dash="dash",
        line_color=RISK_HIGH,
        annotation_text="Mínimo 1.00x"
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color=RISK_LOW,
        annotation_text="Objetivo 1.30x"
    )

    fig_dscr.update_layout(
        margin=dict(
            t=25,
            b=55,
            l=10,
            r=10
        ),
        height=330,
        xaxis=dict(
            tickangle=-35
        ),
        legend=dict(
            orientation="h"
        )
    )

    st.plotly_chart(
        fig_dscr,
        use_container_width=True
    )


# ============================================================
# GRÁFICA 4 - RANKING DSCR
# ============================================================

with g4:

    st.markdown(
        "**DSCR / Cobertura por cliente**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Comparación individual de la capacidad de
            cobertura de deuda.
        </div>
        """,
        unsafe_allow_html=True
    )

    ranking_dscr = datos.copy()

    ranking_dscr["Cliente_Display"] = (
        ranking_dscr.apply(
            nombre_cliente,
            axis=1
        )
    )

    ranking_dscr = ranking_dscr.sort_values(
        "cobertura",
        ascending=True
    )

    fig_horizontal = px.bar(
        ranking_dscr,
        x="cobertura",
        y="Cliente_Display",
        orientation="h",
        color="riesgo",
        color_discrete_map={
            "BAJO": RISK_LOW,
            "MEDIO": RISK_MEDIUM,
            "ALTO": RISK_HIGH
        },
        hover_name="Cliente_Display",
        hover_data={
            "cobertura": ":.2f",
            "riesgo": True
        },
        labels={
            "cobertura": "DSCR / Cobertura (x)",
            "Cliente_Display": "",
            "riesgo": "Riesgo"
        }
    )

    fig_horizontal.add_vline(
        x=1,
        line_dash="dash",
        line_color=RISK_HIGH,
        annotation_text="1.00x"
    )

    fig_horizontal.add_vline(
        x=1.30,
        line_dash="dot",
        line_color=RISK_LOW,
        annotation_text="1.30x"
    )

    fig_horizontal.update_layout(
        margin=dict(
            t=25,
            b=10,
            l=10,
            r=10
        ),
        height=330,
        legend=dict(
            orientation="h"
        )
    )

    st.plotly_chart(
        fig_horizontal,
        use_container_width=True
    )


st.write("")


# ============================================================
# DETALLE DEL CLIENTE
# ============================================================

st.markdown(
    '<h3 class="section-title">👤 Detalle del cliente</h3>',
    unsafe_allow_html=True
)


if cliente_idx is None:

    st.caption(
        "Selecciona un cliente en el menú superior "
        "para visualizar su información."
    )

else:

    fila = df.loc[cliente_idx]

    ciudad = get_field(
        fila,
        [
            "Ciudad",
            "Municipio"
        ],
        "-"
    )

    actividad = get_field(
        fila,
        [
            "Actividad_Economica",
            "Actividad",
            "Actividad Económica"
        ],
        "-"
    )

    d1, d2, d3, d4 = st.columns(4)

    campos = [
        (
            "CLIENTE",
            nombre_cliente(fila)
        ),
        (
            "CIUDAD",
            ciudad
        ),
        (
            "ACTIVIDAD",
            actividad
        ),
        (
            "VENTAS MENSUALES",
            money(fila["ventas"])
        ),
        (
            "UTILIDAD NETA",
            money(fila["utilidadNeta"])
        ),
        (
            "MARGEN",
            percent(fila["margenBruto"])
        ),
        (
            "ENDEUDAMIENTO",
            percent(fila["endeudamiento"])
        ),
        (
            "LIQUIDEZ",
            f"{fila['liquidez']:.2f}x"
        ),
        (
            "COBERTURA",
            f"{fila['cobertura']:.2f}x"
        ),
        (
            "CAPITAL DE TRABAJO",
            money(fila["capitalTrabajo"])
        ),
        (
            "APALANCAMIENTO",
            f"{fila['apalancamiento']:.2f}x"
        ),
        (
            "RIESGO",
            fila["riesgo"]
        ),
        (
            "VIABILIDAD",
            fila["viabilidad"]
        )
    ]

    columnas_detalle = [
        d1,
        d2,
        d3,
        d4
    ]

    for i, (label, value) in enumerate(campos):

        with columnas_detalle[i % 4]:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    border-radius:8px;
                    padding:10px;
                    margin-bottom:8px;
                ">

                    <small style="
                        color:#778399;
                    ">
                        {safe_text(label)}
                    </small>

                    <br>

                    <strong style="
                        color:{TEXT};
                    ">
                        {safe_text(value)}
                    </strong>

                </div>
                """,
                unsafe_allow_html=True
            )


st.write("")


# ============================================================
# TABLA
# ============================================================

st.markdown(
    '<h3 class="section-title">'
    '⚠️ Señales y recomendación comercial'
    '</h3>',
    unsafe_allow_html=True
)

tabla = df.copy()

tabla["Cliente"] = (
    tabla.apply(
        nombre_cliente,
        axis=1
    )
)

tabla_mostrar = tabla[
    [
        "Cliente",
        "ventas",
        "margenBruto",
        "endeudamiento",
        "cobertura",
        "riesgo",
        "viabilidad",
        "recomendacion"
    ]
].copy()

tabla_mostrar["ventas"] = (
    tabla_mostrar["ventas"]
    .apply(money)
)

tabla_mostrar["margenBruto"] = (
    tabla_mostrar["margenBruto"]
    .apply(percent)
)

tabla_mostrar["endeudamiento"] = (
    tabla_mostrar["endeudamiento"]
    .apply(percent)
)

tabla_mostrar["cobertura"] = (
    tabla_mostrar["cobertura"]
    .apply(
        lambda x: f"{x:.2f}x"
    )
)

tabla_mostrar.columns = [
    "Cliente",
    "Ventas",
    "Margen",
    "Endeudamiento",
    "Cobertura",
    "Riesgo",
    "Viabilidad",
    "Recomendación"
]

st.dataframe(
    tabla_mostrar,
    use_container_width=True,
    hide_index=True
)


st.write("")


# ============================================================
# ASISTENTE IA COMERCIAL
# ============================================================

bajo = (
    df["riesgo"] == "BAJO"
).sum()

medio = (
    df["riesgo"] == "MEDIO"
).sum()

alto = (
    df["riesgo"] == "ALTO"
).sum()

viables = (
    df["viabilidad"] == "VIABLE"
).sum()


st.markdown(
    f"""
    <div class="assistant-box">

        <div class="assistant-title">
            🤖 Asistente IA comercial
        </div>

        <div class="assistant-text">

            El análisis identifica
            <strong>{bajo}</strong>
            negocios en riesgo bajo,

            <strong>{medio}</strong>
            en riesgo medio y

            <strong>{alto}</strong>
            en riesgo alto.

            Se identifican
            <strong>{viables}</strong>
            perfiles viables en primera instancia.

            <br><br>

            Estos resultados constituyen una herramienta
            de apoyo para el análisis comercial y financiero.
            No reemplazan la política de crédito ni la decisión
            crediticia definitiva.

        </div>

    </div>
    """,
    unsafe_allow_html=True
)
