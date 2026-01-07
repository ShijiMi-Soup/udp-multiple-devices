# OSC Server with Progress Bar Tutorial

This repository contains a step-by-step tutorial for implementing an OSC (Open Sound Control) server with progress bar visualization.

## Overview

Learn how to:
1. Set up a basic OSC server
2. Implement an asynchronous OSC server for multiple devices
3. Visualize received data with progress bars

## Files

- **1_base_server.py** - Basic OSC server (single port)
- **2_async_server.py** - Asynchronous OSC server (multiple ports)
- **3_progressbar.py** - OSC server with progress bar visualization
- **test_osc_sender.py** - Test script to send OSC messages
- **TUTORIAL_JA.md** - Complete tutorial in Japanese (日本語チュートリアル)

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Examples

#### 1. Basic Server
```bash
python 1_base_server.py
```

#### 2. Async Server
```bash
python 2_async_server.py
```

#### 3. Progress Bar (with test)
Terminal 1:
```bash
python 3_progressbar.py
```

Terminal 2:
```bash
python test_osc_sender.py
```

## Documentation

For a detailed Japanese tutorial, see [TUTORIAL_JA.md](./TUTORIAL_JA.md)

## Requirements

- Python 3.7+
- python-osc
- rich

## License

MIT
