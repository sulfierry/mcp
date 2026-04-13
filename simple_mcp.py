#!/usr/bin/env python3
import sys, json

def main():
    while True:
        line = sys.stdin.readline()
        if not line: break
        try:
            req = json.loads(line)
        except:
            continue
            
        if req.get("method") == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "TestServer", "version": "1.0"}
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif req.get("method") == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "result": {
                    "tools": [{
                        "name": "dummy_test_tool",
                        "description": "A dummy tool to test connection",
                        "inputSchema": {"type": "object", "properties": {}}
                    }]
                }
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
            
if __name__ == "__main__":
    main()
