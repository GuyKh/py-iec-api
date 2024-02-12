
HEADERS_NO_AUTH = {
    "Content-Type": "application/json; charset=utf-8",
    "X-Iec-Idt": "1",
    "X-Iec-Webview": "1",
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.iec.co.il",
    "authority": "iecapi.iec.co.il",
    "referer": "https://www.iec.co.il/",
    "Dnt": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Recaptchtoken": "03AFcWeA5xe43I00jSCrH-aX7wMuQb6WRW2xevCwVO11LLqPWBuwsn0FeIv_LcQ"
                     "-2lCIJuKckwJaLfMQ_JXyQR4jRLpS9ebXASA8l16w319BDh9HNUOZ50UC6dp7n9iaqZhNgfCJNu4qDWHGNQaLT5xF"
                     "-dNQRQyNbycDswmXa9-LnfMU5bMnXABM99S7-3"
                     "-1VsJXlXJPass7lvybsAzggAMpODUm5FqHjWDZhQxiG7Q6PpbA1RZaj_s6wfwaN5_n5lujhLbPy12giJSMC8FglinwLFtPIYYhvOb5lwrnNk_hpdCzitwLW8aNfSMcwV74ZQZsW4hbtFu7aVtEeDoZJ3Q4Wr9kj_XhW0X5HRYGqj5P7QbZlu1_LNDBkv4Yxk43WcA-rB9Ms4M0cpCDyPvagHRvtNXyPytqtPo8UP3OI64ztFLCG-EJ1LWSiErwAnSNrpiYuOGDAl9XBImp5JhZPfOTvhg4iA4UFd3MSFDF9ddlOWeWPJfmOuGOyMUnEyn67KY84GCWbQOZBJrGO5dTqaBqxojyKC7iVkX-5EivLhXQVmFRsoe6GxgI5nnLKfl_deRTfmoGxSrlWTUBsUzfEmGbqIqQAw_9kFakyNbS9xugsZPfy8S8hZ7o8"
}

HEADERS_WITH_AUTH = HEADERS_NO_AUTH.copy()  # Make a copy of the original dictionary
HEADERS_WITH_AUTH["Authorization"] = "YourAuthorizationTokenHere"

GET_CONSUMER_URL = "https://iecapi.iec.co.il/api/Consumer"