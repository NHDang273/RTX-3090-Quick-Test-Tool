# 🚀 START HERE - RTX 3090 Quick Test Tool

**Welcome!** This tool helps you test second-hand RTX 3090 GPUs in ~12 minutes.

---

## ⚡ Super Quick Start (At Shop)

**If you just want to test a GPU RIGHT NOW:**

```bash
# 1. Clone to USB or laptop
git clone https://github.com/yourusername/rtx-3090-quick-test.git
cd rtx-3090-quick-test

# 2. Install (one-time)
pip install -r requirements.txt

# 3. Run test
bash quick_test.sh
```

**That's it!** Results will show ✅ PASS / ⚠️ WARNING / ❌ FAIL

---

## 📚 What to Read

### 🎯 **If you're at the shop NOW:**
→ Just run `bash quick_test.sh` and see results
→ Print/save: [docs/BUYING_GUIDE.md](docs/BUYING_GUIDE.md) (decision matrix)

### 📖 **If you're preparing to buy:**
1. [README.md](README.md) - Overview and setup
2. [docs/BUYING_GUIDE.md](docs/BUYING_GUIDE.md) - What to check, prices, decisions
3. [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - If something goes wrong

### 🛠️ **If you're a developer:**
1. [README.md](README.md) - Technical details
2. [GITHUB_SETUP.md](GITHUB_SETUP.md) - How to push to GitHub
3. Source code in `tests/` - All test implementations

---

## 🎯 What This Tool Does

| Test | Time | Critical? | Detects |
|------|------|-----------|---------|
| GPU Info | 10s | No | Verifies specs |
| **VRAM Test** | 5min | ✅ **YES** | Memory errors |
| Thermal Test | 3min | ✅ YES | Cooling issues |
| Performance | 2min | No | Compute capability |

**Total: ~12 minutes for confident decision**

---

## 🚨 Most Important Test: VRAM

**VRAM errors = DO NOT BUY** (cannot be fixed)

This test allocates 20GB VRAM and performs intensive computations.
If ANY errors detected → GPU is damaged (likely from mining)

---

## ✅ What Results Mean

### ✅ PASS (All tests green)
- Safe to buy at fair price (~22-23.5M VND)
- GPU is in good condition
- Ready for AI/ML workloads

### ⚠️ WARNING (Some yellow warnings)
- GPU has minor issues (high temps, slight low perf)
- Can buy but negotiate 1-2M VND discount
- May need thermal pad replacement

### ❌ FAIL (Any red failures)
- **DO NOT BUY**
- Critical issues detected
- Walk away and find another GPU

---

## 💰 Quick Price Guide (Vietnam)

| Condition | Price | Recommendation |
|-----------|-------|----------------|
| Excellent (tests perfect) | 22-23.5M | ✅ Buy |
| Good (minor warnings) | 21-22M | ✅ Buy |
| Mining card (tests OK) | 18-20M | ⚠️ Risky |
| >25M or test failures | - | 🚫 Pass |

---

## 🛠️ Requirements

### Hardware (for testing):
- PC with PCIe x16 slot
- PSU 750W+ with 2x 8-pin PCIe
- Monitor + cable

### Software:
```bash
# Ubuntu 22.04/24.04
sudo apt install nvidia-driver-555 python3-pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# Verify
nvidia-smi
python3 -c "import torch; print(torch.cuda.is_available())"
```

---

## 📂 Project Structure

```
rtx-3090-quick-test/
├── README.md              ← Technical overview
├── START_HERE.md          ← This file!
├── GITHUB_SETUP.md        ← How to push to GitHub
├── quick_test.sh          ← Main test script (RUN THIS)
├── requirements.txt       ← Python dependencies
├── config.yaml           ← Test configuration
├── tests/                ← Test modules
│   ├── gpu_info.py       ← GPU information
│   ├── vram_test.py      ← VRAM stress test (CRITICAL)
│   ├── thermal_test.py   ← Temperature monitoring
│   └── performance_test.py ← Compute benchmarks
└── docs/                 ← Documentation
    ├── BUYING_GUIDE.md   ← Decision matrix, prices
    └── TROUBLESHOOTING.md ← Common issues
```

---

## 🎯 Common Questions

**Q: Do I need to test for full 12 minutes?**
A: Yes! VRAM test (5 mins) is most important. Don't skip it.

**Q: What if shop won't let me test?**
A: Don't buy. Testing is essential for used GPUs.

**Q: Can I test on Windows?**
A: Yes, but Linux recommended. Install Python + PyTorch on Windows.

**Q: Is thermal pad replacement hard?**
A: No, but costs ~300-500k. Better to negotiate discount.

**Q: Should I buy mining card?**
A: Only if tests pass perfectly, price is low, warranty is good. Still risky.

**Q: What's the #1 red flag?**
A: VRAM errors. If detected, walk away immediately.

---

## 🆘 Need Help?

### Something wrong?
→ Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

### Questions?
→ Open GitHub Issue or Discussion

### Want to contribute?
→ PRs welcome! See [GITHUB_SETUP.md](GITHUB_SETUP.md)

---

## 📱 Quick Reference Card (Print This)

```
┌─────────────────────────────────────────┐
│  RTX 3090 QUICK TEST CHEATSHEET        │
├─────────────────────────────────────────┤
│  RUN: bash quick_test.sh                │
│  TIME: ~12 minutes                      │
├─────────────────────────────────────────┤
│  ✅ BUY IF:                             │
│    • VRAM: 0 errors                     │
│    • Temp: <80°C                        │
│    • Perf: >25 TFLOPS                   │
│    • Price: ≤23.5M                      │
├─────────────────────────────────────────┤
│  ❌ DON'T BUY IF:                       │
│    • VRAM: ANY errors                   │
│    • Temp: >85°C                        │
│    • Perf: <20 TFLOPS                   │
│    • Price: >25M                        │
├─────────────────────────────────────────┤
│  ⚠️ NEGOTIATE IF:                       │
│    • Temp: 80-85°C (-1M)                │
│    • Perf: 20-25 TFLOPS (-1M)           │
│    • Mining card (-2M)                  │
└─────────────────────────────────────────┘
```

---

## 🚀 What's Next?

1. **Now:** Run the test at shop
2. **After purchase:** Test again at home (extended 30min test)
3. **Within 7 days:** Claim warranty if issues found
4. **Share:** Star repo on GitHub if this helped! ⭐

---

## 🙏 Credits

Made with ❤️ for AI Engineers buying RTX 3090

**Contributors:**
- You? Submit a PR! 🚀

**Special thanks:**
- Vietnamese tech community (Võ Lâm Máy Tính)
- r/LocalLLaMA for inspiration
- All RTX 3090 owners sharing experiences

---

**Ready to test? Run:** `bash quick_test.sh`

**Good luck! 🍀**
