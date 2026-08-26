"""
FinanData AI
Dashboard comercial y análisis financiero de negocios

Archivo de entrada:
Excel o CSV con únicamente las variables base del negocio.

El dashboard calcula automáticamente:
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
- Recomendación comercial
"""

# ==============================================================
# IMPORTACIONES
# ==============================================================

import textwrap
from html import escape

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================================================
# CONFIGURACIÓN
# ==============================================================

st.set_page_config(
    page_title="FinanData AI - Dashboard comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#0757C9"


# ==============================================================
# FUNCIÓN PARA HTML SEGURO
# ==============================================================

def render_html(html):
    """
    Renderiza HTML eliminando la indentación del código fuente.

    Esto evita que Streamlit interprete el HTML como bloque de código.
    """
    html = textwrap.dedent(html).strip()

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ==============================================================
# ESTILOS
# ==============================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

/* ==========================================================
   CONTENEDOR PRINCIPAL
   ========================================================== */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* ==========================================================
   LOGO
   ========================================================== */

.logo-container {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.logo-box {
    width: 32px;
    height: 32px;
    background: #0757c9;
    color: white;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
}

.logo-text {
    font-weight: 700;
    font-size: 18px;
    color: #26364d;
}


/* ==========================================================
   KPI
   ========================================================== */

.kpi-card {
    width: 100%;
    height: 105px;
    min-height: 105px;
    box-sizing: border-box;

    border-radius: 12px;

    padding: 15px;

    color: white;

    display: flex;
    flex-direction: column;
    justify-content: center;

    box-shadow: 0 3px 10px rgba(0,0,0,.10);

    overflow: hidden;
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;

    margin-bottom: 8px;

    opacity: .95;

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

.kpi-sales-value {
    font-size: 18px;
    font-weight: 800;

    line-height: 1.1;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.k1 {
    background: #7050f6;
}

.k2 {
    background: #0878e8;
}

.k3 {
    background: #0ca5ba;
}

.k4 {
    background: #05c47a;
}

.k5 {
    background: #8b4df1;
}

.k6 {
    background: #0756c9;
}


/* ==========================================================
   DIAGNÓSTICO
   ========================================================== */

.diag-box {
    background: #ffffff;

    border-left: 5px solid #1264d6;

    border-radius: 10px;

    padding: 18px 20px;

    box-shadow: 0 2px 8px rgba(0,0,0,.07);

    color: #25344a;

    margin-top: 8px;
}

.diag-title {
    font-size: 16px;
    font-weight: 700;

    color: #26364d;

    margin-bottom: 15px;
}

.diag-row {
    display: flex;

    align-items: flex-start;

    gap: 9px;

    font-size: 14px;

    line-height: 1.5;

    margin: 10px 0;

    color: #344054;
}

.diag-icon {
    width: 18px;
    min-width: 18px;

    font-size: 14px;
}

.diag-text {
    flex: 1;
}

.diag-text strong {
    color: #26364d;
}

.conclusion-box {
    background: #f4f6f9;

    border-radius: 8px;

    padding: 15px;

    margin-top: 16px;

    color: #344054;

    font-size: 14px;

    line-height: 1.5;
}

.conclusion-title {
    font-weight: 700;

    color: #344054;

    margin-bottom: 6px;
}

.recommendation {
    margin-top: 12px;
}

.recommendation strong {
    color: #344054;
}


/* ==========================================================
   RIESGO
   ========================================================== */

.risk-card {
    background: #ffffff;

    border-radius: 10px;

    padding: 14px 16px;

    box-shadow: 0 2px 7px rgba(0,0,0,.06);

    min-height: 90px;
}

.risk-low {
    border-left: 5px solid #10b981;
}

.risk-med {
    border-left: 5px solid #f59e0b;
}

.risk-high {
    border-left: 5px solid #ef4444;
}

.risk-label {
    font-size: 12px;

    color: #667085;

    font-weight: 700;
}

.risk-number {
    font-size: 28px;

    font-weight: 800;

    margin-top: 4px;

    color: #25344a;
}


/* ==========================================================
   ASISTENTE
   ========================================================== */

.assistant-box {
    background: linear-gradient(
        135deg,
        #eef5ff,
        #f8fbff
    );

    border: 1px solid #dceafe;

    border-radius: 10px;

    padding: 18px;

    color: #344054;

    margin-top: 10px;
}

.assistant-title {
    font-size: 17px;

    font-weight: 700;

    color: #25344a;

    margin-bottom: 8px;
}

.assistant-text {
    font-size: 14px;

    line-height: 1.6;

    margin: 0;
}


/* ==========================================================
   DETALLE
   ========================================================== */

.detail-card {
    background: #ffffff;

    border: 1px solid #eaecf0;

    border-radius: 8px;

    padding: 12px 14px;

    min-height: 72px;

    margin-bottom: 10px;
}

.detail-label {
    font-size: 11px;

    color: #778399;

    font-weight: 700;

    text-transform: uppercase;

    margin-bottom: 5px;
}

.detail-value {
    font-size: 15px;

    color: #26364d;

    font-weight: 700;
}


/* ==========================================================
   DESCRIPCIÓN DE GRÁFICAS
   ========================================================== */

.chart-description {
    color: #667085;

    font-size: 12px;

    line-height: 1.4;

    margin-top: -5px;

    margin-bottom: 8px;
}


/* ==========================================================
   RESPONSIVE
   ========================================================== */

@media (max-width: 900px) {

    .kpi-card {
        height: 95px;
        min-height: 95px;
    }

    .kpi-value {
        font-size: 17px;
    }

    .kpi-sales-value {
        font-size: 15px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================
# FUNCIONES DE UTILIDAD
# ==============================================================

def to_number(value):
    """
    Convierte números colombianos a float.

    Ejemplos:
    $10.000.000 -> 10000000
    10.000.000 -> 10000000
    10,5 -> 10.5
    """

    if pd.isna(value):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    if not value:
        return 0.0

    value = (
        value
        .replace("$", "")
        .replace(" ", "")
    )

    if "," in value and "." in value:
        value = value.replace(".", "")
        value = value.replace(",", ".")

    elif "," in value:
        value = value.replace(",", ".")

    try:
        return float(value)

    except (ValueError, TypeError):
        return 0.0


def money(value):
    """Formato monetario colombiano."""

    try:
        return f"${value:,.0f}".replace(",", ".")

    except Exception:
        return "$0"


def percent(value):
    """Formato porcentaje."""

    try:
        return f"{value * 100:.1f}%"

    except Exception:
        return "0.0%"


def safe_text(value):
    """Protege texto que será utilizado dentro de HTML."""

    return escape(str(value))


def get_field(row, names, default=0):
    """
    Busca el primer campo disponible entre varios nombres.
    """

    for name in names:

        if name not in row:
            continue

        value = row[name]

        if value is None:
            continue

        try:
            if pd.isna(value):
                continue
        except Exception:
            pass

        if str(value).strip() == "":
            continue

        return value

    return default


def nombre_cliente(row):
    """Obtiene el nombre del cliente."""

    for column in [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
    ]:

        if column in row:

            value = row[column]

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    return value

    return "Cliente"


# ==============================================================
# COLUMNAS REQUERIDAS
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
        }
    )


# ==============================================================
# CLASIFICACIÓN DE RIESGO
# ==============================================================

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
            ],
            "",
        )
    ).strip().lower()

    centrales = str(
        get_field(
            row,
            [
                "Tiene_Centrales",
            ],
            "",
        )
    ).strip().lower()

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
    # HISTORIAL
    # ----------------------------------------------------------

    if (
        "malo" in historial
        or "incum" in historial
    ):
        puntos += 3

    elif "regular" in historial:
        puntos += 1

    # ----------------------------------------------------------
    # CENTRALES
    # ----------------------------------------------------------

    centrales_negativas = [
        "si",
        "sí",
        "malo",
        "negativo",
        "reportado",
        "reportes",
    ]

    if any(
        palabra in centrales
        for palabra in centrales_negativas
    ):
        puntos += 2

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
        and row["cobertura"] >= 1
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

def semaforo_endeudamiento(value):

    if value > 0.70:

        return (
            "🔴",
            "Alto",
            "Una proporción elevada de los activos está financiada con deuda.",
        )

    if value > 0.50:

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


def semaforo_cobertura(value):

    if value < 1:

        return (
            "🔴",
            "Riesgo",
            "El flujo disponible no alcanza para cubrir completamente la cuota.",
        )

    if value < 1.30:

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


def semaforo_margen(value):

    if value < 0.20:

        return (
            "🔴",
            "Bajo",
            "El negocio tiene poca capacidad para absorber gastos adicionales.",
        )

    if value < 0.30:

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


def semaforo_liquidez(value):

    if value < 1:

        return (
            "🔴",
            "Atención",
            "Los activos corrientes no alcanzan para cubrir totalmente las obligaciones.",
        )

    if value < 1.20:

        return (
            "🟠",
            "Ajustada",
            "La liquidez cubre lo corriente pero con poco colchón.",
        )

    return (
        "🟢",
        "Adecuada",
        "Los activos corrientes cubren cómodamente las obligaciones.",
    )


def semaforo_utilidad(value):

    if value < 0:

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
            "información adicional y ajustar monto o plazo "
            "según la capacidad de pago real."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente "
        "y/o un nivel de riesgo elevado. No se recomienda "
        "aprobar en primera instancia. Se recomienda revisar "
        "la estructura de obligaciones antes de continuar."
    )


# ==============================================================
# DIAGNÓSTICO
# ==============================================================

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
            <strong>Margen:</strong>
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
            Conclusión
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


# ==============================================================
# PROCESAMIENTO DEL DATAFRAME
# ==============================================================

@st.cache_data(show_spinner=False)
def procesar_dataframe(df):

    df = df.copy()

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


# ==============================================================
# SIDEBAR
# ==============================================================

with st.sidebar:

    render_html(
        f"""
        <div class="logo-container">

            <div class="logo-box">
                F
            </div>

            <div class="logo-text">
                FinanData AI
            </div>

        </div>
        """
    )

    st.caption(
        "Dashboard comercial · Análisis financiero de negocios"
    )

    st.divider()

    # ----------------------------------------------------------
    # CARGAR ARCHIVO
    # ----------------------------------------------------------

    archivo = st.file_uploader(
        "📁 Cargar Excel",
        type=[
            "xlsx",
            "xls",
            "csv",
        ],
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

                faltantes = [
                    column
                    for column in COLUMNAS_REQUERIDAS
                    if column not in df_raw.columns
                ]

                if faltantes:

                    st.error(
                        "El archivo no tiene todas las columnas requeridas."
                    )

                    st.warning(
                        "Columnas faltantes: "
                        + ", ".join(faltantes)
                    )

                else:

                    df_base = df_raw[
                        COLUMNAS_REQUERIDAS
                    ].copy()

                    st.session_state.clientes_df = (
                        procesar_dataframe(
                            df_base
                        )
                    )

                    st.success(
                        f"Archivo cargado: {archivo.name}"
                    )

        except Exception as error:

            st.error(
                f"No fue posible leer el archivo: {error}"
            )

    st.divider()

    # ----------------------------------------------------------
    # AYUDA
    # ----------------------------------------------------------

    with st.expander(
        "ℹ️ ¿Cómo interpretar los indicadores?"
    ):

        st.markdown(
            """
**Endeudamiento**

Pasivos totales / Activos totales.

- Menor o igual a 50% → adecuado
- Entre 50% y 70% → moderado
- Mayor a 70% → alto

**Cobertura / DSCR**

Flujo disponible / Cuota mensual.

- Menor a 1.00x → riesgo
- 1.00x a 1.30x → ajustada
- Mayor o igual a 1.30x → adecuada

**Margen bruto**

(Ventas − Costo de ventas) / Ventas.

**Liquidez**

Activos corrientes / Pasivos corrientes.

**Utilidad neta**

Utilidad bruta − Gastos operativos − Gastos financieros.
"""
        )

    # ----------------------------------------------------------
    # ESTRUCTURA DEL EXCEL
    # ----------------------------------------------------------

    with st.expander(
        "📄 Estructura del archivo"
    ):

        st.markdown(
            """
### Columnas requeridas

El Excel debe contener exactamente las variables base:

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

### Importante

El Excel debe contener solamente los **datos base**.

No agregues al Excel los indicadores calculados.

El dashboard los calcula automáticamente.
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
    [2.5, 1]
)

with col_titulo:

    st.title(
        "Dashboard comercial"
    )

    st.caption(
        "Visualización y análisis financiero de negocios"
    )


# ==============================================================
# SELECTOR
# ==============================================================

opciones_cliente = [
    "Todos los clientes"
]

if df is not None:

    opciones_cliente.extend(
        [
            f"{index} · {nombre_cliente(row)}"
            for index, row in df.iterrows()
        ]
    )


with col_selector:

    seleccion = st.selectbox(
        "Cliente",
        opciones_cliente,
        label_visibility="collapsed",
    )


# ==============================================================
# SI NO HAY ARCHIVO
# ==============================================================

if df is None:

    st.info(
        "Carga un archivo Excel desde la barra lateral "
        "para comenzar el análisis."
    )

    st.stop()


# ==============================================================
# FILTRO
# ==============================================================

if seleccion == "Todos los clientes":

    datos = df.copy()

    cliente_idx = None

else:

    cliente_idx = int(
        seleccion.split(" · ")[0]
    )

    datos = df.loc[
        [cliente_idx]
    ].copy()


# ==============================================================
# KPIs
# ==============================================================

k1, k2, k3, k4, k5, k6 = st.columns(
    6
)

kpi_data = [
    (
        k1,
        "k1",
        "Total negocios",
        f"{len(datos)}",
    ),
    (
        k2,
        "k2",
        "Ventas promedio",
        money(datos["ventas"].mean()),
    ),
    (
        k3,
        "k3",
        "Margen promedio",
        percent(datos["margenBruto"].mean()),
    ),
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


for column, color_class, label, value in kpi_data:

    with column:

        render_html(
            f"""
            <div class="kpi-card {color_class}">

                <div class="kpi-label">
                    {safe_text(label)}
                </div>

                <div class="kpi-value">
                    {safe_text(value)}
                </div>

            </div>
            """
        )


st.write("")


# ==============================================================
# DIAGNÓSTICO
# ==============================================================

st.subheader(
    "💡 Diagnóstico y recomendación financiera"
)

if cliente_idx is not None:

    fila = df.loc[
        cliente_idx
    ]

    render_html(
        generar_diagnostico_cliente(
            fila
        )
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
            "Se identifica una concentración importante "
            "de negocios en riesgo alto. Se recomienda "
            "fortalecer la validación de capacidad de pago, "
            "endeudamiento y comportamiento de pago."
        )

    else:

        texto = (
            f"El análisis preliminar identifica {viables} "
            f"negocios viables en primera instancia. "
            f"La cobertura promedio es "
            f"{datos['cobertura'].mean():.2f}x y el "
            f"endeudamiento promedio es "
            f"{percent(datos['endeudamiento'].mean())}."
        )

    render_html(
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
        """
    )


st.write("")


# ==============================================================
# DISTRIBUCIÓN DEL RIESGO
# ==============================================================

st.subheader(
    "Distribución del riesgo"
)

r1, r2, r3 = st.columns(
    3
)


with r1:

    cantidad_bajo = (
        (df["riesgo"] == "BAJO").sum()
    )

    render_html(
        f"""
        <div class="risk-card risk-low">

            <div class="risk-label">
                RIESGO BAJO
            </div>

            <div class="risk-number">
                {cantidad_bajo}
            </div>

        </div>
        """
    )


with r2:

    cantidad_medio = (
        (df["riesgo"] == "MEDIO").sum()
    )

    render_html(
        f"""
        <div class="risk-card risk-med">

            <div class="risk-label">
                RIESGO MEDIO
            </div>

            <div class="risk-number">
                {cantidad_medio}
            </div>

        </div>
        """
    )


with r3:

    cantidad_alto = (
        (df["riesgo"] == "ALTO").sum()
    )

    render_html(
        f"""
        <div class="risk-card risk-high">

            <div class="risk-label">
                RIESGO ALTO
            </div>

            <div class="risk-number">
                {cantidad_alto}
            </div>

        </div>
        """
    )


st.write("")


# ==============================================================
# GRÁFICA 1 Y 2
# ==============================================================

g1, g2 = st.columns(
    2
)


# ==============================================================
# GRÁFICA 1 - DISTRIBUCIÓN DEL RIESGO
# ==============================================================

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
                marker_colors=[
                    "#10b981",
                    "#f59e0b",
                    "#ef4444",
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
            t=20,
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


# ==============================================================
# GRÁFICA 2 - LIQUIDEZ VS ENDEUDAMIENTO
# ==============================================================

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
            "BAJO": "#10b981",
            "MEDIO": "#f59e0b",
            "ALTO": "#ef4444",
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
        line_color="#64748b",
        annotation_text="50%",
    )

    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color="#ef4444",
        annotation_text="70%",
    )

    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color="#64748b",
        annotation_text="1.0x",
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


# ==============================================================
# GRÁFICA 3 Y 4
# ==============================================================

g3, g4 = st.columns(
    2
)


# ==============================================================
# GRÁFICA 3 - DSCR
# ==============================================================

with g3:

    st.markdown(
        "**DSCR / Cobertura de deuda**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Capacidad del flujo disponible para cubrir la cuota mensual.
            Un DSCR superior a 1.30x representa mayor holgura.
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
            "BAJO": "#10b981",
            "MEDIO": "#f59e0b",
            "ALTO": "#ef4444",
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
        line_color="#ef4444",
        annotation_text="1.00x",
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color="#10b981",
        annotation_text="1.30x",
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


# ==============================================================
# GRÁFICA 4 - DSCR HORIZONTAL
# ==============================================================

with g4:

    st.markdown(
        "**DSCR / Cobertura por cliente**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Comparación individual de cobertura de deuda.
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
            "BAJO": "#10b981",
            "MEDIO": "#f59e0b",
            "ALTO": "#ef4444",
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
        line_color="#ef4444",
        annotation_text="1.00x",
    )

    fig_horizontal.add_vline(
        x=1.30,
        line_dash="dot",
        line_color="#10b981",
        annotation_text="1.30x",
    )

    fig_horizontal.update_layout(
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
        fig_horizontal,
        use_container_width=True,
    )


st.write("")


# ==============================================================
# DETALLE DEL CLIENTE
# ==============================================================

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

    detalle = [
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

    detalle_cols = st.columns(
        4
    )

    for index, (label, value) in enumerate(detalle):

        with detalle_cols[index % 4]:

            render_html(
                f"""
                <div class="detail-card">

                    <div class="detail-label">
                        {safe_text(label)}
                    </div>

                    <div class="detail-value">
                        {safe_text(value)}
                    </div>

                </div>
                """
            )


st.write("")


# ==============================================================
# TABLA
# ==============================================================

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


# ==============================================================
# ASISTENTE IA
# ==============================================================

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


render_html(
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

            Estos resultados sirven como apoyo comercial y
            no reemplazan la decisión crediticia definitiva.

        </p>

    </div>
    """
)
