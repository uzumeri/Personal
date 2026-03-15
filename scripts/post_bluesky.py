# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Post to Bluesky from a text file.

Usage:
    python scripts/post_bluesky.py published/YYYY-MM-DD-slug-bluesky-post.txt

Requires a .env file in the repo root with:
    BLUESKY_HANDLE=your-handle.bsky.social
    BLUESKY_APP_PASSWORD=your-app-password

Generate an App Password at: https://bsky.app/settings/app-passwords
Do NOT use your main account password.
"""

import sys
import os
import json
from urllib import request, error, parse
from pathlib import Path


def loadEnv(envPath):
    """Load key=value pairs from a .env file into a dict."""
    env = {}
    if envPath.exists():
        for line in envPath.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip().strip("'\"")
    return env


def createSession(handle, appPassword):
    """Authenticate with Bluesky and return the session (DID + access token)."""
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    payload = json.dumps({"identifier": handle, "password": appPassword}).encode()
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read())
    except error.HTTPError as e:
        body = e.read().decode()
        print(f"Authentication failed ({e.code}): {body}")
        sys.exit(1)


def createPost(session, text):
    """Create a post on Bluesky. Detects URLs and adds link facets."""
    import re
    from datetime import datetime, timezone

    did = session["did"]
    token = session["accessJwt"]

    # Build facets for any URLs in the text
    facets = []
    urlPattern = re.compile(r"https?://\S+")
    for match in urlPattern.finditer(text):
        byteStart = len(text[: match.start()].encode("utf-8"))
        byteEnd = len(text[: match.end()].encode("utf-8"))
        facets.append(
            {
                "index": {"byteStart": byteStart, "byteEnd": byteEnd},
                "features": [{"$type": "app.bsky.richtext.facet#link", "uri": match.group()}],
            }
        )

    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    if facets:
        record["facets"] = facets

    payload = json.dumps(
        {"repo": did, "collection": "app.bsky.feed.post", "record": record}
    ).encode()

    url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    try:
        with request.urlopen(req) as resp:
            result = json.loads(resp.read())
            return result
    except error.HTTPError as e:
        body = e.read().decode()
        print(f"Post failed ({e.code}): {body}")
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/post_bluesky.py <path-to-bluesky-post.txt>")
        sys.exit(1)

    postFile = Path(sys.argv[1])
    if not postFile.exists():
        print(f"File not found: {postFile}")
        sys.exit(1)

    text = postFile.read_text().strip()
    if len(text.encode("utf-8")) > 300:
        print(f"Warning: Post is {len(text.encode('utf-8'))} bytes (Bluesky limit is 300).")
        print("The post may be truncated. Edit the file and try again.")
        sys.exit(1)

    # Load credentials
    repoRoot = Path(__file__).resolve().parent.parent
    env = loadEnv(repoRoot / ".env")
    handle = env.get("BLUESKY_HANDLE", os.environ.get("BLUESKY_HANDLE", ""))
    appPassword = env.get("BLUESKY_APP_PASSWORD", os.environ.get("BLUESKY_APP_PASSWORD", ""))

    if not handle or not appPassword:
        print("Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD.")
        print("Add them to .env in the repo root, or set as environment variables.")
        print("Generate an App Password at: https://bsky.app/settings/app-passwords")
        sys.exit(1)

    # Confirm before posting
    print(f"About to post to Bluesky as @{handle}:")
    print("-" * 40)
    print(text)
    print("-" * 40)
    confirm = input("Post this? [y/N] ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        sys.exit(0)

    # Authenticate and post
    print("Authenticating...")
    session = createSession(handle, appPassword)
    print(f"Authenticated as {session['handle']}")

    print("Posting...")
    result = createPost(session, text)
    print(f"Posted successfully!")
    print(f"URI: {result.get('uri', 'unknown')}")

    # Construct web URL from URI
    uri = result.get("uri", "")
    if uri.startswith("at://"):
        parts = uri.replace("at://", "").split("/")
        if len(parts) >= 3:
            webUrl = f"https://bsky.app/profile/{parts[0]}/post/{parts[2]}"
            print(f"View: {webUrl}")


if __name__ == "__main__":
    main()
