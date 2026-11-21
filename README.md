# Arabic + European + Turkish IPTV playlist

An auto-generated, deduplicated M3U playlist for IPTV players, including Samsung Tizen M3U IPTV apps.

**Sources:** public IPTV-org country stream lists. Regions: Middle East, North Africa, Turkey, and EU countries (plus United Kingdom). Stream availability and regional restrictions vary. This project does not host video content.

## Setup
1. Create a **public** GitHub repository named `iptv-playlist` under your account.
2. Upload `build_playlist.py` and `.github/workflows/update.yml` from this archive, preserving directory paths.
3. In the repository's **Actions** tab, enable workflows and run **Refresh IPTV playlist** once (Workflow dispatch). Set Actions workflow permissions to *Read and write permissions* under Settings → Actions → General if necessary.
4. When `playlist.m3u` appears, enter this URL in your TV app:

   `https://cdn.jsdelivr.net/gh/YOUR-USERNAME/iptv-playlist@main/playlist.m3u`

   Replace `YOUR-USERNAME` with your actual GitHub username. For `Abduhus`, that is:

   `https://cdn.jsdelivr.net/gh/Abduhus/iptv-playlist@main/playlist.m3u`

For the freshest output, you can also try GitHub's raw-content URL:

`https://raw.githubusercontent.com/Abduhus/iptv-playlist/main/playlist.m3u`

GitHub Actions runs daily at 03:15 UTC. jsDelivr may cache older playlist versions. Source playlists can include dead, geo-restricted, or incompatible streams. This playlist is not guaranteed to play every channel.
