import os
import uvicorn
from fastapi import FastAPI
from random import randint
from datetime import datetime
from dotenv import load_dotenv
from ProxiesGrabber import ProxiesGrabber
from BucketConnector import BucketConnector
from fastapi.middleware.cors import CORSMiddleware
from facebook_page_scraper import Facebook_scraper


load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_ORIGIN_ALL")],
    allow_credentials=True,
    allow_methods=[os.environ.get("CORS_ALLOW_METHODS")],
    allow_headers=[os.environ.get("CORS_ALLOW_HEADERS")],
)


def get_page_data(page_id, browser_proxy, days_count):
    page_name = page_id
    browser = "chrome"
    if browser_proxy:
        proxy = browser_proxy
    timeout = 600  # 600 seconds
    headless = True
    if browser_proxy:
        scrapper_obj = Facebook_scraper(
            page_name=page_name,
            browser=browser,
            proxy=proxy,
            timeout=timeout,
            headless=headless,
            days_count=days_count,
        )
    else:
        scrapper_obj = Facebook_scraper(
            page_name=page_name,
            browser=browser,
            timeout=timeout,
            headless=headless,
            days_count=days_count,
        )

    json_data = scrapper_obj.scrap_to_json()
    return json_data


@app.get("/")
def read_root():
    return {"api_version": "1.0"}


@app.get("/fb_page")
def get_fb_page_data(
    page_id: str,
    days_count: str,
):
    start_time = datetime.now()
    raw_proxies_list = ProxiesGrabber.get_proxies_list(
        token=os.environ.get("WEBSHARE_TOKEN"),
        proxies_url=os.environ.get("LIST_PROXIES_URL"),
    )
    proxies_list = [aa.get("http").split("/")[-2] for aa in raw_proxies_list]

    random_num = randint(0, len(proxies_list) - 1)
    random_proxy = proxies_list[random_num]
    all_posts = get_page_data(
        page_id=page_id,
        browser_proxy=random_proxy if "None" not in random_proxy else False,
        days_count=int(days_count),
    )

    print("[*]  Dumping Posts Data to S3!")
    BucketConnector.store_data(
        data=all_posts,
        bucket_name="fb-page-bucket",
        category_name="Posts",
        folder_name=page_id,
    )
    print("[+]  Posts Data Successfully dumped to S3!")
    end_time = datetime.now()
    total_time = str(end_time - start_time)

    return {"status": "Success", "total_time": total_time}


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=80,
        reload=True
        if os.environ.get(
            "ENVIRONMENT",
        )
        == "DEVELOPMENT"
        else False,
    )
