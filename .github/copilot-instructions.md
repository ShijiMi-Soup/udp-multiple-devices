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

### Best Practices

- Handle missing arguments gracefully in OSC handlers (check `if not args`)
- Use type conversion with try/except for OSC message values
- Properly clean up server resources in `finally` blocks
- For GUI apps, use Qt signals and slots for thread-safe communication
- Use `deque` from `collections` module with `maxlen` for fixed-size buffers

### Dependencies

When adding dependencies, update `requirements.txt` with the package name only (no version pinning unless necessary).

### Error Handling

- Validate OSC message arguments before processing
- Use try/except for type conversions
- Properly shutdown and close servers on exit

### Testing

- Test OSC servers manually with OSC client tools
- Verify multiple port configurations work correctly
- Test GUI responsiveness and proper cleanup on close
