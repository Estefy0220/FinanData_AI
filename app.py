"""
FinanData AI - Dashboard comercial (Streamlit)

Análisis financiero automatizado para estudio de crédito de negocios.

El Excel debe contener únicamente las variables base del negocio
hasta Tiene_Centrales.

Los indicadores financieros, riesgo, viabilidad y recomendación
son calculados automáticamente por el dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from html import escape


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


# ----------------------------------------------------------------------
# ESTILOS
# ----------------------------------------------------------------------

st.markdown(
    """
    <style>

    /* ==============================================================
       KPI
       ============================================================== */

    .kpi-card {
        border-radius: 10px;
        padding: 13px 14px;
        color: white;
        box-shadow: 0 2px 7px rgba(0,0,0,.08);
        min-height: 92px;
        height: 92px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
        overflow: hidden;
    }

    .kpi-label {
        font-size: clamp(10px, 0.80vw, 12px);
        font-weight: 600;
        opacity: .92;
        margin-bottom: 7px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1;
    }

    .kpi-value {
        font-size: clamp(15px, 1.35vw, 21px);
        font-weight: 800;
        line-height: 1.05;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        letter-spacing: -0.3px;
    }

    .kpi-sales-value {
        font-size: clamp(13px, 1.12vw, 19px);
        font-weight: 800;
        line-height: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        letter-spacing: -0.45px;
        width: 100%;
        display: block;
    }

    .k1 { background: #7050f6; }
    .k2 { background: #0878e8; }
    .k3 { background: #0ca5ba; }
    .k4 { background: #05c47a; }
    .k5 { background: #8b4df1; }
    .k6 { background: #0756c9; }


    /* ==============================================================
       DIAGNÓSTICO
       ============================================================== */

    .diag-box {
        background: #ffffff;
        border-left: 5px solid #1264d6;
        border-radius: 9px;
        padding: 16px 18px;
        box-shadow: 0 2px 7px rgba(0,0,0,.06);
        color: #25344a;
        font-family: Arial, sans-serif;
    }

    .diag-title {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 14px;
        color: #26364d;
    }

    .diag-row {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 13px;
        line-height: 1.45;
        margin: 8px 0;
        color: #344054;
    }

    .diag-icon {
        width: 16px;
        min-width: 16px;
        font-size: 13px;
        line-height: 18px;
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
        padding: 14px 15px;
        margin-top: 14px;
        color: #344054;
        font-size: 13px;
        line-height: 1.5;
    }

    .conclusion-title {
        font-weight: 700;
        color: #344054;
        margin-bottom: 5px;
    }

    .recommendation {
        margin-top: 14px;
    }

    .recommendation strong {
        color: #344054;
    }


    /* ==============================================================
       ASISTENTE IA
       ============================================================== */

    .assistant-box {
        background: linear-gradient(
            135deg,
            #eef5ff,
            #f8fbff
        );
        border: 1px solid #dceafe;
        border-radius: 9px;
        padding: 18px;
        color: #344054;
        font-family: Arial, sans-serif;
    }

    .assistant-title {
        font-size: 16px;
        font-weight: 700;
        color: #25344a;
        margin-bottom: 8px;
    }

    .assistant-text {
        font-size: 13px;
        line-height: 1.55;
        margin: 0;
    }


    /* ==============================================================
       RIESGO
       ============================================================== */

    .risk-low {
        border-left: 4px solid #10b981;
        padding: 10px 14px;
        border-radius: 8px;
        background: #fff;
    }

    .risk-med {
        border-left: 4px solid #f59e0b;
        padding: 10px 14px;
        border-radius: 8px;
        background: #fff;
    }

    .risk-high {
        border-left: 4px solid #ef4444;
        padding: 10px 14px;
        border-radius: 8px;
        background: #fff;
    }


    /* ==============================================================
       GRÁFICAS
       ============================================================== */

    .chart-description {
        color: #667085;
        font-size: 12px;
        margin-top: -5px;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------
# FUNCIONES DE UTILIDAD
# ----------------------------------------------------------------------

def to_number(v):
    """Convierte valores colombianos a número."""

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

        if (
            name in row
            and row[name] not in ("", None)
            and not pd.isna(row[name])
        ):
            return row[name]

    return default


def safe_text(value):
    """Evita que datos del Excel rompan el HTML."""
    return escape(str(value))


# ----------------------------------------------------------------------
# KPI VENTAS PROMEDIO
# ----------------------------------------------------------------------

def ventas_kpi_html(valor):

    valor_formateado = money(valor)

    return (
        f"<div class='kpi-sales-value'>"
        f"{safe_text(valor_formateado)}"
        f"</div>"
    )


# ----------------------------------------------------------------------
# CÁLCULO DE INDICADORES
# ----------------------------------------------------------------------

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

    ac = to_number(
        get_field(
            row,
            [
                "Activos_Corrientes",
                "Activos corrientes",
            ],
        )
    )

    pc = to_number(
        get_field(
            row,
            [
                "Pasivos_Corrientes",
                "Pasivos corrientes",
            ],
        )
    )

    at = to_number(
        get_field(
            row,
            [
                "Activos_Totales",
                "Activos totales",
            ],
        )
    )

    pt = to_number(
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

    utilidad_bruta = ventas - costo

    # --------------------------------------------------------------
    # MARGEN BRUTO
    # --------------------------------------------------------------

    margen_bruto = (
        utilidad_bruta / ventas
        if ventas
        else 0
    )

    # --------------------------------------------------------------
    # UTILIDAD NETA
    # --------------------------------------------------------------

    utilidad_neta = (
        utilidad_bruta
        - gastos
        - (2 * financieros)
    )

    # --------------------------------------------------------------
    # MARGEN NETO
    # --------------------------------------------------------------

    margen_neto = (
        utilidad_neta / ventas
        if ventas
        else 0
    )

    # --------------------------------------------------------------
    # CAPITAL DE TRABAJO
    # --------------------------------------------------------------

    capital_trabajo = ac - pc

    # --------------------------------------------------------------
    # ENDEUDAMIENTO
    # --------------------------------------------------------------

    endeudamiento = (
        pt / at
        if at
        else 0
    )

    # --------------------------------------------------------------
    # LIQUIDEZ
    # --------------------------------------------------------------

    liquidez = (
        ac / pc
        if pc
        else 0
    )

    # --------------------------------------------------------------
    # FLUJO DISPONIBLE
    # --------------------------------------------------------------

    flujo = utilidad_bruta - gastos

    # --------------------------------------------------------------
    # DSCR / COBERTURA
    # --------------------------------------------------------------

    cobertura = (
        flujo / cuota
        if cuota
        else 0
    )

    # --------------------------------------------------------------
    # APALANCAMIENTO
    # --------------------------------------------------------------

    apalancamiento = (
        pt / patrimonio
        if patrimonio
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


# ----------------------------------------------------------------------
# RIESGO
# ----------------------------------------------------------------------

def clasificar_riesgo(row):

    p = 0

    mora = to_number(
        get_field(
            row,
            [
                "Dias_Mora_Max",
                "Días de mora",
                "Dias_Mora",
            ],
        )
    )

    hist = str(
        get_field(
            row,
            [
                "Historial_Pagos",
                "Historial de pagos",
            ],
            "",
        )
    ).lower()

    centrales = str(
        get_field(
            row,
            [
                "Tiene_Centrales",
            ],
            "",
        )
    ).lower()

    # Endeudamiento

    if row["endeudamiento"] > 0.70:
        p += 3

    elif row["endeudamiento"] > 0.50:
        p += 1

    # Cobertura

    if row["cobertura"] < 1:
        p += 3

    elif row["cobertura"] < 1.30:
        p += 1

    # Margen

    if row["margenBruto"] < 0.20:
        p += 2

    elif row["margenBruto"] < 0.30:
        p += 1

    # Utilidad

    if row["utilidadNeta"] < 0:
        p += 2

    # Mora

    if mora > 30:
        p += 3

    elif mora > 15:
        p += 1

    # Historial de pagos

    if "malo" in hist or "incum" in hist:
        p += 3

    elif "regular" in hist:
        p += 1

    # Centrales de riesgo

    if (
        "malo" in centrales
        or "negativo" in centrales
        or "si" in centrales
        or "sí" in centrales
    ):
        p += 2

    return (
        "ALTO"
        if p >= 7
        else (
            "MEDIO"
            if p >= 3
            else "BAJO"
        )
    )


# ----------------------------------------------------------------------
# VIABILIDAD
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# RECOMENDACIÓN
# ----------------------------------------------------------------------

def generar_recomendacion(viabilidad):

    if viabilidad == "VIABLE":

        return (
            "Continuar estudio y validar soportes, flujo de caja "
            "y capacidad de pago."
        )

    if viabilidad == "VIABLE CON CONDICIONES":

        return (
            "Solicitar soportes adicionales y evaluar monto/plazo "
            "según capacidad de pago."
        )

    return (
        "No recomendar aprobación en primera instancia. Revisar "
        "endeudamiento, capacidad de pago, rentabilidad e historial."
    )


# ----------------------------------------------------------------------
# SEMÁFOROS
# ----------------------------------------------------------------------

def semaforo_endeudamiento(v):

    if v > 0.70:
        return (
            "🔴",
            "Alto",
            "Una proporción elevada de los activos está financiada con deuda.",
        )

    if v > 0.50:
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


def semaforo_cobertura(v):

    if v < 1:
        return (
            "🔴",
            "Riesgo",
            "El flujo disponible no alcanza para cubrir completamente la cuota.",
        )

    if v < 1.30:
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


def semaforo_margen(v):

    if v < 0.20:
        return (
            "🔴",
            "Bajo",
            "El negocio tiene poca capacidad para absorber gastos adicionales.",
        )

    if v < 0.30:
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


def semaforo_liquidez(v):

    if v < 1:
        return (
            "🔴",
            "Atención",
            "Los activos corrientes no alcanzan para cubrir totalmente las obligaciones de corto plazo.",
        )

    if v < 1.20:
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


def semaforo_utilidad(v):

    if v < 0:
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


# ----------------------------------------------------------------------
# CONCLUSIÓN
# ----------------------------------------------------------------------

def generar_conclusion(row):

    v = row["viabilidad"]

    if v == "VIABLE":

        return (
            "El negocio presenta indicadores financieros sólidos y consistentes. "
            "Por esta razón, se recomienda continuar con el estudio de crédito, "
            "validando soportes documentales y comportamiento de pago histórico."
        )

    if v == "VIABLE CON CONDICIONES":

        return (
            "El negocio presenta un perfil aceptable pero con puntos de atención. "
            "Se recomienda solicitar información adicional y ajustar monto o plazo "
            "según la capacidad de pago real antes de continuar el estudio."
        )

    return (
        "El negocio presenta una capacidad de pago insuficiente y/o un nivel de "
        "riesgo elevado. Por estos indicadores, no se recomienda aprobar en primera "
        "instancia. Se recomienda solicitar información adicional y revisar la "
        "estructura de obligaciones antes de continuar con el estudio."
    )


# ----------------------------------------------------------------------
# DIAGNÓSTICO
# ----------------------------------------------------------------------

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

    html = f"""
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
                <strong>Margen:</strong>
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
                {safe_text(generar_conclusion(row))}
            </div>

            <div class="recommendation">
                <strong>Recomendación comercial:</strong>
                {safe_text(row["recomendacion"])}
            </div>

        </div>

    </div>
    """

    return html


# ----------------------------------------------------------------------
# PROCESAMIENTO
# ----------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def procesar_dataframe(df: pd.DataFrame) -> pd.DataFrame:

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
        lambda r: evaluar_viabilidad(
            r["riesgo"],
            r
        ),
        axis=1,
    )

    df["recomendacion"] = (
        df["viabilidad"]
        .apply(generar_recomendacion)
    )

    return df


# ----------------------------------------------------------------------
# NOMBRE DEL CLIENTE
# ----------------------------------------------------------------------

def nombre_cliente(row):

    for col in [
        "Cliente",
        "Nombre_Cliente",
        "Nombre cliente",
    ]:

        if (
            col in row
            and pd.notna(row[col])
            and str(row[col]).strip()
        ):
            return row[col]

    return "Cliente"


# ----------------------------------------------------------------------
# BARRA LATERAL
# ----------------------------------------------------------------------

with st.sidebar:

    # --------------------------------------------------------------
    # LOGO
    # --------------------------------------------------------------

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
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------------
    # DESCRIPCIÓN
    # --------------------------------------------------------------

    st.caption(
        "Dashboard comercial · Análisis financiero de negocios"
    )

    st.divider()

    # --------------------------------------------------------------
    # CARGAR EXCEL
    # --------------------------------------------------------------

    archivo = st.file_uploader(
        "📁 Cargar Excel",
        type=[
            "xlsx",
            "xls",
            "csv"
        ]
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

                # --------------------------------------------------
                # COLUMNAS BASE ESPERADAS
                # --------------------------------------------------

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

                columnas_faltantes = [
                    col
                    for col in columnas_requeridas
                    if col not in df_raw.columns
                ]

                if columnas_faltantes:

                    st.error(
                        "El archivo no tiene todas las columnas requeridas."
                    )

                    st.warning(
                        "Columnas faltantes: "
                        + ", ".join(columnas_faltantes)
                    )

                    st.info(
                        "El archivo debe contener las columnas desde "
                        "`ID_Cliente` hasta `Tiene_Centrales`."
                    )

                else:

                    # --------------------------------------------------
                    # IMPORTANTE:
                    # SOLO SE UTILIZAN LAS COLUMNAS BASE
                    # HASTA TIENE_CENTRALES.
                    # --------------------------------------------------

                    df_base = df_raw[
                        columnas_requeridas
                    ].copy()

                    st.session_state.clientes_df = (
                        procesar_dataframe(
                            df_base
                        )
                    )

                    st.success(
                        f"Archivo cargado: {archivo.name}"
                    )

        except Exception as e:

            st.error(
                f"No fue posible leer el archivo: {e}"
            )

    st.divider()

    # --------------------------------------------------------------
    # INTERPRETACIÓN DE INDICADORES
    # --------------------------------------------------------------

    with st.expander(
        "ℹ️ ¿Cómo interpretar los indicadores?"
    ):

        st.markdown(
            """
            - **Endeudamiento** = Pasivos totales / Activos totales.
              Menor a 50% es sano; sobre 70% es alto.

            - **Cobertura / DSCR** = Flujo disponible / Cuota del crédito.
              Debe ser mayor a 1.3x para tener holgura.

            - **Margen bruto** = (Ventas − Costo de ventas) / Ventas.
              Refleja la rentabilidad del negocio.

            - **Liquidez** = Activos corrientes / Pasivos corrientes.
              Mayor a 1x indica capacidad de cubrir el corto plazo.

            - **Utilidad neta** = Utilidad bruta − Gastos operativos
              − Gastos financieros. Debe ser positiva.

            Estos indicadores combinados determinan el **riesgo**
            y la **viabilidad** de cada negocio.
            """
        )

    # --------------------------------------------------------------
    # ESTRUCTURA DEL ARCHIVO
    # --------------------------------------------------------------

    with st.expander(
        "📄 ¿Cómo debe estar compuesto el archivo a analizar?"
    ):

        st.markdown(
            """
            ### 📋 Columnas que debe contener el Excel

            El archivo debe contener las siguientes variables,
            respetando exactamente estos nombres:

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

            ### ⚙️ Importante

            El archivo debe contener únicamente los **datos base
            del negocio**.

            **El Excel debe llegar solamente hasta `Tiene_Centrales`.**

            No es necesario incluir los indicadores calculados,
            porque el dashboard los genera automáticamente.

            ---

            ### 🚫 No incluir estas columnas calculadas

            No es necesario que el Excel contenga:

            - `Utilidad_Bruta`
            - `Margen_Bruto`
            - `Utilidad_Neta`
            - `Margen_Neto`
            - `Capital_Trabajo`
            - `Endeudamiento`
            - `Liquidez_Corriente`
            - `DSCR_Cobertura`
            - `Apalancamiento`
            - `Nivel_Riesgo`
            - `Viabilidad_Primera_Instancia`
            - `Recomendacion_Comercial`

            ---

            ### 🤖 ¿Qué calcula FinanData AI?

            A partir de los datos base del Excel, el dashboard
            calcula automáticamente:

            - Utilidad bruta
            - Margen bruto
            - Utilidad neta
            - Margen neto
            - Capital de trabajo
            - Endeudamiento
            - Liquidez corriente
            - DSCR / Cobertura
            - Apalancamiento
            - Nivel de riesgo
            - Viabilidad
            - Recomendación comercial

            Esto permite cargar un Excel con información
            financiera básica y dejar que el dashboard realice
            automáticamente el análisis.
            """
        )


# ----------------------------------------------------------------------
# DATAFRAME
# ----------------------------------------------------------------------

df = st.session_state.get(
    "clientes_df"
)


# ----------------------------------------------------------------------
# ENCABEZADO
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# SELECTOR DE CLIENTE
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# SI NO HAY ARCHIVO
# ----------------------------------------------------------------------

if df is None:

    st.info(
        "Carga un archivo Excel desde la barra lateral para comenzar "
        "el análisis. El archivo debe contener las variables desde "
        "`ID_Cliente` hasta `Tiene_Centrales`."
    )

    st.stop()


# ----------------------------------------------------------------------
# FILTRO CLIENTE
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# KPIs
# ----------------------------------------------------------------------

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
        "Utilidad neta",
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


for col, klass, label, value, is_sales in kpis:

    with col:

        if is_sales:

            value_html = ventas_kpi_html(
                value
            )

        else:

            value_html = (
                f"<div class='kpi-value'>"
                f"{safe_text(value)}"
                f"</div>"
            )

        st.markdown(
            f"""
            <div class="kpi-card {klass}">
                <div class="kpi-label">
                    {safe_text(label)}
                </div>
                {value_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


st.write("")


# ----------------------------------------------------------------------
# DIAGNÓSTICO
# ----------------------------------------------------------------------

st.subheader(
    "💡 Diagnóstico y recomendación financiera"
)


if cliente_idx is not None:

    fila = df.loc[
        cliente_idx
    ]

    st.html(
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

    if total and alto / total >= 0.4:

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

    st.html(
        f"""
        <div class="diag-box">

            <div class="diag-title">
                Diagnóstico general de cartera
            </div>

            <div class="diag-row">
                <span class="diag-icon">📊</span>

                <span class="diag-text">
                    {safe_text(texto)}
                </span>
            </div>

        </div>
        """
    )


st.write("")


# ----------------------------------------------------------------------
# DISTRIBUCIÓN DEL RIESGO
# ----------------------------------------------------------------------

st.subheader(
    "Distribución del riesgo"
)

r1, r2, r3 = st.columns(
    3
)


with r1:

    st.markdown(
        f"""
        <div class="risk-low">

            <small>
                RIESGO BAJO
            </small>

            <h2>
                {(df["riesgo"] == "BAJO").sum()}
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )


with r2:

    st.markdown(
        f"""
        <div class="risk-med">

            <small>
                RIESGO MEDIO
            </small>

            <h2>
                {(df["riesgo"] == "MEDIO").sum()}
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )


with r3:

    st.markdown(
        f"""
        <div class="risk-high">

            <small>
                RIESGO ALTO
            </small>

            <h2>
                {(df["riesgo"] == "ALTO").sum()}
            </h2>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ----------------------------------------------------------------------
# GRÁFICAS
# ----------------------------------------------------------------------

g1, g2 = st.columns(
    2
)


# ----------------------------------------------------------------------
# GRÁFICA 1 - DISTRIBUCIÓN DEL RIESGO
# ----------------------------------------------------------------------

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
                hole=0.5,
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
        use_container_width=True
    )


# ----------------------------------------------------------------------
# GRÁFICA 2 - LIQUIDEZ VS ENDEUDAMIENTO
# ----------------------------------------------------------------------

with g2:

    st.markdown(
        "**Liquidez vs. Endeudamiento**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Relación entre capacidad de cubrir obligaciones de corto plazo
            y nivel de deuda del negocio.
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

    chart_data["Riesgo"] = (
        chart_data["riesgo"]
    )

    fig_liquidez = px.scatter(
        chart_data,
        x="Endeudamiento_%",
        y="Liquidez_x",
        color="Riesgo",
        color_discrete_map={
            "BAJO": "#10b981",
            "MEDIO": "#f59e0b",
            "ALTO": "#ef4444",
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
        line_color="#64748b",
        annotation_text="50%",
        annotation_position="top",
    )

    fig_liquidez.add_vline(
        x=70,
        line_dash="dot",
        line_color="#ef4444",
        annotation_text="70%",
        annotation_position="top right",
    )

    fig_liquidez.add_hline(
        y=1,
        line_dash="dash",
        line_color="#64748b",
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
        use_container_width=True
    )


# ----------------------------------------------------------------------
# DSCR
# ----------------------------------------------------------------------

g3, g4 = st.columns(
    2
)


# ----------------------------------------------------------------------
# GRÁFICA 3 - DSCR / COBERTURA
# ----------------------------------------------------------------------

with g3:

    st.markdown(
        "**DSCR / Cobertura de deuda**"
    )

    st.markdown(
        """
        <div class="chart-description">
            Capacidad del flujo disponible para cubrir la cuota mensual
            del crédito. Un DSCR superior a 1.30x representa mayor holgura.
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
            "BAJO": "#10b981",
            "MEDIO": "#f59e0b",
            "ALTO": "#ef4444",
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
        line_color="#ef4444",
        annotation_text="Mínimo 1.00x",
        annotation_position="top left",
    )

    fig_dscr.add_hline(
        y=1.30,
        line_dash="dot",
        line_color="#10b981",
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
        use_container_width=True
    )


# ----------------------------------------------------------------------
# GRÁFICA 4 - DSCR HORIZONTAL
# ----------------------------------------------------------------------

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
        unsafe_allow_html=True
    )

    ranking_dscr = datos.copy()

    ranking_dscr["Cliente_Display"] = (
        ranking_dscr.apply(
            nombre_cliente,
            axis=1
        )
    )

    ranking_dscr["DSCR"] = (
        ranking_dscr["cobertura"]
    )

    ranking_dscr = ranking_dscr.sort_values(
        "DSCR",
        ascending=True
    )

    fig_dscr_horizontal = px.bar(
        ranking_dscr,
        x="DSCR",
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
        line_color="#ef4444",
        annotation_text="1.00x",
        annotation_position="top",
    )

    fig_dscr_horizontal.add_vline(
        x=1.30,
        line_dash="dot",
        line_color="#10b981",
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
        use_container_width=True
    )


st.write("")


# ----------------------------------------------------------------------
# DETALLE DEL CLIENTE
# ----------------------------------------------------------------------

st.subheader(
    "👤 Detalle del cliente"
)


if cliente_idx is None:

    st.caption(
        "Selecciona un cliente en el menú superior para visualizar su información."
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
        "-"
    )

    actividad = get_field(
        fila,
        [
            "Actividad_Economica",
            "Actividad",
        ],
        "-"
    )

    d1, d2, d3, d4 = st.columns(
        4
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
            "RIESGO",
            fila["riesgo"]
        ),
        (
            "VIABILIDAD",
            fila["viabilidad"]
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
                <small style="color:#778399;">
                    {safe_text(label)}
                </small>

                <br>

                <strong>
                    {safe_text(value)}
                </strong>
                """,
                unsafe_allow_html=True
            )

            st.write("")


st.write("")


# ----------------------------------------------------------------------
# TABLA
# ----------------------------------------------------------------------

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
    "Recomendación",
]


st.dataframe(
    tabla_mostrar,
    use_container_width=True,
    hide_index=True
)


st.write("")


# ----------------------------------------------------------------------
# ASISTENTE IA COMERCIAL
# ----------------------------------------------------------------------

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


st.html(
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

            Estos resultados sirven como apoyo comercial y no reemplazan
            la decisión crediticia definitiva.

        </p>

    </div>
    """
)
