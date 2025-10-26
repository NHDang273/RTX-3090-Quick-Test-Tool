#!/usr/bin/env python3
"""Thermal Stress Test - Check cooling and temperature limits"""

import torch
import subprocess
import argparse
import sys
import time

def get_temperature():
    """Get current GPU temperature"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
            capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    except:
        return None

def thermal_stress_test(duration_minutes=3, temp_limit_gpu=85):
    """
    Thermal stress test with temperature monitoring
    
    Args:
        duration_minutes: Test duration in minutes
        temp_limit_gpu: GPU temperature limit (°C)
    """
    
    print("=" * 60)
    print("THERMAL STRESS TEST")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return False
    
    device = torch.device("cuda:0")
    gpu_name = torch.cuda.get_device_name(0)
    
    print(f"\n🔧 GPU: {gpu_name}")
    print(f"⏱️  Duration: {duration_minutes} minutes")
    print(f"🌡️  Temperature limit: {temp_limit_gpu}°C GPU")
    print("-" * 60)
    
    # Get initial temperature
    start_temp = get_temperature()
    if start_temp:
        print(f"\n📊 Starting temperature: {start_temp}°C")
    
    # Create workload
    print(f"\n1️⃣  Creating thermal workload...")
    size = 8192
    
    try:
        # Allocate tensors
        tensor_a = torch.randn(size, size, device=device, dtype=torch.float32)
        tensor_b = torch.randn(size, size, device=device, dtype=torch.float32)
        
        print(f"   ✓ Workload created ({size}x{size} matrices)")
        
        # Stress test
        print(f"\n2️⃣  Running thermal stress test...")
        print("   Monitoring temperature every 10 seconds\n")
        
        start_time = time.time()
        test_duration = duration_minutes * 60
        iterations = 0
        
        max_temp = 0
        temps = []
        throttled = False
        
        while (time.time() - start_time) < test_duration:
            # Compute-intensive operations
            for _ in range(50):
                result = torch.matmul(tensor_a, tensor_b)
                result = torch.matmul(result, tensor_b)
            
            iterations += 1
            
            # Check temperature every 10 seconds
            if iterations % 5 == 0:
                current_temp = get_temperature()
                if current_temp:
                    temps.append(current_temp)
                    max_temp = max(max_temp, current_temp)
                    
                    elapsed = time.time() - start_time
                    progress = (elapsed / test_duration) * 100
                    
                    # Temperature indicator
                    if current_temp < 75:
                        temp_status = "✓ GOOD"
                    elif current_temp < 80:
                        temp_status = "⚠ WARM"
                    elif current_temp < temp_limit_gpu:
                        temp_status = "⚠ HOT"
                    else:
                        temp_status = "❌ TOO HOT"
                        throttled = True
                    
                    print(f"   [{progress:5.1f}%] Temp: {current_temp:3d}°C | {temp_status}")
        
        # Results
        print(f"\n3️⃣  Test completed!")
        print(f"   Iterations: {iterations}")
        print(f"   Max temperature: {max_temp}°C")
        
        if temps:
            avg_temp = sum(temps) / len(temps)
            print(f"   Avg temperature: {avg_temp:.1f}°C")
        
        # Evaluation
        print("\n" + "=" * 60)
        
        if max_temp < 75:
            print("✅ THERMAL TEST: EXCELLENT")
            print("✅ Cooling is very good (<75°C)")
            result_code = 0
        elif max_temp < 80:
            print("✅ THERMAL TEST: PASS")
            print("✅ Cooling is good (<80°C)")
            result_code = 0
        elif max_temp < temp_limit_gpu:
            print("⚠️  THERMAL TEST: WARNING")
            print("⚠️  Temperature is high but acceptable")
            print("⚠️  Consider thermal pad replacement (-1M VND)")
            result_code = 2  # Warning
        else:
            print("❌ THERMAL TEST: FAIL")
            print(f"❌ Temperature exceeded limit ({max_temp}°C > {temp_limit_gpu}°C)")
            print("❌ Cooling system may be inadequate")
            result_code = 1
        
        if throttled:
            print("⚠️  Thermal throttling detected during test")
        
        print("=" * 60)
        
        # Cleanup
        del tensor_a, tensor_b, result
        torch.cuda.empty_cache()
        
        # Cool down
        print("\n🧊 Cooling down (10 seconds)...")
        time.sleep(10)
        
        final_temp = get_temperature()
        if final_temp:
            print(f"   Final temperature: {final_temp}°C")
        
        return result_code
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        torch.cuda.empty_cache()
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RTX 3090 Thermal Test")
    parser.add_argument("--duration", type=int, default=3,
                        help="Test duration in minutes (default: 3)")
    parser.add_argument("--limit", type=int, default=85,
                        help="GPU temperature limit in °C (default: 85)")
    
    args = parser.parse_args()
    
    result = thermal_stress_test(args.duration, args.limit)
    
    sys.exit(result)
