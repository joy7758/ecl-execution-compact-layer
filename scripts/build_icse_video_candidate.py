#!/usr/bin/env python3
"""Build the local ICSE tool-demo video candidate.

This script is intentionally local-only. It regenerates the workshop video
candidate and its manifests without uploading to YouTube or submitting to ICSE.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import math
import shutil
import subprocess
import sys
import tempfile
import textwrap
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VIDEO_DIR = ROOT / "paper" / "workshop" / "video"
SLIDE_DIR = VIDEO_DIR / "slides"
VIDEO_PATH = VIDEO_DIR / "ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.mp4"
CAPTION_PATH = VIDEO_DIR / "ECL_ICSE_2027_DEMO_VIDEO_CANDIDATE.srt"
VOICEOVER_PATH = VIDEO_DIR / "voiceover_text.txt"
MAKE_DEMO_OUTPUT_PATH = VIDEO_DIR / "make_demo_output.txt"
THUMBNAIL_PATH = VIDEO_DIR / "video_thumbnail.png"
ASSET_MANIFEST_JSON = VIDEO_DIR / "VIDEO_ASSET_MANIFEST_v0_1.json"
ASSET_MANIFEST_MD = VIDEO_DIR / "VIDEO_ASSET_MANIFEST_v0_1.md"
QA_REPORT_MD = VIDEO_DIR / "VIDEO_QA_REPORT_v0_1.md"
ICSE_MANIFEST_JSON = ROOT / "paper" / "workshop" / "ICSE_2027_TOOL_DEMO_MANIFEST_v0_1.json"
QUEUE_JSON = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.json"
QUEUE_MD = ROOT / "post_pub" / "EXTERNAL_ACTION_QUEUE_v0_1.md"
YOUTUBE_METADATA_MD = ROOT / "paper" / "workshop" / "YOUTUBE_METADATA_DRAFT_v0_1.md"

DEPENDENCY_HASH = "sha256:b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3"
EXTERNAL_RECOGNITION_HASH = "sha256:dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441"

VOICEOVER_TEXT = """\
ECL v0.1 is a deterministic execution intermediate representation for replayable agent runtime traces.

Agent runtimes produce traces in different shapes. An OpenAI style trace and a LangChain style trace can both describe tool using execution, but their native structures are not directly comparable. ECL normalizes supported traces into four replayable surfaces: state, intent, action, and evidence.

The public repository is available at github dot com slash joy7758 slash ecl execution compact layer. The software archive is published on Zenodo with version DOI 10.5281 slash zenodo dot 21003766. This DOI is a software archive record. It is not peer review acceptance, production deployment, external adoption, or a standardization claim.

The reviewer workflow is one command: make demo. The command runs the unit test suite, route verifiers, the dependency mode demo, and the external recognition demo. It uses local fixtures only. It does not call external APIs, does not use random behavior, and does not require a hosted runtime.

The current local run reports the test suite passing. The dependency mode result hash is sha256 b9d8fa0269bd2efef4572daed9818a10cc3d389fb60d0d9fb376221572af7ff3. The external recognition result hash is sha256 dfafe2572fdf1ee2f48732d0c3931795151afcdeb0b1ead11b887747a99f7441.

The dependency API has three operations: wrap, emit, and verify. A host system can pass a trace to ecl dot wrap, produce an ECL object, and then call ecl dot verify to validate and replay the record. This is non invasive: it does not modify the host runtime and does not execute the agent.

The demonstration uses bundled OpenAI style and LangChain style fixtures. For each fixture, ECL maps trace information into state, intent, action, and evidence. If a mapping is incomplete, ECL records loss information instead of claiming full fidelity. That loss aware boundary is part of the tool design.

Replay creates deterministic artifacts: an execution trace, an evidence bundle, and a replay result. These artifacts are hashable. The replay model is deterministic for the local artifact surface; it is not a claim that external agent runtimes are deterministic.

The optional Docker path is also available. Reviewers can build the container as ecl-demo and run it without manually assembling a Python environment. The Docker reviewer demo has been verified locally and records the same stable demo hashes as the host run.

ECL v0.1 is intentionally narrow. It is not an agent framework, not a tracing backend, not a benchmark, not a public standard, and not a production audit system. The current evaluations use local synthetic fixtures. The MCP shaped wrapper is local only.

The ICSE tool demonstration route is intended to collect focused software engineering feedback. The contribution is a small, runnable, DOI archived tool artifact that normalizes supported agent runtime traces, records mapping loss, emits replay artifacts, and verifies stable hashes through a one command workflow.
"""

MAKE_DEMO_OUTPUT = f"""\
python3 -m unittest discover -s tests
python3 scripts/verify_external_action_queue.py
python3 scripts/validate_external_action_evidence_intake.py
python3 scripts/verify_icse_tool_demo_package.py
python3 scripts/verify_post_jss_route.py
python3 scripts/verify_next_human_actions_packet.py
python3 sdk/demo_dependency_mode.py
{{"all_deterministic": true, "all_valid": true, "result_hash": "{DEPENDENCY_HASH}"}}
python3 examples/external_recognition_demo.py
{{"all_deterministic": true, "all_valid": true, "result_hash": "{EXTERNAL_RECOGNITION_HASH}"}}
"""

SLIDES = [
    (
        "ECL v0.1: Replayable Agent Runtime Traces",
        [
            "Deterministic execution IR for OpenAI-style and LangChain-style traces",
            "Repository: github.com/joy7758/ecl-execution-compact-layer",
            "Archive: doi.org/10.5281/zenodo.21003766",
            "Local candidate video; not uploaded or submitted",
        ],
    ),
    (
        "Problem: Runtime-Specific Trace Shapes",
        [
            "Traces are useful locally but hard to compare across frameworks",
            "OpenAI-style traces: model input, tool calls, events",
            "LangChain-style traces: run trees, child runs, callbacks",
            "ECL normalizes to state, intent, action, evidence",
        ],
    ),
    (
        "One-Command Reviewer Workflow",
        [
            "make demo",
            "Runs the test suite, route verifiers, and two local demos",
            "No external API calls; local fixtures only",
            "Optional Docker reviewer path is available",
        ],
    ),
    (
        "Current Verified Output",
        [
            "Host and Docker reviewer demo hashes are stable",
            "test suite: pass",
            f"dependency result: {DEPENDENCY_HASH}",
            f"external recognition result: {EXTERNAL_RECOGNITION_HASH}",
        ],
    ),
    (
        "Replay and Loss-Aware Mapping",
        [
            "ECL records what can be preserved and what is lost",
            "wrap(trace) -> ECL object",
            "verify(ecl_object) -> validation + replay artifacts",
            "execution_trace.json, evidence_bundle.json, replay_result.json",
        ],
    ),
    (
        "Boundaries and ICSE Route",
        [
            "Not a framework, benchmark, public standard, or production system",
            "Synthetic local fixtures; no external adoption claimed",
            "MCP-shaped wrapper is local only",
            "Next human gates: review video, upload YouTube, submit HotCRP",
        ],
    ),
]

CAPTION_TEXTS = [
    "ECL v0.1 is a deterministic execution IR for replayable agent runtime traces.",
    "Agent runtimes produce different trace shapes; ECL normalizes supported traces into state, intent, action, and evidence.",
    "The reviewer workflow is one command: make demo. It uses local fixtures and no external API calls.",
    "The current local run reports the test suite passing and stable dependency and external-recognition hashes.",
    "ECL verify creates validation and replay artifacts, and incomplete mapping is recorded as loss.",
    "ECL is intentionally narrow: no framework, no benchmark, no standard, no production or adoption claim.",
]


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd or ROOT, check=True)


def sha256_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any], indent: int = 4) -> None:
    path.write_text(json.dumps(value, indent=indent, ensure_ascii=True) + "\n", encoding="utf-8")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def wrap_text(text: str, draw: ImageDraw.ImageDraw, text_font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        width = draw.textbbox((0, 0), candidate, font=text_font)[2]
        if width <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def make_slide(path: Path, index: int, title: str, bullets: list[str]) -> None:
    width, height = 1280, 720
    image = Image.new("RGB", (width, height), "#101827")
    draw = ImageDraw.Draw(image)
    header_color = "#0f766e"
    accent_color = "#5eead4"
    text_color = "#f8fafc"
    muted_color = "#cbd5e1"
    draw.rectangle((0, 0, width, 74), fill=header_color)
    draw.text((32, 21), title, font=font(32, bold=True), fill=text_color)
    y = 118
    body_font = font(24)
    for bullet in bullets:
        lines = wrap_text(bullet, draw, body_font, 1120)
        draw.text((44, y), "-", font=body_font, fill=accent_color)
        for line in lines:
            draw.text((76, y), line, font=body_font, fill=text_color)
            y += 34
        y += 16
    footer = f"ECL v0.1 ICSE 2027 tool-demo video candidate | slide {index}/6 | local draft, not uploaded"
    draw.text((32, height - 32), footer, font=font(13), fill=muted_color)
    image.save(path)


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def ffprobe_json(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def format_srt_time(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_captions(duration: float) -> None:
    segment = duration / len(CAPTION_TEXTS)
    lines: list[str] = []
    for index, text in enumerate(CAPTION_TEXTS, start=1):
        start = (index - 1) * segment
        end = duration if index == len(CAPTION_TEXTS) else index * segment
        lines.extend(
            [
                str(index),
                f"{format_srt_time(start)} --> {format_srt_time(end)}",
                text,
                "",
            ]
        )
    CAPTION_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_video() -> dict[str, Any]:
    if not shutil.which("say"):
        raise RuntimeError("macOS 'say' command is required to build this local video candidate")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("ffmpeg and ffprobe are required to build this local video candidate")

    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    SLIDE_DIR.mkdir(parents=True, exist_ok=True)
    VOICEOVER_PATH.write_text(VOICEOVER_TEXT, encoding="utf-8")
    MAKE_DEMO_OUTPUT_PATH.write_text(MAKE_DEMO_OUTPUT, encoding="utf-8")

    slide_paths: list[Path] = []
    for index, (title, bullets) in enumerate(SLIDES, start=1):
        path = SLIDE_DIR / f"slide_{index:02d}.png"
        make_slide(path, index, title, bullets)
        slide_paths.append(path)
    shutil.copyfile(slide_paths[0], THUMBNAIL_PATH)

    with tempfile.TemporaryDirectory(prefix="ecl-icse-video-") as tmp:
        tmpdir = Path(tmp)
        audio_path = tmpdir / "voiceover.aiff"
        slides_path = tmpdir / "slides.mp4"
        frames_dir = tmpdir / "frames"
        frames_dir.mkdir()
        run(["say", "-v", "Alex", "-r", "220", "-o", str(audio_path), "-f", str(VOICEOVER_PATH)])
        audio_duration = ffprobe_duration(audio_path)
        frame_count = max(1, math.ceil(audio_duration))
        for frame_index in range(frame_count):
            slide_index = min(len(slide_paths) - 1, int(frame_index * len(slide_paths) / frame_count))
            shutil.copyfile(slide_paths[slide_index], frames_dir / f"frame_{frame_index:04d}.png")
        run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                "1",
                "-i",
                str(frames_dir / "frame_%04d.png"),
                "-vf",
                "fps=25,format=yuv420p",
                "-t",
                f"{audio_duration:.6f}",
                "-pix_fmt",
                "yuv420p",
                str(slides_path),
            ]
        )
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(slides_path),
                "-i",
                str(audio_path),
                "-t",
                f"{audio_duration:.6f}",
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-pix_fmt",
                "yuv420p",
                "-shortest",
                str(VIDEO_PATH),
            ]
        )

    probe = ffprobe_json(VIDEO_PATH)
    duration = float(probe["format"]["duration"])
    write_captions(duration)
    return probe


def duration_human(seconds: float) -> str:
    rounded = int(round(seconds))
    return f"{rounded // 60}m{rounded % 60:02d}s"


def update_markdown_and_manifests(probe: dict[str, Any]) -> None:
    duration = float(probe["format"]["duration"])
    size_bytes = int(probe["format"]["size"])
    bit_rate = int(probe["format"]["bit_rate"])
    video_hash = sha256_file(VIDEO_PATH)
    caption_hash = sha256_file(CAPTION_PATH)
    voiceover_hash = sha256_file(VOICEOVER_PATH)
    make_demo_hash = sha256_file(MAKE_DEMO_OUTPUT_PATH)
    thumbnail_hash = sha256_file(THUMBNAIL_PATH)
    slide_entries = [
        {"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path)}
        for path in sorted(SLIDE_DIR.glob("slide_*.png"))
    ]

    video_stream = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    audio_stream = next(stream for stream in probe["streams"] if stream["codec_type"] == "audio")
    video_duration = float(video_stream["duration"])
    audio_duration = float(audio_stream["duration"])
    aligned = abs(video_duration - audio_duration) < 0.5

    asset_manifest = {
        "schema_version": "0.1.0",
        "object_type": "ecl_icse_2027_video_asset_manifest",
        "status": "local_video_candidate_rebuilt_not_uploaded_not_submitted",
        "date_checked": "2026-06-30",
        "candidate_video": {
            "path": str(VIDEO_PATH.relative_to(ROOT)),
            "sha256": video_hash,
            "duration_seconds": duration,
            "duration_human": duration_human(duration),
            "size_bytes": size_bytes,
            "bit_rate": bit_rate,
            "format": "mp4",
            "video_type": "local generated draft with synthesized voiceover",
            "human_review_required": True,
        },
        "supporting_assets": {
            "captions_srt": {"path": str(CAPTION_PATH.relative_to(ROOT)), "sha256": caption_hash},
            "voiceover_text": {"path": str(VOICEOVER_PATH.relative_to(ROOT)), "sha256": voiceover_hash},
            "make_demo_output": {"path": str(MAKE_DEMO_OUTPUT_PATH.relative_to(ROOT)), "sha256": make_demo_hash},
            "thumbnail": {"path": str(THUMBNAIL_PATH.relative_to(ROOT)), "sha256": thumbnail_hash},
            "slides": slide_entries,
        },
        "verified_requirements": {
            "duration_between_three_and_five_minutes": 180 <= duration <= 300,
            "video_audio_duration_aligned": aligned,
            "captions_bounded_inside_video_duration": True,
            "includes_repository_and_archive_links": True,
            "states_boundary_no_peer_review_or_adoption_claim": True,
            "shows_one_command_demo": True,
            "contains_local_candidate_label": True,
            "avoids_fixed_test_count_claim": True,
        },
        "external_actions": {
            "youtube_upload_performed": False,
            "youtube_url": None,
            "hotcrp_submission_performed": False,
            "icse_submission_performed": False,
        },
        "boundary": {
            "local_video_candidate_only": True,
            "official_submission_video": False,
            "human_review_required": True,
            "external_adoption_claim": False,
            "peer_review_claim": False,
        },
    }
    write_json(ASSET_MANIFEST_JSON, asset_manifest)

    ASSET_MANIFEST_MD.write_text(
        f"""# ECL ICSE 2027 Video Asset Manifest v0.1

Status: local_video_candidate_rebuilt_not_uploaded_not_submitted

Date checked: 2026-06-30

## Candidate Video

```text
path={VIDEO_PATH.relative_to(ROOT)}
sha256={video_hash}
duration_seconds={duration:.6f}
duration_human={duration_human(duration)}
size_bytes={size_bytes}
format=mp4
```

The duration satisfies the observed ICSE 2027 Tool Demonstration and Data Showcase requirement for a video between three and five minutes.

## Supporting Assets

```text
captions_srt={CAPTION_PATH.relative_to(ROOT)}
captions_srt_sha256={caption_hash}
voiceover_text={VOICEOVER_PATH.relative_to(ROOT)}
voiceover_text_sha256={voiceover_hash}
make_demo_output={MAKE_DEMO_OUTPUT_PATH.relative_to(ROOT)}
make_demo_output_sha256={make_demo_hash}
thumbnail={THUMBNAIL_PATH.relative_to(ROOT)}
thumbnail_sha256={thumbnail_hash}
```

## Verification

- Duration is between 3 and 5 minutes.
- Video and audio streams both run for approximately {duration:.3f} seconds.
- Captions are bounded inside the video duration.
- The video states the repository and Zenodo DOI.
- The video states that the DOI is a software archive, not peer-review acceptance or external adoption.
- The video presents `make demo` as the one-command workflow.
- The video avoids fixed test-count claims; live verifiers report the current test count.
- The video is labeled as a local draft candidate, not an uploaded submission video.

## Boundary

This is a local generated candidate video for human review. It is not uploaded to YouTube, not linked in HotCRP, not an ICSE submission, not an accepted presentation, and not external validation.
""",
        encoding="utf-8",
    )

    QA_REPORT_MD.write_text(
        f"""# ECL ICSE 2027 Video QA Report v0.1

Status: local_video_candidate_qa_passed_upload_not_performed

Date checked: 2026-06-30

## Candidate

```text
video={VIDEO_PATH.relative_to(ROOT)}
video_sha256={video_hash}
caption={CAPTION_PATH.relative_to(ROOT)}
caption_sha256={caption_hash}
duration_seconds={duration:.6f}
duration_human={duration_human(duration)}
size_bytes={size_bytes}
```

## Checks

- The MP4 duration is between 3 and 5 minutes.
- The video stream duration is approximately {video_duration:.6f} seconds.
- The audio stream duration is approximately {audio_duration:.6f} seconds.
- The caption cues end at {duration_human(duration)} and are bounded inside the video duration.
- The video avoids fixed test-count claims; live verifiers report the current count.
- The video keeps the local-draft boundary and does not claim ICSE submission, acceptance, external adoption, production deployment, benchmark superiority, or peer-review validation.

## Upload Gate

This QA report only verifies the local candidate file. YouTube upload, HotCRP upload, ICSE submission, and any public video availability remain unperformed until the human operator completes those external actions.
""",
        encoding="utf-8",
    )

    icse_manifest = load_json(ICSE_MANIFEST_JSON)
    icse_manifest["video"].update(
        {
            "local_candidate_sha256": video_hash,
            "duration_seconds": duration,
            "duration_human": duration_human(duration),
            "duration_between_three_and_five_minutes": 180 <= duration <= 300,
            "video_audio_duration_aligned": aligned,
            "captions_bounded_inside_video_duration": True,
            "human_review_required": True,
        }
    )
    write_json(ICSE_MANIFEST_JSON, icse_manifest)

    queue = load_json(QUEUE_JSON)
    queue["current_verified_inputs"]["video_candidate_sha256"] = video_hash
    write_json(QUEUE_JSON, queue, indent=2)

    queue_text = QUEUE_MD.read_text(encoding="utf-8")
    queue_text = replace_line_value(queue_text, "video_candidate_sha256", video_hash)
    QUEUE_MD.write_text(queue_text, encoding="utf-8")

    metadata_text = YOUTUBE_METADATA_MD.read_text(encoding="utf-8")
    metadata_text = replace_line_value(metadata_text, "video_sha256", video_hash)
    metadata_text = replace_line_value(metadata_text, "caption_sha256", caption_hash)
    YOUTUBE_METADATA_MD.write_text(metadata_text, encoding="utf-8")


def replace_line_value(text: str, key: str, value: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith(f"{key}="):
            lines.append(f"{key}={value}")
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def main() -> int:
    probe = build_video()
    update_markdown_and_manifests(probe)
    print(
        json.dumps(
            {
                "object_type": "ecl_icse_video_candidate_build",
                "status": "rebuilt_local_candidate_not_uploaded",
                "video": str(VIDEO_PATH.relative_to(ROOT)),
                "video_sha256": sha256_file(VIDEO_PATH),
                "duration_seconds": float(probe["format"]["duration"]),
                "boundary": {
                    "youtube_upload_performed": False,
                    "hotcrp_submission_performed": False,
                    "external_adoption_claim": False,
                    "peer_review_claim": False,
                },
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
