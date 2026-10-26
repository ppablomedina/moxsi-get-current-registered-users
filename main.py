from flask          import Flask, request
from moxsi_api      import download_stations_moxsi
from nextbike.utils import set_driver, download_from_nextbike, log_in_nextbike, get_biweekly_dates
from nextbike.paths import *
from gcp.utils      import upload_to_gcp
from gcp.paths      import *
from gs.utils       import download_from_gs_excel, download_from_gs_single_sheet
from gs.paths       import *


def entry_point(req):

    dic = {}

    # Crear driver y carpeta de descargas SOLO para esta ejecución
    driver, download_dir = set_driver()

    try:
        # 1) Login en Nextbike
        log_in_nextbike(driver, link_queries)

        # 2) Descargas que quieras hacer en esta ejecución
        # dic[path_abonos]                   = download_from_nextbike(driver, download_dir, link_abonos)
        # print(f"✅ Abonos")
        # dic[path_vehiculos_anclados]       = download_from_nextbike(driver, download_dir, link_vehiculos_anclados)
        # print(f"✅ Vehículos anclados")
        # dic[path_vehiculos_coords]         = download_from_nextbike(driver, download_dir, link_vehiculos_coords)
        # print(f"✅ Vehículos coords")
        # dic[path_clientes_registrados]     = download_from_nextbike(driver, download_dir, link_clientes_registrados)
        # print(f"✅ Clientes registrados")
        dic[path_clientes_detalles]        = download_from_nextbike(driver, download_dir, link_clientes_detalles)
        print(f"✅ Clientes detalles")
        # dic[path_clientes_ultimo_alquiler] = download_from_nextbike(driver, download_dir, link_clientes_ultimo_alquiler)
        # print(f"✅ Clientes último alquiler")
        # dic[path_alquileres]               = download_from_nextbike(driver, download_dir, link_alquileres)
        # print(f"✅ Alquileres")

        # # Recaudación: dos descargas quincenales combinadas en un único DataFrame
        # q1, q2 = get_biweekly_dates()
        # df_rec1 = download_from_nextbike(driver, download_dir, link_transactions, date_override=q1)
        # df_rec2 = download_from_nextbike(driver, download_dir, link_transactions, date_override=q2)
        # dic[path_transactions] = pd.concat([df_rec1, df_rec2], ignore_index=True)

        # dic[path_inventario]               = download_from_gs_single_sheet(link_inventario)
        # dic[path_revisiones]               = download_from_gs_excel(link_revisiones)
        # dic[path_repuestos]                = download_from_gs_excel(link_repuestos)
        # dic[path_incidencias]              = download_from_gs_excel(link_incidencias)
        # dic[path_estaciones]               = download_stations_moxsi()

        # 3) Subir todo a GCP
        upload_to_gcp(dic)

    finally: driver.quit()

    return "ETL ejecutado correctamente\n", 200


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def run():
    return entry_point(request)

if __name__ == "__main__":
    entry_point(None)
