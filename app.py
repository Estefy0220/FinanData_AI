"""
FINANDATA AI
Dashboard comercial para análisis financiero y estudio preliminar de crédito.

El usuario carga un archivo Excel con información financiera y comercial
de diferentes negocios.

Variables requeridas:
ID_Cliente
Cliente
Ciudad
Actividad_Economica
Ventas_Mensuales
Costo_Ventas
Gastos_Operativos
Gastos_Financieros
Activos_Corrientes
Pasivos_Corrientes
Activos_Totales
Pasivos_Totales
Patrimonio
Cuota_Mensual_Credito
Antiguedad_Negocio_Anios
Historial_Pagos
Dias_Mora_Max
Tiene_Centrales
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from html import escape


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRIMARY = "#0757C9"
BLUE = "#0757C9"
BLUE_LIGHT = "#0878E8"
PURPLE = "#7050F6"
PURPLE_2 = "#8B4DF1"
CYAN = "#0CA5BA"
GREEN = "#05C47A"
ORANGE = "#F59E0B"
RED = "#EF4444"
BACKGROUND = "#F4F6F9"


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       FONDO GENERAL
    ----------------------------------------------------- */

    .stApp {
        background-color: #F4F6F9;
    }

    /* -----------------------------------------------------
       SIDEBAR
    ----------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    /* -----------------------------------------------------
       TITULOS
    ----------------------------------------------------- */

    h1 {
        color: #25344A !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #25344A !important;
    }

    /* -----------------------------------------------------
       KPI
    ----------------------------------------------------- */

    .kpi-card {
        border-radius: 10px;
        padding: 14px 15px;
        color: white;
        min-height: 96px;
        height: 96px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
        box-shadow: 0 3px 8px rgba(0,0,0,0.10);
    }

    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
        opacity: 0.95;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .kpi-value {
        font-size: 21px;
        font-weight: 800;
        line-height: 1.1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .k1 {
        background: #7050F6;
    }

    .k2 {
        background: #0878E8;
    }

    .k3 {
        background: #0CA5BA;
    }

    .k4 {
        background: #05C47A;
    }

    .k5 {
        background: #8B4DF1;
    }

    .k6 {
        background: #0756C9;
    }

    /* -----------------------------------------------------
       INFORMACIÓN EXCEL
    ----------------------------------------------------- */

    .info-box {
        background: #FFFFFF;
        border-left: 5px solid #0757C9;
        border-radius: 9px;
        padding: 17px 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 7px rgba(0,0,0,0.06);
    }

    .info-title {
        color: #25344A;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .info-text {
        color: #475467;
        font-size: 13px;
        line-height: 1.55;
    }

    .column-list {
        background: #F8FAFC;
        border-radius: 7px;
        padding: 10px 14px;
        margin-top: 10px;
        color: #344054;
        font-size: 12px;
        line-height: 1.65;
    }

    /* -----------------------------------------------------
       DIAGNÓSTICO
    ----------------------------------------------------- */

    .diag-box {
        background: #FFFFFF;
        border-left: 5px solid #1264D6;
        border-radius: 9px;
        padding: 17px 19px;
        box-shadow: 0 2px 7px rgba(0,0,0,0.06);
        color: #25344A;
    }

    .diag-title {
        font-size: 16px;
        font-weight: 700;
        color: #25344A;
        margin-bottom: 13px;
    }

    .diag-row {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 13px;
        line-height: 1.5;
        margin: 9px 0;
        color: #344054;
    }

    .diag-icon {
        width: 18px;
        min-width: 18px;
    }

    .diag-text {
        flex: 1;
    }

    .diag-text strong {
        color: #25344A;
    }

    .conclusion-box {
        background: #F4F6F9;
        border-radius: 8px;
        padding: 14px 15px;
        margin-top: 15px;
        color: #344054;
        font-size: 13px;
        line-height: 1.5;
    }

    .conclusion-title {
        font-weight: 700;
        margin-bottom: 6px;
        color: #25344A;
    }

    /* -----------------------------------------------------
       RIESGO
    ----------------------------------------------------- */

    .risk-card {
        background: #FFFFFF;
        border-radius: 9px;
        padding: 13px 16px;
        box-shadow: 0 2px 7px rgba(0,0,0,0.06);
    }

    .risk-low {
        border-left: 5px solid #10B981;
    }

    .risk-med {
        border-left: 5px solid #F59E0B;
    }

    .risk-high {
        border-left: 5px solid #EF4444;
    }

    .risk-title {
        font-size: 12px;
        font-weight: 700;
        color: #667085;
    }

    .risk-number {
        font-size: 25px;
        font-weight: 800;
        color: #25344A;
        margin-top: 4px;
    }

    /* -----------------------------------------------------
       DETALLE
    ----------------------------------------------------- */

    .detail-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 12px 14px;
        min-height: 70px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    .detail-label {
        color: #778399;
        font-size: 11px;
        font-weight: 600;
    }

    .detail-value {
        color: #25344A;
        font-size: 14px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* -----------------------------------------------------
       ASISTENTE
    ----------------------------------------------------- */

    .assistant-box {
        background: linear-gradient(
            135deg,
            #EEF5FF,
            #F8FBFF
        );
        border: 1px solid #DCEAFE;
        border-radius: 9px;
        padding: 18px;
        color: #344054;
    }

    .assistant-title {
        font-size: 16px;
        font-weight: 700;
        color: #25344A;
        margin-bottom: 8px;
    }

    .assistant-text {
        font-size: 13px;
        line-height: 1.55;
        margin: 0;
    }

    /* -----------------------------------------------------
       DESCRIPCIÓN GRÁFICAS
    ----------------------------------------------------- */

    .chart-description {
        color: #667085;
        font-size: 12px;
        margin-top: -5px;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def to_number(value):

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

    except Exception:
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
                and not pd.isna(value)
                and str(value).strip() != ""
            ):
                return value

    return default


def nombre_cliente(row):

    campos = [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
        "Nombre",
        "Razon_Social",
        "Razón_Social"
    ]

    for campo in campos:

        if campo in row:

            valor = row[campo]

            if (
                pd.notna(valor)
                and str(valor).strip() != ""
            ):
                return str(valor)

    return "Cliente"


# ============================================================
# VALIDACIÓN DEL EXCEL
# ============================================================

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
    "Tiene_Centrales"
]


def validar_excel(df):

    columnas_actuales = list(df.columns)

    faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in columnas_actuales
    ]

    return faltantes


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
                "Ingresos"
            ]
        )
    )

    costo = to_number(
        get_field(
            row,
            [
                "Costo_Ventas",
                "Costo de ventas",
                "Costos_Ventas"
            ]
        )
    )

    gastos = to_number(
        get_field(
            row,
            [
                "Gastos_Operativos",
                "Gastos operativos",
                "Gastos_Operacion"
            ]
        )
    )

    financieros = to_number(
        get_field(
            row,
            [
                "Gastos_Financieros",
                "Gastos financieros"
            ]
        )
    )

    activos_corrientes = to_number(
        get_field(
            row,
            [
                "Activos_Corrientes",
                "Activos corrientes"
            ]
        )
    )

    pasivos_corrientes = to_number(
        get_field(
            row,
            [
                "Pasivos_Corrientes",
                "Pasivos corrientes"
            ]
        )
    )

    activos_totales = to_number(
        get_field(
            row,
            [
                "Activos_Totales",
                "Activos totales"
            ]
        )
    )

    pasivos_totales = to_number(
        get_field(
            row,
            [
                "Pasivos_Totales",
                "Pasivos totales"
            ]
        )
    )

    cuota = to_number(
        get_field(
            row,
            [
                "Cuota_Mensual_Credito",
                "Cuota mensual credito",
                "Cuota_Mensual",
                "Cuota"
            ]
        )
    )

    # --------------------------------------------------------
    # INDICADORES
    # --------------------------------------------------------

    utilidad_bruta = ventas - costo

    margen_bruto = (
        utilidad_bruta / ventas
        if ventas > 0
        else 0
    )

    utilidad_neta = (
        utilidad_bruta
        - gastos
        - financieros
    )

    margen_neto = (
        utilidad_neta / ventas
        if ventas > 0
        else 0
    )

    capital_trabajo = (
        activos_corrientes
        - pasivos_corrientes
    )

    endeudamiento = (
        pasivos_totales / activos_totales
        if activos_totales > 0
        else 0
    )

    liquidez = (
        activos_corrientes / pasivos_corrientes
        if pasivos_corrientes > 0
        else 0
    )

    flujo_disponible = (
        utilidad_bruta
        - gastos
    )

    cobertura = (
        flujo_disponible / cuota
        if cuota > 0
        else 0
    )

    patrimonio = max(
        activos_totales - pasivos_totales,
        1
    )

    apalancamiento = (
        pasivos_totales / patrimonio
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
            "apalancamiento": apalancamiento
        }
    )


# ============================================================
# CLASIFICACIÓN DE RIESGO
# ============================================================

def clasificar_riesgo(row):

    puntos = 0

    mora = to_number(
        get_field(
            row,
            [
                "Dias_Mora_Max",
                "Dias_Mora",
                "Días de mora"
            ],
            0
        )
    )

    historial = str(
        get_field(
            row,
            [
                "Historial_Pagos",
                "Historial de pagos",
                "Historial_Pago"
            ],
            ""
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

def semaforo_endeudamiento(valor):

    if valor > 0.70:
        return (
            "🔴",
            "Alto",
            "El nivel de deuda es elevado frente al total de activos."
        )

    if valor > 0.50:
        return (
            "🟠",
            "Moderado",
            "El endeudamiento requiere seguimiento."
        )

    return (
        "🟢",
        "Adecuado",
        "La proporción de deuda es manejable."
    )


def semaforo_cobertura(valor):

    if valor < 1:
        return (
            "🔴",
            "Riesgo",
            "El flujo disponible no cubre completamente la cuota."
        )

    if valor < 1.30:
        return (
            "🟠",
            "Ajustada",
            "La cuota se cubre, pero con poca holgura."
        )

    return (
        "🟢",
        "Adecuada",
        "La cuota se cubre con una holgura favorable."
    )


def semaforo_margen(valor):

    if valor < 0.20:
        return (
            "🔴",
            "Bajo",
            "Existe poca capacidad para absorber gastos adicionales."
        )

    if valor < 0.30:
        return (
            "🟠",
            "Moderado",
            "El margen es aceptable pero debe vigilarse."
        )

    return (
        "🟢",
        "Bueno",
        "El negocio conserva un margen favorable sobre ventas."
    )


def semaforo_liquidez(valor):

    if valor < 1:
        return (
            "🔴",
            "Atención",
            "Los activos corrientes no cubren las obligaciones corrientes."
        )

    if valor < 1.20:
        return (
            "🟠",
            "Ajustada",
            "Existe cobertura, pero con poco margen."
        )

    return (
        "🟢",
        "Adecuada",
        "Existe una cobertura favorable de las obligaciones corrientes."
    )


def semaforo_utilidad(valor):

    if valor < 0:
        return (
            "🔴",
            "Negativa",
            "El negocio no genera excedente después de sus costos y gastos."
        )

    return (
        "🟢",
        "Positiva",
        "El negocio genera excedente después de sus costos y gastos."
    )


# ============================================================
# CONCLUSIÓN
# ============================================================

def generar_conclusion(row):

    if row["viabilidad"] == "VIABLE":

        return (
            "El negocio presenta indicadores financieros favorables. "
            "Se recomienda continuar con el estudio de crédito, "
            "validando soportes y comportamiento histórico de pago."
        )

    if row["viabilidad"] == "VIABLE CON CONDICIONES":

        return (
            "El negocio presenta un perfil aceptable, aunque existen "
            "indicadores que requieren atención. Se recomienda validar "
            "información adicional y ajustar monto o plazo."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente "
        "y/o un nivel de riesgo elevado. No se recomienda aprobar "
        "en primera instancia sin realizar validaciones adicionales."
    )


# ============================================================
# DIAGNÓSTICO CLIENTE
# ============================================================

def generar_diagnostico_cliente(row):

    e_icon, e_label, e_text = semaforo_endeudamiento(
        row["endeudamiento"]
    )

    c_icon, c_label, c_text = semaforo_cobertura(
        row["cobertura"]
    )

    m_icon, m_label, m_text = semaforo_margen(
        row["margenBruto"]
    )

    l_icon, l_label, l_text = semaforo_liquidez(
        row["liquidez"]
    )

    u_icon, u_label, u_text = semaforo_utilidad(
        row["utilidadNeta"]
    )

    html = f"""
    <div class="diag-box">

        <div class="diag-title">
            Diagnóstico financiero — {safe_text(nombre_cliente(row))}
        </div>

        <div class="diag-row">
            <span class="diag-icon">{e_icon}</span>
            <span class="diag-text">
                <strong>Endeudamiento:</strong>
                {percent(row["endeudamiento"])}
                → {e_label}.
                {e_text}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{c_icon}</span>
            <span class="diag-text">
                <strong>Cobertura:</strong>
                {row["cobertura"]:.2f}x
                → {c_label}.
                {c_text}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{m_icon}</span>
            <span class="diag-text">
                <strong>Margen bruto:</strong>
                {percent(row["margenBruto"])}
                → {m_label}.
                {m_text}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{l_icon}</span>
            <span class="diag-text">
                <strong>Liquidez:</strong>
                {row["liquidez"]:.2f}x
                → {l_label}.
                {l_text}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{u_icon}</span>
            <span class="diag-text">
                <strong>Utilidad neta:</strong>
                {money(row["utilidadNeta"])}
                → {u_label}.
                {u_text}
            </span>
        </div>

        <div class="conclusion-box">

            <div class="conclusion-title">
                Conclusión:
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

    return html


# ============================================================
# PROCESAMIENTO
# ============================================================

@st.cache_data(show_spinner=False)
def procesar_dataframe(df):

    df = df.copy()

    indicadores = df.apply(
        calcular_indicadores,
        axis=1
    )

    df = pd.concat(
        [df, indicadores],
        axis=1
    )

    df["riesgo"] = df.apply(
        clasificar_riesgo,
        axis=1
    )

    df["viabilidad"] = df.apply(
        lambda fila: evaluar_viabilidad(
            fila["riesgo"],
            fila
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
            margin-bottom:12px;
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

            <div style="
                font-weight:800;
                font-size:18px;
                color:#25344A;
            ">
                FinanData AI
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Dashboard comercial · Análisis financiero de negocios"
    )

    st.divider()

    # ========================================================
    # INFORMACIÓN REQUERIDA
    # ========================================================

    with st.expander(
        "📋 Información requerida para el Excel",
        expanded=False
    ):

        st.markdown(
            """
            ### Estructura del archivo

            El Excel debe contener **una sola hoja** y una fila por
            negocio o cliente.

            **Columnas requeridas:**

            `ID_Cliente`  
            `Cliente`  
            `Ciudad`  
            `Actividad_Economica`  
            `Ventas_Mensuales`  
            `Costo_Ventas`  
            `Gastos_Operativos`  
            `Gastos_Financieros`  
            `Activos_Corrientes`  
            `Pasivos_Corrientes`  
            `Activos_Totales`  
            `Pasivos_Totales`  
            `Patrimonio`  
            `Cuota_Mensual_Credito`  
            `Antiguedad_Negocio_Anios`  
            `Historial_Pagos`  
            `Dias_Mora_Max`  
            `Tiene_Centrales`

            **Importante:** los nombres de las columnas deben coincidir
            con esta estructura para obtener un análisis completo.

            Los valores financieros deben corresponder al mismo período
            de análisis.
            """
        )

    # ========================================================
    # CARGAR EXCEL
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

                faltantes = validar_excel(
                    df_raw
                )

                if faltantes:

                    st.error(
                        "El archivo tiene columnas faltantes."
                    )

                    st.markdown(
                        "**Columnas que faltan:**"
                    )

                    for columna in faltantes:

                        st.write(
                            f"• `{columna}`"
                        )

                    st.info(
                        "Revisa los nombres de las columnas "
                        "del Excel antes de cargarlo nuevamente."
                    )

                    st.session_state.clientes_df = None

                else:

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
                        f"{len(df_raw)} negocios encontrados."
                    )

        except Exception as error:

            st.error(
                f"No fue posible leer el archivo: {error}"
            )

    st.divider()

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

            • Menor o igual a 50% → adecuado  
            • Entre 50% y 70% → moderado  
            • Mayor a 70% → alto  

            **Cobertura / DSCR**

            Flujo disponible / Cuota mensual.

            • Menor a 1.00x → no cubre la cuota  
            • 1.00x a 1.29x → cobertura ajustada  
            • 1.30x o superior → mayor holgura  

            **Margen bruto**

            (Ventas − Costo de ventas) / Ventas.

            Permite conocer cuánto queda de las ventas después
            de cubrir directamente el costo de ventas.

            **Liquidez**

            Activos corrientes / Pasivos corrientes.

            • Menor a 1.00x → atención  
            • 1.00x a 1.19x → ajustada  
            • 1.20x o superior → adecuada  

            **Utilidad neta**

            Utilidad bruta − gastos operativos − gastos financieros.

            Una utilidad positiva indica que el negocio genera
            excedente después de sus principales costos y gastos.

            **Importante:** estos indicadores constituyen un análisis
            financiero preliminar y deben complementarse con las
            políticas y criterios de crédito correspondientes.
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

    st.title(
        "Dashboard comercial"
    )

    st.caption(
        "Visualización y análisis financiero de negocios"
    )


# ============================================================
# SELECTOR
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
        label_visibility="collapsed"
    )


# ============================================================
# SIN ARCHIVO
# ============================================================

if df is None:

    st.info(
        "Carga un archivo Excel desde la barra lateral "
        "para comenzar el análisis."
    )

    st.stop()


# ============================================================
# FILTRO
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

k1, k2, k3, k4, k5, k6 = st.columns(
    6
)


kpi_data = [
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


for columna, clase, etiqueta, valor in kpi_data:

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

st.subheader(
    "💡 Diagnóstico y recomendación financiera"
)


if cliente_idx is not None:

    fila = df.loc[
        cliente_idx
    ]

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

    if total > 0 and alto / total >= 0.40:

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

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# DISTRIBUCIÓN DEL RIESGO
# ============================================================

st.subheader(
    "Distribución del riesgo"
)


r1, r2, r3 = st.columns(3)


bajo_total = (
    df["riesgo"] == "BAJO"
).sum()

medio_total = (
    df["riesgo"] == "MEDIO"
).sum()

alto_total = (
    df["riesgo"] == "ALTO"
).sum()


with r1:

    st.markdown(
        f"""
        <div class="risk-card risk-low">

            <div class="risk-title">
                RIESGO BAJO
            </div>

            <div class="risk-number">
                {bajo_total}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with r2:

    st.markdown(
        f"""
        <div class="risk-card risk-med">

            <div class="risk-title">
                RIESGO MEDIO
            </div>

            <div class="risk-number">
                {medio_total}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with r3:

    st.markdown(
        f"""
        <div class="risk-card risk-high">

            <div class="risk-title">
                RIESGO ALTO
            </div>

            <div class="risk-number">
                {alto_total}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# GRÁFICA 1
# DISTRIBUCIÓN DEL RIESGO
# ============================================================

g1, g2 = st.columns(2)


with g1:

    st.markdown(
        "**Distribución del riesgo**"
    )

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
                marker=dict(
                    colors=[
                        GREEN,
                        ORANGE,
                        RED
                    ]
                ),
                hole=0.55,
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
        height=340,
        margin=dict(
            t=20,
            b=20,
            l=10,
            r=10
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            y=-0.05
        )
    )

    st.plotly_chart(
        fig_riesgo,
        use_container_width=True
    )


# ============================================================
# GRÁFICA 2
# LIQUIDEZ VS ENDEUDAMIENTO
# ============================================================

with g2:

    st.markdown(
        "**Liquidez vs. Endeudamiento**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Relación entre la capacidad de cubrir obligaciones
            de corto plazo y el nivel de deuda del negocio.
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
            "BAJO": GREEN,
            "MEDIO": ORANGE,
            "ALTO": RED
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
        line_color=BLUE,
        annotation_text="50%"
    )

    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color=RED,
        annotation_text="70%"
    )

    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color=BLUE,
        annotation_text="Liquidez 1.0x"
    )

    fig_liquidez.add_hline(
        y=1.20,
        line_dash="dot",
        line_color=GREEN,
        annotation_text="Liquidez 1.20x"
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
        height=340,
        margin=dict(
            t=30,
            b=20,
            l=10,
            r=10
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig_liquidez,
        use_container_width=True
    )


# ============================================================
# GRÁFICA 3
# DSCR
# ============================================================

g3, g4 = st.columns(2)


with g3:

    st.markdown(
        "**DSCR / Cobertura de deuda**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Capacidad del flujo disponible para cubrir la cuota
            mensual del crédito.
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
            "BAJO": GREEN,
            "MEDIO": ORANGE,
            "ALTO": RED
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
        line_color=RED,
        annotation_text="Mínimo 1.00x"
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color=GREEN,
        annotation_text="Objetivo 1.30x"
    )

    fig_dscr.update_layout(
        height=340,
        margin=dict(
            t=30,
            b=60,
            l=10,
            r=10
        ),
        xaxis=dict(
            tickangle=-35
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig_dscr,
        use_container_width=True
    )


# ============================================================
# GRÁFICA 4
# RANKING DSCR
# ============================================================

with g4:

    st.markdown(
        "**DSCR / Cobertura por cliente**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Comparación individual de la capacidad de cobertura
            de deuda de los negocios analizados.
        </div>
        """,
        unsafe_allow_html=True
    )

    ranking = datos.copy()

    ranking["Cliente_Display"] = (
        ranking.apply(
            nombre_cliente,
            axis=1
        )
    )

    ranking = ranking.sort_values(
        "cobertura",
        ascending=True
    )

    fig_ranking = px.bar(
        ranking,
        x="cobertura",
        y="Cliente_Display",
        orientation="h",
        color="riesgo",
        color_discrete_map={
            "BAJO": GREEN,
            "MEDIO": ORANGE,
            "ALTO": RED
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

    fig_ranking.add_vline(
        x=1,
        line_dash="dash",
        line_color=RED,
        annotation_text="1.00x"
    )

    fig_ranking.add_vline(
        x=1.30,
        line_dash="dot",
        line_color=GREEN,
        annotation_text="1.30x"
    )

    fig_ranking.update_layout(
        height=340,
        margin=dict(
            t=30,
            b=20,
            l=10,
            r=10
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig_ranking,
        use_container_width=True
    )


# ============================================================
# DETALLE DEL CLIENTE
# ============================================================

st.subheader(
    "👤 Detalle del cliente"
)


if cliente_idx is None:

    st.caption(
        "Selecciona un cliente en el menú superior "
        "para visualizar su información detallada."
    )

else:

    fila = df.loc[
        cliente_idx
    ]

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
            "ANTIGÜEDAD",
            f"{to_number(fila['Antiguedad_Negocio_Anios']):.1f} años"
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

    for inicio in range(
        0,
        len(campos),
        4
    ):

        cols = st.columns(4)

        bloque = campos[
            inicio:inicio + 4
        ]

        for col, (label, value) in zip(
            cols,
            bloque
        ):

            with col:

                st.markdown(
                    f"""
                    <div class="detail-card">

                        <div class="detail-label">
                            {safe_text(label)}
                        </div>

                        <div class="detail-value">
                            {safe_text(value)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# TABLA DE SEÑALES
# ============================================================

st.subheader(
    "⚠️ Señales y recomendación comercial"
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
        "liquidez",
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

tabla_mostrar["liquidez"] = (
    tabla_mostrar["liquidez"]
    .apply(
        lambda x: f"{x:.2f}x"
    )
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
    "Liquidez",
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
            perfiles viables en primera instancia.

            Estos resultados constituyen una herramienta de apoyo
            para el análisis comercial y no reemplazan la decisión
            crediticia definitiva.

        </p>

    </div>
    """,
    unsafe_allow_html=True
)
