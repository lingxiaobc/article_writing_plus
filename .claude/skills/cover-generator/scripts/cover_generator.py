# To run this code you need to install the following dependencies:
# pip install google-genai pillow
#
# 用法：python cover_generator.py "文章标题" "生图提示词" [输出目录]
# 参数1：文章标题（必填，仅用于文件命名）
# 参数2：由调用方（大模型）动态编写的完整生图提示词（必填）
# 参数3：图片输出目录（可选，默认使用项目根目录下的 generated_images/）

import mimetypes
import os
import sys
import uuid
import httpx
from google import genai
from google.genai import types

# 修复 Windows 控制台中文编码问题
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
IP_IMAGE_PATH = os.path.join(_SKILL_DIR, "..", "reference", "IP_character", "IP_character.jpg")

_default_output = os.path.join(_SKILL_DIR, "..", "..", "..", "..", "..", "generated_images")
OUTPUT_DIR = sys.argv[3] if len(sys.argv) > 3 else _default_output
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")


def generate():
    if len(sys.argv) < 3:
        print("错误：请提供文章标题和生图提示词")
        print("用法：python cover_generator.py \"文章标题\" \"生图提示词\" [输出目录]")
        sys.exit(1)

    article_title = sys.argv[1]   # 仅用于文件命名
    image_prompt = sys.argv[2]    # 由调用方动态编写的完整生图提示词

    _proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    _httpx_client = httpx.Client(proxy=_proxy) if _proxy else None
    _http_options = types.HttpOptions(httpx_client=_httpx_client) if _httpx_client else None
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
        http_options=_http_options,
    )

    # 加载IP形象参考图片
    with open(IP_IMAGE_PATH, "rb") as f:
        ip_image_data = f.read()

    prompt = image_prompt

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    data=ip_image_data,
                    mime_type="image/jpeg",
                ),
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="MINIMAL",
        ),
        image_config=types.ImageConfig(
            aspect_ratio="21:9",  # API支持的最接近2.35:1的比例（2.33:1）
            image_size="1K",
        ),
        response_modalities=["IMAGE"],
        system_instruction=[
            types.Part.from_text(text="""你是一名专业的公众号封面设计师，风格偏好：简约、克制、留白充足。

## IP形象要求（最高优先级，严格执行）
- 必须高度还原参考图中的IP形象：手绘线描风格的小猫，戴圆框眼镜，配有原子权杖（权杖是标志性道具，其具体位置由行为描述决定），体型Q版但气质严谨学术
- 【强制】IP形象只能使用黑色、白色、灰色，严禁任何彩色上色
- 【强制】必须保持手绘素描线条感，严禁改为光滑卡通风格、3D风格、萌系可爱风格
- 【强制】IP形象必须有严谨、冷静、学术的气质，禁止表现为过度可爱、萌系、活泼的形象
- 【强制】IP形象的姿态和动作必须严格按照用户提供的行为描述执行，不得默认沿用参考图的站立握杖姿态
- 【强制】若画面中出现原子权杖，线条必须清晰完整、无弯折变形、无断裂；权杖仅允许垂直或斜靠等稳定姿态，禁止绘制复杂透视角度
- IP形象固定放置在图片右侧区域，不遮挡标题

## 标题文字设计
- 【强制】标题必须完整显示，一字不少，不得截断、省略；标题过长时自动换行，每行字数均匀
- 字体简洁有力，风格与文章主题贴合，可使用彩色
- 标题放置在图片左侧，字号大、留白足，禁止堆砌装饰
- 禁止出现与文章标题无关的文字

## 背景与色彩
- 背景可使用彩色，风格简约：纯色、渐变或极少量主题图形
- 整体不超过3种主色，色调与文章情绪相符
- 严禁：多种图案叠加、复杂纹理、大量装饰线条

## 构图规范
- 整体比例为超宽屏（约21:9，宽度远大于高度）
- 左侧放标题文字，右侧放IP形象，留白充分
- 视觉重心稳定，整体干净大方"""),
        ],
    )

    file_index = 0
    uid = uuid.uuid4().hex[:8]
    safe_title = "".join(c for c in article_title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title[:30]  # 限制文件名长度

    for chunk in client.models.generate_content_stream(
        model="gemini-3.1-flash-image-preview",
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.parts is None:
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            file_index += 1
            inline_data = chunk.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            file_name = os.path.join(
                OUTPUT_DIR,
                f"cover_{safe_title}_{uid}_{file_index}{file_extension}"
            )
            save_binary_file(file_name, data_buffer)
        else:
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text)


if __name__ == "__main__":
    generate()
