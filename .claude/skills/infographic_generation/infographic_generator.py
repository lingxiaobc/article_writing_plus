# 依赖: pip install google-genai httpx
#
# 公众号文章"大板块信息图"生成器（手绘笔记风格）
#
# 用法：
#   1) 按文章二级标题批量生成（主用法，配合技能使用）：
#      python infographic_generator.py --article "<文章.md>" [--output-dir "<图片目录>"] [--dry-run]
#        - 解析文章中每个 "## " 二级标题（不含 # 与 ###），为每个章节生成一张手绘笔记风信息图
#        - 图片默认存到 <文章所在目录>/image/（可用 --output-dir 覆盖）
#        - 在每个章节正文末尾（下一个 ## 之前 / 文件末尾）插入 ![](image/xxx.png)，原地改写文章
#        - --dry-run：只解析与打印计划，不生图、不写盘
#   2) 单图生成（兼容旧用法）：
#      python infographic_generator.py "<生图提示词>" [输出目录]
#
# 密钥：依次尝试 环境变量 GEMINI_KEY → GEMINI_API_KEY → .claude/settings.local.json 中 env.GEMINI_KEY

import json
import mimetypes
import os
import re
import sys
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 项目根 = .claude/skills/infographic_generation 往上 3 层
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", "..", ".."))

_MODEL = "gemini-3.1-flash-image-preview"

SYSTEM_INSTRUCTION = """## 角色（Role）
你是一名专业的手绘笔记艺术家和信息设计师。

## 任务（Task）
- 生图。字体设计有创意，手写字线条细、圆润，艺术构图，极致清晰，极简主义，简约高级，杰作。
- 基于我提供的章节内容，创建一张清晰、简洁的手绘笔记风格草图，画风要有很强的手绘感。
- 旨在帮助读者快速把握该章节的内在逻辑和核心要点。
- 背景纯白，禁止出现多余元素（如黑板边框、手稿纸边框等）。

## 步骤（Steps）
- 阅读并提取"关键节点"（角色/动作/结果/条件），按流程或因果关系组织。
- 每幅图都要有一个清晰、简短的主题，用大字表现，视觉集中；不要在一幅图里堆砌过多信息。
- 用简洁的中文关键词命名其他关键节点，文字书写正确、易懂，字号比主题小至少一级；文字是次要的，插图第一优先。
- 让生成效果更简洁；填满画布保证视觉均衡，不要过度居中。

## 核心要求（Core Requirements）
- 视觉风格：严格遵循手绘笔记风格，所有元素具手写感；干净极简线条 + 简单图标；像用彩色铅笔在白板/笔记本上绘制。
- 构图与布局：清晰、简洁、有逻辑，自然引导视线；合理自由安排元素，留足空间；严格避免箭头重叠、视觉混乱。
- 颜色：黑色为主素描线条以保证清晰，可用其他颜色强调（红色强调、绿/黄装饰），整体简洁；纯白背景、高对比；不用渐变、阴影、照片/3D/拟物风格。
- 所有文字为简体中文。
- 尺寸：始终保持 16:9 比例。

## 输出目标
生成一张极简手绘草图，能清晰解释该章节的核心思想，让人一眼看懂。背景纯白。"""


def get_api_key():
    """依次从环境变量、settings.local.json 取 GEMINI_KEY。"""
    for var in ("GEMINI_KEY", "GEMINI_API_KEY"):
        v = os.environ.get(var)
        if v:
            return v
    for cand in (
        os.path.join(_PROJECT_ROOT, ".claude", "settings.local.json"),
        os.path.join(os.getcwd(), ".claude", "settings.local.json"),
    ):
        if os.path.isfile(cand):
            try:
                with open(cand, "r", encoding="utf-8") as f:
                    data = json.load(f)
                v = (data.get("env") or {}).get("GEMINI_KEY")
                if v:
                    return v
            except Exception:
                pass
    return None


def make_client():
    import httpx
    from google import genai
    from google.genai import types

    api_key = get_api_key()
    if not api_key:
        print("错误：未找到 GEMINI_KEY（环境变量与 .claude/settings.local.json 均无）", file=sys.stderr)
        sys.exit(1)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    http_options = None
    if proxy:
        http_options = types.HttpOptions(httpx_client=httpx.Client(proxy=proxy))
    return genai.Client(api_key=api_key, http_options=http_options)


def generate_one_image(client, prompt, out_path):
    """生成单张信息图并保存。成功返回实际保存路径，失败返回 None。"""
    from google.genai import types

    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="1K"),
        response_modalities=["IMAGE"],
        system_instruction=[types.Part.from_text(text=SYSTEM_INSTRUCTION)],
    )
    try:
        for chunk in client.models.generate_content_stream(
            model=_MODEL, contents=contents, config=config
        ):
            if chunk.parts is None:
                continue
            for part in chunk.parts:
                inline = getattr(part, "inline_data", None)
                if inline and getattr(inline, "data", None):
                    ext = mimetypes.guess_extension(inline.mime_type) or ".png"
                    if not out_path.lower().endswith(ext.lower()):
                        out_path = out_path + ext
                    with open(out_path, "wb") as f:
                        f.write(inline.data)
                    return out_path
            if getattr(chunk, "text", None):
                print(f"  [模型文本反馈] {chunk.text}", file=sys.stderr)
    except Exception as e:
        print(f"  [生图失败] {e}", file=sys.stderr)
    return None


_H2_RE = re.compile(r"^##(?!\#)\s+(.+?)\s*$")


def parse_h2_sections(text):
    """返回 [(heading, body_text), ...]，按文档顺序，仅 '## ' 二级标题。"""
    lines = text.split("\n")
    sections = []
    cur_heading = None
    cur_body = []
    for line in lines:
        m = _H2_RE.match(line)
        if m:
            if cur_heading is not None:
                sections.append((cur_heading, "\n".join(cur_body).strip()))
            cur_heading = m.group(1).strip()
            cur_body = []
        elif cur_heading is not None:
            cur_body.append(line)
    if cur_heading is not None:
        sections.append((cur_heading, "\n".join(cur_body).strip()))
    return sections


def insert_image_links(text, section_images):
    """
    section_images：与 parse_h2_sections 同序的列表，元素为相对路径字符串或 None。
    在每个章节正文末尾（下一个 ## 之前 / 文件末尾）插入 ![](relpath)。
    """
    lines = text.split("\n")
    out = []
    prev_image = None
    prev_heading = None
    sec_idx = -1
    for line in lines:
        m = _H2_RE.match(line)
        if m:
            if prev_image:
                out.append("")
                out.append(f"![{prev_heading}信息图]({prev_image})")
                out.append("")
            sec_idx += 1
            prev_heading = m.group(1).strip()
            prev_image = section_images[sec_idx] if sec_idx < len(section_images) else None
        out.append(line)
    if prev_image:
        out.append("")
        out.append(f"![{prev_heading}信息图]({prev_image})")
        out.append("")
    return "\n".join(out)


def slugify(s, maxlen=24):
    keep = re.sub(r"[^\w一-鿿]+", "-", s, flags=re.UNICODE).strip("-")
    return keep[:maxlen] or "section"


def run_article_mode(article_path, output_dir, dry_run):
    if not os.path.isfile(article_path):
        print(f"错误：文章不存在：{article_path}", file=sys.stderr)
        sys.exit(1)
    with open(article_path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = parse_h2_sections(text)
    if not sections:
        print("未在文章中发现 ## 二级标题，无法生成板块信息图。")
        print("（提示：本技能以 '## ' 作为章节切分；若文章用 '---' 分隔而无 '##'，请先为各章节补上二级标题。）")
        return

    article_dir = os.path.dirname(os.path.abspath(article_path))
    if not output_dir:
        output_dir = os.path.join(article_dir, "image")

    print(f"发现 {len(sections)} 个二级标题章节：")
    for i, (h, _) in enumerate(sections, 1):
        print(f"  {i}. {h}")
    print(f"图片输出目录：{output_dir}")

    if dry_run:
        print("[dry-run] 跳过生图与写盘。")
        return

    os.makedirs(output_dir, exist_ok=True)
    client = make_client()
    rel_dir = os.path.relpath(output_dir, article_dir).replace(os.sep, "/")
    images = []
    for i, (heading, body) in enumerate(sections, 1):
        snippet = body[:1500]
        prompt = (
            "请为下面这一章节生成一张手绘笔记风格的信息图，提炼它的核心要点与逻辑关系：\n"
            f"章节标题：{heading}\n章节内容：\n{snippet}"
        )
        base = os.path.join(output_dir, f"infographic_{i:02d}_{slugify(heading)}")
        print(f"[{i}/{len(sections)}] 生成：{heading} ...")
        saved = generate_one_image(client, prompt, base)
        if saved:
            images.append(f"{rel_dir}/{os.path.basename(saved)}")
            print(f"    -> 已保存：{saved}")
        else:
            images.append(None)
            print("    -> 生成失败，跳过该章节的图片插入。")

    new_text = insert_image_links(text, images)
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    ok = sum(1 for x in images if x)
    print(f"\n完成：{ok}/{len(sections)} 张信息图已生成并插入文章：{article_path}")


def run_single_mode(prompt, output_dir):
    if not output_dir:
        output_dir = os.path.join(_PROJECT_ROOT, "generated_images")
    os.makedirs(output_dir, exist_ok=True)
    client = make_client()
    out = os.path.join(output_dir, f"infographic_{uuid.uuid4().hex[:8]}")
    saved = generate_one_image(client, prompt, out)
    if saved:
        print(f"File saved to: {saved}")
    else:
        print("生成失败。", file=sys.stderr)
        sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    if args[0] == "--article":
        if len(args) < 2:
            print("错误：--article 需要文章路径", file=sys.stderr)
            sys.exit(1)
        article_path = args[1]
        output_dir = None
        dry_run = False
        rest = args[2:]
        i = 0
        while i < len(rest):
            a = rest[i]
            if a == "--dry-run":
                dry_run = True
            elif a == "--output-dir" and i + 1 < len(rest):
                output_dir = rest[i + 1]
                i += 1
            elif a.startswith("--output-dir="):
                output_dir = a.split("=", 1)[1]
            i += 1
        run_article_mode(article_path, output_dir, dry_run)
    else:
        prompt = args[0]
        output_dir = args[1] if len(args) > 1 else None
        run_single_mode(prompt, output_dir)


if __name__ == "__main__":
    main()
