# Source and review notes

- Supplied: https://x.com/xingbugengming/status/2114987011480367262 (inspected in Ego Lite on 2026-10-28). It embeds an 8:39 boss-fight video, but quotes a different three.js game. The quoted post is not the relevant source for this story.
- Original creator: https://www.youtube.com/watch?v=z1mgtUvTdqg, “I Made a Full Boss Fight in Unreal Engine With AI”, Can It Code? The creator's X profile https://x.com/CanItCode currently shows an earlier animation demonstration, not the boss-fight video. Do not substitute that earlier post as a Quote target.
- The creator describes Unreal Engine 5.8, Claude Opus 5.5 for code, GPT Astra for images and textures, Tripo for models, Seedance for boss motion, and NVIDIA Kimodo for hero motion. A demo is not evidence of a full AAA game or independent verification of functionality.
- https://github.com/canitcode/video2rig documents the public AGPL-3.0 animation tool: train a joint reader per creature, extract motion from generated video, and transfer it to an editable Blender rig. This is not a release of the whole game project. No local test of the tool or playable build has been performed.
- Intended format: standalone English post with complete freshly retrieved original video, subject to final review. Status: media retrieval and composer validation pending; no publication submitted.

## Media evidence

- Original acquired 2026-10-28 00:45 Singapore from https://www.youtube.com/watch?v=z1mgtUvTdqg, yt-dlp 2026.10.26, YouTube formats 398 and 251-7 (original English audio). Merged file `original-youtube.mp4`: 54,245,679 bytes, SHA-256 `6b3b4583fcfee6f5151d7b5ea8ec4a316d198b36d8a2b6d5360b16afc96540bd`, 519.874 seconds, 1280x720, AV1/Opus. Full ffmpeg decode passed. Frames checked at 5, 260, 510 seconds. No added Chinese subtitles visible in those frames.
- `upload.mp4`: full-duration H.264/AAC transcode from original; 126,235,975 bytes, SHA-256 `cbc5740268f7545370d1e163e4c202f8d2ba0e32f4044dddf06c59901d0502b3`. No trimming. Both files kept locally and excluded from Git due to size.
- The intermediary's fresh 360p copy is `source-reupload-360.mp4`, fetched from https://video.twimg.com/amplify_video/2114968090572419073/vid/avc1/640x360/eIMVoNmBsWwE_nv-.mp4?tag=29 on 2026-10-28 00:44 Singapore; 25,436,564 bytes; SHA-256 `47b6f2412bc3949db99595668e38720f04626496f605847f054adafe0d61d200`; 519.941 seconds, H.264/AAC, complete decode passed. Frames at 5 and 510 seconds show added Chinese subtitles. It is not the selected upload.
- Representative audio listening has not been performed; encoding and decode checks alone are not a judgment of audio quality.
