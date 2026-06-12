from pathlib import Path
import base64
import re

import streamlit as st


POST_PATH = Path("site/posts/why-cros-need-more-than-an-llm-on-revenue-data.md")
LOGO_PATH = Path("site/terret_logo.png")


def split_frontmatter(markdown_text: str) -> tuple[str, str]:
    if not markdown_text.startswith("---"):
        return "", markdown_text

    parts = markdown_text.split("---", 2)
    if len(parts) < 3:
        return "", markdown_text

    return parts[1].strip(), parts[2].strip()


def get_frontmatter_value(frontmatter: str, field_name: str) -> str:
    prefix = f"{field_name}:"
    for line in frontmatter.splitlines():
        if line.startswith(prefix):
            return line.replace(prefix, "", 1).strip().strip('"')
    return ""


def get_frontmatter_list(frontmatter: str, field_name: str) -> list[str]:
    lines = frontmatter.splitlines()
    values = []
    inside_list = False

    for line in lines:
        if line.startswith(f"{field_name}:"):
            inside_list = True
            continue

        if inside_list:
            if line.startswith("  - "):
                values.append(line.replace("  - ", "", 1).strip())
            elif line and not line.startswith(" "):
                break

    return values


def estimate_reading_time(markdown_body: str) -> str:
    words = re.findall(r"\w+", markdown_body)
    minutes = max(1, round(len(words) / 220))
    return f"{minutes} min read"

def remove_duplicate_article_title(markdown_body: str, page_title: str) -> str:
    lines = markdown_body.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)

    if lines and lines[0].strip().startswith("#"):
        first_heading = lines[0].strip().lstrip("#").strip()
        if first_heading == page_title:
            return "\n".join(lines[1:]).lstrip()

    return markdown_body

def image_to_data_uri(image_path: Path) -> str:
    if not image_path.exists():
        return ""

    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


st.set_page_config(
    page_title="Terret Blog Preview",
    page_icon="🟣",
    layout="wide",
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        max-width: 980px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .site-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 1rem;
        margin-bottom: 3rem;
        font-size: 0.95rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        font-size: 1.25rem;
    }

    .brand-logo {
        width: 28px;
        height: 28px;
        object-fit: contain;
    }

    .nav-links {
        color: #6b7280;
    }

    .eyebrow {
        color: #6d28d9;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-size: 0.78rem;
        margin-bottom: 1rem;
    }

    .blog-title {
        font-size: 3rem;
        line-height: 1.05;
        letter-spacing: -0.05em;
        font-weight: 850;
        margin-bottom: 1rem;
    }

    .dek {
        font-size: 1.25rem;
        line-height: 1.6;
        color: #4b5563;
        margin-bottom: 1.25rem;
    }

    .byline {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .tag-row {
        margin-top: 0.75rem;
        margin-bottom: 2.5rem;
    }

    .tag {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        border: 1px solid #e5e7eb;
        border-radius: 999px;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        color: #374151;
        font-size: 0.85rem;
        background: #fafafa;
    }

    .article-card {
        border-top: 1px solid #e5e7eb;
        padding-top: 2rem;
    }

    .article-card h1 {
        display: none;
    }

    .article-card h2 {
        font-size: 1.65rem;
        letter-spacing: -0.03em;
        margin-top: 2.2rem;
        margin-bottom: 0.7rem;
    }

    .article-card p {
        font-size: 1.08rem;
        line-height: 1.8;
        color: #1f2937;
    }

    .cms-note {
        margin-top: 3rem;
        padding: 1rem;
        border-radius: 0.75rem;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if not POST_PATH.exists():
    st.error("Published post not found. Approve the draft, then run `python src/publish.py`.")
    st.stop()

markdown_text = POST_PATH.read_text(encoding="utf-8")
frontmatter, body = split_frontmatter(markdown_text)

title = get_frontmatter_value(frontmatter, "title") or "Untitled"
body = remove_duplicate_article_title(body, title)

meta_description = get_frontmatter_value(frontmatter, "meta_description")
author = get_frontmatter_value(frontmatter, "author") or "Terret"
published_at = get_frontmatter_value(frontmatter, "published_at_utc")
slug = get_frontmatter_value(frontmatter, "slug")
tags = get_frontmatter_list(frontmatter, "tags")

reading_time = estimate_reading_time(body)

logo_data_uri = image_to_data_uri(LOGO_PATH)
logo_html = (
    f'<img class="brand-logo" src="{logo_data_uri}" alt="Terret logo" />'
    if logo_data_uri
    else ""
)

st.markdown(
    f"""
    <div class="site-nav">
        <div class="brand">{logo_html}<span>Terret</span></div>
        <div class="nav-links">Revenue AI · Blog · Local Preview</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Revenue AI</div>', unsafe_allow_html=True)
st.markdown(f'<div class="blog-title">{title}</div>', unsafe_allow_html=True)

if meta_description:
    st.markdown(f'<div class="dek">{meta_description}</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="byline">By {author} · {reading_time}</div>',
    unsafe_allow_html=True,
)

if tags:
    tag_html = "".join(f'<span class="tag">{tag}</span>' for tag in tags)
    st.markdown(f'<div class="tag-row">{tag_html}</div>', unsafe_allow_html=True)

st.markdown('<div class="article-card">', unsafe_allow_html=True)
st.markdown(body)
st.markdown("</div>", unsafe_allow_html=True)

with st.expander("CMS metadata written by publish step"):
    st.code(frontmatter, language="yaml")

st.markdown(
    f"""
    <div class="cms-note">
        Local published-output preview. The publish script writes structured Markdown at
        <code>{POST_PATH}</code>. In production, these same fields would map to a CMS API:
        title, slug, meta description, author, tags, source IDs, headings, and body.
    </div>
    """,
    unsafe_allow_html=True,
)