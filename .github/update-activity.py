#!/usr/bin/env python3
"""Update the "Latest Activity" section of README.md with the user's last 5 GitHub events."""
import json
import urllib.request
import os
import re

USER = "Erfix404"
START = "<!-- LATEST-ACTIVITY:START -->"
END = "<!-- LATEST-ACTIVITY:END -->"


def gh_api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    req.add_header("User-Agent", "erfix-activity")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def repo_url(full):
    return f"https://github.com/{full}"


def fmt_event(e):
    t = e["type"]
    repo = e["repo"]["name"]
    url = repo_url(repo)
    created = e.get("created_at", "")[:10]
    if t == "PushEvent":
        commits = len(e.get("payload", {}).get("commits", []))
        if commits == 0:
            return None
        n = "commit" if commits == 1 else "commits"
        msg = e.get("payload", {}).get("commits", [{}])[0].get("message", "")[:60].replace("\n", " ")
        detail = f" — _{msg}_" if msg else ""
        return f"**`{created}`** · pushed **{commits} {n}** to [`{repo}`]({url}){detail}"
    if t == "CreateEvent":
        r = e.get("payload", {}).get("ref_type", "repo")
        ref = e.get("payload", {}).get("ref", "")
        extra = f" `{ref}`" if ref else ""
        return f"**`{created}`** · created **{r}**{extra} in [`{repo}`]({url})"
    if t == "PullRequestEvent":
        pr = e.get("payload", {}).get("pull_request", {})
        action = e.get("payload", {}).get("action", "opened")
        num = pr.get("number", "")
        return f"**`{created}`** · {action} PR [`{repo}#{num}`]({url}/pull/{num})"
    if t == "IssuesEvent":
        action = e.get("payload", {}).get("action", "opened")
        num = e.get("payload", {}).get("issue", {}).get("number", "")
        return f"**`{created}`** · {action} issue [`{repo}#{num}`]({url}/issues/{num})"
    if t == "WatchEvent":
        return f"**`{created}`** · ⭐ starred [`{repo}`]({url})"
    if t == "ForkEvent":
        return f"**`{created}`** · forked [`{repo}`]({url})"
    return f"**`{created}`** · {t} in [`{repo}`]({url})"


def main():
    try:
        events = gh_api(f"/users/{USER}/events/public?per_page=10")
    except Exception as exc:
        print(f"⚠️ could not fetch events: {exc}")
        return
    lines = ["\n", "<!-- LATEST-ACTIVITY:START -->\n"]
    shown = 0
    for e in events:
        if shown >= 5:
            break
        line = fmt_event(e)
        if line:
            lines.append(f"{line}\n\n")
            shown += 1
    lines.append("<!-- LATEST-ACTIVITY:END -->\n")

    block = "".join(lines)
    with open("README.md", encoding="utf-8") as f:
        readme = f.read()

    if START in readme and END in readme:
        readme = re.sub(rf"{START}.*?{END}", block, readme, flags=re.S)
    else:
        marker = "## 📡 Live Activity"
        if marker in readme:
            readme = readme.replace(marker, marker + "\n\n" + block)
        else:
            readme += "\n\n## 📡 Live Activity\n\n" + block

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("✅ latest activity section updated")


if __name__ == "__main__":
    main()
