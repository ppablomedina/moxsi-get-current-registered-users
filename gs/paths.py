import os


# gs_links = os.getenv("GS_LINKS")
gs_links = "https://docs.google.com/spreadsheets/d/1vR6_0pA_3rbWeWCxtM-ohkNpxzoVW0i0rqwuQbxhDJQ/edit?gid=0#gid=0\nhttps://docs.google.com/spreadsheets/d/1-8FirPp5tr0Coiwe3BgR0f_5i0ypjiQp9C9KwCY_zpM/edit?gid=0#gid=0\nhttps://docs.google.com/spreadsheets/d/1XHvI6PcBTOXyfSIVvqNNaAv51u5JOPXbXUJ-CuzTwIg/edit?gid=1869648345#gid=1869648345\nhttps://docs.google.com/spreadsheets/d/1Z6C4g_Ke8pejjSDZHw9ENkBV5ho6JaRY7yhKvDaGOkw/edit?gid=1452533839#gid=1452533839\nhttps://docs.google.com/spreadsheets/d/1JDEAfGl4danYesLPRm2bogu-REnbpD3tbg7Ccn54nvI/edit?gid=303663857#gid=303663857"

link_revisiones       = gs_links.split("\n")[0]
link_inventario       = gs_links.split("\n")[1]
link_repuestos        = gs_links.split("\n")[2]
link_incidencias_2025 = gs_links.split("\n")[3]
link_incidencias      = gs_links.split("\n")[4] # 2026
