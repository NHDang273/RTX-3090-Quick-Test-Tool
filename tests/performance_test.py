#!/usr/bin/env python3
"""Performance Benchmark - Test compute capabilities"""

import torch
import sys
import time

def performance_benchmark():
    """Run performance benchmarks for FP32 and FP16"""
    
    print("=" * 60)
    print("PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return False
    
    device = torch.device("cuda:0")
    gpu_name = torch.cuda.get_device_name(0)
    
    print(f"\n🔧 GPU: {gpu_name}")
    print("-" * 60)
    
    results = {}
    
    # Test 1: FP32 Matrix Multiplication
    print("\n1️⃣  FP32 Matrix Multiplication (Compute)")
    size = 8192
    iterations = 20
    
    print(f"   Size: {size}x{size}")
    print(f"   Iterations: {iterations}")
    
    a = torch.randn(size, size, device=device, dtype=torch.float32)
    b = torch.randn(size, size, device=device, dtype=torch.float32)
    
    # Warmup
    for _ in range(5):
        _ = torch.matmul(a, b)
    torch.cuda.synchronize()
    
    # Benchmark
    start = time.time()
    for _ in range(iterations):
        c = torch.matmul(a, b)
    torch.cuda.synchronize()
    elapsed = time.time() - start
    
    # Calculate TFLOPS
    flops = 2 * size ** 3 * iterations
    tflops = (flops / elapsed) / 1e12
    
    results['fp32_tflops'] = tflops
    
    print(f"   Time: {elapsed:.2f}s")
    print(f"   Performance: {tflops:.2f} TFLOPS")
    
    # Evaluation
    if tflops >= 28:
        print(f"   ✅ EXCELLENT (>28 TFLOPS)")
    elif tflops >= 25:
        print(f"   ✓ GOOD (>25 TFLOPS)")
    elif tflops >= 20:
        print(f"   ⚠ ACCEPTABLE (>20 TFLOPS)")
    else:
        print(f"   ❌ LOW (<20 TFLOPS)")
    
    del a, b, c
    torch.cuda.empty_cache()
    
    # Test 2: FP16 with Tensor Cores
    print("\n2️⃣  FP16 Matrix Multiplication (Tensor Cores)")
    
    a16 = torch.randn(size, size, device=device, dtype=torch.float16)
    b16 = torch.randn(size, size, device=device, dtype=torch.float16)
    
    # Warmup
    for _ in range(5):
        _ = torch.matmul(a16, b16)
    torch.cuda.synchronize()
    
    # Benchmark
    iterations = 40
    start = time.time()
    for _ in range(iterations):
        c16 = torch.matmul(a16, b16)
    torch.cuda.synchronize()
    elapsed = time.time() - start
    
    # Calculate TFLOPS
    flops = 2 * size ** 3 * iterations
    tflops = (flops / elapsed) / 1e12
    
    results['fp16_tflops'] = tflops
    
    print(f"   Time: {elapsed:.2f}s")
    print(f"   Performance: {tflops:.2f} TFLOPS")
    
    # Evaluation
    if tflops >= 90:
        print(f"   ✅ EXCELLENT (>90 TFLOPS)")
    elif tflops >= 75:
        print(f"   ✓ GOOD (>75 TFLOPS)")
    elif tflops >= 60:
        print(f"   ⚠ ACCEPTABLE (>60 TFLOPS)")
    else:
        print(f"   ❌ LOW (<60 TFLOPS)")
    
    del a16, b16, c16
    torch.cuda.empty_cache()
    
    # Test 3: Memory Bandwidth
    print("\n3️⃣  Memory Bandwidth Test")
    
    size_mb = 2000  # 2GB
    elements = int(size_mb * 1024 * 1024 / 4)  # float32 = 4 bytes
    
    a_mem = torch.randn(elements, dtype=torch.float32, device=device)
    b_mem = torch.zeros_like(a_mem)
    
    # Warmup
    for _ in range(5):
        b_mem.copy_(a_mem)
    torch.cuda.synchronize()
    
    # Benchmark
    iterations = 50
    start = time.time()
    for _ in range(iterations):
        b_mem.copy_(a_mem)
    torch.cuda.synchronize()
    elapsed = time.time() - start
    
    # Calculate bandwidth
    bytes_transferred = elements * 4 * iterations
    bandwidth_gbs = (bytes_transferred / elapsed) / 1e9
    
    results['bandwidth_gbs'] = bandwidth_gbs
    
    print(f"   Bandwidth: {bandwidth_gbs:.2f} GB/s")
    
    # Evaluation (RTX 3090 theoretical: 936 GB/s)
    if bandwidth_gbs >= 800:
        print(f"   ✅ EXCELLENT (>800 GB/s)")
    elif bandwidth_gbs >= 600:
        print(f"   ✓ GOOD (>600 GB/s)")
    elif bandwidth_gbs >= 400:
        print(f"   ⚠ ACCEPTABLE (>400 GB/s)")
    else:
        print(f"   ❌ LOW (<400 GB/s)")
    
    del a_mem, b_mem
    torch.cuda.empty_cache()
    
    # Overall evaluation
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"FP32 Performance:  {results['fp32_tflops']:.2f} TFLOPS")
    print(f"FP16 Performance:  {results['fp16_tflops']:.2f} TFLOPS")
    print(f"Memory Bandwidth:  {results['bandwidth_gbs']:.2f} GB/s")
    
    # Decision
    fp32_ok = results['fp32_tflops'] >= 20
    fp16_ok = results['fp16_tflops'] >= 60
    bw_ok = results['bandwidth_gbs'] >= 400
    
    fp32_good = results['fp32_tflops'] >= 25
    fp16_good = results['fp16_tflops'] >= 75
    bw_good = results['bandwidth_gbs'] >= 600
    
    print("\n" + "=" * 60)
    
    if fp32_good and fp16_good and bw_good:
        print("✅ PERFORMANCE TEST: PASS (Excellent)")
        print("=" * 60)
        return 0
    elif fp32_ok and fp16_ok and bw_ok:
        print("⚠️  PERFORMANCE TEST: WARNING (Acceptable)")
        print("⚠️  Performance below expected but usable")
        print("⚠️  Negotiate price down 1M VND")
        print("=" * 60)
        return 2  # Warning code
    else:
        print("❌ PERFORMANCE TEST: FAIL")
        print("❌ Performance significantly below spec")
        issues = []
        if not fp32_ok:
            issues.append(f"FP32: {results['fp32_tflops']:.1f} TFLOPS (expected >20)")
        if not fp16_ok:
            issues.append(f"FP16: {results['fp16_tflops']:.1f} TFLOPS (expected >60)")
        if not bw_ok:
            issues.append(f"Bandwidth: {results['bandwidth_gbs']:.1f} GB/s (expected >400)")
        
        for issue in issues:
            print(f"   - {issue}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    try:
        result = performance_benchmark()
        sys.exit(result)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
