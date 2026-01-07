# GitHub Copilot Instructions

## Repository Overview

This repository contains Python scripts for handling UDP/OSC (Open Sound Control) servers with support for multiple devices and visualization.

## Coding Guidelines

### Language and Style

- **Language**: Python 3.11+
- **Japanese Comments**: Code comments are in Japanese (日本語のコメント)
- Follow existing comment style with section markers: `# 設定 =========================`

### Key Technologies

- **pythonosc**: For OSC protocol handling
  - Use `Dispatcher` for mapping OSC addresses to handlers
  - Use `ThreadingOSCUDPServer` for synchronous servers
  - Use `AsyncIOOSCUDPServer` for async servers
- **rich**: For terminal progress bars and formatting
- **PySide6**: For GUI applications
- **pyqtgraph**: For real-time data visualization

### Dependencies

When adding dependencies, update `requirements.txt` with the package name only (no version pinning unless necessary).
