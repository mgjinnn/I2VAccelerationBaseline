import torch

from diffsynth import ModelManager, WanVideoPipeline, save_video


class I2VMethod:
    def __init__(self):
        model_manager = ModelManager(device="cpu")
        model_manager.load_models(
            ["models/Wan-AI/Wan2.1-I2V-14B-480P/models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth"],
            torch_dtype=torch.float32, # Image Encoder is loaded with float32
        )
        model_manager.load_models(
            [
                [
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00001-of-00007.safetensors",
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00002-of-00007.safetensors",
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00003-of-00007.safetensors",
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00004-of-00007.safetensors",
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00005-of-00007.safetensors",
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00006-of-00007.safetensors",
                    "models/Wan-AI/Wan2.1-I2V-14B-480P/diffusion_pytorch_model-00007-of-00007.safetensors",
                ],
                "models/Wan-AI/Wan2.1-I2V-14B-480P/models_t5_umt5-xxl-enc-bf16.pth",
                "models/Wan-AI/Wan2.1-I2V-14B-480P/Wan2.1_VAE.pth",
            ],
            torch_dtype=torch.float8_e4m3fn,
        )
        self.pipe = WanVideoPipeline.from_model_manager(model_manager, torch_dtype=torch.bfloat16, device="cuda")
        self.pipe.enable_vram_management(num_persistent_param_in_dit=None)
    
    def run_generation(self, prompt, input_image):
        # 生成视频
        video = self.pipe(
            prompt=prompt,
            num_inference_steps=40,
            input_image=input_image,
            seed=42, 
            tiled=True, height=832, width=464,
            tea_cache_l1_thresh=0.4,
            tea_cache_model_id="Wan2.1-I2V-14B-480P"
        )

        return video
