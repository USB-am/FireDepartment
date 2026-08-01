#!/bin/bash
python3.14 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload --loop asyncio