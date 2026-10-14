#!/usr/bin/env python3
"""Inspect the encoded file. Standard library + FFmpeg/ffprobe; no visual verdict."""
from pathlib import Path
from fractions import Fraction
import argparse, json, math, shutil, subprocess, sys


def run(args):
    r = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode:
        raise RuntimeError(f"{Path(args[0]).name} failed ({r.returncode}): {r.stderr[-2500:]}")
    return r


def validate_timeline(t):
    if not isinstance(t, dict):
        raise ValueError('timeline must be a JSON object')
    fps, total = t.get('fps'), t.get('duration_frames')
    if isinstance(fps, bool) or not isinstance(fps, (float, int)) or not math.isfinite(fps) or fps <= 0:
        raise ValueError('fps must be a positive finite number')
    if isinstance(total, bool) or not isinstance(total, int) or total < 1:
        raise ValueError('duration_frames must be a positive integer')
    shots = t.get('shots')
    if not isinstance(shots, list) or not shots:
        raise ValueError('shots must be a nonempty ordered list')
    cursor, ids, indices = 0, set(), {0, total - 1}
    for s in shots:
        if not isinstance(s, dict):
            raise ValueError('each shot must be an object')
        ident, start, end = s.get('id'), s.get('start'), s.get('end')
        if not isinstance(ident, str) or not ident or ident in ids:
            raise ValueError('shot ids must be nonempty and unique')
        if any(isinstance(n, bool) or not isinstance(n, int) for n in (start, end)):
            raise ValueError(f'{ident}: boundaries must be integer frames')
        if start != cursor or not start < end <= total:
            raise ValueError(f'{ident}: shots must be ordered, contiguous, and inside duration')
        ids.add(ident); cursor = end
        indices.add((start + end - 1) // 2)
        indices.update(n for n in (start - 1, start, start + 1, end - 1, end, end + 1) if 0 <= n < total)
    if cursor != total:
        raise ValueError('shots do not cover the full duration')
    event_ids = set()
    events = t.get('events', [])
    if not isinstance(events, list):
        raise ValueError('events must be a list')
    for e in events:
        if not isinstance(e, dict):
            raise ValueError('each event must be an object')
        ident, frame = e.get('id'), e.get('frame')
        if not isinstance(ident, str) or not ident or ident in event_ids:
            raise ValueError('event ids must be nonempty and unique')
        if isinstance(frame, bool) or not isinstance(frame, int) or not 0 <= frame < total:
            raise ValueError(f'{ident}: event frame outside composition')
        event_ids.add(ident)
        indices.update(n for n in (frame - 1, frame, frame + 1) if 0 <= n < total)
    return sorted(indices)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('video', type=Path)
    p.add_argument('--timeline', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--extract', action='store_true')
    a = p.parse_args()
    report = {'video': str(a.video.resolve()), 'checks_passed': False,
              'visual_review': 'not performed by this script',
              'audio_listening': 'not performed by this script'}
    a.out.mkdir(parents=True, exist_ok=True)
    try:
        ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
        if not ffmpeg or not ffprobe:
            raise RuntimeError('FFmpeg and ffprobe must be installed and available on PATH')
        if not a.video.is_file():
            raise ValueError(f'Video file not found: {a.video}')
        timeline = json.loads(a.timeline.read_text()) if a.timeline else None
        indices = validate_timeline(timeline) if timeline is not None else None
        info = json.loads(run([ffprobe, '-v', 'error', '-count_frames', '-show_streams',
                               '-show_format', '-of', 'json', str(a.video)]).stdout)
        streams = info['streams']
        v = next((s for s in streams if s['codec_type'] == 'video' and not s.get('disposition', {}).get('attached_pic')), None)
        if v is None:
            raise ValueError('No video stream found')
        decoded_frames = int(v['nb_read_frames'])
        rate = float(Fraction(v['avg_frame_rate']))
        run([ffmpeg, '-v', 'error', '-xerror', '-err_detect', 'explode', '-i', str(a.video),
             '-map', f"0:{v['index']}", '-map', '0:a?', '-f', 'null', '-'])
        report['timestamp_cadence'] = 'not checked; no frame timeline supplied'
        report.update(full_decode_passed=True, decoded_frames=decoded_frames, fps=rate,
                      width=v['width'], height=v['height'], streams=streams, format=info['format'])
        failures = []
        if timeline is not None:
            expected_duration = timeline['duration_frames'] / timeline['fps']
            actual_duration = float(v.get('duration', info['format'].get('duration', 0)))
            frame_data = json.loads(run([ffprobe, '-v', 'error', '-select_streams', str(v['index']),
                '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(a.video)]).stdout)
            pts = [float(f['best_effort_timestamp_time']) for f in frame_data['frames']]
            tick = float(Fraction(v['time_base']))
            tolerance = max(tick + 1e-6, 2e-6)
            cadence_error = max(abs((t - pts[0]) - n / timeline['fps']) for n, t in enumerate(pts))
            report['timestamp_cadence'] = {'checked_frames': len(pts), 'max_error_seconds': cadence_error,
                'tolerance_seconds': tolerance, 'origin_seconds': pts[0]}
            comparisons = {
                'timestamp_cadence': len(pts) == timeline['duration_frames'] and cadence_error <= tolerance,
                'frames': decoded_frames == timeline['duration_frames'],
                'fps': math.isclose(rate, timeline['fps'], rel_tol=1e-5, abs_tol=1e-5),
                'duration': abs(actual_duration - expected_duration) <= 1 / timeline['fps'] + 1e-3}
            report['timeline_comparison'] = comparisons
            failures.extend(k for k, passed in comparisons.items() if not passed)
        if indices is None:
            indices = sorted({0, decoded_frames // 2, decoded_frames - 1})
        report['review_frame_indices'] = indices
        audio_streams = [s for s in streams if s['codec_type'] == 'audio']
        report['audio_present'] = bool(audio_streams)
        if audio_streams:
            result = run([ffmpeg, '-hide_banner', '-nostats', '-i', str(a.video), '-map', '0:a:0',
                          '-vn', '-af', 'loudnorm=print_format=json', '-f', 'null', '-'])
            start = result.stderr.rfind('{')
            measured = json.JSONDecoder().raw_decode(result.stderr[start:])[0]
            report['audio_measurement'] = {k: measured[k] for k in ('input_i', 'input_tp', 'input_lra', 'input_thresh')}
            report['audio_measurement_note'] = 'First audio stream; LUFS integrated and dBTP true peak; report only, no universal target.'
        if a.extract and not failures:
            selected = a.out / 'frames'; selected.mkdir(exist_ok=True)
            expression = '+'.join(f'eq(n\\,{n})' for n in indices)
            run([ffmpeg, '-v', 'error', '-y', '-i', str(a.video), '-map', f"0:{v['index']}",
                 '-vf', f'select={expression}', '-fps_mode', 'vfr', '-q:v', '2', str(selected / '%06d.jpg')])
            # Index maps sequence filenames to actual zero-based frame numbers.
            report['extracted_frames'] = [{'file': f'frames/{i:06d}.jpg', 'frame': n} for i, n in enumerate(indices, 1)]
        report['checks_passed'] = not failures
        if failures:
            report['error'] = 'Timeline mismatches: ' + ', '.join(failures)
    except (ValueError, KeyError, TypeError, OSError, RuntimeError, StopIteration, ZeroDivisionError) as e:
        report['error'] = str(e)
    (a.out / 'delivery-check.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ('checks_passed', 'decoded_frames', 'audio_present', 'error') if k in report}, ensure_ascii=False))
    return 0 if report['checks_passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
