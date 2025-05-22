import os
import torch
import json
import csv

from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, List

from VBench.vbench2_beta_i2v_c import VBenchI2V

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义文件路径
new_videos_path = "generated_videos/"
custom_image_folder = "data/Test/imgs/"
time_log_file = "generation_time_log.csv"
output_json_file = f"{CUR_DIR}/evaluation_results/results_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}_eval_results.json"
input_json_file = output_json_file
output_json_final = f"{CUR_DIR}/output_results.json"

def evaluate_i2v_folder(
    new_videos_folder: str,
    ori_images_folder: str,
    input_json_file: str,
    output_json_file: str
) -> float:    
    ori_image_files = [f for f in os.listdir(ori_images_folder) if f.endswith('.png') or f.endswith('.jpg')]
    
    # 读取时间日志文件
    total_time_costs = 0
    img_path_list = []
    with open(time_log_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_path = row['img_path']
            img_path_list.append(img_path)
            time_cost = float(row['耗时'])
            total_time_costs += time_cost

    # 生成视频数量与测试输入图片数量不同，则得分为0
    if len(ori_image_files) != len(img_path_list):
        print('generation incomplete')
        with open(output_json_file, 'w') as f:
            json.dump({}, f, indent=4)
        return 0, 'generation incomplete'

    avg_time_cost = total_time_costs / len(ori_image_files)
    print(f'avg_time_cost: {avg_time_cost}')
    if avg_time_cost <= 60:
        i2v_time_score = 1.0
    elif avg_time_cost <= 120:
        i2v_time_score = 0.9
    elif avg_time_cost <= 240:
        i2v_time_score = 0.80
    elif avg_time_cost <= 360:
        i2v_time_score = 0.75
    elif avg_time_cost <= 600:
        i2v_time_score = 0.7
    else:
        i2v_time_score = 0

    with open(input_json_file, 'r') as f:
        input_results = json.load(f)

    i2v_subject = input_results["i2v_subject"][0] if input_results["i2v_subject"] else 0.0
    i2v_background = input_results["i2v_background"][0] if input_results["i2v_background"] else 0.0
    i2v_motion_smoothness = input_results["motion_smoothness"][0] if input_results["motion_smoothness"] else 0.0
    i2v_imaging_quality = input_results["imaging_quality"][0] if input_results["imaging_quality"] else 0.0
    i2v_dynamic_degree = input_results["dynamic_degree"][0] if input_results["dynamic_degree"] else 0.0

    results = {}
    results['avg_score'] = {
        "i2v_subject": i2v_subject,
        "i2v_background": i2v_background,
        "i2v_motion_smoothness": i2v_motion_smoothness,
        "i2v_imaging_quality": i2v_imaging_quality,
        "i2v_dynamic_degree": i2v_dynamic_degree, # i2v_dynamic_degree 值过小会审核不通过
        "i2v_time_score": i2v_time_score
    }
    
    with open(output_json_file, 'w') as f:
        json.dump(results, f, indent=4)

    if i2v_time_score == 0:
        return 0, 'generation timeout'
    
    final_score = (i2v_subject + i2v_background + i2v_motion_smoothness + i2v_imaging_quality + i2v_time_score) / 5

    return final_score, 'successful'

if __name__ == "__main__":
    device = torch.device("cuda")
    my_VBench = VBenchI2V(device, f'{CUR_DIR}/VBench/vbench2_beta_i2v/vbench2_i2v_full_info.json', "evaluation_results")

    my_VBench.evaluate(
        videos_path=new_videos_path,
        name=f'results_{datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}',
        dimension_list=['i2v_subject', 'i2v_background', 'motion_smoothness', 'imaging_quality', 'dynamic_degree'],
        resolution=None,
        local=True,
        custom_image_folder=custom_image_folder,
        mode='custom_input',
        **{'imaging_quality_preprocessing_mode': 'longer'}
    )

    average_score, msg = evaluate_i2v_folder(
        new_videos_path, custom_image_folder, input_json_file, output_json_final)
    
    print(f"总体加权平均值: {average_score:.4f}")

    result_file = 'result.txt'
    if os.path.exists(result_file):
        os.remove(result_file)
    
    fp = open(result_file, 'a')
    fp.write(f"{average_score:.4f},{msg}")
    fp.write("\n")
    fp.close()