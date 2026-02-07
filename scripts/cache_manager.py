#!/usr/bin/env python3
import subprocess
import json
import argparse
import sys
import os

# Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_DB = os.getenv("REDIS_DB", "0")
REDIS_PASS = os.getenv("REDIS_PASSWORD", "")

def run_redis_cmd(args):
    """Execute redis-cli command securely"""
    cmd = ["redis-cli", "-h", REDIS_HOST, "-p", REDIS_PORT, "-n", REDIS_DB]
    if REDIS_PASS:
        cmd.extend(["-a", REDIS_PASS, "--no-auth-warning"])
    
    cmd.extend(args)
    
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode().strip()
        return result
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.decode().strip()}"

def set_key(key, value, ttl=None):
    cmd = ["SET", key, value]
    if ttl:
        cmd.extend(["EX", str(ttl)])
    return run_redis_cmd(cmd)

def get_key(key):
    return run_redis_cmd(["GET", key])

def del_key(key):
    return run_redis_cmd(["DEL", key])

def list_keys(pattern="*"):
    return run_redis_cmd(["KEYS", pattern])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mema Memory Cache Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # SET
    p_set = subparsers.add_parser("set", help="Set a key")
    p_set.add_argument("key")
    p_set.add_argument("value")
    p_set.add_argument("--ttl", type=int, help="Time to live in seconds")

    # GET
    p_get = subparsers.add_parser("get", help="Get a key")
    p_get.add_argument("key")

    # DEL
    p_del = subparsers.add_parser("del", help="Delete a key")
    p_del.add_argument("key")

    # KEYS
    p_keys = subparsers.add_parser("keys", help="List keys by pattern")
    p_keys.add_argument("pattern", default="*", nargs="?")

    args = parser.parse_args()

    if args.command == "set":
        print(set_key(args.key, args.value, args.ttl))
    elif args.command == "get":
        print(get_key(args.key))
    elif args.command == "del":
        print(del_key(args.key))
    elif args.command == "keys":
        print(list_keys(args.pattern))
