# Troubleshooting Guide

## Common Issues & Solutions

### 1. "CUDA not available" Error

**Symptoms:**
```
❌ CUDA not available in PyTorch
```

**Causes:**
- NVIDIA driver not installed
- Wrong PyTorch version (CPU-only)
- Driver/CUDA version mismatch

**Solutions:**

#### Ubuntu:
```bash
# Check driver
nvidia-smi

# If not working, install driver
sudo apt update
sudo apt install nvidia-driver-555 nvidia-utils-555
sudo reboot

# Reinstall PyTorch with CUDA
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

#### Windows:
1. Download driver from nvidia.com/drivers
2. Install and reboot
3. Reinstall PyTorch:
   ```bash
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
   ```

---

### 2. "Out of Memory" Error

**Symptoms:**
```
RuntimeError: CUDA out of memory
```

**Causes:**
- Test size too large
- Other processes using GPU
- GPU already has issues

**Solutions:**

#### Reduce test size:
```bash
# Instead of 22GB, try 20GB
python3 tests/vram_test.py --duration 5 --size 20

# Or even 18GB for safer test
python3 tests/vram_test.py --duration 5 --size 18
```

#### Check GPU usage:
```bash
# See what's using GPU
nvidia-smi

# Kill other processes if needed
# Then retry test
```

#### If still failing:
- GPU may have VRAM issues
- Run GPU-Z to verify 24GB detected
- This could be a red flag

---

### 3. Tests Run Too Slow

**Symptoms:**
- Tests take much longer than expected
- Very low FPS/iteration rate

**Causes:**
- CPU bottleneck
- PCIe slot not x16
- Power limit too low
- Thermal throttling

**Solutions:**

#### Check PCIe slot:
```bash
nvidia-smi --query-gpu=pcie.link.gen.current,pcie.link.width.current --format=csv
```
Expected: Gen 3 or 4, x16

#### Check power limit:
```bash
nvidia-smi --query-gpu=power.draw,power.limit --format=csv
```
Expected: ~340-350W under load

#### Check thermal throttling:
```bash
watch -n 1 nvidia-smi
# Monitor temp and clocks during test
```

If GPU is throttling:
- Temperature too high (>85°C)
- Need better cooling

---

### 4. High Temperatures (>85°C)

**Symptoms:**
```
⚠️ Temperature: 88°C | HOT
❌ Temperature exceeded limit
```

**Causes:**
- Thermal pads dried out
- Poor case airflow
- Dust buildup
- Mining card with damaged cooling

**Solutions:**

#### Immediate (at shop):
- Ask seller to clean GPU
- Negotiate 1-2M VND discount for thermal pad replacement
- Consider if you want this GPU

#### After purchase:
1. **Thermal pad replacement** (~300-500k)
   - Buy: Gelid GP-Extreme 2mm pads
   - Or: Thermalright VALOR ODIN pads
   - DIY or pay shop ~200k labor

2. **Thermal paste replacement** (~150k)
   - Arctic MX-4 or MX-6
   - Clean old paste carefully
   - Apply new paste (small amount)

3. **Improve case airflow**
   - Add intake fans
   - Clean dust filters
   - Ensure GPU gets fresh air

---

### 5. Low Performance (<20 TFLOPS)

**Symptoms:**
```
❌ Performance: 18 TFLOPS (expected >25)
```

**Causes:**
- GPU is damaged
- Power limit too low
- Thermal throttling
- Driver issues

**Solutions:**

#### Check power delivery:
```bash
nvidia-smi --query-gpu=power.draw --format=csv

# During stress test, should show 340-360W
# If much lower, power delivery issue
```

#### Check if throttling:
```bash
watch -n 1 nvidia-smi
# Watch clocks during test
# Should stay ~1700-1800 MHz
# If dropping to <1500 MHz = throttling
```

#### Update drivers:
```bash
# Ubuntu
sudo apt update
sudo apt install --reinstall nvidia-driver-555

# Check version
nvidia-smi
```

#### If nothing helps:
- GPU may be damaged from mining
- Consider not buying or heavy discount

---

### 6. VRAM Errors Detected

**Symptoms:**
```
❌ VRAM errors detected
❌ DO NOT BUY THIS GPU
```

**This is CRITICAL - DO NOT BUY!**

**Why:**
- VRAM errors indicate hardware damage
- Cannot be fixed (VRAM chips soldered)
- Will cause crashes, corruption in AI/ML
- Likely from heavy mining or manufacturing defect

**What to do:**
1. Stop test immediately
2. Thank seller politely
3. Look for different GPU
4. Do NOT negotiate - walk away

**Even if:**
- Seller offers huge discount
- Says "just a small issue"
- Promises it works fine

**VRAM errors = permanent damage**

---

### 7. Fan Noise Issues

**Symptoms:**
- Fan makes grinding/clicking noise
- Fan rattles
- Fan doesn't spin

**Causes:**
- Worn bearings
- Dust in fan
- Fan blade damaged

**Solutions:**

#### At shop:
- Note the issue
- Negotiate 500k-1M discount
- Ask seller to replace fan

#### After purchase:
- Replacement fans: ~500k-1M per fan
- Can buy from Taobao/AliExpress
- Or buy from local repair shop

#### If acceptable:
- Some noise is normal under load
- But grinding/clicking is not

---

### 8. Script Errors / Python Issues

**Symptoms:**
```
ImportError: No module named 'torch'
```

**Solution:**
```bash
pip install -r requirements.txt
```

---

**Symptoms:**
```
Permission denied: ./quick_test.sh
```

**Solution:**
```bash
chmod +x quick_test.sh
chmod +x tests/*.py
```

---

**Symptoms:**
```
Python version error
```

**Solution:**
```bash
# Need Python 3.8+
python3 --version

# If too old, install newer Python
# Ubuntu:
sudo apt install python3.10

# Then use python3.10 instead of python3
```

---

### 9. Test Gets Stuck / Hangs

**Symptoms:**
- Test freezes
- No progress for >5 minutes
- System becomes unresponsive

**Causes:**
- GPU crashed
- Driver issue
- System instability

**Solutions:**

1. **Wait 2-3 minutes**
   - Some tests are compute-intensive
   - Check if GPU fan is spinning

2. **Press Ctrl+C**
   - Try to interrupt gracefully
   - Check if VRAM errors detected

3. **Force restart if needed**
   - Hard reset
   - Re-run tests

4. **If happens repeatedly:**
   - GPU is unstable
   - Likely hardware issue
   - Do not buy

---

### 10. "This GPU is not RTX 3090"

**Symptoms:**
```
⚠️ WARNING: Expected RTX 3090, got RTX 3080
```

**This is FRAUD - seller is lying!**

**What to do:**
1. Show seller the error
2. Ask why GPU name is wrong
3. If they can't explain: WALK AWAY
4. This is likely a scam

**Possible scams:**
- RTX 3080 flashed to show as 3090
- Fake GPU (rare but possible)
- Wrong card in wrong box

---

## When to Walk Away

### Absolute Deal-Breakers:
1. ❌ VRAM errors (any amount)
2. ❌ Seller refuses testing
3. ❌ GPU name doesn't match (fraud)
4. ❌ Temperature >95°C even with cleaning
5. ❌ Performance <15 TFLOPS
6. ❌ Physical damage (burns, cracks)
7. ❌ Price >25M without justification

### Red Flags (be cautious):
- ⚠️ High temps (85-90°C)
- ⚠️ Low performance (20-25 TFLOPS)
- ⚠️ No warranty
- ⚠️ Seller is evasive
- ⚠️ "Friend's GPU" story
- ⚠️ Multiple GPUs available

---

## Getting Help

### This Tool:
- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions

### Community Support:
- Võ Lâm Máy Tính (Facebook) - Vietnamese community
- r/VietNamGaming (Reddit)
- r/MachineLearning (Reddit)

### Technical Support:
- NVIDIA Forums: forums.developer.nvidia.com
- PyTorch Forums: discuss.pytorch.org
- Ubuntu Forums: ubuntuforums.org

---

## FAQ

**Q: How long should tests take?**
A: ~12 minutes total (5min VRAM + 3min thermal + 2min performance)

**Q: Can I skip VRAM test?**
A: NO! This is the most important test. VRAM errors = DO NOT BUY

**Q: Is 80°C too hot?**
A: No, but not great. <80°C is good, 80-85°C is acceptable, >85°C is too hot.

**Q: What if shop won't let me test?**
A: Don't buy. Testing is essential for used GPUs.

**Q: Should I buy mining card?**
A: Only if tests pass perfectly, price is 1.5-2M lower, and warranty is 6+ months. Still risky.

**Q: Can thermal issues be fixed?**
A: Yes, usually with thermal pad replacement (~300-500k). But negotiating discount is better.

**Q: Is RTX 3090 good for AI in 2025?**
A: Yes! 24GB VRAM is excellent for LLMs. Best value for AI on second-hand market.

---

**Still stuck? Open an issue on GitHub!**
