from gcp.secret_manager import get_moxsi_gs_links


gs_links = get_moxsi_gs_links()

link_revisiones       = gs_links["revisiones"]
link_inventario       = gs_links["inventario"]
link_repuestos        = gs_links["repuestos"]
link_almacen          = gs_links["almacen"]
link_incidencias_2025 = gs_links["incidencias_2025"]
link_incidencias_2026 = gs_links["incidencias_2026"]
