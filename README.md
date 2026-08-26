# FinanData AI — Dashboard comercial

Dashboard de análisis financiero para el estudio de crédito de negocios, desarrollado
como proyecto académico basado en el formato de crédito de Banco Caja Social.

Carga un Excel con los datos financieros de los negocios y la aplicación calcula
automáticamente:

- Endeudamiento, cobertura, margen bruto, liquidez y utilidad neta.
- Clasificación de riesgo (bajo / medio / alto).
- Viabilidad (viable / viable con condiciones / no viable).
- **Diagnóstico explicado indicador por indicador**, con semáforo (🟢🟠🔴) y una
  conclusión y recomendación comercial redactadas automáticamente.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Luego abre el enlace que aparece en la terminal (normalmente `http://localhost:8501`).

## Estructura del proyecto

```
FinanData_AI/
│
├── app.py                          # Aplicación Streamlit
├── requirements.txt                # Librerías necesarias
├── README.md
└── datos/
    └── ejemplo_100_negocios.xlsx   # Archivo de ejemplo para probar el dashboard
```

## Columnas esperadas en el Excel

El archivo es flexible con los nombres de columna (acepta variaciones en español),
pero idealmente debe incluir:

| Columna | Descripción |
|---|---|
| `Cliente` | Nombre del negocio |
| `Ciudad`, `Actividad_Economica` | Datos descriptivos |
| `Ventas_Mensuales` | Ventas mensuales |
| `Costo_Ventas`, `Gastos_Operativos`, `Gastos_Financieros` | Costos y gastos |
| `Activos_Corrientes`, `Pasivos_Corrientes` | Para liquidez |
| `Activos_Totales`, `Pasivos_Totales` | Para endeudamiento |
| `Cuota_Mensual_Credito` | Para cobertura |
| `Dias_Mora_Max`, `Historial_Pagos` | Para clasificación de riesgo |

## Despliegue

Ver los pasos de publicación en GitHub + Streamlit Cloud en la conversación del proyecto
o en la documentación de [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud).
