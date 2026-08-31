# Helper (not the scheduled-task entrypoint itself) — reference implementation for
# rendering a single new Review N folder for one adviser, given a chosen
# {customerName, review}. Used by the recurring "check Airtable for new reviews" task.
import hashlib
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/sessions/sleepy-determined-hypatia/mnt/KnowledgeHUB"
TEMPLATES_DIR = f"{ROOT}/public/assets/trust-templates"
OUT_DIR = f"{ROOT}/public/assets/social-trust-content"
FONT_BOLD = f"{ROOT}/public/static/fonts/PlusJakartaSans-ExtraBold.ttf"
FONT_MED = f"{ROOT}/public/static/fonts/PlusJakartaSans-Medium.ttf"
SIZES = {"li": (1200, 630), "fb": (1200, 630), "ig": (1080, 1350), "tik": (1080, 1920), "square": (1200, 1200)}
CONFIG = json.load(open(f"{ROOT}/trust-template-config.json"))

MIN_SIZE = 40
MAX_SIZE = 96

def wrap_words(draw, words, max_width, font_path, size):
    font = ImageFont.truetype(font_path, size)
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def fit_text(draw, text, max_width, max_height, font_path, max_size=MAX_SIZE):
    words = text.split()
    for size in range(max_size, MIN_SIZE - 1, -1):
        font = ImageFont.truetype(font_path, size)
        lines = wrap_words(draw, words, max_width, font_path, size)
        line_h = size * 1.3
        if line_h * len(lines) <= max_height:
            return size, lines, line_h
    size = MIN_SIZE
    font = ImageFont.truetype(font_path, size)
    line_h = size * 1.3
    max_lines = max(1, int(max_height // line_h))
    lines = wrap_words(draw, words, max_width, font_path, size)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while draw.textlength(last + "…", font=font) > max_width and len(last) > 1:
            last = last[:-1].rstrip()
        lines[-1] = last + "…"
    return size, lines, line_h

def render_one(key, review, customer_name):
    w, h = SIZES[key]
    img = Image.open(f"{TEMPLATES_DIR}/{key}.png").convert("RGB")
    draw = ImageDraw.Draw(img)
    cfg = CONFIG[key]
    box_x, box_y = w * cfg["xPct"] / 100, h * cfg["yPct"] / 100
    box_w, box_h = w * cfg["wPct"] / 100, h * cfg["hPct"] / 100
    font_scale = cfg.get("fontScale", 1.0)
    max_size = int(MAX_SIZE * font_scale)
    color = cfg.get("fontColor", "#111111")
    provisional_max_h = box_h * 0.85 if customer_name else box_h
    size, lines, line_h = fit_text(draw, review, box_w, provisional_max_h, FONT_BOLD, max_size)
    y = box_y
    font = ImageFont.truetype(FONT_BOLD, size)
    for line in lines:
        draw.text((box_x, y), line, font=font, fill=color)
        y += line_h
    if customer_name:
        byline_size = max(10, round(size * 0.5))
        byline_font = ImageFont.truetype(FONT_MED, byline_size)
        y += line_h * 0.15
        draw.text((box_x, y), customer_name, font=byline_font, fill=color)
    return img

def next_review_num(folder):
    nums = []
    for name in os.listdir(folder):
        if name.startswith("Review "):
            try: nums.append(int(name.replace("Review ", "")))
            except ValueError: pass
    return max(nums, default=0) + 1

def _md5_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def _existing_square_hashes(folder):
    """MD5 of the 'square' render in every existing Review N folder for this
    adviser — used as a fingerprint to catch accidental re-renders of the
    same review (e.g. a text-matching quirk like stray whitespace/quote
    differences letting the same review through used-reviews.json's text
    check twice). Comparing just one representative size per folder is
    enough since all 5 sizes are always rendered from the same input."""
    hashes = {}
    if not os.path.isdir(folder):
        return hashes
    for name in os.listdir(folder):
        square_path = os.path.join(folder, name, "square.png")
        if name.startswith("Review ") and os.path.isfile(square_path):
            hashes[_md5_file(square_path)] = name
    return hashes

def add_review_for_adviser(slug, customer_name, review_text):
    """Renders one new Review N folder for the given adviser slug. Returns the
    new folder path — or None if this would be a byte-identical duplicate of
    an existing Review N folder for the same adviser (in which case nothing
    is written, so callers should still record the review text as used so it
    isn't retried every run, but should NOT count it as a newly added post)."""
    folder = os.path.join(OUT_DIR, slug)
    if not os.path.isdir(folder):
        raise RuntimeError(f"No existing folder for slug {slug}")

    existing_hashes = _existing_square_hashes(folder)

    n = next_review_num(folder)
    dest = os.path.join(folder, f"Review {n}")
    os.makedirs(dest, exist_ok=True)
    for key in SIZES:
        img = render_one(key, review_text, customer_name)
        img.save(f"{dest}/{key}.png")

    new_hash = _md5_file(os.path.join(dest, "square.png"))
    if new_hash in existing_hashes:
        # Duplicate of an already-existing post for this adviser — remove
        # what we just wrote rather than leaving a second identical card.
        for key in SIZES:
            os.remove(os.path.join(dest, f"{key}.png"))
        os.rmdir(dest)
        return None

    return dest
