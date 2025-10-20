from scholarly import scholarly
import json
from datetime import datetime
import os
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # 直接硬编码你的 Google Scholar ID（替换 YOUR_SCHOLAR_ID）
        SCHOLAR_ID = "e5ng8m0AAAAJ"  # 例如 "e5ng8m0AAAAJ"
        if not SCHOLAR_ID:
            raise ValueError("Google Scholar ID 未设置")

        logger.info(f"Fetching data for Google Scholar ID: {SCHOLAR_ID}")

        # 获取作者数据
        author = scholarly.search_author_id(SCHOLAR_ID)
        scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

        # 保存数据（其余代码不变）
        os.makedirs("results", exist_ok=True)
        with open("results/gs_data.json", "w", encoding="utf-8") as f:
            json.dump(author, f, ensure_ascii=False, indent=2)

        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{author.get('citedby', 'N/A')}",
            "color": "9cf",
        }
        with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
            json.dump(shieldio_data, f, ensure_ascii=False)

    except Exception as e:
        logger.error(f"Script failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
