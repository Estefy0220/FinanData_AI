"""
FinanData AI - Dashboard Comercial
----------------------------------

Dashboard financiero para análisis preliminar de negocios.

El Excel debe contener únicamente las variables base:

1. ID_Cliente
2. Cliente
3. Ciudad
4. Actividad_Economica
5. Ventas_Mensuales
6. Costo_Ventas
7. Gastos_Operativos
8. Gastos_Financieros
9. Activos_Corrientes
10. Pasivos_Corrientes
11. Activos_Totales
12. Pasivos_Totales
13. Patrimonio
14. Cuota_Mensual_Credito
15. Antiguedad_Negocio_Anios
16. Historial_Pagos
17. Dias_Mora_Max
18. Tiene_Centrales

Todos los indicadores financieros son calculados automáticamente.
"""

# ==============================================================
# IMPORTACIONES
# ==============================================================

from pathlib import Path
import re
import unicodedata

import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# ==============================================================
# CONFIGURACIÓN
# ==============================================================

st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================
# PALETA DE COLORES
# ==============================================================

PRIMARY = "#0757C9"

COLORS = {
    "purple": "#7050F6",
    "blue": "#0878E8",
    "turquoise": "#0CA5BA",
    "green": "#05C47A",
    "violet": "#8B4DF1",
    "dark_blue": "#0756C9",
    "text": "#25344A",
    "muted": "#667085",
    "background": "#F7F9FC",
    "border": "#E4E7EC",
    "white": "#FFFFFF",
    "low": "#05C47A",
    "medium": "#F59E0B",
    "high": "#EF4444",
}


# ==============================================================
# CSS
# ==============================================================

st.markdown(
    f"""
    <style>

    /* ==========================================================
       GENERAL
       ========================================================== */

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    h1 {{
        color: {COLORS["text"]};
        font-weight: 800 !important;
        letter-spacing: -1px;
    }}

    h2, h3 {{
        color: {COLORS["text"]};
    }}

    .subtitle {{
        color: {COLORS["muted"]};
        font-size: 15px;
        margin-top: -8px;
        margin-bottom: 22px;
    }}


    /* ==========================================================
       LOGO
       ========================================================== */

    .logo-wrapper {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }}

    .logo-box {{
        width: 34px;
        height: 34px;
        background: {PRIMARY};
        color: white;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 17px;
        flex-shrink: 0;
    }}

    .logo-text {{
        font-weight: 750;
        font-size: 18px;
        color: {COLORS["text"]};
    }}


    /* ==========================================================
       KPI
       ========================================================== */

    .kpi-card {{
        width: 100%;
        min-height: 112px;
        height: 112px;
        border-radius: 12px;
        padding: 16px;
        color: white;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(16, 24, 40, 0.10);
    }}

    .kpi-label {{
        font-size: 12px;
        font-weight: 650;
        opacity: 0.94;
        margin-bottom: 9px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .kpi-value {{
        font-size: 21px;
        font-weight: 800;
        line-height: 1.1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .kpi-1 {{
        background: {COLORS["purple"]};
    }}

    .kpi-2 {{
        background: {COLORS["blue"]};
    }}

    .kpi-3 {{
        background: {COLORS["turquoise"]};
    }}

    .kpi-4 {{
        background: {COLORS["green"]};
    }}

    .kpi-5 {{
        background: {COLORS["violet"]};
    }}

    .kpi-6 {{
        background: {COLORS["dark_blue"]};
    }}


    /* ==========================================================
       DIAGNÓSTICO
       ========================================================== */

    .section-title {{
        color: {COLORS["text"]};
        font-size: 25px;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 18px;
    }}

    .diagnostic-card {{
        background: white;
        border-left: 5px solid {PRIMARY};
        border-radius: 10px;
        padding: 20px 22px;
        box-shadow: 0 3px 12px rgba(16, 24, 40, 0.07);
        margin-bottom: 20px;
    }}

    .diagnostic-title {{
        color: {COLORS["text"]};
        font-size: 16px;
        font-weight: 750;
        margin-bottom: 16px;
    }}

    .diagnostic-row {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin: 11px 0;
        color: #344054;
        font-size: 14px;
        line-height: 1.5;
    }}

    .diagnostic-icon {{
        width: 20px;
        min-width: 20px;
        font-size: 14px;
    }}

    .diagnostic-row strong {{
        color: {COLORS["text"]};
    }}

    .conclusion {{
        background: {COLORS["background"]};
        border-radius: 8px;
        padding: 15px;
        margin-top: 17px;
        color: #344054;
        font-size: 14px;
        line-height: 1.55;
    }}

    .recommendation {{
        margin-top: 10px;
    }}


    /* ==========================================================
       RIESGO
       ========================================================== */

    .risk-card {{
        background: white;
        border-radius: 10px;
        padding: 17px 18px;
        box-shadow: 0 3px 10px rgba(16, 24, 40, 0.06);
    }}

    .risk-low {{
        border-left: 5px solid {COLORS["low"]};
    }}

    .risk-medium {{
        border-left: 5px solid {COLORS["medium"]};
    }}

    .risk-high {{
        border-left: 5px solid {COLORS["high"]};
    }}

    .risk-label {{
        color: {COLORS["muted"]};
        font-size: 11px;
        font-weight: 700;
    }}

    .risk-number {{
        color: {COLORS["text"]};
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
    }}


    /* ==========================================================
       DETALLE
       ========================================================== */

    .detail-card {{
        background: white;
        border: 1px solid {COLORS["border"]};
        border-radius: 9px;
        padding: 13px 15px;
        min-height: 76px;
        box-sizing: border-box;
    }}

    .detail-label {{
        color: #778399;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}

    .detail-value {{
        color: {COLORS["text"]};
        font-size: 15px;
        font-weight: 700;
        word-break: break-word;
    }}


    /* ==========================================================
       ASISTENTE
       ========================================================== */

    .assistant-card {{
        background: linear-gradient(
            135deg,
            #EEF5FF 0%,
            #F8FBFF 100%
        );
        border: 1px solid #DCEAFE;
        border-radius: 10px;
        padding: 19px;
        color: #344054;
        margin-top: 15px;
    }}

    .assistant-title {{
        color: {COLORS["text"]};
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 8px;
    }}

    .assistant-text {{
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
    }}


    /* ==========================================================
       TABLA
       ========================================================== */

    .table-note {{
        color: {COLORS["muted"]};
        font-size: 12px;
        margin-bottom: 8px;
    }}


    /* ==========================================================
       RESPONSIVE
       ========================================================== */

    @media (max-width: 1100px) {{
        .kpi-card {{
            min-height: 100px;
            height: 100px;
            padding: 12px;
        }}

        .kpi-value {{
            font-size: 17px;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================
# COLUMNAS ESPERADAS DEL EXCEL
# ==============================================================

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


# ==============================================================
# FUNCIONES DE UTILIDAD
# ==============================================================

def normalizar_texto(valor):
    """
    Convierte texto a minúsculas y elimina tildes.
    Facilita comparar valores como:
    Sí / Si / SI / sí.
    """

    if valor is None:
        return ""

    texto = str(valor).strip().lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    return texto


def to_number(valor):
    """
    Convierte números colombianos a float.

    Ejemplos:
    $10.000.000
    10.000.000
    10,5
    10.5
    """

    if valor is None:
        return 0.0

    if isinstance(valor, bool):
        return float(valor)

    if isinstance(valor, (int, float)):
        if pd.isna(valor):
            return 0.0
        return float(valor)

    texto = str(valor).strip()

    if not texto:
        return 0.0

    texto = (
        texto
        .replace("$", "")
        .replace(" ", "")
        .replace("%", "")
    )

    # Caso: 10.000.000,50
    if "." in texto and "," in texto:

        texto = texto.replace(".", "")
        texto = texto.replace(",", ".")

    # Caso: 10.000.000
    elif texto.count(".") > 1:

        texto = texto.replace(".", "")

    # Caso: 10,50
    elif "," in texto:

        texto = texto.replace(",", ".")

    try:
        return float(texto)

    except (ValueError, TypeError):
        return 0.0


def money(valor):
    """
    Formato colombiano sin decimales.
    """

    try:

        return (
            f"${float(valor):,.0f}"
            .replace(",", ".")
        )

    except Exception:

        return "$0"


def percent(valor):
    """
    Convierte 0.363 en 36.3%.
    """

    try:

        return f"{float(valor) * 100:.1f}%"

    except Exception:

        return "0.0%"


def safe_text(valor):
    """
    Limpia texto para insertarlo dentro de HTML.
    """

    texto = str(valor)

    return (
        texto
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def get_field(row, names, default=0):

    for nombre in names:

        if nombre in row.index:

            valor = row[nombre]

            if pd.notna(valor) and str(valor).strip() != "":

                return valor

    return default


def nombre_cliente(row):

    for columna in [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
    ]:

        if columna in row.index:

            valor = row[columna]

            if pd.notna(valor):

                texto = str(valor).strip()

                if texto:

                    return texto

    return "Cliente"


# ==============================================================
# CÁLCULO DE INDICADORES
# ==============================================================

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

    # ----------------------------------------------------------
    # UTILIDAD BRUTA
    # ----------------------------------------------------------

    utilidad_bruta = ventas - costo

    # ----------------------------------------------------------
    # MARGEN BRUTO
    # ----------------------------------------------------------

    margen_bruto = (
        utilidad_bruta / ventas
        if ventas > 0
        else 0
    )

    # ----------------------------------------------------------
    # UTILIDAD NETA
    # ----------------------------------------------------------

    # Corrección:
    # El gasto financiero se resta UNA sola vez.

    utilidad_neta = (
        utilidad_bruta
        - gastos
        - financieros
    )

    # ----------------------------------------------------------
    # MARGEN NETO
    # ----------------------------------------------------------

    margen_neto = (
        utilidad_neta / ventas
        if ventas > 0
        else 0
    )

    # ----------------------------------------------------------
    # CAPITAL DE TRABAJO
    # ----------------------------------------------------------

    capital_trabajo = (
        activos_corrientes
        - pasivos_corrientes
    )

    # ----------------------------------------------------------
    # ENDEUDAMIENTO
    # ----------------------------------------------------------

    endeudamiento = (
        pasivos_totales / activos_totales
        if activos_totales > 0
        else 0
    )

    # ----------------------------------------------------------
    # LIQUIDEZ
    # ----------------------------------------------------------

    liquidez = (
        activos_corrientes / pasivos_corrientes
        if pasivos_corrientes > 0
        else 0
    )

    # ----------------------------------------------------------
    # FLUJO DISPONIBLE
    # ----------------------------------------------------------

    flujo_disponible = (
        utilidad_bruta
        - gastos
    )

    # ----------------------------------------------------------
    # COBERTURA / DSCR
    # ----------------------------------------------------------

    cobertura = (
        flujo_disponible / cuota
        if cuota > 0
        else 0
    )

    # ----------------------------------------------------------
    # APALANCAMIENTO
    # ----------------------------------------------------------

    apalancamiento = (
        pasivos_totales / patrimonio
        if patrimonio > 0
        else 0
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
            "flujoDisponible": flujo_disponible,
        }
    )


# ==============================================================
# CLASIFICACIÓN DE RIESGO
# ==============================================================

def clasificar_riesgo(row):

    puntos = 0

    # ----------------------------------------------------------
    # MORA
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # HISTORIAL
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # CENTRALES
    # ----------------------------------------------------------

    centrales = normalizar_texto(
        get_field(
            row,
            [
                "Tiene_Centrales",
            ],
            "",
        )
    )

    # ----------------------------------------------------------
    # ENDEUDAMIENTO
    # ----------------------------------------------------------

    if row["endeudamiento"] > 0.70:

        puntos += 3

    elif row["endeudamiento"] > 0.50:

        puntos += 1

    # ----------------------------------------------------------
    # COBERTURA
    # ----------------------------------------------------------

    if row["cobertura"] < 1:

        puntos += 3

    elif row["cobertura"] < 1.30:

        puntos += 1

    # ----------------------------------------------------------
    # MARGEN
    # ----------------------------------------------------------

    if row["margenBruto"] < 0.20:

        puntos += 2

    elif row["margenBruto"] < 0.30:

        puntos += 1

    # ----------------------------------------------------------
    # UTILIDAD
    # ----------------------------------------------------------

    if row["utilidadNeta"] < 0:

        puntos += 2

    # ----------------------------------------------------------
    # MORA
    # ----------------------------------------------------------

    if mora > 30:

        puntos += 3

    elif mora > 15:

        puntos += 1

    # ----------------------------------------------------------
    # HISTORIAL DE PAGOS
    # ----------------------------------------------------------

    if (
        "malo" in historial
        or "incum" in historial
        or "negativo" in historial
    ):

        puntos += 3

    elif "regular" in historial:

        puntos += 1

    # ----------------------------------------------------------
    # CENTRALES
    # ----------------------------------------------------------

    # Se conserva la lógica de tu modelo original:
    # presencia de reporte negativo suma riesgo.

    if (
        "malo" in centrales
        or "negativo" in centrales
    ):

        puntos += 2

    # Si el Excel utiliza "Si/No" para indicar simplemente
    # existencia de consulta en centrales, NO se penaliza.
    #
    # Esto evita interpretar automáticamente "Sí" como algo malo.

    # ----------------------------------------------------------
    # RESULTADO
    # ----------------------------------------------------------

    if puntos >= 7:

        return "ALTO"

    if puntos >= 3:

        return "MEDIO"

    return "BAJO"


# ==============================================================
# VIABILIDAD
# ==============================================================

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
        and row["cobertura"] >= 1.00
        and row["utilidadNeta"] >= 0
    ):

        return "VIABLE CON CONDICIONES"

    return "NO VIABLE"


# ==============================================================
# RECOMENDACIÓN
# ==============================================================

def generar_recomendacion(viabilidad):

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


# ==============================================================
# SEMÁFOROS
# ==============================================================

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
        "El flujo disponible cubre la cuota con holgura suficiente.",
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
            "El margen es aceptable, aunque con espacio limitado de maniobra.",
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
            "Los activos corrientes no alcanzan para cubrir totalmente las obligaciones de corto plazo.",
        )

    if valor < 1.20:

        return (
            "🟠",
            "Ajustada",
            "La liquidez cubre lo corriente pero con poco colchón.",
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
            "El negocio no está generando excedente después de sus costos y gastos.",
        )

    return (
        "🟢",
        "Positiva",
        "El negocio genera excedente después de costos y gastos.",
    )


# ==============================================================
# CONCLUSIÓN
# ==============================================================

def generar_conclusion(row):

    viabilidad = row["viabilidad"]

    if viabilidad == "VIABLE":

        return (
            "El negocio presenta indicadores financieros sólidos y "
            "consistentes. Se recomienda continuar con el estudio "
            "de crédito, validando soportes documentales y "
            "comportamiento de pago histórico."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "El negocio presenta un perfil aceptable pero con "
            "puntos de atención. Se recomienda solicitar "
            "información adicional y ajustar monto o plazo según "
            "la capacidad de pago real."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente "
        "y/o un nivel de riesgo elevado. No se recomienda aprobar "
        "en primera instancia sin revisar la estructura de "
        "obligaciones y la información complementaria."
    )


# ==============================================================
# DIAGNÓSTICO HTML
# ==============================================================

def generar_diagnostico_cliente(row):

    e_icono, e_nivel, e_texto = semaforo_endeudamiento(
        row["endeudamiento"]
    )

    c_icono, c_nivel, c_texto = semaforo_cobertura(
        row["cobertura"]
    )

    m_icono, m_nivel, m_texto = semaforo_margen(
        row["margenBruto"]
    )

    l_icono, l_nivel, l_texto = semaforo_liquidez(
        row["liquidez"]
    )

    u_icono, u_nivel, u_texto = semaforo_utilidad(
        row["utilidadNeta"]
    )

    nombre = safe_text(
        nombre_cliente(row)
    )

    conclusion = safe_text(
        generar_conclusion(row)
    )

    recomendacion = safe_text(
        row["recomendacion"]
    )

    html = f"""
    <div class="diagnostic-card">

        <div class="diagnostic-title">
            Diagnóstico financiero — {nombre}
        </div>

        <div class="diagnostic-row">
            <span class="diagnostic-icon">
                {e_icono}
            </span>

            <span>
                <strong>Endeudamiento:</strong>
                {percent(row["endeudamiento"])}
                → {e_nivel}.
                {safe_text(e_texto)}
            </span>
        </div>

        <div class="diagnostic-row">
            <span class="diagnostic-icon">
                {c_icono}
            </span>

            <span>
                <strong>Cobertura:</strong>
                {row["cobertura"]:.2f}x
                → {c_nivel}.
                {safe_text(c_texto)}
            </span>
        </div>

        <div class="diagnostic-row">
            <span class="diagnostic-icon">
                {m_icono}
            </span>

            <span>
                <strong>Margen bruto:</strong>
                {percent(row["margenBruto"])}
                → {m_nivel}.
                {safe_text(m_texto)}
            </span>
        </div>

        <div class="diagnostic-row">
            <span class="diagnostic-icon">
                {l_icono}
            </span>

            <span>
                <strong>Liquidez:</strong>
                {row["liquidez"]:.2f}x
                → {l_nivel}.
                {safe_text(l_texto)}
            </span>
        </div>

        <div class="diagnostic-row">
            <span class="diagnostic-icon">
                {u_icono}
            </span>

            <span>
                <strong>Utilidad neta:</strong>
                {money(row["utilidadNeta"])}
                → {u_nivel}.
                {safe_text(u_texto)}
            </span>
        </div>

        <div class="conclusion">

            <strong>Conclusión</strong>

            <div style="margin-top:6px;">
                {conclusion}
            </div>

            <div class="recommendation">
                <strong>Recomendación comercial:</strong>
                {recomendacion}
            </div>

        </div>

    </div>
    """

    return html


# ==============================================================
# PROCESAMIENTO DEL DATAFRAME
# ==============================================================

@st.cache_data(show_spinner=False)
def procesar_dataframe(df):

    df = df.copy()

    # ----------------------------------------------------------
    # INDICADORES
    # ----------------------------------------------------------

    indicadores = df.apply(
        calcular_indicadores,
        axis=1
    )

    df = pd.concat(
        [
            df.reset_index(drop=True),
            indicadores.reset_index(drop=True),
        ],
        axis=1
    )

    # ----------------------------------------------------------
    # RIESGO
    # ----------------------------------------------------------

    df["riesgo"] = df.apply(
        clasificar_riesgo,
        axis=1
    )

    # ----------------------------------------------------------
    # VIABILIDAD
    # ----------------------------------------------------------

    df["viabilidad"] = df.apply(
        lambda fila: evaluar_viabilidad(
            fila["riesgo"],
            fila
        ),
        axis=1
    )

    # ----------------------------------------------------------
    # RECOMENDACIÓN
    # ----------------------------------------------------------

    df["recomendacion"] = df[
        "viabilidad"
    ].apply(
        generar_recomendacion
    )

    return df


# ==============================================================
# LECTURA DEL EXCEL
# ==============================================================

def cargar_archivo(archivo):

    if archivo is None:

        return None

    try:

        nombre = archivo.name.lower()

        if nombre.endswith(".csv"):

            return pd.read_csv(archivo)

        return pd.read_excel(archivo)

    except Exception as error:

        st.error(
            f"No fue posible leer el archivo: {error}"
        )

        return None


def validar_columnas(df):

    if df is None:

        return False

    faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]

    if faltantes:

        st.error(
            "El archivo no contiene todas las columnas requeridas."
        )

        st.warning(
            "Columnas faltantes: "
            + ", ".join(faltantes)
        )

        return False

    return True


# ==============================================================
# SIDEBAR
# ==============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo-wrapper">

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
        "Dashboard comercial · Análisis financiero de negocios"
    )

    st.divider()

    st.markdown(
        "### 📁 Cargar datos"
    )

    archivo = st.file_uploader(
        "Selecciona tu Excel",
        type=["xlsx", "xls", "csv"],
        help=(
            "El archivo debe contener las 18 columnas "
            "base definidas para el dashboard."
        ),
    )

    # ----------------------------------------------------------
    # ARCHIVO DEL REPOSITORIO
    # ----------------------------------------------------------

    archivo_repositorio = None

    posibles_archivos = [
        Path("base_datos.xlsx"),
        Path("base_datos.xls"),
        Path("base_datos.csv"),
    ]

    for ruta in posibles_archivos:

        if ruta.exists():

            archivo_repositorio = ruta

            break

    # ----------------------------------------------------------
    # SELECCIONAR FUENTE
    # ----------------------------------------------------------

    if archivo is not None:

        df_raw = cargar_archivo(
            archivo
        )

        nombre_archivo = archivo.name

    elif archivo_repositorio is not None:

        try:

            if archivo_repositorio.suffix.lower() == ".csv":

                df_raw = pd.read_csv(
                    archivo_repositorio
                )

            else:

                df_raw = pd.read_excel(
                    archivo_repositorio
                )

            nombre_archivo = (
                archivo_repositorio.name
            )

        except Exception as error:

            df_raw = None

            st.error(
                "No se pudo leer el archivo del repositorio: "
                f"{error}"
            )

    else:

        df_raw = None
        nombre_archivo = None

    # ----------------------------------------------------------
    # PROCESAR
    # ----------------------------------------------------------

    if df_raw is not None:

        if df_raw.empty:

            st.error(
                "El archivo no contiene registros."
            )

        elif validar_columnas(df_raw):

            # Solo conservar las columnas base.
            df_base = df_raw[
                COLUMNAS_REQUERIDAS
            ].copy()

            st.session_state["clientes_df"] = (
                procesar_dataframe(
                    df_base
                )
            )

            st.success(
                f"Datos cargados: {nombre_archivo}"
            )

    st.divider()

    # ==========================================================
    # INTERPRETACIÓN
    # ==========================================================

    with st.expander(
        "ℹ️ Interpretación de indicadores"
    ):

        st.markdown(
            """
            **Endeudamiento**

            Pasivos totales / Activos totales.

            - Hasta 50% → adecuado
            - 50%–70% → moderado
            - Más de 70% → alto

            **Cobertura / DSCR**

            Flujo disponible / Cuota mensual.

            - Menor a 1.00x → riesgo
            - 1.00x–1.30x → ajustada
            - Mayor o igual a 1.30x → adecuada

            **Margen bruto**

            (Ventas − Costo de ventas) / Ventas.

            **Liquidez**

            Activos corrientes / Pasivos corrientes.

            - Menor a 1.00x → atención
            - 1.00x–1.20x → ajustada
            - Mayor a 1.20x → adecuada

            **Utilidad neta**

            Utilidad bruta − Gastos operativos − Gastos financieros.
            """
        )

    # ==========================================================
    # ESTRUCTURA DEL EXCEL
    # ==========================================================

    with st.expander(
        "📄 Estructura del Excel"
    ):

        st.markdown(
            """
            El archivo debe contener únicamente los datos base
            del negocio.

            **Columnas requeridas:**

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

            No debes agregar indicadores calculados al Excel.

            FinanData AI calcula automáticamente:

            - Utilidad bruta
            - Margen bruto
            - Utilidad neta
            - Margen neto
            - Capital de trabajo
            - Endeudamiento
            - Liquidez
            - Cobertura / DSCR
            - Apalancamiento
            - Riesgo
            - Viabilidad
            - Recomendación
            """
        )


# ==============================================================
# OBTENER DATAFRAME
# ==============================================================

df = st.session_state.get(
    "clientes_df"
)


# ==============================================================
# ENCABEZADO
# ==============================================================

col_titulo, col_selector = st.columns(
    [2.1, 1]
)

with col_titulo:

    st.title(
        "Dashboard comercial"
    )

    st.markdown(
        """
        <div class="subtitle">
            Visualización y análisis financiero de negocios
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================
# SIN DATOS
# ==============================================================

if df is None:

    st.info(
        "Carga tu archivo Excel desde la barra lateral "
        "o coloca `base_datos.xlsx` en el mismo repositorio "
        "de GitHub que contiene el `app.py`."
    )

    st.stop()


# ==============================================================
# SELECTOR CLIENTE
# ==============================================================

opciones_cliente = [
    "Todos los clientes"
]

for indice, fila in df.iterrows():

    opciones_cliente.append(
        f"{indice + 1} · {nombre_cliente(fila)}"
    )


with col_selector:

    seleccion = st.selectbox(
        "Cliente",
        opciones_cliente,
        label_visibility="collapsed",
    )


# ==============================================================
# FILTRO
# ==============================================================

if seleccion == "Todos los clientes":

    datos = df.copy()

    cliente_idx = None

else:

    posicion = int(
        seleccion.split(" · ")[0]
    ) - 1

    cliente_idx = df.index[posicion]

    datos = df.loc[
        [cliente_idx]
    ].copy()


# ==============================================================
# KPIs
# ==============================================================

k1, k2, k3, k4, k5, k6 = st.columns(
    6
)

ventas_promedio = datos["ventas"].mean()
margen_promedio = datos["margenBruto"].mean()
utilidad_promedio = datos["utilidadNeta"].mean()
endeudamiento_promedio = datos["endeudamiento"].mean()
cobertura_promedio = datos["cobertura"].mean()


kpi_data = [

    (
        k1,
        "kpi-1",
        "Total negocios",
        f"{len(datos)}",
    ),

    (
        k2,
        "kpi-2",
        "Ventas promedio",
        money(ventas_promedio),
    ),

    (
        k3,
        "kpi-3",
        "Margen promedio",
        percent(margen_promedio),
    ),

    (
        k4,
        "kpi-4",
        "Utilidad neta",
        money(utilidad_promedio),
    ),

    (
        k5,
        "kpi-5",
        "Endeudamiento",
        percent(endeudamiento_promedio),
    ),

    (
        k6,
        "kpi-6",
        "Cobertura",
        f"{cobertura_promedio:.2f}x",
    ),
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
            unsafe_allow_html=True,
        )


st.write("")


# ==============================================================
# DIAGNÓSTICO
# ==============================================================

st.markdown(
    """
    <div class="section-title">
        💡 Diagnóstico y recomendación financiera
    </div>
    """,
    unsafe_allow_html=True,
)


if cliente_idx is not None:

    fila = df.loc[
        cliente_idx
    ]

    # IMPORTANTE:
    # st.markdown renderiza el HTML correctamente.
    st.markdown(
        generar_diagnostico_cliente(fila),
        unsafe_allow_html=True,
    )

else:

    total = len(datos)

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

    if total > 0 and alto / total >= 0.40:

        texto = (
            "Se identifica una concentración importante de "
            "negocios en riesgo alto. Se recomienda fortalecer "
            "la validación de capacidad de pago, endeudamiento "
            "y comportamiento de pago antes de continuar con "
            "las aprobaciones."
        )

    else:

        texto = (
            f"El análisis preliminar identifica {viables} "
            f"negocios viables en primera instancia. La cobertura "
            f"promedio es {cobertura_promedio:.2f}x y el "
            f"endeudamiento promedio es "
            f"{percent(endeudamiento_promedio)}. "
            "La clasificación es preliminar y debe "
            "complementarse con la política de crédito vigente."
        )

    st.markdown(
        f"""
        <div class="diagnostic-card">

            <div class="diagnostic-title">
                Diagnóstico general de cartera
            </div>

            <div class="diagnostic-row">

                <span class="diagnostic-icon">
                    📊
                </span>

                <span>
                    {safe_text(texto)}
                </span>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================
# DISTRIBUCIÓN DE RIESGO
# ==============================================================

st.markdown(
    """
    <div class="section-title">
        Distribución del riesgo
    </div>
    """,
    unsafe_allow_html=True,
)

r1, r2, r3 = st.columns(
    3
)

bajo_total = (
    datos["riesgo"] == "BAJO"
).sum()

medio_total = (
    datos["riesgo"] == "MEDIO"
).sum()

alto_total = (
    datos["riesgo"] == "ALTO"
).sum()


with r1:

    st.markdown(
        f"""
        <div class="risk-card risk-low">

            <div class="risk-label">
                RIESGO BAJO
            </div>

            <div class="risk-number">
                {bajo_total}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with r2:

    st.markdown(
        f"""
        <div class="risk-card risk-medium">

            <div class="risk-label">
                RIESGO MEDIO
            </div>

            <div class="risk-number">
                {medio_total}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with r3:

    st.markdown(
        f"""
        <div class="risk-card risk-high">

            <div class="risk-label">
                RIESGO ALTO
            </div>

            <div class="risk-number">
                {alto_total}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ==============================================================
# GRÁFICA 1
# DISTRIBUCIÓN DEL RIESGO
# ==============================================================

g1, g2 = st.columns(
    2
)

with g1:

    st.markdown(
        "#### Distribución del riesgo"
    )

    conteo = (
        datos["riesgo"]
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

    fig_riesgo = go.Figure()

    fig_riesgo.add_trace(
        go.Pie(
            labels=[
                "Riesgo bajo",
                "Riesgo medio",
                "Riesgo alto",
            ],
            values=conteo.values,
            hole=0.55,
            marker=dict(
                colors=[
                    COLORS["green"],
                    COLORS["medium"],
                    COLORS["high"],
                ],
                line=dict(
                    color="white",
                    width=3,
                ),
            ),
            textinfo="label+percent",
            textfont=dict(
                size=12,
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Negocios: %{value}<br>"
                "Participación: %{percent}"
                "<extra></extra>"
            ),
        )
    )

    fig_riesgo.update_layout(
        height=350,
        margin=dict(
            t=20,
            b=20,
            l=10,
            r=10,
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.05,
            x=0.5,
            xanchor="center",
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    st.plotly_chart(
        fig_riesgo,
        use_container_width=True,
    )


# ==============================================================
# GRÁFICA 2
# LIQUIDEZ VS ENDEUDAMIENTO
# ==============================================================

with g2:

    st.markdown(
        "#### Liquidez vs. Endeudamiento"
    )

    st.caption(
        "La posición ideal se encuentra hacia mayor liquidez "
        "y menor endeudamiento."
    )

    fig_liquidez = go.Figure()

    colores_riesgo = {
        "BAJO": COLORS["green"],
        "MEDIO": COLORS["medium"],
        "ALTO": COLORS["high"],
    }

    for riesgo in [
        "BAJO",
        "MEDIO",
        "ALTO",
    ]:

        grupo = datos[
            datos["riesgo"] == riesgo
        ]

        if grupo.empty:
            continue

        fig_liquidez.add_trace(
            go.Scatter(
                x=grupo["endeudamiento"] * 100,
                y=grupo["liquidez"],
                mode="markers",
                name=riesgo,
                marker=dict(
                    size=14,
                    color=colores_riesgo[riesgo],
                    line=dict(
                        color="white",
                        width=2,
                    ),
                ),
                text=grupo.apply(
                    nombre_cliente,
                    axis=1,
                ),
                customdata=grupo[
                    [
                        "endeudamiento",
                        "liquidez",
                    ]
                ].values,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Endeudamiento: "
                    "%{customdata[0]:.1%}<br>"
                    "Liquidez: "
                    "%{customdata[1]:.2f}x"
                    "<extra></extra>"
                ),
            )
        )

    # Línea 50%
    fig_liquidez.add_vline(
        x=50,
        line_dash="dash",
        line_color=COLORS["purple"],
        line_width=1.5,
        annotation_text="50%",
        annotation_position="top",
    )

    # Línea 70%
    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color=COLORS["high"],
        line_width=1.5,
        annotation_text="70%",
        annotation_position="top",
    )

    # Liquidez 1x
    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color=COLORS["blue"],
        line_width=1.5,
        annotation_text="1.0x",
        annotation_position="bottom right",
    )

    fig_liquidez.update_layout(
        height=350,
        margin=dict(
            t=30,
            b=20,
            l=10,
            r=10,
        ),
        xaxis=dict(
            title="Endeudamiento (%)",
            gridcolor="#EAECF0",
        ),
        yaxis=dict(
            title="Liquidez (x)",
            gridcolor="#EAECF0",
        ),
        legend=dict(
            orientation="h",
            y=-0.15,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    st.plotly_chart(
        fig_liquidez,
        use_container_width=True,
    )


# ==============================================================
# GRÁFICAS DSCR
# ==============================================================

g3, g4 = st.columns(
    2
)


# ==============================================================
# GRÁFICA 3
# DSCR VERTICAL
# ==============================================================

with g3:

    st.markdown(
        "#### DSCR / Cobertura de deuda"
    )

    st.caption(
        "Mayor a 1.30x indica una mayor holgura de capacidad de pago."
    )

    fig_dscr = go.Figure()

    if not datos.empty:

        for riesgo in [
            "BAJO",
            "MEDIO",
            "ALTO",
        ]:

            grupo = datos[
                datos["riesgo"] == riesgo
            ]

            if grupo.empty:
                continue

            fig_dscr.add_trace(
                go.Bar(
                    x=grupo.apply(
                        nombre_cliente,
                        axis=1,
                    ),
                    y=grupo["cobertura"],
                    name=riesgo,
                    marker_color=colores_riesgo[riesgo],
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "DSCR: %{y:.2f}x"
                        "<extra></extra>"
                    ),
                )
            )

    fig_dscr.add_hline(
        y=1,
        line_dash="dash",
        line_color=COLORS["high"],
        line_width=1.5,
        annotation_text="Mínimo 1.00x",
        annotation_position="top left",
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color=COLORS["green"],
        line_width=1.5,
        annotation_text="Objetivo 1.30x",
        annotation_position="top right",
    )

    fig_dscr.update_layout(
        height=350,
        barmode="group",
        margin=dict(
            t=35,
            b=65,
            l=10,
            r=10,
        ),
        xaxis=dict(
            title="Cliente",
            tickangle=-35,
        ),
        yaxis=dict(
            title="DSCR / Cobertura (x)",
            gridcolor="#EAECF0",
        ),
        legend=dict(
            orientation="h",
            y=-0.28,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    st.plotly_chart(
        fig_dscr,
        use_container_width=True,
    )


# ==============================================================
# GRÁFICA 4
# DSCR HORIZONTAL
# ==============================================================

with g4:

    st.markdown(
        "#### Comparativo de cobertura"
    )

    st.caption(
        "Ordenamiento de los negocios según capacidad de cobertura."
    )

    ranking = datos.copy()

    ranking["Cliente_Display"] = (
        ranking.apply(
            nombre_cliente,
            axis=1,
        )
    )

    ranking = ranking.sort_values(
        "cobertura",
        ascending=True,
    )

    fig_horizontal = go.Figure()

    for _, fila in ranking.iterrows():

        riesgo = fila["riesgo"]

        fig_horizontal.add_trace(
            go.Bar(
                x=[fila["cobertura"]],
                y=[fila["Cliente_Display"]],
                orientation="h",
                name=riesgo,
                marker_color=colores_riesgo[riesgo],
                showlegend=False,
                hovertemplate=(
                    "<b>"
                    + safe_text(
                        fila["Cliente_Display"]
                    )
                    + "</b><br>"
                    f"DSCR: {fila['cobertura']:.2f}x"
                    "<extra></extra>"
                ),
            )
        )

    fig_horizontal.add_vline(
        x=1,
        line_dash="dash",
        line_color=COLORS["high"],
        line_width=1.5,
        annotation_text="1.00x",
        annotation_position="top",
    )

    fig_horizontal.add_vline(
        x=1.30,
        line_dash="dot",
        line_color=COLORS["green"],
        line_width=1.5,
        annotation_text="1.30x",
        annotation_position="top",
    )

    fig_horizontal.update_layout(
        height=350,
        margin=dict(
            t=35,
            b=20,
            l=10,
            r=10,
        ),
        xaxis=dict(
            title="DSCR / Cobertura (x)",
            gridcolor="#EAECF0",
        ),
        yaxis=dict(
            title="",
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    st.plotly_chart(
        fig_horizontal,
        use_container_width=True,
    )


st.write("")


# ==============================================================
# DETALLE DEL CLIENTE
# ==============================================================

st.markdown(
    """
    <div class="section-title">
        👤 Detalle del cliente
    </div>
    """,
    unsafe_allow_html=True,
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

    campos = [

        (
            "CLIENTE",
            nombre_cliente(fila),
        ),

        (
            "ID CLIENTE",
            get_field(
                fila,
                ["ID_Cliente"],
                "-",
            ),
        ),

        (
            "CIUDAD",
            get_field(
                fila,
                ["Ciudad"],
                "-",
            ),
        ),

        (
            "ACTIVIDAD",
            get_field(
                fila,
                ["Actividad_Economica"],
                "-",
            ),
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
            "MARGEN BRUTO",
            percent(fila["margenBruto"]),
        ),

        (
            "MARGEN NETO",
            percent(fila["margenNeto"]),
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
            "RIESGO",
            fila["riesgo"],
        ),

        (
            "VIABILIDAD",
            fila["viabilidad"],
        ),

        (
            "ANTIGÜEDAD",
            f"{to_number(fila['Antiguedad_Negocio_Anios']):.1f} años",
        ),
    ]

    columnas_detalle = st.columns(
        4
    )

    for indice, (etiqueta, valor) in enumerate(campos):

        with columnas_detalle[
            indice % 4
        ]:

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


# ==============================================================
# TABLA DE SEÑALES
# ==============================================================

st.markdown(
    """
    <div class="section-title">
        ⚠️ Señales y recomendación comercial
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="table-note">
        Esta tabla resume los principales indicadores calculados
        automáticamente a partir del Excel.
    </div>
    """,
    unsafe_allow_html=True,
)


tabla = datos.copy()

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
        "liquidez",
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
    "Recomendación",
]


st.dataframe(
    tabla_mostrar,
    use_container_width=True,
    hide_index=True,
)


# ==============================================================
# ASISTENTE IA
# ==============================================================

bajo_global = (
    df["riesgo"] == "BAJO"
).sum()

medio_global = (
    df["riesgo"] == "MEDIO"
).sum()

alto_global = (
    df["riesgo"] == "ALTO"
).sum()

viables_global = (
    df["viabilidad"] == "VIABLE"
).sum()


st.markdown(
    f"""
    <div class="assistant-card">

        <div class="assistant-title">
            🤖 Asistente IA comercial
        </div>

        <p class="assistant-text">

            El análisis identifica

            <strong>{bajo_global}</strong>
            negocios en riesgo bajo,

            <strong>{medio_global}</strong>
            en riesgo medio y

            <strong>{alto_global}</strong>
            en riesgo alto.

            Se identifican

            <strong>{viables_global}</strong>
            perfiles viables en primera instancia.

            Estos resultados constituyen un apoyo para el análisis
            comercial y no reemplazan la decisión crediticia definitiva.

        </p>

    </div>
    """,
    unsafe_allow_html=True,
)
