from flask    import Flask, request
from nextbike import set_driver, log_in_nextbike, download_customers_details
from datetime import date
from mail     import send_email


def entry_point(req):

    today_date = date.today().strftime("%Y-%m-%d")

    driver, download_dir = set_driver()
    
    log_in_nextbike(driver)

    df = download_customers_details(driver, download_dir, today_date)

    driver.quit()

    n_active_users = df[df['active'] == 1].shape[0]

    send_email(
        to="pmedina",
        subject=f"ℹ️ Usuarios registrados Moxsi ({today_date})",
        body=f"Número de usuarios registrados en Moxsi a día {today_date}: {n_active_users} usuarios"
    )

    return "ETL ejecutado correctamente\n", 200


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def run():
    return entry_point(request)

if __name__ == "__main__":
    entry_point(None)
