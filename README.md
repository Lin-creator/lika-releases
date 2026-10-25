# lika releases

Signed builds of lika, a low-latency karaoke mic processor for Apple Silicon Macs (macOS 14 or later), and the feed lika checks for Updates.

## Installing

1. Download the newest `lika-<version>.zip` from [Releases](https://github.com/Lin-creator/lika-releases/releases) and open it.
2. Move `lika.app` to Applications.
3. Open it. macOS refuses the first time, because lika isn't signed by an Apple Developer ID. Open System Settings → Privacy & Security, scroll down to the line about lika, and click **Open Anyway**.

You need to do this only once. After that, lika installs its own Updates.

## How a release gets here

The source lives in a private repository. `make release` there builds and tests lika, tags the version and uploads the unsigned app here as a draft release. Then [the release workflow](.github/workflows/release.yml) code-signs it with the "lika Release Signing" certificate, signs the zip for Sparkle, publishes the release and adds it to the appcast on the `gh-pages` branch, served at <https://lin-creator.github.io/lika-releases/appcast.xml>.
