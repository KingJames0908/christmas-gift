import os
from PIL import Image


def compress_images(directory='.', quality=85, max_width=1024):
    # 支持的图片格式
    extensions = ['.jpg', '.jpeg', '.png']

    # 创建一个输出目录
    output_dir = os.path.join(directory, 'compressed')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"🚀 开始压缩图片，目标宽: {max_width}px...")

    count = 0
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in extensions):
            file_path = os.path.join(directory, filename)

            try:
                with Image.open(file_path) as img:
                    # 获取原始尺寸
                    w, h = img.size

                    # 如果图片比目标宽度大，就按比例缩小
                    if w > max_width:
                        ratio = max_width / w
                        new_h = int(h * ratio)
                        img = img.resize((max_width, new_h), Image.LANCZOS)

                    # 转换颜色模式（防止PNG转JPG报错）
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # 保存到 compressed 目录，保持原文件名
                    output_path = os.path.join(output_dir, filename)
                    # 这里的 optimize=True 和 quality=85 是压缩核心
                    img.save(output_path, 'JPEG', optimize=True, quality=quality)

                    # 对比一下大小
                    src_size = os.path.getsize(file_path) / 1024
                    dst_size = os.path.getsize(output_path) / 1024
                    print(f"✅ {filename}: {src_size:.0f}KB -> {dst_size:.0f}KB")
                    count += 1
            except Exception as e:
                print(f"❌ 处理 {filename} 失败: {e}")

    print(f"\n🎉 完成！共压缩 {count} 张图片。请把 compressed 文件夹里的图片上传到服务器。")


if __name__ == '__main__':
    compress_images()