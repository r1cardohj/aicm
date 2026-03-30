# acm - AI Complete Me

[![WIP](https://img.shields.io/badge/status-WIP-orange)](https://github.com/r1cardohj/acm)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> A local-first, privacy-focused code completion CLI tool for developers who want AI assistance without sending their code to the cloud.

## 🚧 Work In Progress

**This project is in active development. Core features are being implemented and APIs may change. Follow the progress and contribute!**

## 🎯 Concept & Vision

**acm** is designed to be the **Unix-philosophy** code completion tool:

- **Local-only**: Your code never leaves your machine
- **Lightweight**: Optimized for Apple Silicon and modern hardware  
- **Composable**: Works with pipes, files, and editor integrations
- **Hackable**: Simple Python codebase, easy to customize

### Philosophy

```
$ echo "def quick_osrt(arr):" | acm
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
```

Just like `cat`, `grep`, or `sed` — acm does one thing well: **complete your code**.

## ✨ Planned Features

### Core
- [x] Pipe-based input (`echo "..." | acm`)
- [x] Fill-in-the-middle (FIM) completion
- [x] Single-line suggestions
- [ ] simple indent handle
- [ ] Daemon mode (persistent model in memory)
- [ ] Configuration file support

### Models
- [x] Qwen2.5-Coder-1.5B (default)
- [ ] Qwen2.5-Coder-0.5B (lightweight option)
- [ ] Custom GGUF model support
- [ ] Automatic model downloading

### Integrations
- [ ] (Neo)vim plugin
- [ ] VSCode extension
- [ ] LSP protocol support

## 🏗️ Architecture (Conceptual)

```
┌─────────────────┐
│   Input Source  │  stdin / file / editor
│  (stdin/file)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  acm CLI        │  Argument parsing, context detection
│  (entry point)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  CodeComplete   │────▶│  llama-cpp-python │
│  Engine         │     │  (local inference) │
│                 │◀────│                   │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│   Post-process  │  Indentation fix, deduplication
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Output        │  stdout / editor
│                 │
└─────────────────┘
```

## 🛤️ Roadmap

### Phase 1: Foundation (Current)
- [x] Basic completion via stdin
- [x] Model loading and inference
- [ ] Indentation handling
- [ ] Configuration system
- [ ] Error handling & logging
- [ ] Lanuch PYPI for install

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
echo "def calculate_fibonacci(n):" | acm
```

## 🖥️ System Requirements

- **macOS**: Apple Silicon (M1/M2/M3) or Intel
- **Linux**: x86_64 or ARM64
- **RAM**: 4GB+ (for 1.5B model), 2GB+ (for 0.5B model)
- **Python**: 3.10+
- **Storage**: ~1.5GB for models

## 🤝 Contributing

This is a passion project. Contributions, ideas, and feedback are welcome!


## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Made with ❤️ for the local-first AI movement.**