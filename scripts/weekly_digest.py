#!/usr/bin/env python3
"""
AutoClip pertranslated：GitHub translated issue + translated + PostHog translatedusetranslated → onetranslated。

translated Cursor Automation（translated cron）translated，translatedintranslated。translateddependencies Python 3 translated。

translated（translated translatedskiptranslated ，translatedintranslated）
  GitHub   : `gh` CLI（translated）or GH_TOKtranslated + REST。
  translated : translated `lark-cli`（personal profile，user translated）translated CLI；
             translateduse LARK_APP_ID / LARK_APP_SECRET translated tenant_access_token translated
             multitranslated API（translatedusetranslated base:record:read / bitable:app:readonly，
             translated translatedusetranslatedmultitranslated）。
  PostHog  : POSTHOG_PERSONAL_API_KEY + POSTHOG_PROJECT_ID（HogQL translated
             `feedback_submitted` / `survey sent` translated）。

translated
  FEISHU_WEBHOOK_URL（translated webhook，canSelect FEISHU_WEBHOOK_SECRET Signature）。
  translated webhook translated stdout。

usetranslated
  python3 scripts/weekly_digest.py                # translated markdown translated
  python3 scripts/weekly_digest.py --json         # translated（translated agent translated）
  python3 scripts/weekly_digest.py --post         # translated
  python3 scripts/weekly_digest.py --post --message-file digest.md   # translated agent translated'stranslated
  python3 scripts/weekly_digest.py --days 14      # translated
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

REPO = os.environ.get("AUTOCLIP_REPO", "zhouxiaoka/autoclip")
FEISHU_BASE_TOKtranslated = os.environ.get("FEISHU_BASE_TOKtranslated", "EuYLb3lQ2awwDFsTkDXchabsnbd")
FEISHU_TABLE_ID = os.environ.get("FEISHU_TABLE_ID", "tbl92rUV2NnRX6GJ")
FEISHU_FORM_URL = "https://my.feishu.cn/share/base/shrcn8hKUG2icIJLpNry6uWVNJe"
FEISHU_BASE_URL = f"https://my.feishu.cn/base/{FEISHU_BASE_TOKtranslated}?table={FEISHU_TABLE_ID}"
LARK_PROFILE = os.environ.get("LARK_PROFILE", "personal")
POSTHOG_HOST = os.environ.get("POSTHOG_HOST", "https://us.posthog.com").rstrip("/")

CATEGORY_LABEL = {"bug": "translatedissuetranslated", "feature": "translatedfeature", "other": "translated"}


# ---------------------------------------------------------------- helpers ---
def _http_json(url: str, *, method: str = "GET", headers: dict[str, str] | None = None, body: Any = None, timeout: int = 30) -> Any:
    data = None
    hdrs = {"Accept": "application/json", **(headers or {})}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json; charset=utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def _run(cmd: list[str], timeout: int = 60) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def _parse_iso(s: str) -> dt.datetime | None:
    if not s:
        return None
    try:
        s = s.replace("Z", "+00:00")
        d = dt.datetime.fromisoformat(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        return d
    except ValueError:
        return None


def _trunc(s: str, n: int = 120) -> str:
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _first(v: Any) -> str:
    """translated select translatedIs list，translatedcantranslatedIs str / list[{text}]。translatedonetranslated str。"""
    if v is None:
        return ""
    if isinstance(v, list):
        parts = []
        for x in v:
            if isinstance(x, dict):
                parts.append(str(x.get("text") or x.get("name") or ""))
            else:
                parts.append(str(x))
        return " / ".join(p for p in parts if p)
    if isinstance(v, dict):
        return str(v.get("text") or v.get("name") or "")
    return str(v)


# ---------------------------------------------------------------- GitHub ---
def fetch_github(since: dt.datetime) -> dict[str, Any]:
    day = since.date().isoformat()
    out: dict[str, Any] = {"ok": False, "opened": [], "closed": [], "note": ""}
    fields = "number,title,labels,state,createdAt,closedAt,url,author"
    if shutil.which("gh"):
        try:
            rc, so, se = _run(["gh", "issue", "list", "--repo", REPO, "--state", "all", "--limit", "200",
                               "--search", f"created:>={day}", "--json", fields])
            if rc != 0:
                raise RuntimeError(se.strip())
            opened = json.loads(so or "[]")
            rc, so, se = _run(["gh", "issue", "list", "--repo", REPO, "--state", "closed", "--limit", "200",
                               "--search", f"closed:>={day}", "--json", fields])
            closed = json.loads(so or "[]") if rc == 0 else []
        except Exception as e:  # noqa: BLE001
            out["note"] = f"gh failed：{e}"
            return out
    else:
        token = os.environ.get("GH_TOKtranslated") or os.environ.get("GITHUB_TOKtranslated")
        if not token:
            out["note"] = "translated gh，translated GH_TOKtranslated"
            return out
        hdr = {"Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}
        try:
            q = f"repo:{REPO} is:issue created:>={day}"
            r = _http_json(f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=100", headers=hdr)
            opened = [_gh_norm(i) for i in r.get("items", [])]
            q = f"repo:{REPO} is:issue closed:>={day}"
            r = _http_json(f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=100", headers=hdr)
            closed = [_gh_norm(i) for i in r.get("items", [])]
        except Exception as e:  # noqa: BLE001
            out["note"] = f"GitHub API failed：{e}"
            return out

    def norm(i: dict[str, Any]) -> dict[str, Any]:
        return {
            "number": i.get("number"),
            "title": i.get("title", ""),
            "labels": [l.get("name") if isinstance(l, dict) else str(l) for l in i.get("labels", [])],
            "state": (i.get("state") or "").lower(),
            "created_at": i.get("createdAt") or i.get("created_at"),
            "url": i.get("url") or i.get("html_url"),
            "author": (i.get("author") or {}).get("login") if isinstance(i.get("author"), dict) else i.get("author"),
        }

    out.update(ok=True, opened=[norm(i) for i in opened], closed=[norm(i) for i in closed])
    return out


def _gh_norm(i: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": i.get("number"), "title": i.get("title"), "labels": i.get("labels", []),
        "state": i.get("state"), "createdAt": i.get("created_at"), "closedAt": i.get("closed_at"),
        "url": i.get("html_url"), "author": {"login": (i.get("user") or {}).get("login")},
    }


# ---------------------------------------------------------------- Feishu ---
def fetch_feishu_form(since: dt.datetime) -> dict[str, Any]:
    out: dict[str, Any] = {"ok": False, "items": [], "total_all": 0, "note": "", "via": ""}
    rows: list[dict[str, Any]] = []

    if shutil.which("lark-cli"):
        cmd = ["lark-cli", "base", "+record-list", "--base-token", FEISHU_BASE_TOKtranslated, "--table-id", FEISHU_TABLE_ID,
               "--as", "user", "--limit", "200", "--json"]
        if LARK_PROFILE:
            cmd += ["--profile", LARK_PROFILE]
        try:
            rc, so, se = _run(cmd)
            j = json.loads(so) if so.strip().startswith("{") else {}
            if rc == 0 and j.get("ok"):
                d = j["data"]
                names = d.get("fields", [])
                for matrix_row in d.get("data", []):
                    rows.append(dict(zip(names, matrix_row)))
                out["via"] = "lark-cli"
            else:
                out["note"] = f"lark-cli failed：{(j.get('error') or {}).get('message') or se.strip()[:200]}"
        except Exception as e:  # noqa: BLE001
            out["note"] = f"lark-cli translated：{e}"

    if not out["via"]:
        app_id, app_secret = os.environ.get("LARK_APP_ID"), os.environ.get("LARK_APP_SECRET")
        if not (app_id and app_secret):
            out["note"] = out["note"] or "translated lark-cli，translated LARK_APP_ID / LARK_APP_SECRET"
            return out
        try:
            tok = _http_json("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal", method="POST",
                             body={"app_id": app_id, "app_secret": app_secret})
            if tok.get("code") != 0:
                raise RuntimeError(tok.get("msg"))
            hdr = {"Authorization": f"Bearer {tok['tenant_access_token']}"}
            page_token, items = "", []
            while True:
                url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_BASE_TOKtranslated}/tables/{FEISHU_TABLE_ID}/records/search?page_size=200"
                if page_token:
                    url += f"&page_token={page_token}"
                r = _http_json(url, method="POST", headers=hdr, body={})
                if r.get("code") != 0:
                    raise RuntimeError(f"{r.get('code')} {r.get('msg')}")
                items += r.get("data", {}).get("items", [])
                if not r.get("data", {}).get("has_more"):
                    break
                page_token = r["data"].get("page_token", "")
            for it in items:
                f = dict(it.get("fields", {}))
                # created_at translatedin API translatedIstranslatedsecondstranslated
                ct = f.get("translated")
                if isinstance(ct, (int, float)):
                    f["translated"] = dt.datetime.fromtimestamp(ct / 1000, tz=dt.timezone.utc).isoformat()
                rows.append(f)
            out["via"] = "open-api"
        except Exception as e:  # noqa: BLE001
            out["note"] = f"translated API failed：{e}"
            return out

    out["total_all"] = len(rows)
    for r in rows:
        t = _parse_iso(_first(r.get("translated")))
        if t and t < since:
            continue
        out["items"].append({
            "time": t.isoformat() if t else "",
            "type": _first(r.get("translated")),
            "platform": _first(r.get("translated")),
            "version": _first(r.get("version")),
            "content": _first(r.get("translated")),
            "contact": _first(r.get("Contacttranslated")),
            "status": _first(r.get("status")),
            "has_attachment": bool(r.get("translated / logs")),
        })
    out["items"].sort(key=lambda x: x["time"], reverse=True)
    out["ok"] = True
    return out


# ---------------------------------------------------------------- PostHog ---
def fetch_posthog(since: dt.datetime, days: int) -> dict[str, Any]:
    out: dict[str, Any] = {"ok": False, "items": [], "survey_responses": 0, "note": ""}
    key, pid = os.environ.get("POSTHOG_PERSONAL_API_KEY"), os.environ.get("POSTHOG_PROJECT_ID")
    if not (key and pid):
        out["note"] = "translated POSTHOG_PERSONAL_API_KEY / POSTHOG_PROJECT_ID"
        return out
    hdr = {"Authorization": f"Bearer {key}"}
    q = f"""
      SELECT timestamp, properties.category, properties.source, properties.stage, properties.text,
             properties.app_version, properties.os, properties.arch, properties.llm_provider, properties.llm_model,
             properties.error_message, properties.contact, distinct_id
      FROM events
      WHERE event = 'feedback_submitted' AND timestamp > now() - INTERVAL {int(days)} DAY
      ORDER BY timestamp DESC LIMIT 300
    """
    try:
        r = _http_json(f"{POSTHOG_HOST}/api/projects/{pid}/query/", method="POST", headers=hdr,
                       body={"query": {"kind": "HogQLQuery", "query": q}})
        cols = ["time", "category", "source", "stage", "text", "app_version", "os", "arch", "llm_provider",
                "llm_model", "error_message", "contact", "distinct_id"]
        for row in r.get("results", []):
            item = dict(zip(cols, row))
            out["items"].append(item)
        r2 = _http_json(f"{POSTHOG_HOST}/api/projects/{pid}/query/", method="POST", headers=hdr,
                        body={"query": {"kind": "HogQLQuery",
                                        "query": f"SELECT count() FROM events WHERE event = 'survey sent' AND timestamp > now() - INTERVAL {int(days)} DAY"}})
        res = r2.get("results") or [[0]]
        out["survey_responses"] = int(res[0][0] or 0)
        out["ok"] = True
    except urllib.error.HTTPError as e:
        out["note"] = f"PostHog HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:200]}"
    except Exception as e:  # noqa: BLE001
        out["note"] = f"PostHog failed：{e}"
    return out


# ---------------------------------------------------------------- render ---
def render_markdown(data: dict[str, Any]) -> str:
    since, until = data["window"]["since"], data["window"]["until"]
    gh, fs, ph = data["github"], data["feishu_form"], data["posthog"]
    L: list[str] = []
    L.append(f"**AutoClip translated** · {since[:10]} → {until[:10]}")
    L.append("")

    # translated
    n_gh = len(gh["opened"]) if gh["ok"] else "—"
    n_fs = len(fs["items"]) if fs["ok"] else "—"
    n_ph = len(ph["items"]) if ph["ok"] else "—"
    L.append(f"GitHub translated issue **{n_gh}**（translated {len(gh['closed']) if gh['ok'] else '—'}） · translated **{n_fs}** · translatedusetranslated **{n_ph}**")
    L.append("")

    # GitHub
    L.append(f"**GitHub**（[{REPO}](https://github.com/{REPO}/issues)）")
    if not gh["ok"]:
        L.append(f"- translated：{gh['note']}")
    elif not gh["opened"]:
        L.append("- translated issue。")
    else:
        for i in gh["opened"][:15]:
            tag = f"[{', '.join(i['labels'])}] " if i["labels"] else ""
            st = "" if i["state"] == "open" else " ✓translated"
            L.append(f"- [#{i['number']}]({i['url']}) {tag}{_trunc(i['title'], 70)}{st}")
        if len(gh["opened"]) > 15:
            L.append(f"- … translated {len(gh['opened']) - 15} translated")
    L.append("")

    # translated
    L.append(f"**translated**（[translated]({FEISHU_BASE_URL})）")
    if not fs["ok"]:
        L.append(f"- translated：{fs['note']}")
    elif not fs["items"]:
        L.append("- translated。")
    else:
        for it in fs["items"][:15]:
            meta = " · ".join(x for x in [it["type"], it["platform"], it["version"]] if x)
            extra = " 📎" if it["has_attachment"] else ""
            contact = f" — {it['contact']}" if it["contact"] else ""
            L.append(f"- {meta and f'[{meta}] '}{_trunc(it['content'], 90)}{extra}{contact}")
        if len(fs["items"]) > 15:
            L.append(f"- … translated {len(fs['items']) - 15} translated")
    L.append("")

    # PostHog
    L.append("**translatedusetranslated**（PostHog）")
    if not ph["ok"]:
        L.append(f"- translated：{ph['note']}")
    elif not ph["items"]:
        L.append("- translatedusetranslated。")
    else:
        by_cat: dict[str, int] = {}
        by_src: dict[str, int] = {}
        for it in ph["items"]:
            by_cat[CATEGORY_LABEL.get(str(it.get("category")), str(it.get("category")))] = by_cat.get(CATEGORY_LABEL.get(str(it.get("category")), str(it.get("category"))), 0) + 1
            by_src[str(it.get("source") or "—")] = by_src.get(str(it.get("source") or "—"), 0) + 1
        L.append("- translated：" + " · ".join(f"{k} {v}" for k, v in sorted(by_cat.items(), key=lambda kv: -kv[1])) +
                 "；translated：" + " · ".join(f"{k} {v}" for k, v in sorted(by_src.items(), key=lambda kv: -kv[1])) +
                 (f"；Survey translated {ph['survey_responses']}" if ph["survey_responses"] else ""))
        for it in ph["items"][:12]:
            meta = " · ".join(str(x) for x in [CATEGORY_LABEL.get(str(it.get("category")), it.get("category")), it.get("app_version"), it.get("os"),
                                              (f"{it.get('llm_provider')}/{it.get('llm_model')}" if it.get("llm_provider") else None)] if x)
            err = f"  `{_trunc(str(it['error_message']), 60)}`" if it.get("error_message") else ""
            L.append(f"- [{meta}] {_trunc(str(it.get('text') or ''), 90)}{err}")
        if len(ph["items"]) > 12:
            L.append(f"- … translated {len(ph['items']) - 12} translated")
    L.append("")
    L.append("_translatedandtranslated agent translatedintranslated。_")
    return "\n".join(L)


# ---------------------------------------------------------------- send ---
def post_feishu(markdown: str, title: str = "AutoClip translated") -> None:
    url = os.environ.get("FEISHU_WEBHOOK_URL")
    if not url:
        raise SystemExit("translatedconfig FEISHU_WEBHOOK_URL，translated。")
    body: dict[str, Any] = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": title}, "template": "grey"},
            "elements": [{"tag": "markdown", "content": markdown}],
        },
    }
    secret = os.environ.get("FEISHU_WEBHOOK_SECRET")
    if secret:
        ts = str(int(dt.datetime.now(dt.timezone.utc).timestamp()))
        string_to_sign = f"{ts}\n{secret}"
        sign = base64.b64encode(hmac.new(string_to_sign.encode("utf-8"), b"", digestmod=hashlib.sha256).digest()).decode()
        body["timestamp"], body["sign"] = ts, sign
    r = _http_json(url, method="POST", body=body)
    if r.get("code") not in (0, None) or (r.get("StatusCode") not in (0, None)):
        raise SystemExit(f"translated webhook returnerror：{r}")
    print("translated。", file=sys.stderr)


# ---------------------------------------------------------------- main ---
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7, help="translated（translated），default 7")
    ap.add_argument("--json", action="store_true", help="translated JSON translatedIs markdown")
    ap.add_argument("--post", action="store_true", help="translated（translated FEISHU_WEBHOOK_URL）")
    ap.add_argument("--message-file", help="translatedthis filetranslated's markdown（translatedIs agent translated'sversion），translatedIstranslated's")
    ap.add_argument("--title", default="AutoClip translated")
    args = ap.parse_args()

    if args.post and args.message_file:
        with open(args.message_file, encoding="utf-8") as f:
            post_feishu(f.read(), args.title)
        return 0

    until = dt.datetime.now(dt.timezone.utc)
    since = until - dt.timedelta(days=args.days)
    data = {
        "window": {"since": since.isoformat(), "until": until.isoformat(), "days": args.days},
        "github": fetch_github(since),
        "feishu_form": fetch_feishu_form(since),
        "posthog": fetch_posthog(since, args.days),
    }
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    md = render_markdown(data)
    print(md)
    if args.post:
        post_feishu(md, args.title)
    return 0


if __name__ == "__main__":
    sys.exit(main())
