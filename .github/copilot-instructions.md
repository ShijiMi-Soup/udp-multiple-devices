# GitHub Copilot Instructions

## Repository Overview

This repository contains Python scripts for handling UDP/OSC (Open Sound Control) servers with support for multiple devices and visualization.

## Code Structure

- `1_base_server.py` - Basic threaded OSC UDP server implementation
- `2_async_server.py` - Async-based OSC server for handling multiple ports
- `3_progressbar.py` - OSC server with rich progress bar visualization
- `4_udp_mulit_gui.py` - GUI-based OSC monitor using PySide6 and pyqtgraph

## Coding Guidelines

### Language and Style

- **Language**: Python 3.7+
- **Async**: Use `asyncio` for asynchronous operations
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

### Architecture Patterns

1. **Server Configuration**: Define `IP` and `PORT`/`PORTS` at the top of files
2. **Handler Functions**: Create handler functions that accept `(address, *args)` for OSC messages
3. **Dispatcher Pattern**: Map OSC addresses to handler functions using `Dispatcher`
4. **Async Patterns**: Use `asyncio.get_running_loop()` and `await asyncio.Event().wait()` for async servers

### Best Practices

- Handle missing arguments gracefully in OSC handlers (check `if not args`)
- Use type conversion with try/except for OSC message values
- Properly clean up server resources in `finally` blocks
- For GUI apps, use Qt signals and slots for thread-safe communication
- Use `deque` with `maxlen` for fixed-size buffers

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

## Common Tasks

### Adding a New OSC Address

1. Add the address to the `addresses` list
2. Create or map a handler function using `disp.map(address, handler)`
3. Ensure the handler accepts `(address, *args)` parameters

### Creating a New Server Script

1. Import required modules: `pythonosc.dispatcher`, `pythonosc.osc_server`
2. Define configuration (IP, PORT)
3. Create dispatcher and map handlers
4. Initialize and start the appropriate server type
5. Add Japanese comments for sections (設定, 関数, メインの処理)

### Working with Async Servers

1. Use `async def main()` as entry point
2. Get the event loop with `asyncio.get_running_loop()`
3. Create servers and endpoints
4. Use `await asyncio.Event().wait()` for waiting
5. Clean up endpoints in `finally` block
6. Run with `asyncio.run(main())`
