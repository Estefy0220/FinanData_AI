"""
FinanData AI - Dashboard comercial
Análisis financiero automatizado para estudio preliminar de crédito.

Aplicación desarrollada en Streamlit.

El usuario carga un archivo Excel o CSV con la información financiera
del negocio y el sistema calcula automáticamente indicadores,
clasificación de riesgo, viabilidad y recomendación comercial.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from html import escape


# ======================================================================
# CONFIGURACIÓN
# ======================================================================

st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================================================================
# PALETA FINANDATA AI
# ======================================================================

PRIMARY = "#0757C9"
BLUE = "#0878E8"
CYAN = "#0CA5BA"
PURPLE = "#7050F6"
PURPLE_2 = "#8B4DF1"
GREEN = "#05C47A"

RISK_LOW = "#05C47A"
RISK_MED = "#F59E0B"
RISK_HIGH = "#EF4444"

BACKGROUND = "#F4F7FB"
TEXT = "#25344A"
MUTED = "#667085"


# ======================================================================
# ESTILOS
# ======================================================================

st.markdown(
    f"""
    <style>

    /* ==============================================================
       FONDO GENERAL
       ============================================================== */

    .stApp {{
        background: {BACKGROUND};
    }}

    /* ==============================================================
       TITULOS
       ============================================================== */

    h1, h2, h3 {{
        color: {TEXT} !important;
    }}

    /* ==============================================================
       SIDEBAR
       ============================================================== */

    section[data-testid="stSidebar"] {{
        background: #FFFFFF;
    }}

    /* ==============================================================
       KPI
       ============================================================== */

    .kpi-card {{
        border-radius: 10px;
        padding: 14px 16px;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,.08);
        min-height: 100px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
        overflow: hidden;
        margin-bottom: 8px;
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
        font-size: 22px;
        font-weight: 800;
        line-height: 1.05;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .kpi-sales {{
        font-size: 19px;
        font-weight: 800;
        line-height: 1.05;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .k1 {{ background: {PURPLE}; }}
    .k2 {{ background: {BLUE}; }}
    .k3 {{ background: {CYAN}; }}
    .k4 {{ background: {GREEN}; }}
    .k5 {{ background: {PURPLE_2}; }}
    .k6 {{ background: {PRIMARY}; }}

    /* ==============================================================
       CAJAS
       ============================================================== */

    .info-box {{
        background: #FFFFFF;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,.06);
        margin-bottom: 12px;
    }}

    .info-title {{
        font-size: 16px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 10px;
    }}

    .info-text {{
        font-size: 13px;
        color: #475467;
        line-height: 1.55;
    }}

    /* ==============================================================
       DIAGNÓSTICO
       ============================================================== */

    .diag-box {{
        background: #FFFFFF;
        border-left: 5px solid {PRIMARY};
        border-radius: 9px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,.06);
        color: {TEXT};
        margin-bottom: 12px;
    }}

    .diag-title {{
        font-size: 16px;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 14px;
    }}

    .diag-row {{
        display: flex;
        align-items: flex-start;
        gap: 9px;
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

    .diag-text strong {{
        color: {TEXT};
    }}

    .conclusion-box {{
        background: #F4F6F9;
        border-radius: 8px;
        padding: 14px 16px;
        margin-top: 16px;
        color: #344054;
        font-size: 13px;
        line-height: 1.55;
    }}

    .conclusion-title {{
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 6px;
    }}

    .recommendation {{
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #E4E7EC;
    }}

    /* ==============================================================
       RIESGO
       ============================================================== */

    .risk-low {{
        border-left: 5px solid {RISK_LOW};
        padding: 12px 15px;
        border-radius: 8px;
        background: #FFFFFF;
        box-shadow: 0 2px 6px rgba(0,0,0,.04);
    }}

    .risk-med {{
        border-left: 5px solid {RISK_MED};
        padding: 12px 15px;
        border-radius: 8px;
        background: #FFFFFF;
        box-shadow: 0 2px 6px rgba(0,0,0,.04);
    }}

    .risk-high {{
        border-left: 5px solid {RISK_HIGH};
        padding: 12px 15px;
        border-radius: 8px;
        background: #FFFFFF;
        box-shadow: 0 2px 6px rgba(0,0,0,.04);
    }}

    .risk-number {{
        font-size: 25px;
        font-weight: 800;
        color: {TEXT};
        margin-top: 4px;
    }}

    /* ==============================================================
       ASISTENTE
       ============================================================== */

    .assistant-box {{
        background: linear-gradient(
            135deg,
            #EEF5FF,
            #F8FBFF
        );
        border: 1px solid #DCEAFE;
        border-radius: 10px;
        padding: 18px 20px;
        color: #344054;
        margin-top: 10px;
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
        margin: 0;
    }}

    /* ==============================================================
       INDICADORES
       ============================================================== */

    .indicator-box {{
        background: #FFFFFF;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 8px;
        border: 1px solid #EAECF0;
    }}

    .indicator-title {{
        font-size: 13px;
        font-weight: 700;
        color: {TEXT};
    }}

    .indicator-description {{
        font-size: 12px;
        color: {MUTED};
        line-height: 1.45;
        margin-top: 4px;
    }}

    /* ==============================================================
       INFORMACIÓN REQUERIDA
       ============================================================== */

    .required-box {{
        background: #F8FBFF;
        border: 1px solid #D6E7FF;
        border-left: 4px solid {PRIMARY};
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }}

    .required-title {{
        color: {TEXT};
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .required-text {{
        color: #475467;
        font-size: 12px;
        line-height: 1.55;
    }}

    .field-tag {{
        display: inline-block;
        background: #EAF2FF;
        color: {PRIMARY};
        padding: 3px 7px;
        border-radius: 5px;
        margin: 2px;
        font-size: 11px;
        font-weight: 600;
    }}

    /* ==============================================================
       CHART DESCRIPTION
       ============================================================== */

    .chart-description {{
        color: {MUTED};
        font-size: 12px;
        line-height: 1.45;
        margin-bottom: 8px;
    }}

    /* ==============================================================
       HEADER
       ============================================================== */

    .main-header {{
        background: #FFFFFF;
        border-radius: 10px;
        padding: 15px 20px;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,.04);
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# FUNCIONES DE UTILIDAD
# ======================================================================

def to_number(value):
    """Convierte valores numéricos colombianos a float."""

    if pd.isna(value):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if text == "":
        return 0.0

    text = (
        text
        .replace(" ", "")
        .replace("$", "")
        .replace("%", "")
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
    """Formato monetario colombiano."""

    try:
        return f"${value:,.0f}".replace(",", ".")
    except Exception:
        return "$0"


def percent(value):
    """Convierte decimal a porcentaje."""

    try:
        return f"{value * 100:.1f}%"
    except Exception:
        return "0.0%"


def safe_text(value):
    """Evita problemas de HTML."""

    return escape(str(value))


def get_field(row, names, default=0):
    """Busca un campo entre diferentes nombres."""

    for name in names:

        if name in row.index:

            value = row[name]

            if (
                value is not None
                and not pd.isna(value)
                and str(value).strip() != ""
            ):
                return value

    return default


def nombre_cliente(row):
    """Obtiene nombre del cliente."""

    nombres = [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
        "Nombre",
        "Razón_Social",
        "Razon_Social",
    ]

    for col in nombres:

        if col in row.index:

            value = row[col]

            if (
                pd.notna(value)
                and str(value).strip()
            ):
                return str(value)

    return "Cliente"


# ======================================================================
# INFORMACIÓN REQUERIDA
# ======================================================================

COLUMNAS_REQUERIDAS = [
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


# ======================================================================
# PREPARAR DATAFRAME
# ======================================================================

def preparar_dataframe_base(df):

    df = df.copy()

    # Limpiar nombres de columnas
    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    # Si existe Tiene_Centrales, conservar hasta esa columna
    columnas = list(df.columns)

    indice_centrales = None

    for i, columna in enumerate(columnas):

        normalizado = (
            str(columna)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        if (
            "tiene" in normalizado
            and "central" in normalizado
        ):
            indice_centrales = i
            break

    if indice_centrales is not None:

        df = df.iloc[
            :,
            :indice_centrales + 1
        ]

    return df


def validar_columnas(df):

    columnas = set(df.columns)

    faltantes = [
        col
        for col in COLUMNAS_REQUERIDAS
        if col not in columnas
    ]

    return faltantes


# ======================================================================
# CÁLCULO DE INDICADORES
# ======================================================================

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
                "Costo_Ventas_Mensual",
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
                "Activo_Corriente",
            ],
        )
    )

    pasivos_corrientes = to_number(
        get_field(
            row,
            [
                "Pasivos_Corrientes",
                "Pasivos corrientes",
                "Pasivo_Corriente",
            ],
        )
    )

    activos_totales = to_number(
        get_field(
            row,
            [
                "Activos_Totales",
                "Activos totales",
                "Activo_Total",
            ],
        )
    )

    pasivos_totales = to_number(
        get_field(
            row,
            [
                "Pasivos_Totales",
                "Pasivos totales",
                "Pasivo_Total",
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
                "Cuota_Credito",
            ],
        )
    )

    # --------------------------------------------------------------
    # INDICADORES
    # --------------------------------------------------------------

    utilidad_bruta = (
        ventas - costo
    )

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

    flujo_disponible = (
        utilidad_bruta - gastos
    )

    cobertura = (
        flujo_disponible / cuota
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


# ======================================================================
# CLASIFICACIÓN DE RIESGO
# ======================================================================

def clasificar_riesgo(row):

    puntos = 0

    mora = to_number(
        get_field(
            row,
            [
                "Dias_Mora_Max",
                "Días de mora",
                "Dias_Mora",
                "Dias_Mora_Maximo",
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
        or "negativo" in historial
    ):
        puntos += 3

    elif "regular" in historial:
        puntos += 1

    # Centrales
    centrales = str(
        get_field(
            row,
            ["Tiene_Centrales"],
            "",
        )
    ).lower()

    if (
        "no" in centrales
        or "negativo" in centrales
    ):
        puntos += 2

    # Clasificación
    if puntos >= 7:
        return "ALTO"

    if puntos >= 3:
        return "MEDIO"

    return "BAJO"


# ======================================================================
# VIABILIDAD
# ======================================================================

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


# ======================================================================
# RECOMENDACIÓN
# ======================================================================

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


# ======================================================================
# SEMÁFOROS
# ======================================================================

def semaforo_endeudamiento(valor):

    if valor > 0.70:

        return (
            "🔴",
            "Alto",
            "Una proporción elevada de los activos está financiada con deuda.",
        )

    if valor > 0.50:

        return (
            "🟠",
            "Moderado",
            "El nivel de deuda es considerable y debe vigilarse.",
        )

    return (
        "🟢",
        "Adecuado",
        "La proporción de deuda sobre los activos es manejable.",
    )


def semaforo_cobertura(valor):

    if valor < 1:

        return (
            "🔴",
            "Riesgo",
            "El flujo disponible no alcanza para cubrir completamente la cuota.",
        )

    if valor < 1.30:

        return (
            "🟠",
            "Ajustada",
            "El flujo cubre la cuota, pero con poco margen de holgura.",
        )

    return (
        "🟢",
        "Adecuada",
        "El flujo disponible cubre la cuota con una holgura favorable.",
    )


def semaforo_margen(valor):

    if valor < 0.20:

        return (
            "🔴",
            "Bajo",
            "El negocio tiene poca capacidad para absorber gastos adicionales.",
        )

    if valor < 0.30:

        return (
            "🟠",
            "Moderado",
            "El margen es aceptable, aunque tiene espacio limitado de maniobra.",
        )

    return (
        "🟢",
        "Bueno",
        "El negocio conserva un margen saludable sobre sus ventas.",
    )


def semaforo_liquidez(valor):

    if valor < 1:

        return (
            "🔴",
            "Atención",
            "Los activos corrientes no alcanzan para cubrir completamente las obligaciones de corto plazo.",
        )

    if valor < 1.20:

        return (
            "🟠",
            "Ajustada",
            "La liquidez cubre las obligaciones corrientes con poco colchón.",
        )

    return (
        "🟢",
        "Adecuada",
        "Los activos corrientes cubren cómodamente las obligaciones de corto plazo.",
    )


def semaforo_utilidad(valor):

    if valor < 0:

        return (
            "🔴",
            "Negativa",
            "El negocio no genera excedente después de costos y gastos.",
        )

    return (
        "🟢",
        "Positiva",
        "El negocio genera excedente después de costos y gastos.",
    )


# ======================================================================
# CONCLUSIÓN
# ======================================================================

def generar_conclusion(row):

    viabilidad = row["viabilidad"]

    if viabilidad == "VIABLE":

        return (
            "El negocio presenta indicadores financieros sólidos y "
            "consistentes. Se recomienda continuar con el estudio de "
            "crédito, validando soportes documentales y comportamiento "
            "de pago histórico."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "El negocio presenta un perfil aceptable, pero con puntos "
            "de atención. Se recomienda solicitar información adicional "
            "y ajustar monto o plazo según la capacidad de pago real."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente y/o "
        "un nivel de riesgo elevado. No se recomienda aprobar en primera "
        "instancia. Se recomienda revisar las obligaciones, capacidad "
        "de pago y comportamiento histórico."
    )


# ======================================================================
# DIAGNÓSTICO CLIENTE
# ======================================================================

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

    cliente = safe_text(
        nombre_cliente(row)
    )

    conclusion = safe_text(
        generar_conclusion(row)
    )

    recomendacion = safe_text(
        row["recomendacion"]
    )

    return f"""
    <div class="diag-box">

        <div class="diag-title">
            Diagnóstico financiero — {cliente}
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
                <strong>Cobertura / DSCR:</strong>
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
                Conclusión:
            </div>

            <div>
                {conclusion}
            </div>

            <div class="recommendation">
                <strong>Recomendación comercial:</strong>
                {recomendacion}
            </div>

        </div>

    </div>
    """


# ======================================================================
# PROCESAMIENTO
# ======================================================================

@st.cache_data(show_spinner=False)
def procesar_dataframe(df):

    df = preparar_dataframe_base(df)

    indicadores = df.apply(
        calcular_indicadores,
        axis=1,
    )

    df = pd.concat(
        [
            df,
            indicadores,
        ],
        axis=1,
    )

    df["riesgo"] = df.apply(
        clasificar_riesgo,
        axis=1,
    )

    df["viabilidad"] = df.apply(
        lambda row: evaluar_viabilidad(
            row["riesgo"],
            row,
        ),
        axis=1,
    )

    df["recomendacion"] = (
        df["viabilidad"]
        .apply(generar_recomendacion)
    )

    return df


# ======================================================================
# SIDEBAR
# ======================================================================

with st.sidebar:

    # Logo
    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            margin-bottom:8px;
        ">

            <div style="
                width:34px;
                height:34px;
                background:{PRIMARY};
                color:white;
                border-radius:7px;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:800;
                font-size:18px;
            ">
                F
            </div>

            <span style="
                font-weight:700;
                font-size:18px;
                color:{TEXT};
            ">
                FinanData AI
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Dashboard comercial · Análisis financiero de negocios"
    )

    st.divider()

    # ==============================================================
    # CARGAR ARCHIVO
    # ==============================================================

    st.markdown(
        "### 📁 Cargar información"
    )

    archivo = st.file_uploader(
        "Selecciona un archivo",
        type=[
            "xlsx",
            "xls",
            "csv",
        ],
        key="archivo_excel",
    )

    if "clientes_df" not in st.session_state:

        st.session_state.clientes_df = None

    if archivo is not None:

        try:

            if archivo.name.lower().endswith(".csv"):

                df_raw = pd.read_csv(
                    archivo
                )

            else:

                df_raw = pd.read_excel(
                    archivo
                )

            if df_raw.empty:

                st.error(
                    "El archivo no contiene registros."
                )

            else:

                faltantes = validar_columnas(
                    df_raw
                )

                if faltantes:

                    st.warning(
                        "El archivo fue leído, pero faltan algunas "
                        "columnas esperadas."
                    )

                    with st.expander(
                        "Ver columnas faltantes"
                    ):

                        for columna in faltantes:

                            st.write(
                                f"• `{columna}`"
                            )

                    st.info(
                        "El sistema intentará continuar utilizando "
                        "las columnas disponibles."
                    )

                st.session_state.clientes_df = (
                    procesar_dataframe(
                        df_raw
                    )
                )

                st.success(
                    f"Archivo cargado correctamente: "
                    f"{archivo.name}"
                )

                st.caption(
                    f"{len(df_raw)} registros encontrados."
                )

        except Exception as error:

            st.error(
                f"No fue posible leer el archivo: {error}"
            )

    st.divider()

    # ==============================================================
    # INFORMACIÓN REQUERIDA
    # ==============================================================

    st.markdown(
        "### 📋 Información requerida"
    )

    st.markdown(
        f"""
        <div class="required-box">

            <div class="required-title">
                El Excel debe contener estas 18 variables:
            </div>

            <div class="required-text">

                <span class="field-tag">ID_Cliente</span>
                <span class="field-tag">Cliente</span>
                <span class="field-tag">Ciudad</span>
                <span class="field-tag">Actividad_Economica</span>
                <span class="field-tag">Ventas_Mensuales</span>
                <span class="field-tag">Costo_Ventas</span>
                <span class="field-tag">Gastos_Operativos</span>
                <span class="field-tag">Gastos_Financieros</span>
                <span class="field-tag">Activos_Corrientes</span>
                <span class="field-tag">Pasivos_Corrientes</span>
                <span class="field-tag">Activos_Totales</span>
                <span class="field-tag">Pasivos_Totales</span>
                <span class="field-tag">Patrimonio</span>
                <span class="field-tag">Cuota_Mensual_Credito</span>
                <span class="field-tag">Antiguedad_Negocio_Anios</span>
                <span class="field-tag">Historial_Pagos</span>
                <span class="field-tag">Dias_Mora_Max</span>
                <span class="field-tag">Tiene_Centrales</span>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Los nombres de las columnas deben coincidir "
        "con la estructura indicada."
    )

    # ==============================================================
    # INTERPRETACIÓN
    # ==============================================================

    with st.expander(
        "ℹ️ ¿Cómo interpretar los indicadores?"
    ):

        st.markdown(
            """
            **Endeudamiento**

            Pasivos totales / Activos totales.

            • Menor o igual a 50% → nivel favorable.  
            • Entre 50% y 70% → requiere seguimiento.  
            • Mayor a 70% → nivel elevado de endeudamiento.

            **Cobertura / DSCR**

            Flujo disponible / Cuota mensual del crédito.

            • Menor a 1.00x → no alcanza a cubrir la cuota.  
            • Entre 1.00x y 1.30x → cobertura ajustada.  
            • Mayor o igual a 1.30x → mayor holgura.

            **Margen bruto**

            (Ventas − Costo de ventas) / Ventas.

            Mide cuánto queda de las ventas después de cubrir
            directamente el costo de ventas.

            **Liquidez**

            Activos corrientes / Pasivos corrientes.

            • Menor a 1.00x → alerta.  
            • Entre 1.00x y 1.20x → ajustada.  
            • Mayor a 1.20x → favorable.

            **Utilidad neta**

            Utilidad bruta − Gastos operativos − Gastos financieros.

            Permite identificar si el negocio genera excedentes
            después de cubrir sus principales costos y gastos.

            **Riesgo**

            Se determina combinando endeudamiento, cobertura,
            margen, utilidad, mora, historial de pagos y centrales.

            **Importante:** estos resultados constituyen un análisis
            preliminar y no reemplazan la política ni la decisión
            crediticia definitiva.
            """
        )


# ======================================================================
# OBTENER DATAFRAME
# ======================================================================

df = st.session_state.get(
    "clientes_df"
)


# ======================================================================
# ENCABEZADO
# ======================================================================

col_titulo, col_selector = st.columns(
    [2.2, 1]
)

with col_titulo:

    st.title(
        "Dashboard comercial"
    )

    st.caption(
        "Visualización y análisis financiero de negocios"
    )


# ======================================================================
# SELECTOR CLIENTE
# ======================================================================

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
        key="selector_cliente",
    )


# ======================================================================
# SIN ARCHIVO
# ======================================================================

if df is None:

    st.info(
        "📁 Carga un archivo Excel desde la barra lateral "
        "para comenzar el análisis."
    )

    st.stop()


# ======================================================================
# FILTRO
# ======================================================================

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


# ======================================================================
# KPI - FILA 1
# ======================================================================

k1, k2, k3 = st.columns(
    3
)


kpi_data_1 = [
    (
        k1,
        "k1",
        "Total negocios",
        f"{len(datos)}",
        "normal",
    ),
    (
        k2,
        "k2",
        "Ventas promedio",
        money(datos["ventas"].mean()),
        "sales",
    ),
    (
        k3,
        "k3",
        "Margen promedio",
        percent(datos["margenBruto"].mean()),
        "normal",
    ),
]


for col, clase, label, value, tipo in kpi_data_1:

    with col:

        value_class = (
            "kpi-sales"
            if tipo == "sales"
            else "kpi-value"
        )

        st.markdown(
            f"""
            <div class="kpi-card {clase}">

                <div class="kpi-label">
                    {safe_text(label)}
                </div>

                <div class="{value_class}">
                    {safe_text(value)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ======================================================================
# KPI - FILA 2
# ======================================================================

k4, k5, k6 = st.columns(
    3
)


kpi_data_2 = [
    (
        k4,
        "k4",
        "Utilidad neta",
        money(datos["utilidadNeta"].mean()),
    ),
    (
        k5,
        "k5",
        "Endeudamiento",
        percent(datos["endeudamiento"].mean()),
    ),
    (
        k6,
        "k6",
        "Cobertura",
        f"{datos['cobertura'].mean():.2f}x",
    ),
]


for col, clase, label, value in kpi_data_2:

    with col:

        st.markdown(
            f"""
            <div class="kpi-card {clase}">

                <div class="kpi-label">
                    {safe_text(label)}
                </div>

                <div class="kpi-value">
                    {safe_text(value)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


st.write("")


# ======================================================================
# DIAGNÓSTICO
# ======================================================================

st.subheader(
    "💡 Diagnóstico y recomendación financiera"
)


if cliente_idx is not None:

    fila = df.loc[
        cliente_idx
    ]

    st.markdown(
        generar_diagnostico_cliente(
            fila
        ),
        unsafe_allow_html=True,
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
            f"viables en primera instancia. La cobertura promedio es "
            f"{datos['cobertura'].mean():.2f}x y el endeudamiento "
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

            <div class="conclusion-box">

                <div class="conclusion-title">
                    Recomendación comercial:
                </div>

                Analizar individualmente los negocios clasificados
                como riesgo medio y alto antes de tomar una decisión
                de aprobación.

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================================
# DISTRIBUCIÓN DEL RIESGO
# ======================================================================

st.subheader(
    "Distribución del riesgo"
)

r1, r2, r3 = st.columns(
    3
)


with r1:

    cantidad_bajo = (
        df["riesgo"] == "BAJO"
    ).sum()

    st.markdown(
        f"""
        <div class="risk-low">

            <small>
                RIESGO BAJO
            </small>

            <div class="risk-number">
                {cantidad_bajo}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with r2:

    cantidad_medio = (
        df["riesgo"] == "MEDIO"
    ).sum()

    st.markdown(
        f"""
        <div class="risk-med">

            <small>
                RIESGO MEDIO
            </small>

            <div class="risk-number">
                {cantidad_medio}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with r3:

    cantidad_alto = (
        df["riesgo"] == "ALTO"
    ).sum()

    st.markdown(
        f"""
        <div class="risk-high">

            <small>
                RIESGO ALTO
            </small>

            <div class="risk-number">
                {cantidad_alto}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ======================================================================
# GRÁFICA 1 - RIESGO
# ======================================================================

g1, g2 = st.columns(
    2
)


with g1:

    st.markdown(
        "### Distribución del riesgo"
    )

    conteo = (
        df["riesgo"]
        .value_counts()
        .reindex(
            [
                "BAJO",
                "MEDIO",
                "ALTO",
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
                    "Riesgo alto",
                ],
                values=conteo.values,
                hole=0.52,
                marker=dict(
                    colors=[
                        RISK_LOW,
                        RISK_MED,
                        RISK_HIGH,
                    ]
                ),
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Negocios: %{value}<br>"
                    "Participación: %{percent}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    fig_riesgo.update_layout(
        margin=dict(
            t=15,
            b=10,
            l=10,
            r=10,
        ),
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h"
        ),
    )

    st.plotly_chart(
        fig_riesgo,
        use_container_width=True,
    )


# ======================================================================
# GRÁFICA 2 - LIQUIDEZ VS ENDEUDAMIENTO
# ======================================================================

with g2:

    st.markdown(
        "### Liquidez vs. Endeudamiento"
    )

    st.markdown(
        """
        <div class="chart-description">
            Permite identificar negocios con mayor nivel de deuda
            y menor capacidad de cobertura de obligaciones de corto plazo.
        </div>
        """,
        unsafe_allow_html=True,
    )

    chart_data = datos.copy()

    chart_data["Cliente_Display"] = (
        chart_data.apply(
            nombre_cliente,
            axis=1,
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
            "MEDIO": RISK_MED,
            "ALTO": RISK_HIGH,
        },
        hover_name="Cliente_Display",
        hover_data={
            "Endeudamiento_%": ":.1f",
            "Liquidez_x": ":.2f",
            "riesgo": True,
        },
        labels={
            "Endeudamiento_%": "Endeudamiento (%)",
            "Liquidez_x": "Liquidez (x)",
            "riesgo": "Riesgo",
        },
    )

    fig_liquidez.add_vline(
        x=50,
        line_dash="dash",
        line_color="#94A3B8",
        annotation_text="50%",
        annotation_position="top",
    )

    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color=RISK_HIGH,
        annotation_text="70%",
        annotation_position="top right",
    )

    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color="#94A3B8",
        annotation_text="1.0x",
        annotation_position="bottom right",
    )

    fig_liquidez.update_traces(
        marker=dict(
            size=12,
            line=dict(
                width=1,
                color="white",
            ),
        )
    )

    fig_liquidez.update_layout(
        margin=dict(
            t=30,
            b=10,
            l=10,
            r=10,
        ),
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h"
        ),
    )

    st.plotly_chart(
        fig_liquidez,
        use_container_width=True,
    )


# ======================================================================
# GRÁFICA 3 Y 4 - DSCR
# ======================================================================

g3, g4 = st.columns(
    2
)


# ======================================================================
# GRÁFICA 3 - DSCR
# ======================================================================

with g3:

    st.markdown(
        "### DSCR / Cobertura de deuda"
    )

    st.markdown(
        """
        <div class="chart-description">
            Muestra la capacidad del flujo disponible para cubrir
            la cuota mensual del crédito.
            1.00x representa el mínimo de cobertura y 1.30x
            una zona de mayor holgura.
        </div>
        """,
        unsafe_allow_html=True,
    )

    dscr_data = datos.copy()

    dscr_data["Cliente_Display"] = (
        dscr_data.apply(
            nombre_cliente,
            axis=1,
        )
    )

    fig_dscr = px.bar(
        dscr_data,
        x="Cliente_Display",
        y="cobertura",
        color="riesgo",
        color_discrete_map={
            "BAJO": RISK_LOW,
            "MEDIO": RISK_MED,
            "ALTO": RISK_HIGH,
        },
        hover_name="Cliente_Display",
        hover_data={
            "cobertura": ":.2f",
            "riesgo": True,
        },
        labels={
            "Cliente_Display": "Cliente",
            "cobertura": "DSCR / Cobertura (x)",
            "riesgo": "Riesgo",
        },
    )

    fig_dscr.add_hline(
        y=1,
        line_dash="dash",
        line_color=RISK_HIGH,
        annotation_text="Mínimo 1.00x",
        annotation_position="top left",
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color=RISK_LOW,
        annotation_text="Objetivo 1.30x",
        annotation_position="top right",
    )

    fig_dscr.update_layout(
        margin=dict(
            t=30,
            b=50,
            l=10,
            r=10,
        ),
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            tickangle=-35
        ),
        legend=dict(
            orientation="h"
        ),
    )

    st.plotly_chart(
        fig_dscr,
        use_container_width=True,
    )


# ======================================================================
# GRÁFICA 4 - RANKING DSCR
# ======================================================================

with g4:

    st.markdown(
        "### DSCR / Cobertura por cliente"
    )

    st.markdown(
        """
        <div class="chart-description">
            Ranking de los negocios según su capacidad de cubrir
            la cuota mensual del crédito.
        </div>
        """,
        unsafe_allow_html=True,
    )

    ranking_dscr = datos.copy()

    ranking_dscr["Cliente_Display"] = (
        ranking_dscr.apply(
            nombre_cliente,
            axis=1,
        )
    )

    ranking_dscr = ranking_dscr.sort_values(
        "cobertura",
        ascending=True,
    )

    fig_horizontal = px.bar(
        ranking_dscr,
        x="cobertura",
        y="Cliente_Display",
        orientation="h",
        color="riesgo",
        color_discrete_map={
            "BAJO": RISK_LOW,
            "MEDIO": RISK_MED,
            "ALTO": RISK_HIGH,
        },
        hover_name="Cliente_Display",
        hover_data={
            "cobertura": ":.2f",
            "riesgo": True,
        },
        labels={
            "cobertura": "DSCR / Cobertura (x)",
            "Cliente_Display": "",
            "riesgo": "Riesgo",
        },
    )

    fig_horizontal.add_vline(
        x=1,
        line_dash="dash",
        line_color=RISK_HIGH,
        annotation_text="1.00x",
        annotation_position="top",
    )

    fig_horizontal.add_vline(
        x=1.30,
        line_dash="dot",
        line_color=RISK_LOW,
        annotation_text="1.30x",
        annotation_position="top",
    )

    fig_horizontal.update_layout(
        margin=dict(
            t=30,
            b=10,
            l=10,
            r=10,
        ),
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h"
        ),
    )

    st.plotly_chart(
        fig_horizontal,
        use_container_width=True,
    )


st.write("")


# ======================================================================
# EXPLICACIÓN DE INDICADORES
# ======================================================================

st.subheader(
    "📚 Lectura de los principales indicadores"
)

i1, i2 = st.columns(
    2
)

with i1:

    st.markdown(
        f"""
        <div class="indicator-box">

            <div class="indicator-title">
                Endeudamiento
            </div>

            <div class="indicator-description">
                Mide qué proporción de los activos está financiada
                mediante obligaciones. Un nivel inferior al 50%
                se considera más favorable dentro de este análisis.
            </div>

        </div>

        <div class="indicator-box">

            <div class="indicator-title">
                Cobertura / DSCR
            </div>

            <div class="indicator-description">
                Indica cuántas veces el flujo disponible puede cubrir
                la cuota mensual del crédito. Un resultado de 1.30x
                o superior refleja mayor holgura.
            </div>

        </div>

        <div class="indicator-box">

            <div class="indicator-title">
                Margen bruto
            </div>

            <div class="indicator-description">
                Representa el porcentaje de las ventas que permanece
                después de cubrir el costo directo de ventas.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with i2:

    st.markdown(
        f"""
        <div class="indicator-box">

            <div class="indicator-title">
                Liquidez
            </div>

            <div class="indicator-description">
                Mide la capacidad del negocio para responder por
                sus obligaciones de corto plazo mediante sus activos
                corrientes.
            </div>

        </div>

        <div class="indicator-box">

            <div class="indicator-title">
                Utilidad neta
            </div>

            <div class="indicator-description">
                Muestra el resultado después de costos, gastos
                operativos y gastos financieros.
            </div>

        </div>

        <div class="indicator-box">

            <div class="indicator-title">
                Capital de trabajo
            </div>

            <div class="indicator-description">
                Corresponde a activos corrientes menos pasivos
                corrientes y permite observar el margen financiero
                disponible para la operación de corto plazo.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================================
# DETALLE DEL CLIENTE
# ======================================================================

st.subheader(
    "👤 Detalle del cliente"
)


if cliente_idx is None:

    st.caption(
        "Selecciona un cliente en el menú superior "
        "para visualizar su información individual."
    )

else:

    fila = df.loc[
        cliente_idx
    ]

    ciudad = get_field(
        fila,
        [
            "Ciudad",
            "Municipio",
        ],
        "-",
    )

    actividad = get_field(
        fila,
        [
            "Actividad_Economica",
            "Actividad",
            "Actividad Económica",
        ],
        "-",
    )

    antiguedad = get_field(
        fila,
        [
            "Antiguedad_Negocio_Anios",
        ],
        "-",
    )

    historial = get_field(
        fila,
        [
            "Historial_Pagos",
        ],
        "-",
    )

    d1, d2, d3, d4 = st.columns(
        4
    )

    campos = [
        (
            "CLIENTE",
            nombre_cliente(fila),
        ),
        (
            "CIUDAD",
            ciudad,
        ),
        (
            "ACTIVIDAD",
            actividad,
        ),
        (
            "ANTIGÜEDAD",
            f"{antiguedad} años",
        ),
        (
            "VENTAS MENSUALES",
            money(fila["ventas"]),
        ),
        (
            "UTILIDAD NETA",
            money(fila["utilidadNeta"]),
        ),
        (
            "MARGEN",
            percent(fila["margenBruto"]),
        ),
        (
            "ENDEUDAMIENTO",
            percent(fila["endeudamiento"]),
        ),
        (
            "LIQUIDEZ",
            f"{fila['liquidez']:.2f}x",
        ),
        (
            "COBERTURA",
            f"{fila['cobertura']:.2f}x",
        ),
        (
            "CAPITAL DE TRABAJO",
            money(fila["capitalTrabajo"]),
        ),
        (
            "APALANCAMIENTO",
            f"{fila['apalancamiento']:.2f}x",
        ),
        (
            "HISTORIAL DE PAGOS",
            historial,
        ),
        (
            "DÍAS DE MORA",
            get_field(
                fila,
                ["Dias_Mora_Max"],
                0,
            ),
        ),
        (
            "RIESGO",
            fila["riesgo"],
        ),
        (
            "VIABILIDAD",
            fila["viabilidad"],
        ),
    ]

    cols = [
        d1,
        d2,
        d3,
        d4,
    ]

    for i, (label, value) in enumerate(campos):

        with cols[i % 4]:

            st.markdown(
                f"""
                <div class="info-box">

                    <div style="
                        color:{MUTED};
                        font-size:11px;
                        font-weight:600;
                        margin-bottom:5px;
                    ">
                        {safe_text(label)}
                    </div>

                    <div style="
                        color:{TEXT};
                        font-size:14px;
                        font-weight:700;
                    ">
                        {safe_text(value)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ======================================================================
# TABLA
# ======================================================================

st.subheader(
    "⚠️ Señales y recomendación comercial"
)

tabla = df.copy()

tabla["Cliente"] = (
    tabla.apply(
        nombre_cliente,
        axis=1,
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
        "recomendacion",
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
        lambda value: f"{value:.2f}x"
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
    "Recomendación",
]

st.dataframe(
    tabla_mostrar,
    use_container_width=True,
    hide_index=True,
)


# ======================================================================
# ASISTENTE IA COMERCIAL
# ======================================================================

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

condicionados = (
    df["viabilidad"]
    == "VIABLE CON CONDICIONES"
).sum()

no_viables = (
    df["viabilidad"]
    == "NO VIABLE"
).sum()


st.markdown(
    f"""
    <div class="assistant-box">

        <div class="assistant-title">
            🤖 Asistente IA comercial
        </div>

        <p class="assistant-text">

            El análisis identifica
            <strong>{bajo}</strong>
            negocios en riesgo bajo,

            <strong>{medio}</strong>
            en riesgo medio y

            <strong>{alto}</strong>
            en riesgo alto.

            Se identifican
            <strong>{viables}</strong>
            perfiles viables en primera instancia,

            <strong>{condicionados}</strong>
            viables con condiciones y

            <strong>{no_viables}</strong>
            no viables bajo los criterios definidos.

            <br><br>

            Estos resultados constituyen una herramienta de apoyo
            para el análisis comercial y no reemplazan la política
            de crédito ni la decisión crediticia definitiva.

        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# PIE DE PÁGINA
# ======================================================================

st.write("")

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:#98A2B3;
        font-size:11px;
        padding:15px 0 5px 0;
    ">
        FinanData AI · Dashboard de análisis financiero comercial
        <br>
        Herramienta de apoyo para evaluación preliminar de negocios
    </div>
    """,
    unsafe_allow_html=True,
)
