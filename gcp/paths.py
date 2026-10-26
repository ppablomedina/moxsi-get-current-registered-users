from dates import prev_month_year, prev_month_str, crrnt_year, crrnt_full_date


PROJECT_ID         = 'bigdata-fase2'
BUCKET_NAME        = "sagulpa-datalake"
PATH_DATALAKE_DOCS = "moxsi/documents"

def monthly_path(dataset, ext): return f"{PATH_DATALAKE_DOCS}/{prev_month_year}/{dataset}/{prev_month_str}.{ext}"
def daily_path(dataset, ext):   return f"{PATH_DATALAKE_DOCS}/{crrnt_year}/{dataset}/{crrnt_full_date}.{ext}"

path_incidencias              = monthly_path("moxsi.incidencias",                            ext="xlsx")
path_inventario               = monthly_path("moxsi.inventario",                             ext="csv")
path_repuestos                = monthly_path("moxsi.repuestos",                              ext="xlsx")
path_revisiones               = monthly_path("moxsi.revisiones",                             ext="xlsx")
path_almacen                  = monthly_path("moxsi.almacen",                                ext="xlsx")
path_abonos                   = monthly_path("nextbike.abonos",                              ext="csv")
path_clientes_detalles        = monthly_path("nextbike.clientes-detalles",                   ext="csv")
path_alquileres               = monthly_path("nextbike.alquileres",                          ext="csv")
path_transactions             = monthly_path("nextbike.transactions",                        ext="csv")
path_estaciones               =   daily_path("nextbike.estaciones",                          ext="csv")
path_vehiculos_anclados       =   daily_path("nextbike.vehiculos-anclados",                  ext="csv")
path_vehiculos_coords         =   daily_path("nextbike.vehiculos-coords",                    ext="csv")
path_clientes_registrados     =   daily_path("nextbike.clientes-registrados",                ext="csv")
path_clientes_ultimo_alquiler =   daily_path("nextbike.clientes-ult-alquiler-suscripciones", ext="csv")
