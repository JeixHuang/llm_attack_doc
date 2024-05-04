from datasets import load_dataset
import pandas as pd
from metric.image2text_similarity import ImageTextSimilarity  
from metric.BiomedCLIP import ImageTextSimilarity_bio
import os

# 列出所有分割
splits = [
    "Dermoscopy_Skin", "MRI_Alzheimer", "MRI_Brain", "Fundus_Retina",
    "Mamography_Breast", "OCT_Retina", "CT_Chest", "CT_Heart", "CT_Brain",
    "Xray_Chest", "Xray_Skeleton", "Xray_Dental", "Endoscopy_Gastroent",
    "Ultrasound_Baby", "Ultrasound_Breast", "Ultrasound_Carotid",
    "Ultrasound_Ovary", "Ultrasound_Brain"
]

# 创建相似度计算器实例
similarity_calculator_i2t = ImageTextSimilarity()  
similarity_calculator_i2t_bio = ImageTextSimilarity_bio()

# 定义函数计算图像与文本的相似度，并存储结果
def calculate_image_text_similarity(dataset_name, splits):
    all_results = []  # 用于收集所有结果的列表

    for split in splits:
        # 加载数据集的当前分割
        data = load_dataset(dataset_name, split=split)

        # 遍历数据集中的每条数据
        for item in data:
            image_path = item['image']  # 图片路径
            original_text = item['original_attribute']  # 原始文本
            unmatch_text = item['unmatch_attribute']  # 不匹配文本

            # 计算图片与原始文本的相似度
            results_original = similarity_calculator_i2t.calculate_similarity_hf(image_path, original_text)
            results_original_bio = similarity_calculator_i2t_bio.calculate_similarity_hf(image_path, original_text)

            # 计算图片与不匹配文本的相似度
            results_unmatch = similarity_calculator_i2t.calculate_similarity_hf(image_path, unmatch_text)
            results_unmatch_bio = similarity_calculator_i2t_bio.calculate_similarity_hf(image_path, unmatch_text)

            # 保存每个结果，包括分割名称
            all_results.append({
                'Split': split,
                'Image': image_path,
                'Text Type': 'Original',
                'Similarity Score (CLIP-ViT)': results_original,
                'Similarity Score (BiomedCLIP)': results_original_bio
            })
            all_results.append({
                'Split': split,
                'Image': image_path,
                'Text Type': 'Unmatch',
                'Similarity Score (CLIP-ViT)': results_unmatch,
                'Similarity Score (BiomedCLIP)': results_unmatch_bio
            })

    # 创建一个DataFrame来显示所有结果
    results_df = pd.DataFrame(all_results)
    return results_df

# 调用函数并保存结果到 CSV 文件
results_df = calculate_image_text_similarity("MedMLLM-attack/3MAD-70K", splits)
results_df.to_csv('image_text_similarity_results.csv', index=False)
print(results_df)
