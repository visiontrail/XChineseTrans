# Video Director

A Codex Skill for making original videos through six production stages:

1. Director brief
2. Shot plan
3. Shared timeline
4. Motion and sound
5. Review and revision
6. Final-file verification

Use it for explanations, product films, motion graphics, visual stories, or other authored sequences. The subject, style, duration, shot count, rendering tools, and use of audio follow the brief.

## Install and invoke

Download `video-director.zip`. Extract its `video-director` folder into `~/.codex/skills/`, so the entrypoint is `~/.codex/skills/video-director/SKILL.md`.

In a Codex task with the skill available, invoke `$video-director` and describe your topic, audience, and intended output. Include an existing brand or project when relevant. The skill guides production through a playable video and editable source.

The workflow does not require one particular video stack. The optional delivery checker needs Python 3 and FFmpeg/ffprobe on PATH; it has no third-party Python dependencies.

## Contents

- `SKILL.md`: the production workflow.
- `agents/openai.yaml`: Codex UI metadata.
- `references/timeline.md`: timing semantics and an adaptable manifest.
- `scripts/check_delivery.py`: full decode, stream metadata, optional frame-timing comparison, loudness measurements, and review-frame extraction.

The checker reports evidence; it does not assess visual quality or listen to audio. Compare dimensions, audio presence, color, and measured loudness against the actual brief separately.
