#!/usr/bin/env python3
"""
Velix - Trouveur de pseudos sur les réseaux sociaux
Version 2.1 — par Bachir
"""

import sys
import os
import re
import csv
import json
import signal
import datetime
import threading
import webbrowser
import requests
from time import monotonic
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from requests_futures.sessions import FuturesSession
from concurrent.futures import TimeoutError as FuturesTimeoutError
from colorama import init as colorama_init, Fore, Style
from importlib.resources import files

colorama_init(autoreset=True)

__version__ = "3.0.0"
__author__  = "Bachir"

STOP = threading.Event()

TOP50 = [
    "GitHub","GitLab","Reddit","Twitter","Instagram","TikTok","LinkedIn",
    "Pinterest","tumblr","Flickr","Twitch","SoundCloud","Spotify",
    "Steam Community (User)","DeviantArt","ArtStation","Behance","Dribbble",
    "Medium","Substack","HackerNews","Codepen","Replit.com","LeetCode",
    "HackerRank","Kaggle","Bandcamp","last.fm","GoodReads","Letterboxd",
    "About.me","Linktree","Patreon","BuyMeACoffee","ProductHunt","Freelancer",
    "TradingView","HackTheBox","TryHackMe","HackerOne","MuseScore","Wattpad",
    "Issuu","Sketchfab","SourceForge","Docker Hub","npm","PyPi","Mixcloud","Newgrounds",
]

# ─────────────────────────────────────────────────────
#  BANNIÈRE
# ─────────────────────────────────────────────────────
def get_banner():
    return (
        f"\n{Fore.CYAN}{Style.BRIGHT}"
        "██╗   ██╗███████╗██╗     ██╗██╗  ██╗\n"
        "██║   ██║██╔════╝██║     ██║╚██╗██╔╝\n"
        "██║   ██║█████╗  ██║     ██║ ╚███╔╝ \n"
        "╚██╗ ██╔╝██╔══╝  ██║     ██║ ██╔██╗ \n"
        " ╚████╔╝ ███████╗███████╗██║██╔╝ ██╗\n"
        "  ╚═══╝  ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝\n"
        f"{Style.RESET_ALL}"
        f"{Fore.WHITE}      Trouveur de pseudos v{__version__}\n"
        f"{Fore.YELLOW}      Fait par {__author__} | github.com/{__author__.lower()}\n"
        f"{Style.RESET_ALL}{Fore.WHITE}{'─'*45}{Style.RESET_ALL}\n"
    )

# ─────────────────────────────────────────────────────
#  CATÉGORIES
#  ✅ FIX Bug 6 — noms corrigés : tumblr, GoodReads, threads
# ─────────────────────────────────────────────────────
CATEGORIES = {
    "1": {"nom": "🌐 Tous les sites", "sites": None},
    "2": {
        "nom": "📱 Réseaux sociaux",
        "sites": [
            "Twitter","Instagram","TikTok","Snapchat","Bluesky","threads",
            "VK","Clubhouse","mastodon.social","mastodon.cloud","mastodon.xyz",
            "Plurk","YouNow","Vero","Myspace","SpaceHey","tumblr","LinkedIn",
            "Pinterest","Reddit","Discord","Telegram","Signal","Kik",
            "AllMyLinks","Linktree","About.me","Carrd","minds","chaos.social",
            "Fosstodon","Flipboard","LiveJournal","Blogger","Medium","Substack",
            "Letterboxd","Trakt","GoodReads",
        ],
    },
    "3": {
        "nom": "💻 Développement",
        "sites": [
            "GitHub","GitLab","BitBucket","Codeberg","Gitea","Gitee","Codepen",
            "CodeSandbox","Replit.com","HackerNews","DEV Community","Hashnode",
            "HackMD","Coderwall","Codecademy","Codewars","CodeChef","Codeforces",
            "HackerRank","HackerEarth","Atcoder","LeetCode","Topcoder","DMOJ",
            "Vjudge","SourceForge","Launchpad","npm","PyPi","RubyGems","Packagist",
            "Docker Hub","GeeksforGeeks","freecodecamp","Platzi","Asciinema",
            "Wakatime","Coders Rank","Codolio","ObservableHQ","SpeakerDeck",
            "SlideShare","Slides","AWS Skills Profile","Apple Developer","Gradle",
            "devRant","habr","Career.habr","toster","CTAN","Cplusplus",
            "Ruby Forums","Arduino Forum","Python.org Discussions",
            "Jupyter Community Forum","CSSBattle","Code Snippet Wiki",
            "n8n Community","Kaggle","ResearchGate","HuggingFace",
        ],
    },
    "4": {
        "nom": "🎮 Gaming",
        "sites": [
            "Steam Community (User)","Steam Community (Group)","Roblox","Minecraft",
            "Twitch","Kick","Trovo","Xbox Gamertag","PSNProfiles.com","FortniteTracker",
            "Kongregate","Newgrounds","GameFAQs","Gamespot","GaiaOnline",
            "BoardGameGeek","Giant Bomb","NintendoLife","Speedrun.com","osu!",
            "Lichess","Chess","Blitz Tactics","Playstrategy","Pychess",
            "Pokemon Showdown","NationStates Nation","Wowhead","RuneScape","Realmeye",
            "Star Citizen","Valorant Forums","VLR","Cfx.re Forum","addons.wago.io",
            "Warframe Market","exophase","TETR.IO","MonkeyType","Typeracer",
            "NitroType","Sporcle","jeuxvideo","igromania","Ninja Kiwi","Nightbot",
        ],
    },
    "5": {
        "nom": "🎵 Musique",
        "sites": [
            "Spotify","SoundCloud","Bandcamp","MixCloud","Audiojungle","Freesound",
            "Smule","MuseScore","last.fm","YandexMusic","ReverbNation","Splice",
            "TRAKTRAIN","PromoDJ","Airbit","Rate Your Music","Discogs","Ultimate-Guitar",
        ],
    },
    "6": {
        "nom": "🎨 Art & Créatif",
        "sites": [
            "DeviantArt","ArtStation","Behance","Dribbble","Unsplash","Flickr",
            "SmugMug","EyeEm","YouPic","VSCO","Exposure","Blipfoto","Carbonmade",
            "Coroflot","Crevado","Contently","Sketchfab","CGTrader","MyMiniFactory",
            "Cults3D","OpenGameArt","LottieFiles","ColourLovers","2Dimensions",
            "Giphy","Tenor","Imgur","BOOTH","Gumroad","Issuu","Scribd","Wattpad",
            "Archive of Our Own","Fandom","Fanpop","LibraryThing","Polarsteps",
            "Strava","Untappd",
        ],
    },
    "7": {
        "nom": "🔐 Cybersécurité",
        "sites": [
            "HackTheBox","TryHackMe","CyberDefenders","HackerOne","BugCrowd",
            "Intigriti","HackenProof (Hackers)","PentesterLab",
            "BreachSta.rs Forum","CryptoHack","VirusTotal","HudsonRock",
        ],
    },
    "8": {
        "nom": "🛍️ Shopping & Finance",
        "sites": [
            "ProductHunt","Patreon","BuyMeACoffee","kofi","CashApp","Venmo",
            "Freelancer","Warrior Forum","BiggerPockets","TradingView","Rarible",
            "Coinvote","OpenCollective","Topmate","Dealabs","Mydealz",
            "Chollometro","HotUKdeals","mercadolivre",
        ],
    },
    "9": {
        "nom": "⭐ Top 50 sites les plus fiables",
        "sites": TOP50,
    },
}

# ─────────────────────────────────────────────────────
#  CHARGEMENT DATA.JSON
#  ✅ FIX Bug 3 — Instagram probe direct (sans imginn)
#  ✅ FIX Bug 3 — Twitter probe direct (sans nitter)
# ─────────────────────────────────────────────────────
def charger_sites(json_path=None):
    if json_path is None:
        try:
            json_path = str(files("velix").joinpath("data.json"))
        except Exception:
            base = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base, "data.json")
    if not json_path or not os.path.exists(str(json_path)):
        raise FileNotFoundError("data.json introuvable")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ✅ FIX Bug 3 — Instagram : probe direct sur instagram.com
    if "Instagram" in data:
        data["Instagram"].pop("urlProbe", None)
        data["Instagram"]["url"]       = "https://www.instagram.com/{}/"
        data["Instagram"]["errorType"] = "status_code"
        data["Instagram"]["errorCode"] = [404]

    # ✅ FIX Bug 3 — Twitter : probe direct sur x.com
    if "Twitter" in data:
        data["Twitter"].pop("urlProbe", None)
        data["Twitter"]["url"]       = "https://x.com/{}"
        data["Twitter"]["errorType"] = "status_code"
        data["Twitter"]["errorCode"] = [404]

    return {k: v for k, v in data.items() if isinstance(v, dict)}


def filtrer_sites(tous, cat_key, filtre_mot=None, exclude=None):
    sites_voulus = CATEGORIES[cat_key]["sites"]
    result = tous if sites_voulus is None else {k: v for k, v in tous.items() if k in sites_voulus}
    if filtre_mot:
        result = {k: v for k, v in result.items() if filtre_mot.lower() in k.lower()}
    if exclude:
        exclus = [e.strip().lower() for e in exclude.split(",")]
        result = {k: v for k, v in result.items() if k.lower() not in exclus}
    return result

# ─────────────────────────────────────────────────────
#  VALIDATION DU PSEUDO
# ─────────────────────────────────────────────────────
def valider_pseudo(username):
    if not username:
        return False, "Le pseudo est vide"
    if len(username) > 64:
        return False, "Le pseudo est trop long (max 64 caractères)"
    if re.search(r'[<>"\']', username):
        return False, "Caractères invalides détectés"
    return True, ""

# ─────────────────────────────────────────────────────
#  VARIANTES AUTOMATIQUES
# ─────────────────────────────────────────────────────
def generer_variantes(username):
    leet = username.replace("a","4").replace("e","3").replace("i","1").replace("o","0")
    return list(dict.fromkeys([
        username, username+"_", username+".", username+"-",
        username+"1", username+"123", leet,
    ]))

# ─────────────────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────────────────
def afficher_menu(tous_les_sites):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  📂 CHOISIR UNE CATÉGORIE :{Style.RESET_ALL}\n")
    for key, val in CATEGORIES.items():
        sites_cat = val["sites"]
        nb = len(tous_les_sites) if sites_cat is None else len([s for s in sites_cat if s in tous_les_sites])
        print(f"  {Fore.YELLOW}[{key}]{Style.RESET_ALL}  {val['nom']}  {Fore.WHITE}({nb} sites){Style.RESET_ALL}")
    print()
    choix = input(f"  {Fore.GREEN}➤ Ton choix (1-{len(CATEGORIES)}) : {Style.RESET_ALL}").strip()
    if choix not in CATEGORIES:
        print(f"{Fore.RED}  Choix invalide → tous les sites.{Style.RESET_ALL}")
        choix = "1"
    return choix

# ─────────────────────────────────────────────────────
#  SESSION PARALLÈLE
# ─────────────────────────────────────────────────────
class VelixSession(FuturesSession):
    def request(self, method, url, hooks=None, *args, **kwargs):
        if hooks is None:
            hooks = {}
        start = monotonic()
        def response_time(resp, *args, **kwargs):
            resp.elapsed = monotonic() - start
        try:
            if isinstance(hooks["response"], list):
                hooks["response"].insert(0, response_time)
            else:
                hooks["response"] = [response_time, hooks["response"]]
        except KeyError:
            hooks["response"] = [response_time]
        return super().request(method, url, hooks=hooks, *args, **kwargs)

def interpolate(obj, username):
    if isinstance(obj, str):
        return obj.replace("{}", username)
    elif isinstance(obj, dict):
        return {k: interpolate(v, username) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [interpolate(i, username) for i in obj]
    return obj

def couleur_vitesse(ms):
    if ms < 800:   return Fore.GREEN
    if ms < 2000:  return Fore.YELLOW
    return Fore.RED

# ─────────────────────────────────────────────────────
#  RECHERCHE PRINCIPALE
#  ✅ FIX Bug 1 — GET au lieu de HEAD (plus de faux 405)
#  ✅ FIX Bug 2 — errorCode précis par site (pas >= 300)
#  ✅ FIX Bug 4 — WAF détectable car on a le corps de la réponse
#  ✅ FIX Bug 5 — retry supprimé (inutile avec futures)
#  ✅ FIX Bug 7 — nb_illegal supprimé
# ─────────────────────────────────────────────────────
WAF_MSGS = [
    '.loading-spinner{visibility:hidden}body.no-js',
    '<span id="challenge-error-text">',
    'AwsWafIntegration.forceRefreshToken',
    'perimeterxIdentifiers',
    'cf-browser-verification',
    '__cf_chl_managed',
]
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def rechercher(username, sites, silent=False, timeout=15, proxy=None,
               no_color=False, fast=False, show_http=False):
    resultats = {}
    trouves   = []
    workers   = 30 if fast else min(20, len(sites))
    tmt       = 5  if fast else timeout

    def c(color, txt):
        return txt if no_color else f"{color}{txt}{Style.RESET_ALL}"

    print(f"\n{c(Fore.CYAN+Style.BRIGHT, f'  🔍 Recherche de « {username} » sur {len(sites)} sites...')}\n")

    session_base = requests.Session()
    session_base.verify = False
    session = VelixSession(max_workers=workers, session=session_base)

    futures = {}

    for site, info in sites.items():
        url   = interpolate(info.get("url", ""), username.replace(" ", "%20"))
        h     = {**HEADERS, **info.get("headers", {})}
        regex = info.get("regexCheck")

        if regex and re.search(regex, username) is None:
            resultats[site] = {"status": "ILLEGAL", "url": url, "time_ms": 0, "http": "-"}
            continue

        url_probe      = interpolate(info.get("urlProbe", url), username)
        error_type     = info.get("errorType", "status_code")
        # ✅ FIX Bug 1 : toujours GET (évite les faux 405 avec HEAD)
        allow_redirect = (error_type != "response_url")
        proxies        = {"http": proxy, "https": proxy} if proxy else None

        try:
            fut = session.get(
                url=url_probe, headers=h,
                allow_redirects=allow_redirect,
                timeout=tmt, proxies=proxies
            )
            futures[site] = (fut, info, url)
        except Exception:
            resultats[site] = {"status": "ERREUR", "url": url, "time_ms": 0, "http": "?"}

    total_futures = len(futures)
    compteur = 0

    for site, (fut, info, url) in futures.items():
        if STOP.is_set():
            break
        compteur += 1

        pct_num = int((compteur / max(total_futures, 1)) * 100)
        pct     = int((compteur / max(total_futures, 1)) * 25)
        barre   = f"[{'█'*pct}{'░'*(25-pct)}] {pct_num}%"
        print(f"\r  {c(Fore.YELLOW, barre)} {compteur}/{total_futures} ", end="", flush=True)

        try:
            r = fut.result(timeout=tmt + 3)
        except (FuturesTimeoutError, TimeoutError):
            resultats[site] = {"status": "TIMEOUT", "url": url, "time_ms": tmt*1000, "http": "-"}
            continue
        except Exception:
            resultats[site] = {"status": "ERREUR", "url": url, "time_ms": 0, "http": "?"}
            continue

        error_type = info.get("errorType", "status_code")
        time_ms    = round(r.elapsed * 1000) if isinstance(getattr(r, "elapsed", None), float) else 0
        http_code  = getattr(r, "status_code", "?")
        status     = "AVAILABLE"

        try:
            txt = r.text or ""
        except Exception:
            txt = ""

        try:
            # ✅ FIX Bug 4 — WAF détectable car on a le corps maintenant
            if any(w in txt for w in WAF_MSGS):
                status = "WAF"

            elif error_type == "message":
                errors = info.get("errorMsg", "")
                if isinstance(errors, str):
                    errors = [errors]
                status = "AVAILABLE" if any(e in txt for e in errors) else "CLAIMED"

            elif error_type == "status_code":
                # ✅ FIX Bug 2 — errorCode précis du site, défaut [404] seulement
                codes = info.get("errorCode", [404])
                if isinstance(codes, int):
                    codes = [codes]
                # Seulement les codes d'erreur explicites → pas le ">= 300" qui était faux
                status = "AVAILABLE" if http_code in codes else "CLAIMED"

            elif error_type == "response_url":
                status = "CLAIMED" if isinstance(http_code, int) and 200 <= http_code < 300 else "AVAILABLE"

        except Exception:
            status = "UNKNOWN"

        resultats[site] = {"status": status, "url": url, "time_ms": time_ms, "http": http_code}

        http_txt = f" [{http_code}]" if show_http else ""
        v_color  = couleur_vitesse(time_ms) if not no_color else ""
        time_txt = (f" {v_color}{time_ms}ms{Style.RESET_ALL}" if (time_ms and not no_color)
                    else (f" {time_ms}ms" if time_ms else ""))

        if status == "CLAIMED":
            trouves.append((site, url, time_ms))
            print(f"\r  {c(Fore.GREEN,'[+]')} {c(Fore.GREEN,f'{site:<32}')}{http_txt}{time_txt}  {url}")
        elif not silent and status == "AVAILABLE":
            print(f"\r  {c(Fore.RED,'[-]')} {c(Fore.RED,f'{site:<32}')}{http_txt}  Non trouvé")
        elif not silent and status in ("WAF","TIMEOUT"):
            print(f"\r  {c(Fore.YELLOW,'[!]')} {c(Fore.YELLOW,f'{site:<32}')}  {status}")

    print()
    trouves.sort(key=lambda x: x[0])

    if not trouves:
        print(f"  {Fore.YELLOW}💡 Aucun compte trouvé. Essaie --variantes ou une autre catégorie.{Style.RESET_ALL}")

    return resultats, trouves

# ─────────────────────────────────────────────────────
#  RÉSUMÉ
# ─────────────────────────────────────────────────────
def afficher_resume(username, resultats, trouves, cat_nom, duree, no_color=False):
    def c(color, txt):
        return txt if no_color else f"{color}{txt}{Style.RESET_ALL}"

    total        = len(resultats)
    nb_trouves   = len(trouves)
    nb_available = sum(1 for v in resultats.values() if v.get("status") == "AVAILABLE")
    nb_waf       = sum(1 for v in resultats.values() if v.get("status") in ("WAF","TIMEOUT"))
    nb_erreur    = sum(1 for v in resultats.values() if v.get("status") in ("ERREUR","UNKNOWN"))

    print(f"\n{c(Fore.CYAN+Style.BRIGHT,'─'*52)}")
    print(f"  📊 RÉSUMÉ — {username}")
    print(c(Fore.CYAN,"─"*52))
    print(f"  {c(Fore.GREEN,  f'✓ Comptes trouvés   : {nb_trouves}')}")
    print(f"  {c(Fore.RED,    f'✗ Non trouvés       : {nb_available}')}")
    print(f"  {c(Fore.YELLOW, f'! Bloqués/Timeout   : {nb_waf}')}")
    print(f"  {c(Fore.WHITE,  f'? Erreurs           : {nb_erreur}')}")
    print(f"  {c(Fore.CYAN,   f'⏱  Durée            : {duree:.1f}s')}")
    print(f"  {c(Fore.CYAN,   f'📂 Catégorie        : {cat_nom}')}")
    print(f"  {c(Fore.WHITE,  '🟢 <800ms  🟡 <2s  🔴 >2s')}")

    if total > 0:
        pct   = nb_trouves / total
        barre = int(pct * 30)
        print(f"\n  {c(Fore.GREEN,'█'*barre)}{c(Fore.RED,'░'*(30-barre))}"
              f"  {nb_trouves}/{total} ({pct*100:.1f}%)")

    if trouves:
        print(f"\n  {c(Fore.GREEN+Style.BRIGHT,'🔗 Comptes trouvés :')}")
        for site, url, ms in trouves:
            vc = couleur_vitesse(ms) if not no_color else ""
            print(f"  {c(Fore.GREEN,f'  • {site:<28}')} {url}  "
                  f"{vc}{ms}ms{Style.RESET_ALL if not no_color else ''}")

    print(f"\n{c(Fore.CYAN,'─'*52)}\n")

# ─────────────────────────────────────────────────────
#  STATS GLOBALES (multi-pseudos)
# ─────────────────────────────────────────────────────
def afficher_stats_globales(stats_all):
    if len(stats_all) < 2:
        return
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'─'*52}")
    print("  📈 STATS GLOBALES")
    print(f"{'─'*52}{Style.RESET_ALL}")
    total_trouves = sum(s["trouves"] for s in stats_all)
    print(f"  Pseudos testés : {len(stats_all)}")
    print(f"  Total trouvés  : {Fore.GREEN}{total_trouves}{Style.RESET_ALL}")
    for s in stats_all:
        bar = int((s["trouves"] / max(s["total"],1)) * 20)
        print(f"  {Fore.YELLOW}{s['username']:<20}{Style.RESET_ALL} "
              f"{Fore.GREEN}{'█'*bar}{Fore.RED}{'░'*(20-bar)}{Style.RESET_ALL} "
              f"{s['trouves']}/{s['total']}")
    print(f"{Fore.CYAN}{'─'*52}{Style.RESET_ALL}\n")

# ─────────────────────────────────────────────────────
#  EXPORT HTML
# ─────────────────────────────────────────────────────
def exporter_html(username, resultats, trouves, cat_nom, duree, output_dir="."):
    date       = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    total      = len(resultats)
    nb_trouves = len(trouves)
    pct_w      = f"{(nb_trouves/max(total,1))*100:.1f}%"

    lignes = ""
    for site, data in sorted(resultats.items(),
                              key=lambda x: (x[1].get("status") != "CLAIMED", x[0])):
        status  = data.get("status","?")
        url     = data.get("url","")
        http    = data.get("http","-")
        time_ms = data.get("time_ms",0)
        color   = {"CLAIMED":"#2ecc71","WAF":"#f39c12","TIMEOUT":"#e67e22",
                   "ILLEGAL":"#95a5a6"}.get(status,"#e74c3c")
        icone   = {"CLAIMED":"✓","WAF":"!","TIMEOUT":"⏱","ILLEGAL":"~"}.get(status,"✗")
        lien    = (f'<a href="{url}" target="_blank">{url}</a>'
                   if status == "CLAIMED" else (url or "—"))
        bold    = "font-weight:700" if status == "CLAIMED" else ""
        vc      = "#2ecc71" if time_ms < 800 else ("#f39c12" if time_ms < 2000 else "#e74c3c")
        lignes += (
            f"<tr class='{'found' if status=='CLAIMED' else ''}'>"
            f"<td><span style='color:{color};font-weight:700'>{icone}</span></td>"
            f"<td style='{bold}'>{site}</td><td>{lien}</td>"
            f"<td style='color:{color}'>{status}</td>"
            f"<td style='color:#666'>{http}</td>"
            f"<td style='color:{vc}'>{time_ms}ms</td></tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Velix — {username}</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:'Segoe UI',sans-serif;background:#0a0a0f;color:#eee;padding:30px}}
    h1{{color:#00d4ff;font-size:2.4em;text-align:center;letter-spacing:4px;margin-bottom:4px}}
    .sub{{text-align:center;color:#555;margin-bottom:22px;font-size:.93em}}
    .stats{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:22px}}
    .stat{{background:#12121e;border-radius:12px;padding:16px 26px;text-align:center;
           border-left:4px solid #00d4ff;min-width:110px}}
    .stat .num{{font-size:1.9em;font-weight:700;color:#00d4ff}}
    .stat .lbl{{font-size:.78em;color:#555;margin-top:3px}}
    .prog{{background:#12121e;border-radius:10px;margin:0 auto 20px;
           max-width:480px;height:14px;overflow:hidden}}
    .prog-bar{{height:100%;background:linear-gradient(90deg,#00d4ff,#2ecc71);width:{pct_w}}}
    .search-bar{{text-align:center;margin-bottom:16px}}
    input{{background:#12121e;border:1px solid #00d4ff33;color:#eee;
           padding:7px 14px;border-radius:8px;width:240px;font-size:.92em;outline:none}}
    input:focus{{border-color:#00d4ff}}
    table{{width:100%;border-collapse:collapse;background:#12121e;
           border-radius:12px;overflow:hidden}}
    th{{background:#00d4ff15;color:#00d4ff;padding:11px 13px;text-align:left;
        font-size:.78em;text-transform:uppercase;letter-spacing:1px}}
    td{{padding:10px 13px;border-bottom:1px solid #ffffff08;font-size:.9em}}
    td a{{color:#2ecc71;text-decoration:none}}
    td a:hover{{text-decoration:underline}}
    tr:hover{{background:#ffffff05}}
    tr.found{{background:#2ecc7106}}
    .footer{{text-align:center;margin-top:22px;color:#333;font-size:.78em}}
    .legend{{text-align:center;margin-bottom:12px;font-size:.8em;color:#666}}
  </style>
</head>
<body>
  <h1>⚡ VELIX</h1>
  <p class="sub">@{username} — {date} — {cat_nom} — {duree:.1f}s</p>
  <div class="stats">
    <div class="stat">
      <div class="num" style="color:#2ecc71">{nb_trouves}</div>
      <div class="lbl">Trouvés</div>
    </div>
    <div class="stat">
      <div class="num">{total}</div>
      <div class="lbl">Analysés</div>
    </div>
    <div class="stat">
      <div class="num" style="color:#f39c12">{duree:.1f}s</div>
      <div class="lbl">Durée</div>
    </div>
    <div class="stat">
      <div class="num" style="color:#00d4ff">{pct_w}</div>
      <div class="lbl">Taux</div>
    </div>
  </div>
  <div class="prog"><div class="prog-bar"></div></div>
  <div class="legend">🟢 &lt;800ms &nbsp; 🟡 &lt;2s &nbsp; 🔴 &gt;2s</div>
  <div class="search-bar">
    <input id="s" placeholder="🔍 Filtrer les sites..." oninput="filtrer()">
  </div>
  <table id="t">
    <thead>
      <tr><th>#</th><th>Site</th><th>URL</th><th>Statut</th><th>HTTP</th><th>Vitesse</th></tr>
    </thead>
    <tbody>{lignes}</tbody>
  </table>
  <div class="footer">Généré par Velix v{__version__} — github.com/{__author__.lower()}</div>
  <script>
    function filtrer(){{
      const v = document.getElementById('s').value.toLowerCase();
      document.querySelectorAll('#t tbody tr').forEach(r => {{
        r.style.display = r.innerText.toLowerCase().includes(v) ? '' : 'none';
      }});
    }}
  </script>
</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    nom = os.path.join(output_dir, f"{username}_velix.html")
    with open(nom, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.abspath(nom)

# ─────────────────────────────────────────────────────
#  EXPORTS CSV / JSON
# ─────────────────────────────────────────────────────
def exporter_csv(username, resultats, output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    nom = os.path.join(output_dir, f"{username}_velix.csv")
    with open(nom, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Site","Statut","URL","HTTP","Temps(ms)"])
        for site, data in resultats.items():
            w.writerow([site, data.get("status","?"), data.get("url",""),
                        data.get("http","-"), data.get("time_ms",0)])
    return nom

def exporter_json_file(username, resultats, trouves, cat_nom, duree, output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    nom = os.path.join(output_dir, f"{username}_velix.json")
    payload = {
        "username": username, "version": __version__,
        "date": datetime.datetime.now().isoformat(),
        "categorie": cat_nom, "duree_s": round(duree, 2),
        "nb_trouves": len(trouves), "resultats": resultats,
    }
    with open(nom, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
    return nom

# ─────────────────────────────────────────────────────
#  HISTORIQUE
# ─────────────────────────────────────────────────────
def sauvegarder_historique(username, nb_trouves, total, cat_nom, output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    fichier = os.path.join(output_dir, "velix_historique.json")
    hist = []
    if os.path.exists(fichier):
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                hist = json.load(f)
        except Exception:
            hist = []
    hist.append({
        "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "username": username, "trouves": nb_trouves,
        "total": total, "categorie": cat_nom,
    })
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

def afficher_historique(output_dir="."):
    fichier = os.path.join(output_dir, "velix_historique.json")
    if not os.path.exists(fichier):
        print(f"  {Fore.YELLOW}Aucun historique trouvé.{Style.RESET_ALL}")
        return
    with open(fichier, "r", encoding="utf-8") as f:
        hist = json.load(f)
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  📜 HISTORIQUE ({len(hist)} recherches){Style.RESET_ALL}\n")
    for h in reversed(hist[-20:]):
        print(f"  {Fore.YELLOW}{h['date']}{Style.RESET_ALL}  "
              f"{Fore.WHITE}{h['username']:<20}{Style.RESET_ALL}  "
              f"{Fore.GREEN}{h['trouves']}/{h['total']}{Style.RESET_ALL}  "
              f"{Fore.CYAN}{h['categorie']}{Style.RESET_ALL}")
    print()

def afficher_liste_sites(sites, cat_nom):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}  📋 SITES — {cat_nom} ({len(sites)} sites){Style.RESET_ALL}\n")
    for i, site in enumerate(sorted(sites.keys()), 1):
        print(f"  {Fore.YELLOW}{i:>3}.{Style.RESET_ALL}  {site}")
    print()

# ─────────────────────────────────────────────────────
#  CTRL+C
# ─────────────────────────────────────────────────────
def handler(sig, frame):
    STOP.set()
    print(f"\n\n{Fore.YELLOW}  [!] Recherche annulée.{Style.RESET_ALL}\n")
    os._exit(0)

# ─────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────
def main():
    signal.signal(signal.SIGINT, handler)
    requests.packages.urllib3.disable_warnings()
    os.system("clear" if os.name != "nt" else "cls")
    print(get_banner())

    parser = ArgumentParser(
        description=f"Velix v{__version__} — Trouveur de pseudos sur 480+ sites",
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("username",        nargs="*",           help="Pseudo(s) à rechercher")
    parser.add_argument("--version","-v",  action="version",    version=f"Velix v{__version__}")
    parser.add_argument("--silent", "-s",  action="store_true", help="Afficher seulement les comptes trouvés")
    parser.add_argument("--html",          action="store_true", help="Exporter en HTML")
    parser.add_argument("--csv",           action="store_true", help="Exporter en CSV")
    parser.add_argument("--json",          action="store_true", help="Exporter en JSON")
    parser.add_argument("--browser","-b",  action="store_true", help="Ouvrir le rapport HTML dans le navigateur")
    parser.add_argument("--variantes",     action="store_true", help="Tester des variantes du pseudo")
    parser.add_argument("--fast",          action="store_true", help="Mode rapide : timeout 5s, 30 workers")
    parser.add_argument("--no-color",      action="store_true", help="Désactiver les couleurs")
    parser.add_argument("--show-http",     action="store_true", help="Afficher le code HTTP de chaque site")
    parser.add_argument("--timeout",       type=int,default=15, help="Timeout en secondes (défaut: 15)")
    parser.add_argument("--proxy",         default=None,        help="Proxy (ex: socks5://127.0.0.1:1080)")
    parser.add_argument("--categorie","-c",default=None,        help="Numéro de catégorie (1-9) sans menu")
    parser.add_argument("--filter",        default=None,        help="Filtrer les sites par mot-clé")
    parser.add_argument("--exclude",       default=None,        help="Exclure des sites (ex: tiktok,reddit)")
    parser.add_argument("--output",        default=".",         help="Dossier de sauvegarde (défaut: .)")
    parser.add_argument("--list-sites",    action="store_true", help="Lister les sites disponibles")
    parser.add_argument("--historique",    action="store_true", help="Afficher l'historique des recherches")
    args = parser.parse_args()

    try:
        tous_les_sites = charger_sites()
    except FileNotFoundError:
        print(f"{Fore.RED}  [!] data.json introuvable.{Style.RESET_ALL}")
        print("  Assure-toi que data.json est dans le même dossier que velix.py")
        sys.exit(1)

    if args.historique:
        afficher_historique(args.output)
        sys.exit(0)

    choix = args.categorie if args.categorie in CATEGORIES else None
    if not choix:
        choix = afficher_menu(tous_les_sites)
    cat_nom = CATEGORIES[choix]["nom"]
    sites   = filtrer_sites(tous_les_sites, choix, args.filter, args.exclude)

    if args.filter:
        print(f"  {Fore.CYAN}🔎 Filtre : «{args.filter}» → {len(sites)} sites{Style.RESET_ALL}")
    if args.exclude:
        print(f"  {Fore.CYAN}🚫 Exclus : {args.exclude}{Style.RESET_ALL}")

    if args.list_sites:
        afficher_liste_sites(sites, cat_nom)
        sys.exit(0)

    print(f"\n  {Fore.CYAN}📂 {cat_nom}  ({len(sites)} sites){Style.RESET_ALL}")

    if args.username:
        usernames_base = args.username
    else:
        print()
        saisie = input(
            f"  {Fore.GREEN}➤ Pseudo(s) à rechercher (espace pour plusieurs) : {Style.RESET_ALL}"
        ).strip()
        if not saisie:
            print(f"{Fore.RED}  Aucun pseudo saisi.{Style.RESET_ALL}")
            sys.exit(1)
        usernames_base = saisie.split()

    usernames = []
    for u in usernames_base:
        ok, msg = valider_pseudo(u)
        if not ok:
            print(f"  {Fore.RED}[✗] Pseudo invalide «{u}» : {msg}{Style.RESET_ALL}")
            continue
        if args.variantes:
            vars_ = generer_variantes(u)
            print(f"  {Fore.CYAN}🔀 Variantes : {', '.join(vars_)}{Style.RESET_ALL}")
            usernames.extend(vars_)
        else:
            usernames.append(u)

    if not usernames:
        print(f"{Fore.RED}  Aucun pseudo valide.{Style.RESET_ALL}")
        sys.exit(1)

    stats_all = []

    for username in usernames:
        STOP.clear()
        debut = monotonic()
        resultats, trouves = rechercher(
            username=username, sites=sites, silent=args.silent,
            timeout=args.timeout, proxy=args.proxy,
            no_color=args.no_color, fast=args.fast, show_http=args.show_http,
        )
        duree = monotonic() - debut

        afficher_resume(username, resultats, trouves, cat_nom, duree, args.no_color)
        sauvegarder_historique(username, len(trouves), len(resultats), cat_nom, args.output)
        stats_all.append({"username": username, "trouves": len(trouves), "total": len(resultats)})

        if trouves:
            os.makedirs(args.output, exist_ok=True)
            txt = os.path.join(args.output, f"{username}_velix.txt")
            with open(txt, "w", encoding="utf-8") as f:
                for site, url, _ in trouves:
                    f.write(url + "\n")
            print(f"  {Fore.GREEN}[✓] TXT  : {txt}{Style.RESET_ALL}")

        if args.csv:
            f = exporter_csv(username, resultats, args.output)
            print(f"  {Fore.GREEN}[✓] CSV  : {f}{Style.RESET_ALL}")

        if args.json:
            f = exporter_json_file(username, resultats, trouves, cat_nom, duree, args.output)
            print(f"  {Fore.GREEN}[✓] JSON : {f}{Style.RESET_ALL}")

        if args.html or args.browser:
            f = exporter_html(username, resultats, trouves, cat_nom, duree, args.output)
            print(f"  {Fore.GREEN}[✓] HTML : {f}{Style.RESET_ALL}")
            if args.browser:
                webbrowser.open(f"file://{f}")
                print(f"  {Fore.CYAN}[🌐] Rapport ouvert dans le navigateur{Style.RESET_ALL}")

    afficher_stats_globales(stats_all)

    print()
    again = input(
        f"  {Fore.GREEN}➤ Nouvelle recherche ? (o/N) : {Style.RESET_ALL}"
    ).strip().lower()
    if again == "o":
        main()


if __name__ == "__main__":
    main()
