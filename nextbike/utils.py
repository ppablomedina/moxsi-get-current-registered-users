from webdriver_manager.chrome          import ChromeDriverManager
from selenium.common.exceptions        import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by      import By
from datetime  import date, timedelta
from selenium  import webdriver
from mail      import get_code
from gcp.paths import num_months_back
import time, glob, os, pandas as pd


try: 
    creds = os.getenv("NEXTBIKE_CREDS")
    NEXTBIKE_USER = creds.split("\n")[0]
    NEXTBIKE_PASS = creds.split("\n")[1]
except:
    NEXTBIKE_USER  = "pmedina"
    NEXTBIKE_PASS  = "nPmse.52725"

REQUEST_TIMEOUT = 400 

def set_driver():    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    try:    
        service = Service(os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver"))
        driver = webdriver.Chrome(service=service, options=chrome_options)

    except: 
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    # ESTE es el que realmente usa urllib3
    driver.command_executor._client_config.timeout = REQUEST_TIMEOUT

    return driver, download_dir

def log_in_nextbike(driver, url):
    
    driver.get(url)

    driver.find_element(By.ID, "parameters[username]").send_keys(NEXTBIKE_USER)
    driver.find_element(By.ID, "parameters[password]").send_keys(NEXTBIKE_PASS)
    driver.find_element(By.ID, "login_post").click()

    time.sleep(3)
    
    verification_code = get_code()
    
    driver.find_element(By.ID, "parameters[otp_code]").send_keys(verification_code)
    driver.find_element(By.ID, "login_post").click() 

def get_dates():
    
    today = pd.Timestamp(date.today()) - pd.DateOffset(months=num_months_back - 1)
    
    last_day_prev_month = today.replace(day=1) - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)
     
    return (
        first_day_prev_month.strftime("%Y-%m-%d 00:00"),
        last_day_prev_month.strftime("%Y-%m-%d 23:59"),
        first_day_prev_month.strftime("%Y-%m-%d"),
        last_day_prev_month.strftime("%Y-%m-%d")
    )                              

def get_biweekly_dates():
    """Devuelve dos rangos de fechas (primera y segunda quincena) del mes anterior."""
    today = date.today() - pd.DateOffset(months=num_months_back - 1)
    last_day = today.replace(day=1) - timedelta(days=1)
    first_day = last_day.replace(day=1)
    mid_last = last_day.replace(day=15)
    mid_first = last_day.replace(day=16)

    biweekly_dates = [
        (
            first_day.strftime("%Y-%m-%d 00:00"),
            mid_last.strftime("%Y-%m-%d 23:59"),
            first_day.strftime("%Y-%m-%d"),
            mid_last.strftime("%Y-%m-%d"),
        ),
        (
            mid_first.strftime("%Y-%m-%d 00:00"),
            last_day.strftime("%Y-%m-%d 23:59"),
            mid_first.strftime("%Y-%m-%d"),
            last_day.strftime("%Y-%m-%d"),
        ),
    ]

    print("Rangos quincenales:")
    for i, rango in enumerate(biweekly_dates, start=1):
        print(f"Quincena {i}: {rango}")

    return biweekly_dates

def safe_get(driver, url, timeout=REQUEST_TIMEOUT):
    driver.set_page_load_timeout(timeout)
    try: driver.get(url)
    except TimeoutException:
        if url.endswith("410"): return
        raise Exception(f"La página {url} tardó más de {timeout} segundos en cargar.")

def download_from_nextbike(driver, download_dir, url, date_override=None):

    if url.endswith("410"): timeout = 5
    else:                   timeout = REQUEST_TIMEOUT
        
    safe_get(driver, url, timeout)

    if date_override: start_time, end_time, start_date, end_date = date_override
    else:             start_time, end_time, start_date, end_date = get_dates()

    print(f"start_time: {start_time}")
    print(f"end_time:   {end_time}")
    print(f"start_date: {start_date}")
    print(f"end_date:   {end_date}")    
    
    start_cron = time.time()
    
    if url.endswith(("639", "641", "640")):
        driver.find_element(By.ID, "parameters[start_time]").send_keys(start_time)
        driver.find_element(By.ID, "parameters[end_time]").send_keys(end_time)

    elif url.endswith(("730", "129", "525")):
        driver.find_element(By.ID, "parameters[start_date]").send_keys(start_date)
        driver.find_element(By.ID, "parameters[end_date]").send_keys(end_date)

    if not url.endswith("424"):
        if url.endswith("410"): time.sleep(20)
        if num_months_back >= 3: 
            try:    driver.find_element(By.ID, "parameters[execute_on_lendings_archive]").click()
            except: pass
        driver.find_element(By.ID, "parameters[export_csv]").click()  
        driver.find_element(By.ID, "queries_view_get").click()

    file_path = None
    for _ in range(320):
        files = glob.glob(os.path.join(download_dir, "*.csv"))
        new_files = [f for f in files if os.path.getmtime(f) > start_cron]

        if new_files:
            file_path = max(new_files, key=os.path.getmtime)
            break

        time.sleep(1)

    if not file_path: raise RuntimeError("No se encontró ningún CSV generado por Nextbike")
    try:               return pd.read_csv(file_path, sep='\t', dtype={'mobile': str})
    except ValueError: return pd.read_csv(file_path, sep='\t')

def run_nextbike_etl(url):
    driver, download_dir = set_driver()
    try:
        log_in_nextbike(driver, url)
        df = download_from_nextbike(driver, download_dir, url)
        return df
    finally: driver.quit()
