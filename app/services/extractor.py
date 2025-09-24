import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

# Map of popular job boards and their job description container selectors
SITE_SELECTORS = {
    "indeed.com": ".jobsearch-jobDescriptionText",
    "glassdoor.com": ".jobDescriptionContent",
    "linkedin.com": [
        ".description__text",       # older LinkedIn selector
        ".show-more-less-html__markup"  # newer LinkedIn selector
    ],
    "monster.com": ".job-description",
    "ziprecruiter.com": ".job_description",
}


def clean_text(text: str) -> str:
    """Clean up whitespace and remove junk lines."""
    lines = text.splitlines()
    cleaned = []
    blacklist = ["apply now", "sign up", "login", "create account", "subscribe"]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(line) < 8:  # allow shorter valid lines (e.g. "C++", "3+ yrs")
            continue
        if any(bad in line.lower() for bad in blacklist):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def extract_text_from_url(url: str) -> str:
    """Extract job description text from a job posting URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove obvious junk tags
    for tag in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
        tag.decompose()

    hostname = urlparse(url).hostname or ""

    # Step 1: Site-specific selector(s)
    for site, selector in SITE_SELECTORS.items():
        if site in hostname:
            if isinstance(selector, list):  # multiple possible selectors
                for sel in selector:
                    el = soup.select_one(sel)
                    if el:
                        print(f"[INFO] Extracted using site-specific selector ({site})")
                        text = el.get_text(separator="\n", strip=True)
                        return clean_text(text)
            else:
                el = soup.select_one(selector)
                if el:
                    print(f"[INFO] Extracted using site-specific selector ({site})")
                    text = el.get_text(separator="\n", strip=True)
                    return clean_text(text)

    # Step 2: Heuristic fallback → largest <div>/<section> with many <p>/<li>
    candidates = []
    for container in soup.find_all(["div", "section"], recursive=True):
        texts = container.find_all(["p", "li"])
        joined = " ".join([t.get_text(" ", strip=True) for t in texts])
        length = len(joined.split())
        if length > 50:  # at least some real text
            candidates.append((length, joined))

    if candidates:
        candidates.sort(reverse=True, key=lambda x: x[0])
        print("[INFO] Extracted using heuristic fallback (largest div/section)")
        return clean_text(candidates[0][1])

    # Step 3: Fallback → all visible text
    print("[WARN] Falling back to all visible text")
    all_text = soup.get_text(separator="\n", strip=True)
    return clean_text(all_text)
