# Estilos CSS con anulación estricta para el tema oscuro de Streamlit
st.markdown(
    """
    <style>
    /* 1. Ajuste de KPIs para evitar saltos de línea */
    .kpi-card {
        border-radius: 10px;
        padding: 10px 8px;
        color: #ffffff !important;
        box-shadow: 0 2px 7px rgba(0,0,0,.15);
        min-height: 85px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }
    .kpi-label {
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        margin-bottom: 4px;
        text-transform: uppercase;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi-value {
        font-size: 15px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        word-break: break-all;
        line-height: 1.1;
    }
    .k1{background:#7050f6} .k2{background:#0878e8} .k3{background:#0ca5ba}
    .k4{background:#05c47a} .k5{background:#8b4df1} .k6{background:#0756c9}

    /* 2. FORZAR TEXTO NEGRO SOBRE FONDO BLANCO EN DIAGNÓSTICO Y RIESGO */
    .diag-box, .diag-box *, 
    .conclusion-box, .conclusion-box *,
    .risk-card, .risk-card *,
    .assistant-box, .assistant-box * {
        color: #0f172a !important;
    }

    .diag-box {
        background-color: #ffffff !important;
        border-left: 6px solid #1264d6 !important;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,.15);
    }

    .ind-row { 
        font-size: 14px !important; 
        margin: 8px 0 !important; 
        color: #1e293b !important; 
    }
    .ind-row * { color: #1e293b !important; }

    .conclusion-box {
        background-color: #f1f5f9 !important;
        border-radius: 8px;
        padding: 14px;
        margin-top: 12px;
        font-size: 14px !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* 3. Tarjetas de Riesgo */
    .risk-card {
        background-color: #ffffff !important;
        padding: 14px 16px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,.12);
    }
    .risk-low { border-left: 6px solid #10b981 !important; }
    .risk-med { border-left: 6px solid #f59e0b !important; }
    .risk-high { border-left: 6px solid #ef4444 !important; }
    
    .risk-title { 
        font-size: 12px !important; 
        font-weight: 700 !important; 
        color: #475569 !important; 
        letter-spacing: 0.5px; 
    }
    .risk-count { 
        font-size: 28px !important; 
        font-weight: 800 !important; 
        color: #0f172a !important; 
        margin-top: 4px;
    }

    /* 4. Asistente IA */
    .assistant-box {
        background-color: #f0f9ff !important;
        border: 1px solid #bae6fd !important;
        border-radius: 9px;
        padding: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
