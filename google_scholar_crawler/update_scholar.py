import requests
import json
import os
import logging
import sys
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def get_scholar_data_serpapi(scholar_id, api_key):
    """使用 SerpAPI 获取 Google Scholar 数据并转换为原有格式"""
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google_scholar_author",
        "author_id": scholar_id,
        "api_key": api_key,
        "hl": "en"
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        serpapi_data = response.json()
        
        # 转换为原有格式
        author_data = {
            "container_type": "Author",
            "filled": [
                "basics",
                "publications", 
                "indices",
                "counts"
            ],
            "scholar_id": scholar_id,
            "source": "AUTHOR_PROFILE_PAGE",
            "name": serpapi_data.get("author", {}).get("name", ""),
            "url_picture": "",  # SerpAPI 不提供头像URL
            "affiliation": serpapi_data.get("author", {}).get("affiliations", ""),
            "interests": [],  # SerpAPI 不提供研究兴趣
            "email_domain": "",  # SerpAPI 不提供邮箱
            "homepage": "",  # SerpAPI 不提供主页
            "citedby": serpapi_data.get("cited_by", {}).get("table", [{}])[0].get("citations", {}).get("all", 0),
            "publications": [],
            "citedby5y": serpapi_data.get("cited_by", {}).get("table", [{}])[1].get("citations", {}).get("last_5_years", 0),
            "hindex": serpapi_data.get("cited_by", {}).get("table", [{}])[2].get("h_index", {}).get("all", 0),
            "hindex5y": serpapi_data.get("cited_by", {}).get("table", [{}])[3].get("h_index", {}).get("last_5_years", 0),
            "i10index": serpapi_data.get("cited_by", {}).get("table", [{}])[4].get("i10_index", {}).get("all", 0),
            "i10index5y": serpapi_data.get("cited_by", {}).get("table", [{}])[5].get("i10_index", {}).get("last_5_years", 0),
            "cites_per_year": {}
        }
        
        # 处理年度引用数据
        yearly_data = serpapi_data.get("cited_by", {}).get("graph", {}).get("citations", {})
        for year_data in yearly_data:
            year = year_data.get("year")
            citations = year_data.get("citations", 0)
            if year:
                author_data["cites_per_year"][str(year)] = citations
        
        # 处理出版物
        for i, pub in enumerate(serpapi_data.get("articles", [])):
            publication = {
                "container_type": "Publication",
                "source": "AUTHOR_PUBLICATION_ENTRY", 
                "bib": {
                    "title": pub.get("title", ""),
                    "pub_year": str(pub.get("year", "")),
                    "citation": pub.get("citation", "")
                },
                "filled": False,
                "author_pub_id": f"{scholar_id}:{pub.get('citation_id', f'pub{i}')}",
                "num_citations": pub.get("cited_by", {}).get("value", 0),
                "citedby_url": pub.get("cited_by", {}).get("link", ""),
                "cites_id": []
            }
            author_data["publications"].append(publication)
        
        return author_data
        
    except Exception as e:
        logger.error(f"SerpAPI request failed: {e}")
        return None

def main():
    try:
        SCHOLAR_ID = "e5ng8m0AAAAJ"  # 纯ID，不要带参数
        SERPAPI_KEY = os.getenv("SERPAPI_KEY")
        
        if not SERPAPI_KEY:
            logger.error("SERPAPI_KEY environment variable not set")
            sys.exit(1)

        logger.info(f"Fetching data for Google Scholar ID: {SCHOLAR_ID} using SerpAPI")

        # 获取作者数据
        author_data = get_scholar_data_serpapi(SCHOLAR_ID, SERPAPI_KEY)
        
        if not author_data:
            raise ValueError("Failed to fetch data from SerpAPI")

        # 保存数据
        os.makedirs("results", exist_ok=True)
        with open("results/gs_data.json", "w", encoding="utf-8") as f:
            json.dump(author_data, f, ensure_ascii=False, indent=2)

        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{author_data.get('citedby', 'N/A')}",
            "color": "9cf",
        }
        with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
            json.dump(shieldio_data, f, ensure_ascii=False)

        logger.info("Data successfully fetched and saved")
        
        # 打印关键信息用于验证
        logger.info(f"Name: {author_data.get('name')}")
        logger.info(f"Citations: {author_data.get('citedby')}")
        logger.info(f"5-Year Citations: {author_data.get('citedby5y')}")
        logger.info(f"H-index: {author_data.get('hindex')}")
        logger.info(f"Publications: {len(author_data.get('publications', []))}")

    except Exception as e:
        logger.error(f"Script failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
