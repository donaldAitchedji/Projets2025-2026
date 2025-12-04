# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Refactored scraper for Église catholique - glossaire

Features:
- Finds term links on the letter page, follows each term page to extract the definition
- Robust selectors with fallbacks, Unicode normalization
- Request timeout, headers, simple retry behavior
- CLI: --url, --output, --limit, --timeout, --sleep
- Logging and error handling

Usage example (test 3 terms):
    python extractiondeSiteCréationQuestionaire.py --limit 3

"""

from __future__ import annotations

import argparse
import logging
import time
import unicodedata
from typing import List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import csv
import json
import math
import random
import re
from urllib import robotparser


LOGGER = logging.getLogger(__name__)


def make_session(user_agent: str = None, timeout: int = 10) -> requests.Session:
    s = requests.Session()
    headers = {
        "User-Agent": user_agent
        or "Mozilla/5.0 (compatible; glossaire-scraper/1.0; +https://example.org)"
    }
    s.headers.update(headers)
    s.request_timeout = timeout  # informal attribute for default timeout usage below
    return s


def check_robots(base_url: str, user_agent: str = None) -> bool:
    """Check robots.txt for permission to fetch paths under base_url's host for /glossaire/"""
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        ua = user_agent or "*"
        return rp.can_fetch(ua, base_url)
    except Exception:
        # If robots.txt cannot be fetched, be conservative and allow, but caller should set politeness
        LOGGER.warning("Impossible de lire robots.txt (%s). Continuer avec précaution.", robots_url)
        return True


def retryable_get(session: requests.Session, url: str, timeout: int = 10, max_retries: int = 3) -> requests.Response:
    attempt = 0
    while True:
        try:
            return session.get(url, timeout=timeout)
        except requests.RequestException as e:
            attempt += 1
            if attempt > max_retries:
                raise
            backoff = (2 ** attempt) + random.random()
            LOGGER.debug("Retry %d for %s after %.1fs due to %s", attempt, url, backoff, e)
            time.sleep(backoff)


def fetch(session: requests.Session, url: str, timeout: Optional[int] = None) -> str:
    to = timeout or getattr(session, "request_timeout", 10)
    resp = retryable_get(session, url, timeout=to)
    resp.raise_for_status()
    return resp.text


def clean_text(s: str) -> str:
    if not s:
        return ""
    # Normalize unicode and collapse whitespace
    normalized = unicodedata.normalize("NFKC", s)
    collapsed = " ".join(normalized.split())
    return collapsed.strip()


def find_term_links(soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
    """Return list of (term_text, absolute_url) for links that look like glossaire entries."""
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        # ignore anchor-only or javascript links
        if href.startswith("#") or href.startswith("javascript:"):
            continue
        absolute = urljoin(base_url, href)
        # we only want links under /glossaire/ and not the letter navigation itself
        parsed = urlparse(absolute)
        if "/glossaire/" in parsed.path and "/glossaire/lettre/" not in parsed.path:
            term = clean_text(a.get_text(" ", strip=True))
            if not term:
                # fallback: use last part of path
                term = parsed.path.rstrip("/").split("/")[-1]
            key = (term, absolute)
            if key not in seen:
                seen.add(key)
                links.append((term, absolute))
    return links


def parse_term_page(soup: BeautifulSoup) -> Optional[str]:
    """Try several strategies to extract the term definition from a term page."""
    # Strategy 1: common WP-like container classes
    selectors = [
        "div.glossary-excerpt",
        "div.entry-content",
        "div#main-content",
        "main",
        "article",
        "div.content",
    ]
    for sel in selectors:
        container = soup.select_one(sel)
        if container:
            # get the first meaningful paragraph
            p = container.find("p")
            if p:
                return clean_text(p.get_text(" ", strip=True))
            # as fallback, return container text
            text = clean_text(container.get_text(" ", strip=True))
            if text:
                return text

    # Strategy 2: find H1 then next paragraphs until a stop marker
    h1 = soup.find(["h1", "h2"])  # some pages use h2 for title
    if h1:
        # gather following siblings until another heading or a share block
        parts = []
        for sib in h1.find_next_siblings():
            if sib.name and sib.name.startswith("h"):
                break
            if sib.name == "p":
                text = clean_text(sib.get_text(" ", strip=True))
                if text:
                    parts.append(text)
            # stop on common markers
            if sib.get_text() and "ÇA PEUT" in sib.get_text().upper():
                break
        if parts:
            return "\n\n".join(parts)

    # Strategy 3: first paragraph in body
    body_p = soup.find("p")
    if body_p:
        return clean_text(body_p.get_text(" ", strip=True))

    return None


def scrape(url: str, output_path: str, limit: Optional[int] = None, timeout: int = 10, sleep: float = 0.5) -> None:
    session = make_session(timeout=timeout)
    LOGGER.info("Fetching index page: %s", url)
    html = fetch(session, url, timeout=timeout)
    soup = BeautifulSoup(html, "html.parser")

    terms = find_term_links(soup, url)
    LOGGER.info("Found %d candidate links", len(terms))
    if limit:
        terms = terms[:limit]

    with open(output_path, "w", encoding="utf-8") as out:
        for i, (term, link) in enumerate(terms, start=1):
            try:
                LOGGER.info("[%d/%d] Fetching %s -> %s", i, len(terms), term, link)
                term_html = fetch(session, link, timeout=timeout)
                term_soup = BeautifulSoup(term_html, "html.parser")
                definition = parse_term_page(term_soup)
                if definition:
                    out.write(f"{term} : {definition}\n")
                else:
                    out.write(f"{term} : [definition non trouvée]\n")
            except requests.RequestException as e:
                LOGGER.warning("Échec récupération %s : %s", link, e)
                out.write(f"{term} : [erreur réseau]\n")
            except Exception as e:
                LOGGER.exception("Erreur inattendue pour %s", link)
                out.write(f"{term} : [erreur interne]\n")
            time.sleep(sleep)

    LOGGER.info("✅ Glossaire sauvegardé dans '%s'", output_path)


def scrape_letters(letters: List[str], base_url_template: str, output_path: str, limit_per_letter: Optional[int], timeout: int, sleep: float, resume: bool = False) -> None:
    """Scrape multiple letters (A-Z). base_url_template should include a placeholder for letter, e.g. '.../lettre/{}'"""
    # If resume and output exists, we'll append and skip terms already present.
    existing_terms = set()
    mode = "w"
    if resume:
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                for line in f:
                    if ":" in line:
                        existing_terms.add(line.split(":", 1)[0].strip())
            mode = "a"
            LOGGER.info("Resume activé: %d termes déjà présents seront ignorés", len(existing_terms))
        except FileNotFoundError:
            mode = "w"

    # We'll collect results in a list, then flush in the selected format at the end
    results = []
    for letter in letters:
        url = base_url_template.format(letter)
        LOGGER.info("--- Scraping lettre: %s (%s)", letter, url)
        try:
            # Respect robots.txt for the host
            if not check_robots(url, session_user_agent := None):
                LOGGER.warning("robots.txt empêche le scraping de %s — sauter.", url)
                continue
            html = fetch(make_session(timeout=timeout), url, timeout=timeout)
        except requests.RequestException as e:
            LOGGER.warning("Impossible de récupérer la lettre %s: %s", letter, e)
            continue

        soup = BeautifulSoup(html, "html.parser")
        terms = find_term_links(soup, url)
        # Filter out the list index itself and the letter nav duplicates
        filtered_terms = []
        for term, link in terms:
            # skip the generic glossaire index link
            if re.fullmatch(r"https?://[\w\.-]+/glossaire/?", link):
                continue
            # skip fragments and duplicates already handled
            filtered_terms.append((term, link))

        LOGGER.info("Found %d candidate links for %s (after filter)", len(filtered_terms), letter)
        if limit_per_letter:
            filtered_terms = filtered_terms[:limit_per_letter]

        for term, link in filtered_terms:
            if term in existing_terms:
                LOGGER.debug("Ignoré (déjà présent): %s", term)
                continue
            try:
                term_html = fetch(make_session(timeout=timeout), link, timeout=timeout)
                term_soup = BeautifulSoup(term_html, "html.parser")
                definition = parse_term_page(term_soup)
                results.append({"term": term, "definition": definition or "" , "url": link, "letter": letter})
                existing_terms.add(term)
            except requests.RequestException as e:
                LOGGER.warning("Échec récupération %s : %s", link, e)
                results.append({"term": term, "definition": "[erreur réseau]", "url": link, "letter": letter})
            except Exception:
                LOGGER.exception("Erreur inattendue pour %s", link)
                results.append({"term": term, "definition": "[erreur interne]", "url": link, "letter": letter})
            # politeness
            time.sleep(sleep)

    # flush results to output_path in a robust way
    try:
        fmt = ("txt")
        # if the file extension suggests format, use it
        if output_path.lower().endswith(".json"):
            fmt = "json"
        elif output_path.lower().endswith(".csv"):
            fmt = "csv"

        if fmt == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        elif fmt == "csv":
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["letter", "term", "definition", "url"])
                writer.writeheader()
                for r in results:
                    writer.writerow({"letter": r.get("letter"), "term": r.get("term"), "definition": r.get("definition"), "url": r.get("url")})
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                for r in results:
                    f.write(f"{r.get('term')} : {r.get('definition')} ({r.get('url')})\n")
    except OSError as e:
        LOGGER.error("Impossible d'écrire le fichier de sortie: %s", e)
        raise

    LOGGER.info("✅ Glossaire complet sauvegardé dans '%s' (%d entrées)", output_path, len(results))



def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape glossaire pages from eglise.catholique.fr")
    parser.add_argument("--url", default="https://eglise.catholique.fr/glossaire/lettre/a", help="URL de la page de lettre")
    parser.add_argument("--output", default="glossaire_A.txt", help="Fichier de sortie UTF-8")
    parser.add_argument("--limit", type=int, default=None, help="Limiter le nombre de termes (pour tests)")
    parser.add_argument("--letters", type=str, default=None, help="Lettres à scraper, séparées par des virgules (ex: a,b,c) ou 'a' pour A")
    parser.add_argument("--all-letters", action="store_true", help="Scrape toutes les lettres A..Z")
    parser.add_argument("--resume", action="store_true", help="Reprendre depuis le fichier de sortie existant (ignorer termes déjà extraits)")
    parser.add_argument("--format", type=str, choices=["txt", "csv", "json"], default=None, help="Format de sortie (déduit du nom de fichier si non précisé)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout HTTP en secondes")
    parser.add_argument("--sleep", type=float, default=0.4, help="Pause entre requêtes en secondes")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(levelname)s: %(message)s")

    try:
        if args.all_letters or args.letters:
            if args.all_letters:
                letters = [chr(c) for c in range(ord("a"), ord("z") + 1)]
            else:
                letters = [s.strip().lower() for s in args.letters.split(",") if s.strip()]
            base_template = "https://eglise.catholique.fr/glossaire/lettre/{}"
            scrape_letters(letters, base_template, args.output, limit_per_letter=args.limit, timeout=args.timeout, sleep=args.sleep, resume=args.resume)
        else:
            scrape(args.url, args.output, limit=args.limit, timeout=args.timeout, sleep=args.sleep)
    except requests.RequestException as e:
        LOGGER.error("Échec réseau général: %s", e)
    except OSError as e:
        LOGGER.error("Erreur fichier/IO: %s", e)


if __name__ == "__main__":
    main()
