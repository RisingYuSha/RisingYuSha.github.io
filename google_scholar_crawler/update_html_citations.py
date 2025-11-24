import json
import re

# 1. 读取爬虫数据
with open("results/gs_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 构建 标题 → 引用数映射（忽略大小写），处理 None 值
citation_map = {}
for pub in data.get("publications", []):
    title = pub["bib"]["title"].strip().lower()
    num_citations = pub.get("num_citations", 0)
    # 处理 None 值，将其转换为 0
    if num_citations is None:
        num_citations = 0
    citation_map[title] = int(num_citations)

file_path = "../_pages/includes/publications.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 3. 只处理 ### 📝 Papers 段落
match = re.search(r"(### 📝 Papers:.*?)(?=\n### |\Z)", content, flags=re.S)
if match:
    papers_section = match.group(1)

    # 遍历 JSON 数据
    for title, cites in citation_map.items():
        title_pattern = re.escape(title)

        def repl(m):
            text_after = m.group(2) or ""
            badge_pattern = r'<img src="https://img.shields.io/badge/Citations-\d+-blue" alt="Citations">'
            badge_html_plain = f'<a href="https://scholar.google.com.hk/citations?user=e5ng8m0AAAAJ" target="_blank"><img src="https://img.shields.io/badge/Citations-{cites}-blue" alt="Citations"></a>'

            if re.search(badge_pattern, text_after):
                # 更新已有 Badge 数字
                text_after = re.sub(r'(Citations-)\d+(-blue)', rf'\g<1>{cites}\g<2>', text_after)

            else:
                # ① 有图片（非 Citation Badge）
                if re.search(r'<img(?! src="https://img\.shields\.io/badge/Citations)', text_after):
                    text_after = badge_html_plain + " " + text_after
                # ② Paper + Code → 插在 Code后并加" | "
                elif re.search(r'\| \[Paper\]', text_after) and re.search(r'\| \[Code\]', text_after):
                    text_after = re.sub(
                        r'(\| \[Code\]\([^)]+\))',
                        rf'\1 | {badge_html_plain}',
                        text_after,
                        count=1
                    )
                # ③ 只有 Paper → 插在 Paper后并加" | "
                elif re.search(r'\| \[Paper\]', text_after):
                    text_after = re.sub(
                        r'(\| \[Paper\]\([^)]+\))',
                        rf'\1 | {badge_html_plain}',
                        text_after,
                        count=1
                    )
                # ④ 默认 → 标题后
                else:
                    text_after = badge_html_plain + " " + text_after

            return m.group(1) + text_after

        papers_section = re.sub(rf'({title_pattern})(.*)', repl, papers_section, flags=re.I)

    content = content.replace(match.group(1), papers_section)

# 保存
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已更新 Papers 段落中的 Citation Badge（链接模式下带分隔符）")
