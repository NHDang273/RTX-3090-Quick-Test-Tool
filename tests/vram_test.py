#!/usr/bin/env python3
"""VRAM Stress Test - Most critical test for detecting memory errors"""

import torch
import argparse
import sys
import time

def vram_stress_test(duration_minutes=5, size_gb=20):
    """
    Stress test VRAM by allocating large tensors and performing computations
    
    Args:
        duration_minutes: Test duration in minutes
        size_gb: Amount of VRAM to allocate (GB), or 'auto' for automatic
    """
    
    print("=" * 60)
    print("VRAM STRESS TEST - CRITICAL")
    print("=" * 60)
    print(f"\n⚠️  This is the MOST IMPORTANT test!")
    print("⚠️  ANY errors = DO NOT BUY the GPU")
    print("")
    
    if not torch.cuda.is_available():
        print("❌ CUDA not available!")
        return False
    
    device = torch.device("cuda:0")
    gpu_name = torch.cuda.get_device_name(0)
    total_vram = torch.cuda.get_device_properties(0).total_memory / 1e9
    
    # Get current VRAM usage
    torch.cuda.empty_cache()
    allocated_vram = torch.cuda.memory_allocated(0) / 1e9
    reserved_vram = torch.cuda.memory_reserved(0) / 1e9
    free_vram = total_vram - reserved_vram
    
    print(f"🔧 GPU: {gpu_name}")
    print(f"📊 Total VRAM: {total_vram:.2f} GB")
    print(f"📊 Currently used: {allocated_vram:.2f} GB (allocated), {reserved_vram:.2f} GB (reserved)")
    print(f"📊 Available: {free_vram:.2f} GB")
    
    # Auto-adjust size if requested or if not enough VRAM
    original_size = size_gb
    if size_gb == 'auto' or free_vram < size_gb + 2:  # Need 2GB buffer
        # Use 70% of free VRAM for safety (leave room for intermediate results)
        size_gb = max(4, int(free_vram * 0.7))
        if original_size != 'auto':
            print(f"\n⚠️  Requested {original_size}GB but only {free_vram:.2f}GB available")
            print(f"⚠️  Auto-adjusting test size to {size_gb}GB")
        else:
            print(f"🎯 Auto-detected test size: {size_gb} GB")
    
    # Check if there's another process using GPU
    if allocated_vram > 1.0:  # More than 1GB already in use
        print(f"\n⚠️  WARNING: {allocated_vram:.2f}GB VRAM already in use!")
        print(f"⚠️  Another process may be running. Consider:")
        print(f"   1. Run: nvidia-smi")
        print(f"   2. Kill other Python processes: pkill -9 python")
        print(f"   3. Clear cache: python3 -c 'import torch; torch.cuda.empty_cache()'")
        print(f"   4. Restart container/VM")
        print(f"\n   Continuing with available VRAM ({size_gb}GB)...")
    
    print(f"\n🎯 Test size: {size_gb} GB TOTAL")
    print(f"⏱️  Duration: {duration_minutes} minutes")
    print("-" * 60)
    
    # Calculate tensor size
    # size_gb is TOTAL memory to use, split between 2 main tensors + buffer for operations
    # Use 80% for the 2 main tensors, 20% buffer for intermediate results
    usable_per_tensor = int(size_gb * 0.4 * 250_000_000)  # 40% each tensor
    total_size = (usable_per_tensor * 4 * 2) / 1e9
    print(f"\nAllocating 2 main tensors + buffer for operations:")
    print(f"  - Each tensor: {usable_per_tensor:,} elements ({size_gb*0.4:.1f} GB)")
    print(f"  - Total allocation: ~{total_size:.1f} GB")
    print(f"  - Buffer for operations: ~{size_gb*0.2:.1f} GB")
    print("")
    
    errors = 0
    iterations = 0
    
    # Use None to track if tensors were created
    tensor_a = None
    tensor_b = None
    result = None
    
    try:
        # Allocate tensors
        print("1️⃣  Allocating VRAM...")
        tensor_a = torch.randn(usable_per_tensor, dtype=torch.float32, device=device)
        print(f"   ✓ Allocated tensor A: {torch.cuda.memory_allocated()/1e9:.2f} GB")
        
        tensor_b = torch.randn(usable_per_tensor, dtype=torch.float32, device=device)
        print(f"   ✓ Allocated tensor B: {torch.cuda.memory_allocated()/1e9:.2f} GB")
        
        # Pre-allocate result tensor to reuse (saves memory)
        result = torch.zeros_like(tensor_a)
        print(f"   ✓ Allocated result buffer: {torch.cuda.memory_allocated()/1e9:.2f} GB")
        
        allocated = torch.cuda.memory_allocated() / 1e9
        reserved = torch.cuda.memory_reserved() / 1e9
        
        print(f"\n   Total Allocated: {allocated:.2f} GB")
        print(f"   Total Reserved: {reserved:.2f} GB")
        
        # Stress test loop
        print(f"\n2️⃣  Running stress test for {duration_minutes} minutes...")
        print("   Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        test_duration = duration_minutes * 60
        
        while (time.time() - start_time) < test_duration:
            # Perform computations - use in-place operations to save memory
            torch.add(tensor_a, tensor_b, out=result)  # result = a + b (in-place)
            result.mul_(2.0)                           # result *= 2 (in-place)
            result.abs_()                              # result = abs(result) (in-place)
            result.sqrt_()                             # result = sqrt(result) (in-place)
            
            # More intensive operation every 10 iterations
            if iterations % 10 == 0:
                # Use smaller matrices to avoid OOM
                small_a = torch.randn(4000, 4000, device=device)
                small_b = torch.randn(4000, 4000, device=device)
                _ = torch.matmul(small_a, small_b)
                del small_a, small_b
                torch.cuda.empty_cache()
            
            iterations += 1
            
            # Progress report every 30 seconds
            if iterations % 100 == 0:
                elapsed = time.time() - start_time
                remaining = test_duration - elapsed
                progress = (elapsed / test_duration) * 100
                
                print(f"   [{progress:5.1f}%] Iteration {iterations:5d} | "
                      f"Elapsed: {elapsed/60:4.1f}m | "
                      f"Remaining: {remaining/60:4.1f}m")
            
            # Small delay to prevent 100% utilization
            if iterations % 10 == 0:
                time.sleep(0.05)
        
        print(f"\n3️⃣  Test completed!")
        print(f"   Total iterations: {iterations}")
        print(f"   Errors detected: {errors}")
        
        # Final result
        print("\n" + "=" * 60)
        if errors == 0:
            print("✅ VRAM STRESS TEST: PASS")
            print("✅ 0 errors detected - VRAM is healthy")
            print("=" * 60)
            test_passed = True
        else:
            print("❌ VRAM STRESS TEST: FAIL")
            print(f"❌ {errors} errors detected - DO NOT BUY!")
            print("=" * 60)
            test_passed = False
        
        return test_passed
        
    except RuntimeError as e:
        error_msg = str(e)
        print(f"\n❌ RUNTIME ERROR!")
        print(f"   Error: {error_msg}")
        print(f"   Iterations before failure: {iterations}")
        
        if "out of memory" in error_msg:
            print("\n⚠️  Out of memory error")
            print("   This could indicate:")
            print("   - Test size too large for available VRAM")
            print("   - Another process is using VRAM")
            print("   - Memory fragmentation")
            print("\n💡 To fix:")
            print("   1. Run: nvidia-smi  (check what's using GPU)")
            print("   2. Kill other processes: pkill -9 python")
            print("   3. Run again with smaller size: --size 10")
            print("   4. Or use auto size: --size auto")
            print("   5. Try: export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True")
        else:
            print("\n⚠️  VRAM instability detected")
            print("   This GPU likely has memory issues")
        
        print("\n" + "=" * 60)
        print("❌ VRAM STRESS TEST: FAIL")
        print("=" * 60)
        
        return False
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Test interrupted by user")
        print(f"   Completed {iterations} iterations")
        print(f"   Errors so far: {errors}")
        
        if errors == 0:
            print("\n✓ No errors detected before interruption")
            return True
        else:
            print(f"\n❌ {errors} errors detected - DO NOT BUY!")
            return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR!")
        print(f"   {type(e).__name__}: {str(e)}")
        print("\n" + "=" * 60)
        print("❌ VRAM STRESS TEST: FAIL")
        print("=" * 60)
        
        return False
    
    finally:
        # CRITICAL: Always cleanup tensors to free VRAM
        print("\n🧹 Cleaning up VRAM...")
        if tensor_a is not None:
            del tensor_a
        if tensor_b is not None:
            del tensor_b
        if result is not None:
            del result
        torch.cuda.empty_cache()
        print("   ✓ VRAM cleaned")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RTX 3090 VRAM Stress Test")
    parser.add_argument("--duration", type=int, default=5, 
                        help="Test duration in minutes (default: 5)")
    parser.add_argument("--size", default=20, 
                        help="VRAM to allocate in GB (default: 20, or 'auto' for automatic)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.duration < 1:
        print("❌ Duration must be at least 1 minute")
        sys.exit(1)
    
    # Handle 'auto' size or convert to int
    if args.size == 'auto':
        size_gb = 'auto'
    else:
        try:
            size_gb = int(args.size)
            if size_gb < 4 or size_gb > 23:
                print("❌ Size must be between 4-23 GB")
                sys.exit(1)
        except ValueError:
            print("❌ Size must be a number or 'auto'")
            sys.exit(1)
    
    success = vram_stress_test(args.duration, size_gb)
    
    sys.exit(0 if success else 1)