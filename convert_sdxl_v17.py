import sys
import os
import torch
import logging
import gc

sys.path.insert(0, "D:/Jake/ComfyUI_windows_portable/ComfyUI")

from comfy import diffusers_convert
from safetensors.torch import load_file, save_file
from huggingface_hub import hf_hub_download

DIFFUSERS_MODEL_ID = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"
INPUT_PATH = "D:/Jake/ComfyUI_windows_portable/ComfyUI/models/checkpoints/sdxl_inpainting_0.1.safetensors"
OUTPUT_PATH = "D:/the-exile-king/sdxl_inpainting_v2.safetensors"

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Load existing checkpoint (has UNet + VAE, broken TE)
    print("Loading existing checkpoint...")
    ckpt = dict(load_file(INPUT_PATH, device="cpu"))
    print(f"Base: {len(ckpt)} keys")

    # Clone all tensors to release memory-mapped views
    ckpt = {k: v.clone().contiguous() for k, v in ckpt.items()}
    print(f"Cloned: {len(ckpt)} keys")

    # Remove broken TE keys
    for k in list(ckpt.keys()):
        if "embedders" in k:
            del ckpt[k]
    print(f"After TE removal: {len(ckpt)} keys")

    # Load and convert TE1
    print("Loading TE1...")
    te1_path = hf_hub_download(DIFFUSERS_MODEL_ID, "text_encoder/model.safetensors")
    te1_sd = load_file(te1_path, device="cpu")
    
    te1_final = {}
    for k, v in te1_sd.items():
        v = v.clone().contiguous()
        if k.startswith("text_model."):
            te1_final[f"conditioner.embedders.0.transformer.text_model.{k[11:]}"] = v
        elif k.startswith("text_projection"):
            te1_final["conditioner.embedders.0.text_projection.weight"] = v
        elif k == "logit_scale":
            te1_final["conditioner.embedders.0.logit_scale"] = v
    pos_ids_key = "conditioner.embedders.0.transformer.text_model.embeddings.position_ids"
    if pos_ids_key not in te1_final:
        te1_final[pos_ids_key] = torch.arange(77).expand((1, -1)).clone()
    if "conditioner.embedders.0.logit_scale" not in te1_final:
        te1_final["conditioner.embedders.0.logit_scale"] = torch.tensor(4.60552)
    if "conditioner.embedders.0.text_projection.weight" not in te1_final:
        te1_final["conditioner.embedders.0.text_projection.weight"] = torch.eye(768).half()
    print(f"TE1 final: {len(te1_final)} keys")

    # Free TE1 source
    del te1_sd
    gc.collect()

    # Load and convert TE2
    print("Loading TE2...")
    te2_path = hf_hub_download(DIFFUSERS_MODEL_ID, "text_encoder_2/model.safetensors")
    te2_sd = load_file(te2_path, device="cpu")
    
    te2_final = {}
    for k, v in te2_sd.items():
        v = v.clone().contiguous()
        if k.startswith("text_model.encoder.layers."):
            pass
        elif k.startswith("text_model.embeddings.position_embedding"):
            te2_final["conditioner.embedders.1.model.positional_embedding"] = v
        elif k.startswith("text_model.embeddings.token_embedding"):
            te2_final["conditioner.embedders.1.model.token_embedding.weight"] = v
        elif k.startswith("text_model.final_layer_norm"):
            suffix = k[len("text_model.final_layer_norm"):]
            te2_final[f"conditioner.embedders.1.model.ln_final{suffix}"] = v
        elif k.startswith("text_projection"):
            te2_final["conditioner.embedders.1.model.text_projection.weight"] = v
        elif k == "logit_scale":
            te2_final["conditioner.embedders.1.model.logit_scale"] = v

    te2_prefixed = {f"clip_g.{k}": v.clone().contiguous() for k, v in te2_sd.items()}
    te2_converted = diffusers_convert.convert_text_enc_state_dict_v20(te2_prefixed, "clip_g")
    
    for k, v in te2_converted.items():
        v = v.clone().contiguous()
        if k.startswith("clip_g.resblocks."):
            remaining = k[len("clip_g."):]
            te2_final[f"conditioner.embedders.1.model.transformer.{remaining}"] = v
        elif k.startswith("clip_g.text_projection"):
            te2_final["conditioner.embedders.1.model.text_projection.weight"] = v
        elif k == "clip_g.logit_scale":
            te2_final["conditioner.embedders.1.model.logit_scale"] = v
    
    if "conditioner.embedders.1.model.logit_scale" not in te2_final:
        te2_final["conditioner.embedders.1.model.logit_scale"] = torch.tensor(4.60552)
    
    print(f"TE2 final: {len(te2_final)} keys")

    # Free TE2 source
    del te2_sd, te2_prefixed, te2_converted
    gc.collect()

    # Add TE to checkpoint
    for k, v in te1_final.items():
        ckpt[k] = v
    for k, v in te2_final.items():
        ckpt[k] = v

    print(f"Total: {len(ckpt)} keys")

    # Verify
    from comfy import model_detection
    prefix = model_detection.unet_prefix_from_state_dict(ckpt)
    model_config = model_detection.model_config_from_unet(ckpt, prefix, metadata={})
    if model_config:
        print(f"Model: {type(model_config).__name__}, Inpaint: {model_config.inpaint_model()}")
        clip_sd = model_config.process_clip_state_dict(dict(ckpt))
        print(f"Processed CLIP keys: {len(clip_sd)}")

    print(f"\nSaving to {OUTPUT_PATH}...")
    save_file(ckpt, OUTPUT_PATH)
    print("Save completed!")

    # Verify after save
    size_gb = os.path.getsize(OUTPUT_PATH) / (1024**3)
    print(f"File size: {size_gb:.2f} GB")
    
    reloaded = load_file(OUTPUT_PATH, device="cpu")
    te1_after = len([k for k in reloaded if "embedders.0" in k])
    te2_after = len([k for k in reloaded if "embedders.1" in k])
    print(f"After load: Total={len(reloaded)}, TE1={te1_after}, TE2={te2_after}")

if __name__ == "__main__":
    main()
