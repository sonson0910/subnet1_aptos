#!/usr/bin/env python3
"""
Debug script để kiểm tra registration issues
"""

import subprocess
import json
from typing import Dict, List

# Thông tin contract và network
CONTRACT_ADDRESS = "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04"
TESTNET_URL = "https://fullnode.testnet.aptoslabs.com/v1"

# Test với 1 key đầu tiên
TEST_KEY = {
    "name": "validator_1",
    "private_key": "0x0235dae67c000ce2432014f418578190a1da915a5fc31b857808f3365c8372df",
    "address": "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04"
}

def run_cmd_verbose(cmd: List[str]) -> Dict:
    """Chạy command với verbose output"""
    try:
        print(f"🚀 Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(f"   Return code: {result.returncode}")
        if result.stdout:
            print(f"   STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"   STDERR:\n{result.stderr}")
            
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "code": result.returncode
        }
    except Exception as e:
        print(f"   Exception: {e}")
        return {"success": False, "output": "", "error": str(e), "code": -1}

def test_profile_creation():
    """Test 1: Tạo profile"""
    print("🧪 Test 1: Creating profile...")
    
    # Xóa profile cũ
    cmd = ["aptos", "config", "delete-profile", "--profile", TEST_KEY["name"]]
    run_cmd_verbose(cmd)
    
    # Tạo profile mới
    cmd = [
        "aptos", "init",
        "--profile", TEST_KEY["name"],
        "--private-key", TEST_KEY["private_key"],
        "--network", "testnet",
        "--assume-yes"
    ]
    
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_profile_list():
    """Test 2: Liệt kê profiles"""
    print("\n🧪 Test 2: Listing profiles...")
    
    cmd = ["aptos", "config", "show-profiles"]
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_account_info():
    """Test 3: Kiểm tra account info"""
    print("\n🧪 Test 3: Account info...")
    
    cmd = ["aptos", "account", "list", "--profile", TEST_KEY["name"]]
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_balance_lookup():
    """Test 4: Kiểm tra balance bằng address"""
    print("\n🧪 Test 4: Balance lookup...")
    
    cmd = [
        "aptos", "account", "lookup-address", 
        "--account", TEST_KEY["address"],
        "--url", TESTNET_URL
    ]
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_module_exists():
    """Test 5: Kiểm tra module tồn tại"""
    print("\n🧪 Test 5: Checking if module exists...")
    
    cmd = [
        "aptos", "move", "view",
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::get_enhanced_network_stats",
        "--url", TESTNET_URL
    ]
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_simple_view():
    """Test 6: Test simple view function"""
    print("\n🧪 Test 6: Simple view function...")
    
    cmd = [
        "aptos", "move", "view",
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::is_validator",
        "--args", f"address:{TEST_KEY['address']}",
        "--url", TESTNET_URL
    ]
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_old_module():
    """Test 7: Kiểm tra module cũ"""
    print("\n🧪 Test 7: Checking old module...")
    
    cmd = [
        "aptos", "move", "view",
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::get_network_stats",
        "--url", TESTNET_URL
    ]
    result = run_cmd_verbose(cmd)
    return result["success"]

def test_registration_attempt():
    """Test 8: Thử registration với verbose"""
    print("\n🧪 Test 8: Registration attempt...")
    
    cmd = [
        "aptos", "move", "run",
        "--profile", TEST_KEY["name"],
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::register_validator",
        "--args", "u64:1",
        "--args", "string:http://localhost:8001",
        "--args", "u64:50000000",
        "--assume-yes",
        "--max-gas", "1000000"
    ]
    result = run_cmd_verbose(cmd)
    return result["success"]

def main():
    """Main debug function"""
    print("🔍 ModernTensor Registration Debug")
    print("=" * 50)
    
    tests = [
        ("Profile Creation", test_profile_creation),
        ("Profile List", test_profile_list),
        ("Account Info", test_account_info),
        ("Balance Lookup", test_balance_lookup),
        ("Module Exists", test_module_exists),
        ("Simple View", test_simple_view),
        ("Old Module", test_old_module),
        ("Registration Attempt", test_registration_attempt)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Exception in {test_name}: {e}")
            results[test_name] = False
        
        print("-" * 30)
    
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    return results

if __name__ == "__main__":
    main() 