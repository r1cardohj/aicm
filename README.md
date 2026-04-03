# aicm - AI Complete Me

[![WIP](https://img.shields.io/badge/status-WIP-orange)](https://github.com/r1cardohj/acim)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> A local-first, privacy-focused code completion CLI tool for developers who want AI assistance without sending their code to the cloud.

## Installation & Quick Start

Get up and running in **under 60 seconds**. No API keys, no cloud, no nonsense.

### 1. Install

```bash
# Via pip
pip install aicm

# Or blazing fast with uv
uv pip install aicm
```

### 2. Download Model (One-time)

```bash
aicm --install
```

Downloads the default Qwen2.5-Coder-0.5B model (~400M) locally. Your code never leaves your machine.

### 3. Start Completing

```bash
# Pipe a function stub
echo "def fibonacci(n):" | aicm
```

**That's it.** No config files, no sign-ups, no telemetry. Just pure local AI completion.


## 🚧 Work In Progress

**This project is in active development. Core features are being implemented and APIs may change. Follow the progress and contribute!**

## 🎯 Concept & Vision

**acim** is designed to be the **Unix-philosophy** code completion tool:

- **Local-only**: Your code never leaves your machine
- **Lightweight**: Optimized for Apple Silicon and modern hardware  
- **Fast**: Instant suggestions with efficient models
- **Out-of-the-box**: default is best, no configuration needed in most cases
- **Composable**: Works with pipes, files, and editor integrations
- **Hackable**: Simple Python codebase, easy to customize

### Philosophy

```
$ echo "def quick_sort(arr):" | acim
```

Just like `cat`, `grep`, or `sed` — aicm does one thing well: **complete your code**.

## ✨ Planned Features

### Core
- [x] Pipe-based input (`echo "..." |acim`)
- [x] Fill-in-the-middle (FIM) completion
- [x] Single-line suggestions
- [ ] Daemon mode (persistent model in memory)
- [ ] Configuration file support

### Models
- [x] Qwen2.5-Coder-0.5B (default)
- [x] Qwen2.5-Coder-1.5B (more powerful option)
- [ ] Custom GGUF model support
- [ ] Automatic model downloading

### Integrations
- [ ] (Neo)vim plugin (Working...)
- [ ] VSCode extension
- [ ] LSP protocol support


## 🛤️ Roadmap

### Phase 1: Foundation (Current)
- [x] Basic completion via stdin
- [x] Model loading and inference
- [ ] Configuration system
- [ ] Error handling & logging
- [ ] Installation via pip, uv...

### Phase 2: Usability
- [ ] Daemon mode for instant response
- [ ] Model management (download, switch)
- [ ] Shell completions

### Phase 3: Ecosystem
- [ ] Editor plugins
- [ ] LSP server mode
- [ ] Multi-language support beyond Python
- [ ] Fine-tuning capabilities

## 💡 Use Cases

### Quick prototyping
```bash
# Start a new function
echo "def calculate_fibonacci(n):" |acim
```

## 🖥️ System Requirements

- **macOS**: Apple Silicon (M2/M3...) - Fully supported ✅
- **macOS**: Intel - Work in progress 🚧
- **Linux**: x86_64 or ARM64 - Work in progress 🚧
- **RAM**: 4GB+ (for 1.5B model), 2GB+ (for 0.5B model)
- **Python**: 3.10+
- **Storage**: ~1.5GB for models

## 🤝 Contributing

This is a passion project. Contributions, ideas, and feedback are welcome!


## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Made with for the local-first AI movement.**
