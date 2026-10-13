"""Compare browser-observed draft data with the approved article package."""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parent
manifest = json.loads((root / "publication-manifest.json").read_text())
expected = json.loads((root / "expected-blocks.json").read_text())
observed = json.loads((root / "x-editor-observation.json").read_text())
normalize = lambda text: re.sub(r"\s+", " ", text).strip()
expected_text = [normalize(x["text"]) for x in expected if normalize(x["text"])]
actual_text = [normalize(x["text"]) for x in observed["blocks"]
               if x["tag"] != "SECTION" and normalize(x["text"])]
figures = []
for index, block in enumerate(observed["blocks"]):
    if block["tag"] == "SECTION":
        previous = observed["blocks"][index - 1]["text"] if index else ""
        following = observed["blocks"][index + 1]["text"] if index + 1 < len(observed["blocks"]) else ""
        figures.append({"previous": previous, "following": following, "alt": block.get("alt")})
placement = len(figures) == len(manifest["inline_figures"]) and all(
    expected_figure["caption"] in (figure["previous"], figure["following"])
    for figure, expected_figure in zip(figures, manifest["inline_figures"])
)
alt_match = len(figures) == len(manifest["inline_figures"]) and all(
    figure["alt"] == expected_figure["alt"]
    for figure, expected_figure in zip(figures, manifest["inline_figures"])
)
result = {
    "title_matches": observed["title"] == manifest["title"],
    "source_unchanged": hashlib.sha256(Path(manifest["source_path"]).read_bytes()).hexdigest() == manifest["source_sha256"],
    "expected_text_blocks": len(expected_text),
    "observed_text_blocks": len(actual_text),
    "text_and_order_match": expected_text == actual_text,
    "headings": observed["headings"],
    "prompt_blocks": observed["prompt_blocks"],
    "inline_image_count": len(figures),
    "image_order_and_placement_match": placement,
    "inline_alt_text_matches": alt_match,
    "links": observed["links"],
    "published": False,
}
(root / "draft-verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({key: value for key, value in result.items() if key != "links"}, indent=2))
