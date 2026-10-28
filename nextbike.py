from webdriver_manager.chrome          import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by      import By
from selenium                          import webdriver
from mail                              import get_code
from secret_manager                    import get_nextbike_creds
import time, glob, os, pandas as pd


link_queries           = "https://my.nextbike.net/office/queries/view/"

def set_driver():    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Comentar para pruebas en local
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

    driver.command_executor._client_config.timeout = 400

    return driver, download_dir

def log_in_nextbike(driver):

    NEXTBIKE_USER, NEXTBIKE_PASS = get_nextbike_creds()
    
    driver.get(link_queries)

    driver.find_element(By.ID, "parameters[username]").send_keys(NEXTBIKE_USER)
    driver.find_element(By.ID, "parameters[password]").send_keys(NEXTBIKE_PASS)
    driver.find_element(By.ID, "login_post").click()

    time.sleep(3)
    
    verification_code = get_code()
    
    driver.find_element(By.ID, "parameters[otp_code]").send_keys(verification_code)
    driver.find_element(By.ID, "login_post").click() 

def download_customers_details(driver, download_dir, today_date):
        
    driver.get(link_queries + "730")     
    
    start_cron = time.time()
    
    driver.find_element(By.ID, "parameters[start_date]").send_keys("2018-03-06")
    driver.find_element(By.ID, "parameters[end_date]").send_keys(today_date)

    driver.find_element(By.ID, "parameters[export_csv]").click()
    driver.find_element(By.ID, "queries_view_get").click()

    file_path = None
    for _ in range(120):
        files = glob.glob(os.path.join(download_dir, "*.csv"))
        new_files = [f for f in files if os.path.getmtime(f) > start_cron]

        if new_files:
            file_path = max(new_files, key=os.path.getmtime)
            break

        time.sleep(1)
    
    return pd.read_csv(file_path, sep='\t', dtype={'ID card number': str, 'mobile': str})
