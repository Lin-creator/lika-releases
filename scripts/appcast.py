#!/usr/bin/env python3
"""Adds one release to lika's Sparkle appcast, newest first.

The release notes go in as the Markdown of their CHANGELOG.md section; lika's
own Updates page renders them, so Sparkle never shows them itself. A beta goes
on the `beta` channel, which lika reads only with "Include betas" on. Running
it again for the same version replaces that version's item.
"""

import argparse
import email.utils
import pathlib
import re
from xml.sax.saxutils import escape, quoteattr

EMPTY = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle">
  <channel>
    <title>lika</title>
    <link>https://lin-creator.github.io/lika-releases/appcast.xml</link>
    <description>Updates for lika.</description>
    <language>en</language>
  </channel>
</rss>
"""


def item(a, notes):
    channel = "\n      <sparkle:channel>beta</sparkle:channel>" if "-" in a.version else ""
    notes = notes.replace("]]>", "]]]]><![CDATA[>")
    return f"""    <item>
      <title>{escape(a.version)}</title>
      <pubDate>{email.utils.formatdate(usegmt=True)}</pubDate>
      <sparkle:version>{escape(a.build)}</sparkle:version>
      <sparkle:shortVersionString>{escape(a.version)}</sparkle:shortVersionString>
      <sparkle:minimumSystemVersion>{escape(a.minimum_system)}</sparkle:minimumSystemVersion>{channel}
      <description sparkle:format="markdown"><![CDATA[{notes}]]></description>
      <enclosure url={quoteattr(a.url)} length={quoteattr(a.length)} type="application/octet-stream" sparkle:edSignature={quoteattr(a.signature)}/>
    </item>
"""


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("appcast", type=pathlib.Path)
    p.add_argument("--version", required=True, help="full version, e.g. 1.0.0-beta.1")
    p.add_argument("--build", required=True, help="CFBundleVersion, which Sparkle compares")
    p.add_argument("--minimum-system", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--length", required=True)
    p.add_argument("--signature", required=True)
    p.add_argument("--notes", required=True, type=pathlib.Path)
    a = p.parse_args()

    feed = a.appcast.read_text() if a.appcast.exists() else EMPTY
    # Drop an earlier item for this version, from a re-run.
    own = re.compile(
        r"    <item>\n      <title>" + re.escape(escape(a.version)) + r"</title>\n.*?    </item>\n", re.S)
    feed = own.sub("", feed)

    new = item(a, a.notes.read_text().strip())
    first = feed.find("    <item>")
    at = first if first != -1 else feed.index("  </channel>")
    a.appcast.write_text(feed[:at] + new + feed[at:])


if __name__ == "__main__":
    main()
