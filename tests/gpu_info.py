#!/usr/bin/env python3
"""GPU Information Check - Verify specs and basic health"""

import torch
import subprocess
import sys

def check_gpu_info():
    """Check GPU information and specs"""
    
    print("=" * 60)
    print("GPU INFORMATION CHECK")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return False
    
    gpu_name = torch.cuda.get_device_name(0)
    props = torch.cuda.get_device_properties(0)
    
    # Check if it's RTX 3090
    print(f"\n📊 GPU Details:")
    print(f"   Name: {gpu_name}")
    
    if "3090" not in gpu_name:
        print(f"   ⚠️  WARNING: Expected RTX 3090, got {gpu_name}")
    else:
        print(f"   ✓ Correct model detected")
    
    # Memory
    vram_gb = props.total_memory / 1e9
    print(f"\n💾 VRAM:")
    print(f"   Total: {vram_gb:.2f} GB")
    
    if vram_gb < 23.5:
        print(f"   ❌ VRAM too low! Expected 24GB, got {vram_gb:.2f}GB")
        return False
    else:
        print(f"   ✓ VRAM capacity correct")
    
    # Compute capability
    print(f"\n⚙️  Compute Capability:")
    print(f"   Version: {props.major}.{props.minor}")
    
    if props.major < 8:
        print(f"   ⚠️  Old architecture detected")
    else:
        print(f"   ✓ Ampere architecture (GA102)")
    
    # Temperature
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
            capture_output=True, text=True, check=True
        )
        temp = int(result.stdout.strip())
        
        print(f"\n🌡️  Temperature (Idle):")
        print(f"   Current: {temp}°C")
        
        if temp > 50:
            print(f"   ⚠️  High idle temperature! Should be 30-45°C")
            print(f"   → Possible cooling issue or recent use")
        elif temp > 45:
            print(f"   ⚠️  Slightly warm at idle")
        else:
            print(f"   ✓ Normal idle temperature")
    except:
        print(f"\n⚠️  Could not read temperature")
    
    # CUDA/Driver version
    print(f"\n🔧 Software:")
    print(f"   PyTorch: {torch.__version__}")
    print(f"   CUDA: {torch.version.cuda}")
    
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
            capture_output=True, text=True, check=True
        )
        driver = result.stdout.strip()
        print(f"   Driver: {driver}")
    except:
        print(f"   Driver: Unknown")
    
    # PCIe link
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=pcie.link.gen.current,pcie.link.width.current", "--format=csv,noheader"],
            capture_output=True, text=True, check=True
        )
        pcie_info = result.stdout.strip()
        print(f"\n🔌 PCIe Link:")
        print(f"   {pcie_info}")
        
        if "16" in pcie_info:
            print(f"   ✓ PCIe x16 (full bandwidth)")
        else:
            print(f"   ⚠️  Not running at x16 (may impact performance)")
    except:
        print(f"\n⚠️  Could not read PCIe info")
    
    print("\n" + "=" * 60)
    print("✅ GPU Information Check: PASS")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = check_gpu_info()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
