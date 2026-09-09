import pandas as pd


BUCKET_NAME        = "sagulpa-datalake"
PATH_DATALAKE_DOCS = "moxsi/documents"

# Fechas base
now = pd.Timestamp.now() - pd.DateOffset(months=1)

crrnt_full_date = now.strftime("%Y%m%d")          # p.ej. 20251101
crrnt_year      = now.year

prev_month_ts   = now - pd.DateOffset(months=1)
prev_month_year = prev_month_ts.year
prev_month_str  = prev_month_ts.strftime("%Y%m")  # p.ej. 202510
num_months_back = (now.year - prev_month_ts.year) * 12 + (now.month - prev_month_ts.month)
print(prev_month_str)

# Helpers para construir rutas
def monthly_path(dataset, ext): return f"{PATH_DATALAKE_DOCS}/{prev_month_year}/{dataset}/{prev_month_str}.{ext}"
def daily_path(dataset, ext):   return f"{PATH_DATALAKE_DOCS}/{crrnt_year}/{dataset}/{crrnt_full_date}.{ext}"

# Rutas
path_incidencias              = monthly_path("moxsi.incidencias",                            ext="xlsx")
path_inventario               = monthly_path("moxsi.inventario",                             ext="csv")
path_repuestos                = monthly_path("moxsi.repuestos",                              ext="xlsx")
path_revisiones               = monthly_path("moxsi.revisiones",                             ext="xlsx")
path_abonos                   = monthly_path("nextbike.abonos",                              ext="csv")
path_clientes_detalles        = monthly_path("nextbike.clientes-detalles",                   ext="csv")
path_alquileres               = monthly_path("nextbike.alquileres",                          ext="csv")
path_transactions             = monthly_path("nextbike.transactions",                        ext="csv")
path_estaciones               =   daily_path("moxsi.estaciones",                             ext="csv")
path_vehiculos_anclados       =   daily_path("nextbike.vehiculos-anclados",                  ext="csv")
path_vehiculos_coords         =   daily_path("nextbike.vehiculos-coords",                    ext="csv")
path_clientes_registrados     =   daily_path("nextbike.clientes-registrados",                ext="csv")
path_clientes_ultimo_alquiler =   daily_path("nextbike.clientes-ult-alquiler-suscripciones", ext="csv")
