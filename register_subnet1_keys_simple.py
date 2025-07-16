#!/usr/bin/env python3
"""
Script đăng ký 3 Validators và 2 Miners cho Subnet1 (Simplified)
Bỏ qua funding vì accounts đã có APT
"""

import subprocess
import time
from typing import Dict, List

# Thông tin contract và network
CONTRACT_ADDRESS = "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04"
TESTNET_URL = "https://fullnode.testnet.aptoslabs.com/v1"
SUBNET_UID = 1

# Thông tin từ key.txt
KEYS_INFO = {
    "validator_1": {
        "private_key": "D7BF95D09CBC52BA4D9BBF2C4A5A787495C7908ECA855CE97D4A23A772E80A62",
        "address": "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04",
        "api_endpoint": "http://localhost:8001"
    },
    "validator_2": {
        "private_key": "0xfd1b44dbaf2bf218d92c41c29915bd72109ee95886e863f0ff9124e689021cd8",
        "address": "0x4dcd05a74ea9729d65a75379a8a4eb8e8f7fb440478dec715ac8fcbadf56acf5",
        "api_endpoint": "http://localhost:8002"
    },
    "validator_3": {
        "private_key": "0xf530fb22f73ba74cd2e8a66d57264e34470c07d29e67e3f485027acc72009d4c",
        "address": "0x72c61e80cb7f2b350f81bffc590e415ebf5553699dd1babec3c5a3a067182d66",
        "api_endpoint": "http://localhost:8003"
    },
    "miner_1": {
        "private_key": "0x90702114101ecca796263b0a1a884b2c83de73740c12359bc978e1e6f09ab438",
        "address": "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04",
        "api_endpoint": "http://localhost:8100"
    },
    "miner_2": {
        "private_key": "0x4d37b47207c126859bf5c13a37d8e968e1eb489631ebaf750e0c20f414aef473",
        "address": "0xea10e0e3fbf983d7e65cfb2963f769719027792df8c34ca0aa09e9aeb270cb9d",
        "api_endpoint": "http://localhost:8101"
    }
}

def run_cmd(cmd: List[str], show_output: bool = True) -> Dict:
    """Chạy command và trả về kết quả"""
    try:
        if show_output:
            print(f"🚀 Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout.strip(), "error": ""}
    except subprocess.CalledProcessError as e:
        return {"success": False, "output": "", "error": e.stderr.strip()}

def create_aptos_profile(name: str, private_key: str) -> bool:
    """Tạo Aptos profile cho từng key"""
    print(f"📋 Creating/updating profile for {name}...")
    
    # Xóa profile cũ nếu tồn tại
    cmd = ["aptos", "config", "delete-profile", "--profile", name]
    run_cmd(cmd, show_output=False)  # Không quan tâm kết quả
    
    # Tạo profile mới
    cmd = [
        "aptos", "init",
        "--profile", name,
        "--private-key", private_key,
        "--network", "testnet",
        "--assume-yes"
    ]
    
    result = run_cmd(cmd, show_output=False)
    if result["success"]:
        print(f"✅ Profile {name} ready")
        return True
    else:
        print(f"❌ Failed to create profile {name}: {result['error']}")
        return False

def check_balance(profile: str) -> str:
    """Kiểm tra balance của account"""
    cmd = ["aptos", "account", "list", "--profile", profile]
    result = run_cmd(cmd, show_output=False)
    if result["success"]:
        lines = result["output"].split('\n')
        for line in lines:
            if 'coin' in line.lower() and 'value' in line:
                return line.strip()
    return "Unknown balance"

def register_validator(profile: str, info: Dict) -> bool:
    """Đăng ký validator"""
    print(f"🔰 Registering validator {profile}...")
    
    # Kiểm tra balance trước
    balance = check_balance(profile)
    print(f"   Balance: {balance}")
    
    # Prepare arguments in correct order
    uid = f"hex:{profile.encode('utf-8').hex()}"  # Convert profile name to hex
    wallet_hash = f"hex:{info['address'][2:].encode('utf-8').hex()}"  # Address as hex hash
    api_endpoint = f"hex:{info['api_endpoint'].encode('utf-8').hex()}"  # Endpoint as hex
    
    cmd = [
        "aptos", "move", "run",
        "--profile", profile,
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::register_validator",
        "--args", uid,  # UID as hex
        "--args", f"u64:{SUBNET_UID}",  # subnet_uid
        "--args", f"u64:50000000",  # stake_amount (0.5 APT)
        "--args", wallet_hash,  # wallet_addr_hash as hex
        "--args", api_endpoint,  # api_endpoint as hex
        "--assume-yes"
    ]
    
    result = run_cmd(cmd)
    if result["success"]:
        print(f"✅ Validator {profile} registered successfully")
        return True
    else:
        print(f"❌ Failed to register validator {profile}")
        print(f"   Error: {result['error']}")
        return False

def register_miner(profile: str, info: Dict) -> bool:
    """Đăng ký miner"""
    print(f"⛏️ Registering miner {profile}...")
    
    # Kiểm tra balance trước
    balance = check_balance(profile)
    print(f"   Balance: {balance}")
    
    # Prepare arguments in correct order
    uid = f"hex:{profile.encode('utf-8').hex()}"  # Convert profile name to hex
    wallet_hash = f"hex:{info['address'][2:].encode('utf-8').hex()}"  # Address as hex hash
    api_endpoint = f"hex:{info['api_endpoint'].encode('utf-8').hex()}"  # Endpoint as hex
    
    cmd = [
        "aptos", "move", "run",
        "--profile", profile,
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::register_miner",
        "--args", uid,  # UID as hex
        "--args", f"u64:{SUBNET_UID}",  # subnet_uid
        "--args", f"u64:10000000",  # stake_amount (0.1 APT)
        "--args", wallet_hash,  # wallet_addr_hash as hex
        "--args", api_endpoint,  # api_endpoint as hex
        "--assume-yes"
    ]
    
    result = run_cmd(cmd)
    if result["success"]:
        print(f"✅ Miner {profile} registered successfully")
        return True
    else:
        print(f"❌ Failed to register miner {profile}")
        print(f"   Error: {result['error']}")
        return False

def check_registration(profile: str, entity_type: str, address: str) -> bool:
    """Kiểm tra đăng ký thành công"""
    print(f"🔍 Checking {entity_type} {profile} registration...")
    
    function_name = f"is_{entity_type}"
    cmd = [
        "aptos", "move", "view",
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::{function_name}",
        "--args", f"address:{address}",
        "--url", TESTNET_URL
    ]
    
    result = run_cmd(cmd, show_output=False)
    if result["success"] and "true" in result["output"]:
        print(f"✅ {entity_type.capitalize()} {profile} registration confirmed")
        return True
    else:
        print(f"❌ {entity_type.capitalize()} {profile} registration not found")
        if result["error"]:
            print(f"   Error: {result['error']}")
        return False

def main():
    """Main registration function"""
    print("🎯 Starting Subnet1 Registration Process (Simplified)")
    print("=" * 60)
    
    validators = ["validator_1", "validator_2", "validator_3"]
    miners = ["miner_1", "miner_2"]
    
    all_success = True
    
    # Tạo profiles
    print("\n📋 Step 1: Creating/updating profiles")
    for entity in validators + miners:
        info = KEYS_INFO[entity]
        if not create_aptos_profile(entity, info["private_key"]):
            all_success = False
    
    print("\n🔰 Step 2: Registering Validators")
    for validator in validators:
        info = KEYS_INFO[validator]
        
        if not register_validator(validator, info):
            all_success = False
            
        time.sleep(2)  # Delay giữa registrations
    
    print("\n⛏️ Step 3: Registering Miners") 
    for miner in miners:
        info = KEYS_INFO[miner]
        
        if not register_miner(miner, info):
            all_success = False
            
        time.sleep(2)  # Delay giữa registrations
    
    print("\n🔍 Step 4: Verifying Registrations")
    time.sleep(3)  # Wait for blockchain confirmation
    
    for validator in validators:
        info = KEYS_INFO[validator]
        if not check_registration(validator, "validator", info["address"]):
            all_success = False
    
    for miner in miners:
        info = KEYS_INFO[miner]
        if not check_registration(miner, "miner", info["address"]):
            all_success = False
    
    # Hiển thị network stats cuối cùng
    print("\n📊 Final Network Stats:")
    cmd = [
        "aptos", "move", "view",
        "--function-id", f"{CONTRACT_ADDRESS}::moderntensor::get_network_stats",
        "--url", TESTNET_URL
    ]
    
    result = run_cmd(cmd, show_output=False)
    if result["success"]:
        print("✅ Network Stats:", result["output"])
    else:
        print("❌ Failed to get network stats:", result["error"])
    
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 All registrations completed successfully!")
        print("🎯 Subnet1 is ready with:")
        print("   🔰 3 Validators")
        print("   ⛏️ 2 Miners")
    else:
        print("⚠️ Some registrations failed. Please check the logs above.")
    
    return all_success

if __name__ == "__main__":
    main() 