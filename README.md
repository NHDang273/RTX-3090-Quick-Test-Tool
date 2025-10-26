# RTX 3090 Quick Test Tool 🚀

**Fast & Simple GPU Testing for Second-Hand RTX 3090 Purchase**

Test RTX 3090 in **15 minutes** at shop before buying. Detect critical issues: VRAM errors, thermal problems, and performance issues.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![CUDA](https://img.shields.io/badge/CUDA-12.0+-orange.svg)

---

## 🎯 Purpose

Testing tool specifically for **AI Engineers** buying second-hand RTX 3090:
- ✅ Detect VRAM errors (most critical for AI/ML)
- ✅ Check thermal performance
- ✅ Verify compute capabilities
- ✅ Fast enough for shop testing (15 mins)

---

## 🚀 Quick Start

### At Shop (15 minutes):

```bash
# 1. Clone repo to USB
git clone https://github.com/yourusername/rtx-3090-quick-test.git
cd rtx-3090-quick-test

# 2. Install dependencies (one-time)
pip install -r requirements.txt

# 3. Run test
bash quick_test.sh
```

**That's it!** Results will show: ✅ PASS / ⚠️ WARNING / ❌ FAIL

---

## 📋 What It Tests

| Test | Duration | Critical? | What it detects |
|------|----------|-----------|-----------------|
| **GPU Info** | 10s | No | Verify specs, BIOS, temperature |
| **VRAM Test** | 5 mins | ✅ YES | Memory errors (mining damage) |
| **Thermal Test** | 3 mins | ✅ YES | Cooling issues, thermal throttle |
| **Performance** | 2 mins | No | Compute capability check |

**Total: ~12 minutes**

---

## 🔴 Critical Red Flags

**DO NOT BUY if:**
- ❌ VRAM test shows ANY errors
- ❌ Temperature >85°C GPU or >95°C VRAM under load
- ❌ Performance <70% of expected
- ❌ Thermal throttling occurs

---

## 📦 Requirements

### Hardware:
- Test PC with PCIe x16 slot
- PSU 750W+ with 2x 8-pin PCIe
- Monitor + DisplayPort/HDMI cable

### Software:
- Ubuntu 22.04/24.04 or Windows 10/11
- NVIDIA Driver 555+
- Python 3.8+
- PyTorch 2.0+ with CUDA

### Install:
```bash
# Ubuntu
sudo apt update
sudo apt install nvidia-driver-555 python3-pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124

# Verify
nvidia-smi
python3 -c "import torch; print(torch.cuda.is_available())"
```

---

## 📊 Expected Results (RTX 3090 Founders Edition)

| Metric | Good | Acceptable | Red Flag |
|--------|------|------------|----------|
| **VRAM Test** | 0 errors | 0 errors | ANY errors |
| **GPU Temp** | <75°C | <80°C | >85°C |
| **VRAM Temp** | <85°C | <90°C | >95°C |
| **FP32 Performance** | >28 TFLOPS | >25 TFLOPS | <20 TFLOPS |
| **FP16 (Tensor Cores)** | >90 TFLOPS | >75 TFLOPS | <60 TFLOPS |

---

## 📖 Usage Examples

### Basic Test (at shop):
```bash
bash quick_test.sh
```

### Run Individual Tests:
```bash
# GPU info only
python3 tests/gpu_info.py

# VRAM test only (most important)
python3 tests/vram_test.py --duration 5

# Performance test only
python3 tests/performance_test.py
```

### Extended Test (at home):
```bash
# Longer VRAM test
python3 tests/vram_test.py --duration 30 --size 22
```

---

## 🛠️ Customization

Edit `config.yaml` to adjust test parameters:

```yaml
vram_test:
  duration_minutes: 5
  allocation_gb: 22

thermal_test:
  duration_minutes: 3
  temp_limit_gpu: 85
  temp_limit_vram: 95

performance_test:
  matrix_size: 8192
  iterations: 20
```

---

## 📁 Project Structure

```
rtx-3090-quick-test/
├── README.md              # This file
├── quick_test.sh          # Main test script
├── requirements.txt       # Python dependencies
├── config.yaml           # Test configuration
├── tests/
│   ├── gpu_info.py       # GPU information check
│   ├── vram_test.py      # VRAM stress test (CRITICAL)
│   ├── thermal_test.py   # Temperature monitoring
│   └── performance_test.py  # Compute benchmarks
├── utils/
│   └── helpers.py        # Common utilities
└── docs/
    ├── BUYING_GUIDE.md   # Detailed buying guide
    └── TROUBLESHOOTING.md # Common issues
```

---

## 💰 Price Reference (Vietnam Market - 2025)

| Condition | Price (VND) | Recommendation |
|-----------|-------------|----------------|
| Excellent (1 year, boxed) | 22-23.5M | ✅ Good deal |
| Good (1-2 years) | 21-22M | ✅ Buy |
| Acceptable (2-3 years) | 19-21M | ⚠️ Test carefully |
| Mining card (tests OK) | 18-20M | ⚠️ Risky, must test |
| >25M | - | 🚫 Too expensive |

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## ⚠️ Disclaimer

This tool provides basic testing to help evaluate second-hand GPUs. It does not guarantee the GPU will work perfectly for all use cases. Always:
- Get warranty from seller (minimum 3 months)
- Test thoroughly within return period (7 days)
- Buy from reputable sellers

---

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/rtx-3090-quick-test/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/rtx-3090-quick-test/discussions)
- 📧 **Email:** your.email@example.com

---

## 🌟 Star History

If this tool helped you buy a good GPU, please ⭐ star the repo!

---

## 🙏 Acknowledgments

- NVIDIA for CUDA toolkit
- PyTorch team for GPU frameworks
- Vietnamese tech community (Võ Lâm Máy Tính)

---

**Made with ❤️ for AI Engineers buying RTX 3090**
