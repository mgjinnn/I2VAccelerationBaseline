import csv
import os
import pandas as pd
import time
import torch

from diffsynth import save_video
from PIL import Image

from I2V import I2VMethod


def generate(prompts, video_names, img_names, seeds):
    i2v_generator = I2VMethod()

    # 初始化日志文件
    log_file = 'generation_time_log.csv'
    if os.path.exists(log_file):
        os.remove(log_file)
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['img_path', '耗时'])

    # 遍历每个视频的生成任务
    for i in range(len(prompts)):
        prompt = prompts[i]
        video_name = video_names[i]
        img_name = img_names[i]
        seed = seeds[i]

        # 加载对应的图片
        img_path = os.path.join("data/Test/imgs", img_name)
        if not os.path.exists(img_path):
            print(f"图片 {img_name} 不存在，跳过此视频的生成。")
            continue

        input_image = Image.open(img_path)

        # 记录开始时间
        start_time = time.time()

        # 生成视频
        video = i2v_generator.run_generation(prompt, input_image, seed)

        # 记录结束时间
        end_time = time.time()
        duration = end_time - start_time

        # 保存视频
        video_path = os.path.join("generated_videos", video_name)
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        save_video(video, video_path, fps=15, quality=5)

        # 写入日志文件
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([img_path, duration])

        print(f"视频 {video_name} 生成完成，耗时 {duration:.2f} 秒。")


if __name__ == "__main__":    
    ts = time.time()
    # 数据描述文件路径
    csv_file_path = 'data/Test/datasets.csv'
    df = pd.read_csv(csv_file_path)
    
    prompts = []
    video_names = []
    img_names = []
    seeds = []

    # 读取CSV文件
    for _, row in df.iterrows():
        prompt = str(row.get('prompt', '')).strip()
        video_name = str(row.get('video_name', '')).strip()
        img_name = str(row.get('img_name', '')).strip()
        seed = str(row.get('seed', '')).strip()

        if prompt and video_name and img_name and seed:
            prompts.append(prompt)
            video_names.append(video_name)
            img_names.append(img_name)
            seeds.append(int(seed))

    # 生成视频
    generate(prompts, video_names, img_names, seeds)
    te = time.time()
    print(f"生成 {len(prompts)} 个视频耗时 {te - ts} 秒。")
