"""
FinanData AI - Dashboard comercial
===================================

Dashboard Streamlit para análisis financiero automatizado
de negocios y apoyo al estudio de crédito.

El Excel debe contener únicamente las variables base
del negocio hasta la columna Tiene_Centrales.

Los indicadores financieros, riesgo, viabilidad y
recomendación son calculados automáticamente.

Ejecución:

    streamlit run app.py
"""

# ======================================================================
# IMPORTS
# ======================================================================

import re
import unicodedata
from html import escape

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ======================================================================
# CONFIGURACIÓN
# ======================================================================

st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


PRIMARY = "#0757C9"


# ======================================================================
# ESTILOS
# ======================================================================

st.markdown(
    f"""
    <style>

    /* ==============================================================
       GENERAL
       ============================================================== */

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    h1 {{
        color: #2D3142;
    }}

    h2, h3 {{
        color: #26364D;
    }}


    /* ==============================================================
       LOGO
       ============================================================== */

    .logo-container {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }}

    .logo-box {{
        width: 32px;
        height: 32px;
        background: {PRIMARY};
        color: white;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }}

    .logo-text {{
        font-weight: 700;
        font-size: 18px;
        color: #26364D;
    }}


    /* ==============================================================
       KPI
       ============================================================== */

    .kpi-card {{
        border-radius: 10px;
        padding: 13px 14px;
        color: white;
        box-shadow: 0 2px 7px rgba(0, 0, 0, .08);
        min-height: 92px;
        height: 92px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
        overflow: hidden;
    }}

    .kpi-label {{
        font-size: clamp(10px, 0.80vw, 12px);
        font-weight: 600;
        opacity: .92;
        margin-bottom: 7px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1;
    }}

    .kpi-value {{
        font-size: clamp(15px, 1.35vw, 21px);
        font-weight: 800;
        line-height: 1.05;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        letter-spacing: -0.3px;
    }}

    .kpi-sales-value {{
        font-size: clamp(13px, 1.12vw, 19px);
        font-weight: 800;
        line-height: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        letter-spacing: -0.45px;
        width: 100%;
        display: block;
    }}

    .k1 {{
        background: #7050F6;
    }}

    .k2 {{
        background: #0878E8;
    }}

    .k3 {{
        background: #0CA5BA;
    }}

    .k4 {{
        background: #05C47A;
    }}

    .k5 {{
        background: #8B4DF1;
    }}

    .k6 {{
        background: #0756C9;
    }}


    /* ==============================================================
       DIAGNÓSTICO
       ============================================================== */

    .diag-box {{
        background: #FFFFFF;
        border-left: 5px solid #1264D6;
        border-radius: 9px;
        padding: 16px 18px;
        box-shadow: 0 2px 7px rgba(0, 0, 0, .06);
        color: #25344A;
        font-family: Arial, sans-serif;
    }}

    .diag-title {{
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 14px;
        color: #26364D;
    }}

    .diag-row {{
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 13px;
        line-height: 1.45;
        margin: 8px 0;
        color: #344054;
    }}

    .diag-icon {{
        width: 18px;
        min-width: 18px;
        font-size: 13px;
        line-height: 18px;
    }}

    .diag-text {{
        flex: 1;
    }}

    .diag-text strong {{
        color: #26364D;
    }}

    .conclusion-box {{
        background: #F4F6F9;
        border-radius: 8px;
        padding: 14px 15px;
        margin-top: 14px;
        color: #344054;
        font-size: 13px;
        line-height: 1.5;
    }}

    .conclusion-title {{
        font-weight: 700;
        color: #344054;
        margin-bottom: 5px;
    }}

    .recommendation {{
        margin-top: 14px;
    }}

    .recommendation strong {{
        color: #344054;
    }}


    /* ==============================================================
       ASISTENTE IA
       ============================================================== */

    .assistant-box {{
        background: linear-gradient(
            135deg,
            #EEF5FF,
            #F8FBFF
        );
        border: 1px solid #DCEAFE;
        border-radius: 9px;
        padding: 18px;
        color: #344054;
        font-family: Arial, sans-serif;
    }}

    .assistant-title {{
        font-size: 16px;
        font-weight: 700;
        color: #25344A;
        margin-bottom: 8px;
    }}

    .assistant-text {{
        font-size: 13px;
        line-height: 1.55;
        margin: 0;
    }}


    /* ==============================================================
       RIESGO
       ============================================================== */

    .risk-low {{
        border-left: 4px solid #10B981;
        padding: 10px 14px;
        border-radius: 8px;
        background: #FFFFFF;
    }}

    .risk-med {{
        border-left: 4px solid #F59E0B;
        padding: 10px 14px;
        border-radius: 8px;
        background: #FFFFFF;
    }}

    .risk-high {{
        border-left: 4px solid #EF4444;
        padding: 10px 14px;
        border-radius: 8px;
        background: #FFFFFF;
    }}


    /* ==============================================================
       GRÁFICAS
       ============================================================== */

    .chart-description {{
        color: #667085;
        font-size: 12px;
        margin-top: -5px;
        margin-bottom: 8px;
    }}


    /* ==============================================================
       DETALLE
       ============================================================== */

    .detail-card {{
        background: #FFFFFF;
        border: 1px solid #EAECF0;
        border-radius: 8px;
        padding: 12px 14px;
        min-height: 65px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, .04);
    }}

    .detail-label {{
        color: #778399;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 5px;
    }}

    .detail-value {{
        color: #26364D;
        font-size: 15px;
        font-weight: 700;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# CONSTANTES DEL ARCHIVO
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
# FUNCIONES DE UTILIDAD
# ======================================================================

def normalizar_texto(valor):
    """
    Convierte texto a minúsculas y elimina acentos.
    Facilita comparaciones como Sí/Si/si.
    """

    if valor is None:
        return ""

    texto = str(valor).strip().lower()

    texto = unicodedata.normalize(
        "NFKD",
        texto,
    )

    texto = "".join(
        c
        for c in texto
        if not unicodedata.combining(c)
    )

    return texto


def safe_text(value):
    """
    Evita que valores provenientes del Excel
    rompan el HTML.
    """

    return escape(
        str(value)
    )


def to_number(value):
    """
    Convierte valores numéricos de forma robusta.

    Ejemplos soportados:

        10.978.454
        10.978.454,50
        10978454.50
        $10.978.454
        10,978.45
    """

    if value is None:
        return 0.0

    try:

        if pd.isna(value):
            return 0.0

    except (TypeError, ValueError):

        pass

    if isinstance(
        value,
        (int, float)
    ):

        return float(value)

    texto = str(
        value
    ).strip()

    if not texto:
        return 0.0

    texto = (
        texto
        .replace("$", "")
        .replace(" ", "")
        .replace("COP", "")
        .replace("cop", "")
    )

    # --------------------------------------------------------------
    # Si existen punto y coma:
    #
    # 10.978.454,50
    # --------------------------------------------------------------

    if "," in texto and "." in texto:

        ultimo_punto = texto.rfind(".")
        ultima_coma = texto.rfind(",")

        # La coma es decimal
        if ultima_coma > ultimo_punto:

            texto = texto.replace(
                ".",
                ""
            )

            texto = texto.replace(
                ",",
                "."
            )

        # El punto es decimal
        else:

            texto = texto.replace(
                ",",
                ""
            )

    # --------------------------------------------------------------
    # Solo comas
    # --------------------------------------------------------------

    elif "," in texto:

        partes = texto.split(",")

        # Ejemplo:
        # 10,978,454
        if (
            len(partes) > 2
            and all(
                len(p) == 3
                for p in partes[1:]
            )
        ):

            texto = "".join(
                partes
            )

        else:

            texto = texto.replace(
                ",",
                "."
            )

    # --------------------------------------------------------------
    # Solo puntos
    # --------------------------------------------------------------

    elif "." in texto:

        partes = texto.split(".")

        # Ejemplo:
        # 10.978.454
        if (
            len(partes) > 2
            and all(
                len(p) == 3
                for p in partes[1:]
            )
        ):

            texto = "".join(
                partes
            )

    try:

        return float(
            texto
        )

    except (
        ValueError,
        TypeError,
    ):

        return 0.0


def money(value):
    """
    Formato monetario colombiano.
    """

    try:

        return (
            f"${value:,.0f}"
            .replace(",", ".")
        )

    except (
        ValueError,
        TypeError,
    ):

        return "$0"


def percent(value):
    """
    Convierte decimal a porcentaje.
    """

    try:

        return f"{value * 100:.1f}%"

    except (
        ValueError,
        TypeError,
    ):

        return "0.0%"


def get_field(
    row,
    names,
    default=0,
):
    """
    Busca el primer campo disponible
    dentro de una fila.
    """

    for name in names:

        if name not in row.index:
            continue

        value = row[name]

        if value is None:
            continue

        try:

            if pd.isna(value):
                continue

        except (
            TypeError,
            ValueError,
        ):

            pass

        if (
            isinstance(value, str)
            and not value.strip()
        ):
            continue

        return value

    return default


def nombre_cliente(row):
    """
    Obtiene el nombre del cliente.
    """

    campos = [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
    ]

    for campo in campos:

        if campo not in row.index:
            continue

        valor = row[campo]

        if pd.isna(valor):
            continue

        valor = str(
            valor
        ).strip()

        if valor:
            return valor

    return "Cliente"


# ======================================================================
# KPI
# ======================================================================

def ventas_kpi_html(valor):

    return (
        "<div class='kpi-sales-value'>"
        f"{safe_text(money(valor))}"
        "</div>"
    )


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

    patrimonio = to_number(
        get_field(
            row,
            [
                "Patrimonio",
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

    # --------------------------------------------------------------
    # UTILIDAD BRUTA
    # --------------------------------------------------------------

    utilidad_bruta = (
        ventas
        - costo
    )

    # --------------------------------------------------------------
    # MARGEN BRUTO
    # --------------------------------------------------------------

    margen_bruto = (
        utilidad_bruta / ventas
        if ventas > 0
        else 0.0
    )

    # --------------------------------------------------------------
    # UTILIDAD NETA
    #
    # CORRECCIÓN:
    # Los gastos financieros se descuentan UNA sola vez.
    # --------------------------------------------------------------

    utilidad_neta = (
        utilidad_bruta
        - gastos
        - financieros
    )

    # --------------------------------------------------------------
    # MARGEN NETO
    # --------------------------------------------------------------

    margen_neto = (
        utilidad_neta / ventas
        if ventas > 0
        else 0.0
    )

    # --------------------------------------------------------------
    # CAPITAL DE TRABAJO
    # --------------------------------------------------------------

    capital_trabajo = (
        activos_corrientes
        - pasivos_corrientes
    )

    # --------------------------------------------------------------
    # ENDEUDAMIENTO
    # --------------------------------------------------------------

    endeudamiento = (
        pasivos_totales / activos_totales
        if activos_totales > 0
        else 0.0
    )

    # --------------------------------------------------------------
    # LIQUIDEZ
    # --------------------------------------------------------------

    liquidez = (
        activos_corrientes / pasivos_corrientes
        if pasivos_corrientes > 0
        else 0.0
    )

    # --------------------------------------------------------------
    # FLUJO DISPONIBLE
    #
    # Se utiliza flujo operativo antes de gastos financieros.
    # --------------------------------------------------------------

    flujo = (
        utilidad_bruta
        - gastos
    )

    # --------------------------------------------------------------
    # COBERTURA / DSCR
    # --------------------------------------------------------------

    cobertura = (
        flujo / cuota
        if cuota > 0
        else 0.0
    )

    # --------------------------------------------------------------
    # APALANCAMIENTO
    # --------------------------------------------------------------

    apalancamiento = (
        pasivos_totales / patrimonio
        if patrimonio > 0
        else 0.0
    )

    return pd.Series(
        {
            "ventas": ventas,
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
            ],
            0,
        )
    )

    historial = normalizar_texto(
        get_field(
            row,
            [
                "Historial_Pagos",
                "Historial de pagos",
            ],
            "",
        )
    )

    centrales = normalizar_texto(
        get_field(
            row,
            [
                "Tiene_Centrales",
            ],
            "",
        )
    )

    # --------------------------------------------------------------
    # ENDEUDAMIENTO
    # --------------------------------------------------------------

    if row["endeudamiento"] > 0.70:

        puntos += 3

    elif row["endeudamiento"] > 0.50:

        puntos += 1

    # --------------------------------------------------------------
    # COBERTURA
    # --------------------------------------------------------------

    if row["cobertura"] < 1:

        puntos += 3

    elif row["cobertura"] < 1.30:

        puntos += 1

    # --------------------------------------------------------------
    # MARGEN BRUTO
    # --------------------------------------------------------------

    if row["margenBruto"] < 0.20:

        puntos += 2

    elif row["margenBruto"] < 0.30:

        puntos += 1

    # --------------------------------------------------------------
    # UTILIDAD NETA
    # --------------------------------------------------------------

    if row["utilidadNeta"] < 0:

        puntos += 2

    # --------------------------------------------------------------
    # MORA
    # --------------------------------------------------------------

    if mora > 30:

        puntos += 3

    elif mora > 15:

        puntos += 1

    # --------------------------------------------------------------
    # HISTORIAL
    # --------------------------------------------------------------

    if (
        "malo" in historial
        or "incum" in historial
    ):

        puntos += 3

    elif "regular" in historial:

        puntos += 1

    # --------------------------------------------------------------
    # CENTRALES DE RIESGO
    #
    # Solo se considera negativo cuando el campo
    # realmente indica una situación desfavorable.
    # --------------------------------------------------------------

    centrales_negativas = (
        "malo",
        "negativo",
        "reportado",
        "castigado",
        "incumplimiento",
    )

    if any(
        palabra in centrales
        for palabra in centrales_negativas
    ):

        puntos += 2

    return (
        "ALTO"
        if puntos >= 7
        else (
            "MEDIO"
            if puntos >= 3
            else "BAJO"
        )
    )


# ======================================================================
# VIABILIDAD
# ======================================================================

def evaluar_viabilidad(
    riesgo,
    row,
):

    if (
        riesgo == "BAJO"
        and row["cobertura"] >= 1.30
        and row["endeudamiento"] <= 0.50
        and row["utilidadNeta"] >= 0
    ):

        return "VIABLE"

    if (
        riesgo == "MEDIO"
        and row["cobertura"] >= 1.00
        and row["utilidadNeta"] >= 0
    ):

        return "VIABLE CON CONDICIONES"

    return "NO VIABLE"


# ======================================================================
# RECOMENDACIÓN
# ======================================================================

def generar_recomendacion(
    viabilidad,
):

    if viabilidad == "VIABLE":

        return (
            "Continuar estudio y validar soportes, "
            "flujo de caja y capacidad de pago."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "Solicitar soportes adicionales y evaluar "
            "monto/plazo según capacidad de pago."
        )

    return (
        "No recomendar aprobación en primera instancia. "
        "Revisar endeudamiento, capacidad de pago, "
        "rentabilidad e historial."
    )


# ======================================================================
# SEMÁFOROS
# ======================================================================

def semaforo_endeudamiento(value):

    if value > 0.70:

        return (
            "🔴",
            "Alto",
            "Una proporción elevada de los activos "
            "está financiada con deuda.",
        )

    if value > 0.50:

        return (
            "🟠",
            "Moderado",
            "El nivel de deuda es considerable "
            "y debe vigilarse.",
        )

    return (
        "🟢",
        "Adecuado",
        "La proporción de deuda sobre los activos "
        "es manejable.",
    )


def semaforo_cobertura(value):

    if value < 1:

        return (
            "🔴",
            "Riesgo",
            "El flujo disponible no alcanza para "
            "cubrir completamente la cuota.",
        )

    if value < 1.30:

        return (
            "🟠",
            "Ajustada",
            "El flujo cubre la cuota, pero con "
            "poco margen de holgura.",
        )

    return (
        "🟢",
        "Adecuada",
        "El flujo disponible cubre la cuota "
        "con holgura suficiente.",
    )


def semaforo_margen(value):

    if value < 0.20:

        return (
            "🔴",
            "Bajo",
            "El negocio tiene poca capacidad "
            "para absorber gastos adicionales.",
        )

    if value < 0.30:

        return (
            "🟠",
            "Moderado",
            "El margen es aceptable, aunque "
            "con espacio limitado de maniobra.",
        )

    return (
        "🟢",
        "Bueno",
        "El negocio conserva un margen "
        "saludable sobre sus ventas.",
    )


def semaforo_liquidez(value):

    if value < 1:

        return (
            "🔴",
            "Atención",
            "Los activos corrientes no alcanzan "
            "para cubrir totalmente las obligaciones.",
        )

    if value < 1.20:

        return (
            "🟠",
            "Ajustada",
            "La liquidez cubre lo corriente "
            "pero con poco colchón.",
        )

    return (
        "🟢",
        "Adecuada",
        "Los activos corrientes cubren "
        "cómodamente las obligaciones.",
    )


def semaforo_utilidad(value):

    if value < 0:

        return (
            "🔴",
            "Negativa",
            "El negocio no genera excedente "
            "después de costos y gastos.",
        )

    return (
        "🟢",
        "Positiva",
        "El negocio genera excedente "
        "después de costos y gastos.",
    )


# ======================================================================
# CONCLUSIÓN
# ======================================================================

def generar_conclusion(row):

    viabilidad = row["viabilidad"]

    if viabilidad == "VIABLE":

        return (
            "El negocio presenta indicadores financieros sólidos "
            "y consistentes. Se recomienda continuar con el estudio "
            "de crédito, validando soportes documentales y "
            "comportamiento de pago histórico."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "El negocio presenta un perfil aceptable pero con "
            "puntos de atención. Se recomienda solicitar "
            "información adicional y ajustar monto o plazo "
            "según la capacidad de pago real."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente "
        "y/o un nivel de riesgo elevado. No se recomienda "
        "aprobar en primera instancia. Se recomienda solicitar "
        "información adicional y revisar la estructura "
        "de obligaciones."
    )


# ======================================================================
# DIAGNÓSTICO DEL CLIENTE
# ======================================================================

def generar_diagnostico_cliente(row):

    endeudamiento = semaforo_endeudamiento(
        row["endeudamiento"]
    )

    cobertura = semaforo_cobertura(
        row["cobertura"]
    )

    margen = semaforo_margen(
        row["margenBruto"]
    )

    liquidez = semaforo_liquidez(
        row["liquidez"]
    )

    utilidad = semaforo_utilidad(
        row["utilidadNeta"]
    )

    e_i, e_l, e_t = endeudamiento
    c_i, c_l, c_t = cobertura
    m_i, m_l, m_t = margen
    l_i, l_l, l_t = liquidez
    u_i, u_l, u_t = utilidad

    html = f"""
    <div class="diag-box">

        <div class="diag-title">
            Diagnóstico financiero —
            {safe_text(nombre_cliente(row))}
        </div>

        <div class="diag-row">
            <span class="diag-icon">{e_i}</span>

            <span class="diag-text">
                <strong>Endeudamiento:</strong>
                {percent(row["endeudamiento"])}
                → {safe_text(e_l)}.
                {safe_text(e_t)}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{c_i}</span>

            <span class="diag-text">
                <strong>Cobertura:</strong>
                {row["cobertura"]:.2f}x
                → {safe_text(c_l)}.
                {safe_text(c_t)}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{m_i}</span>

            <span class="diag-text">
                <strong>Margen bruto:</strong>
                {percent(row["margenBruto"])}
                → {safe_text(m_l)}.
                {safe_text(m_t)}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{l_i}</span>

            <span class="diag-text">
                <strong>Liquidez:</strong>
                {row["liquidez"]:.2f}x
                → {safe_text(l_l)}.
                {safe_text(l_t)}
            </span>
        </div>

        <div class="diag-row">
            <span class="diag-icon">{u_i}</span>

            <span class="diag-text">
                <strong>Utilidad neta:</strong>
                {money(row["utilidadNeta"])}
                → {safe_text(u_l)}.
                {safe_text(u_t)}
            </span>
        </div>

        <div class="conclusion-box">

            <div class="conclusion-title">
                Conclusión
            </div>

            <div>
                {safe_text(generar_conclusion(row))}
            </div>

            <div class="recommendation">

                <strong>
                    Recomendación comercial:
                </strong>

                {safe_text(row["recomendacion"])}

            </div>

        </div>

    </div>
    """

    return html


# ======================================================================
# PROCESAMIENTO DEL DATAFRAME
# ======================================================================

@st.cache_data(show_spinner=False)
def procesar_dataframe(
    dataframe,
):

    df = dataframe.copy()

    # --------------------------------------------------------------
    # Elimina columnas completamente vacías
    # --------------------------------------------------------------

    df = df.dropna(
        axis=1,
        how="all",
    )

    # --------------------------------------------------------------
    # Limpia espacios en nombres de columnas
    # --------------------------------------------------------------

    df.columns = [
        str(col).strip()
        for col in df.columns
    ]

    # --------------------------------------------------------------
    # Cálculo de indicadores
    # --------------------------------------------------------------

    indicadores = df.apply(
        calcular_indicadores,
        axis=1,
    )

    df = pd.concat(
        [
            df.reset_index(drop=True),
            indicadores.reset_index(drop=True),
        ],
        axis=1,
    )

    # --------------------------------------------------------------
    # Riesgo
    # --------------------------------------------------------------

    df["riesgo"] = df.apply(
        clasificar_riesgo,
        axis=1,
    )

    # --------------------------------------------------------------
    # Viabilidad
    # --------------------------------------------------------------

    df["viabilidad"] = df.apply(
        lambda fila: evaluar_viabilidad(
            fila["riesgo"],
            fila,
        ),
        axis=1,
    )

    # --------------------------------------------------------------
    # Recomendación
    # --------------------------------------------------------------

    df["recomendacion"] = (
        df["viabilidad"]
        .apply(
            generar_recomendacion
        )
    )

    return df


# ======================================================================
# VALIDACIÓN DEL ARCHIVO
# ======================================================================

def validar_dataframe(
    dataframe,
):

    if dataframe is None:

        return (
            False,
            "No se recibió información.",
            [],
        )

    if dataframe.empty:

        return (
            False,
            "El archivo no contiene registros.",
            [],
        )

    dataframe = dataframe.copy()

    dataframe.columns = [
        str(col).strip()
        for col in dataframe.columns
    ]

    faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in dataframe.columns
    ]

    if faltantes:

        return (
            False,
            "El archivo no contiene todas las columnas requeridas.",
            faltantes,
        )

    return (
        True,
        "Archivo válido.",
        [],
    )


# ======================================================================
# SIDEBAR
# ======================================================================

with st.sidebar:

    # --------------------------------------------------------------
    # LOGO
    # --------------------------------------------------------------

    st.markdown(
        f"""
        <div class="logo-container">

            <div class="logo-box">
                F
            </div>

            <div class="logo-text">
                FinanData AI
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Dashboard comercial · "
        "Análisis financiero de negocios"
    )

    st.divider()

    # --------------------------------------------------------------
    # CARGA DE ARCHIVO
    # --------------------------------------------------------------

    archivo = st.file_uploader(
        "📁 Cargar Excel",
        type=[
            "xlsx",
            "xls",
            "csv",
        ],
    )

    # --------------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------------

    if "clientes_df" not in st.session_state:

        st.session_state.clientes_df = None

    # --------------------------------------------------------------
    # PROCESAR ARCHIVO
    # --------------------------------------------------------------

    if archivo is not None:

        try:

            nombre_archivo = (
                archivo.name.lower()
            )

            if nombre_archivo.endswith(
                ".csv"
            ):

                df_raw = pd.read_csv(
                    archivo
                )

            else:

                df_raw = pd.read_excel(
                    archivo
                )

            # --------------------------------------------------
            # Validar
            # --------------------------------------------------

            valido, mensaje, faltantes = (
                validar_dataframe(
                    df_raw
                )
            )

            if not valido:

                st.error(
                    mensaje
                )

                if faltantes:

                    st.warning(
                        "Columnas faltantes: "
                        + ", ".join(
                            faltantes
                        )
                    )

            else:

                # --------------------------------------------------
                # Seleccionar SOLO columnas base
                # --------------------------------------------------

                df_base = (
                    df_raw[
                        COLUMNAS_REQUERIDAS
                    ]
                    .copy()
                )

                # --------------------------------------------------
                # Eliminar filas totalmente vacías
                # --------------------------------------------------

                df_base = (
                    df_base
                    .dropna(
                        how="all"
                    )
                    .reset_index(
                        drop=True
                    )
                )

                if df_base.empty:

                    st.error(
                        "El archivo no contiene registros válidos."
                    )

                else:

                    # --------------------------------------------------
                    # Procesamiento
                    # --------------------------------------------------

                    st.session_state.clientes_df = (
                        procesar_dataframe(
                            df_base
                        )
                    )

                    st.success(
                        f"Archivo cargado correctamente: "
                        f"{archivo.name}"
                    )

                    # --------------------------------------------------
                    # Duplicados
                    # --------------------------------------------------

                    if (
                        "ID_Cliente"
                        in df_base.columns
                    ):

                        duplicados = (
                            df_base[
                                "ID_Cliente"
                            ]
                            .duplicated()
                            .sum()
                        )

                        if duplicados > 0:

                            st.warning(
                                f"Se encontraron "
                                f"{duplicados} registros "
                                f"con ID_Cliente duplicado."
                            )

        except Exception as error:

            st.error(
                "No fue posible procesar el archivo."
            )

            st.exception(
                error
            )

    st.divider()

    # --------------------------------------------------------------
    # INTERPRETACIÓN
    # --------------------------------------------------------------

    with st.expander(
        "ℹ️ ¿Cómo interpretar los indicadores?"
    ):

        st.markdown(
            """
            **Endeudamiento**

            Pasivos totales / Activos totales.

            - Menor o igual a 50% → adecuado.
            - Entre 50% y 70% → moderado.
            - Mayor a 70% → alto.

            **Cobertura / DSCR**

            Flujo disponible / Cuota del crédito.

            - Menor a 1.00x → riesgo.
            - 1.00x a 1.29x → ajustada.
            - Mayor o igual a 1.30x → adecuada.

            **Margen bruto**

            (Ventas − Costo de ventas) / Ventas.

            **Liquidez**

            Activos corrientes / Pasivos corrientes.

            **Utilidad neta**

            Utilidad bruta − Gastos operativos
            − Gastos financieros.

            Los indicadores se combinan para generar
            una clasificación preliminar de riesgo,
            viabilidad y recomendación comercial.
            """
        )

    # --------------------------------------------------------------
    # ESTRUCTURA DEL EXCEL
    # --------------------------------------------------------------

    with st.expander(
        "📄 Estructura requerida del archivo"
    ):

        st.markdown(
            """
            ### Columnas requeridas

            El archivo debe contener exactamente estas variables:

            1. `ID_Cliente`
            2. `Cliente`
            3. `Ciudad`
            4. `Actividad_Economica`
            5. `Ventas_Mensuales`
            6. `Costo_Ventas`
            7. `Gastos_Operativos`
            8. `Gastos_Financieros`
            9. `Activos_Corrientes`
            10. `Pasivos_Corrientes`
            11. `Activos_Totales`
            12. `Pasivos_Totales`
            13. `Patrimonio`
            14. `Cuota_Mensual_Credito`
            15. `Antiguedad_Negocio_Anios`
            16. `Historial_Pagos`
            17. `Dias_Mora_Max`
            18. `Tiene_Centrales`

            ---

            ### Importante

            El Excel debe contener únicamente
            los datos base del negocio.

            El dashboard calcula automáticamente:

            - Utilidad bruta
            - Margen bruto
            - Utilidad neta
            - Margen neto
            - Capital de trabajo
            - Endeudamiento
            - Liquidez
            - DSCR / Cobertura
            - Apalancamiento
            - Riesgo
            - Viabilidad
            - Recomendación comercial

            No es necesario incluir esas columnas
            calculadas en el Excel.
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
    [2, 1]
)

with col_titulo:

    st.title(
        "Dashboard comercial"
    )

    st.caption(
        "Visualización y análisis financiero de negocios"
    )


# ======================================================================
# SI NO HAY ARCHIVO
# ======================================================================

if df is None:

    st.info(
        "Carga un archivo Excel desde la barra lateral "
        "para comenzar el análisis. El archivo debe contener "
        "las variables desde ID_Cliente hasta Tiene_Centrales."
    )

    st.stop()


# ======================================================================
# SELECTOR DE CLIENTE
# ======================================================================

opciones_cliente = [
    "Todos los clientes"
]

for indice, fila in df.iterrows():

    opciones_cliente.append(
        f"{indice} · {nombre_cliente(fila)}"
    )


with col_selector:

    seleccion = st.selectbox(
        "Cliente",
        opciones_cliente,
        label_visibility="collapsed",
    )


# ======================================================================
# FILTRO
# ======================================================================

if seleccion == "Todos los clientes":

    datos = df.copy()

    cliente_idx = None

else:

    try:

        cliente_idx = int(
            seleccion.split(
                " · ",
                1
            )[0]
        )

        datos = df.loc[
            [cliente_idx]
        ].copy()

    except (
        ValueError,
        KeyError,
        IndexError,
    ):

        st.error(
            "No fue posible seleccionar el cliente."
        )

        st.stop()


# ======================================================================
# KPIs
# ======================================================================

k1, k2, k3, k4, k5, k6 = st.columns(
    6
)

kpis = [
    (
        k1,
        "k1",
        "Total negocios",
        f"{len(datos)}",
        False,
    ),
    (
        k2,
        "k2",
        "Ventas promedio",
        datos["ventas"].mean(),
        True,
    ),
    (
        k3,
        "k3",
        "Margen promedio",
        percent(
            datos["margenBruto"].mean()
        ),
        False,
    ),
    (
        k4,
        "k4",
        "Utilidad neta promedio",
        money(
            datos["utilidadNeta"].mean()
        ),
        False,
    ),
    (
        k5,
        "k5",
        "Endeudamiento",
        percent(
            datos["endeudamiento"].mean()
        ),
        False,
    ),
    (
        k6,
        "k6",
        "Cobertura",
        f"{datos['cobertura'].mean():.2f}x",
        False,
    ),
]


for (
    columna,
    clase,
    etiqueta,
    valor,
    es_ventas,
) in kpis:

    with columna:

        if es_ventas:

            valor_html = ventas_kpi_html(
                valor
            )

        else:

            valor_html = (
                "<div class='kpi-value'>"
                f"{safe_text(valor)}"
                "</div>"
            )

        st.markdown(
            f"""
            <div class="kpi-card {clase}">

                <div class="kpi-label">
                    {safe_text(etiqueta)}
                </div>

                {valor_html}

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

    if (
        total > 0
        and alto / total >= 0.40
    ):

        texto = (
            "Se identifica una concentración importante "
            "de negocios en riesgo alto. Se recomienda "
            "fortalecer la validación de capacidad de pago, "
            "endeudamiento y comportamiento de pago."
        )

    else:

        texto = (
            f"El análisis preliminar identifica "
            f"{viables} negocios viables en primera instancia. "
            f"La cobertura promedio es "
            f"{datos['cobertura'].mean():.2f}x y el "
            f"endeudamiento promedio es "
            f"{percent(datos['endeudamiento'].mean())}. "
            "La clasificación es preliminar y debe "
            "complementarse con la política de crédito vigente."
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
        unsafe_allow_html=True,
    )


st.write("")


# ======================================================================
# DISTRIBUCIÓN DEL RIESGO
# ======================================================================

st.subheader(
    "Distribución del riesgo"
)

r1, r2, r3 = st.columns(
    3
)


riesgo_bajo = (
    df["riesgo"] == "BAJO"
).sum()

riesgo_medio = (
    df["riesgo"] == "MEDIO"
).sum()

riesgo_alto = (
    df["riesgo"] == "ALTO"
).sum()


with r1:

    st.markdown(
        f"""
        <div class="risk-low">

            <small>
                RIESGO BAJO
            </small>

            <h2>
                {riesgo_bajo}
            </h2>

        </div>
        """,
        unsafe_allow_html=True,
    )


with r2:

    st.markdown(
        f"""
        <div class="risk-med">

            <small>
                RIESGO MEDIO
            </small>

            <h2>
                {riesgo_medio}
            </h2>

        </div>
        """,
        unsafe_allow_html=True,
    )


with r3:

    st.markdown(
        f"""
        <div class="risk-high">

            <small>
                RIESGO ALTO
            </small>

            <h2>
                {riesgo_alto}
            </h2>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ======================================================================
# GRÁFICAS SUPERIORES
# ======================================================================

g1, g2 = st.columns(
    2
)


# ======================================================================
# GRÁFICA 1 - DISTRIBUCIÓN DEL RIESGO
# ======================================================================

with g1:

    st.markdown(
        "**Distribución del riesgo**"
    )

    conteo = (
        datos["riesgo"]
        .value_counts()
        .reindex(
            [
                "BAJO",
                "MEDIO",
                "ALTO",
            ],
            fill_value=0,
        )
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
                marker_colors=[
                    "#10B981",
                    "#F59E0B",
                    "#EF4444",
                ],
                hole=0.50,
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
        "**Liquidez vs. Endeudamiento**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Relación entre capacidad de cubrir obligaciones
            de corto plazo y nivel de deuda del negocio.
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
        chart_data["endeudamiento"]
        * 100
    )

    chart_data["Liquidez_x"] = (
        chart_data["liquidez"]
    )

    chart_data["Riesgo"] = (
        chart_data["riesgo"]
    )

    fig_liquidez = px.scatter(
        chart_data,
        x="Endeudamiento_%",
        y="Liquidez_x",
        color="Riesgo",
        color_discrete_map={
            "BAJO": "#10B981",
            "MEDIO": "#F59E0B",
            "ALTO": "#EF4444",
        },
        hover_name="Cliente_Display",
        hover_data={
            "Endeudamiento_%": ":.1f",
            "Liquidez_x": ":.2f",
            "Riesgo": True,
        },
        labels={
            "Endeudamiento_%": "Endeudamiento (%)",
            "Liquidez_x": "Liquidez (x)",
            "Riesgo": "Riesgo",
        },
    )

    fig_liquidez.add_vline(
        x=50,
        line_dash="dash",
        line_color="#64748B",
        annotation_text="50%",
        annotation_position="top",
    )

    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color="#EF4444",
        annotation_text="70%",
        annotation_position="top right",
    )

    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color="#64748B",
        annotation_text="Liquidez 1.0x",
        annotation_position="bottom right",
    )

    fig_liquidez.update_traces(
        marker=dict(
            size=13,
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
        legend=dict(
            orientation="h"
        ),
    )

    st.plotly_chart(
        fig_liquidez,
        use_container_width=True,
    )


# ======================================================================
# GRÁFICAS DSCR
# ======================================================================

g3, g4 = st.columns(
    2
)


# ======================================================================
# GRÁFICA 3 - DSCR
# ======================================================================

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
        unsafe_allow_html=True,
    )

    dscr_data = datos.copy()

    dscr_data["Cliente_Display"] = (
        dscr_data.apply(
            nombre_cliente,
            axis=1,
        )
    )

    dscr_data["DSCR"] = (
        dscr_data["cobertura"]
    )

    dscr_data["Riesgo"] = (
        dscr_data["riesgo"]
    )

    fig_dscr = px.bar(
        dscr_data,
        x="Cliente_Display",
        y="DSCR",
        color="Riesgo",
        color_discrete_map={
            "BAJO": "#10B981",
            "MEDIO": "#F59E0B",
            "ALTO": "#EF4444",
        },
        hover_name="Cliente_Display",
        hover_data={
            "DSCR": ":.2f",
            "Riesgo": True,
        },
        labels={
            "Cliente_Display": "Cliente",
            "DSCR": "DSCR / Cobertura (x)",
            "Riesgo": "Riesgo",
        },
    )

    fig_dscr.add_hline(
        y=1,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text="Mínimo 1.00x",
        annotation_position="top left",
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color="#10B981",
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
# GRÁFICA 4 - DSCR HORIZONTAL
# ======================================================================

with g4:

    st.markdown(
        "**DSCR / Cobertura por cliente**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Comparación individual de cobertura de deuda.
            Se actualiza automáticamente al cambiar el cliente.
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

    ranking_dscr["DSCR"] = (
        ranking_dscr["cobertura"]
    )

    ranking_dscr = (
        ranking_dscr
        .sort_values(
            "DSCR",
            ascending=True,
        )
    )

    fig_dscr_horizontal = px.bar(
        ranking_dscr,
        x="DSCR",
        y="Cliente_Display",
        orientation="h",
        color="riesgo",
        color_discrete_map={
            "BAJO": "#10B981",
            "MEDIO": "#F59E0B",
            "ALTO": "#EF4444",
        },
        hover_name="Cliente_Display",
        hover_data={
            "DSCR": ":.2f",
            "riesgo": True,
        },
        labels={
            "DSCR": "DSCR / Cobertura (x)",
            "Cliente_Display": "",
            "riesgo": "Riesgo",
        },
    )

    fig_dscr_horizontal.add_vline(
        x=1,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text="1.00x",
        annotation_position="top",
    )

    fig_dscr_horizontal.add_vline(
        x=1.30,
        line_dash="dot",
        line_color="#10B981",
        annotation_text="1.30x",
        annotation_position="top",
    )

    fig_dscr_horizontal.update_layout(
        margin=dict(
            t=30,
            b=10,
            l=10,
            r=10,
        ),
        height=330,
        legend=dict(
            orientation="h"
        ),
    )

    st.plotly_chart(
        fig_dscr_horizontal,
        use_container_width=True,
    )


st.write("")


# ======================================================================
# DETALLE DEL CLIENTE
# ======================================================================

st.subheader(
    "👤 Detalle del cliente"
)


if cliente_idx is None:

    st.caption(
        "Selecciona un cliente en el menú superior "
        "para visualizar su información."
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
        ],
        "-",
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
            "RIESGO",
            fila["riesgo"],
        ),
        (
            "VIABILIDAD",
            fila["viabilidad"],
        ),
    ]

    for inicio in range(
        0,
        len(campos),
        4,
    ):

        fila_campos = campos[
            inicio:inicio + 4
        ]

        columnas = st.columns(
            4
        )

        for columna, (
            etiqueta,
            valor,
        ) in zip(
            columnas,
            fila_campos,
        ):

            with columna:

                st.markdown(
                    f"""
                    <div class="detail-card">

                        <div class="detail-label">
                            {safe_text(etiqueta)}
                        </div>

                        <div class="detail-value">
                            {safe_text(valor)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write("")


st.write("")


# ======================================================================
# TABLA DE SEÑALES
# ======================================================================

st.subheader(
    "⚠️ Señales y recomendación comercial"
)


tabla = df.copy()

tabla["Cliente_Display"] = (
    tabla.apply(
        nombre_cliente,
        axis=1,
    )
)

tabla_mostrar = tabla[
    [
        "Cliente_Display",
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
        lambda valor:
        f"{valor:.2f}x"
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


st.write("")


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

            Estos resultados sirven como apoyo comercial
            y no reemplazan la decisión crediticia definitiva.

        </p>

    </div>
    """,
    unsafe_allow_html=True,
)
