---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<span class='anchor' id='about-me'></span>
{% capture publications_content %}
{% include_relative includes/publications.md %}
{% endcapture %}
{% assign paper_count_single_quotes = publications_content | split: "class='paper-box-text'" | size | minus: 1 %}
{% assign paper_count_double_quotes = publications_content | split: 'class="paper-box-text"' | size | minus: 1 %}
{% assign publication_count = paper_count_single_quotes | plus: paper_count_double_quotes %}

{% include_relative includes/intro.md %}

{% include_relative includes/news.md %}

{% include_relative includes/researches.md %}

{% include_relative includes/experiences.md %}

{% include_relative includes/educations.md %}

{{ publications_content }}

{% include_relative includes/projects.md %}

{% include_relative includes/honers.md %}

{% include_relative includes/talks.md %}


<script>
document.addEventListener("DOMContentLoaded", function() {
    const papers = document.querySelectorAll(".paper-box-text"); 
    let num = 1; // 从1开始
    papers.forEach(paper => {
        // 在第一个子元素前插入序号（数字和一个点）
        const firstChild = paper.firstElementChild;
        if (firstChild) {
            // 创建一个 span 来显示编号
            const numSpan = document.createElement("span");
            numSpan.textContent = num + ". ";
            numSpan.style.fontWeight = "bold";
            firstChild.insertAdjacentElement("afterbegin", numSpan);
            num++;
        }
    });
});
</script>




