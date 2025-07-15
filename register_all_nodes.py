#!/usr/bin/env python3
"""
ModernTensor Subnet1 Registration Script
=======================================

This script registers all validators and miners for subnet1
in a professional and organized way.
"""

import subprocess
import sys
import time
import json
import os

# Configuration
CONTRACT_ADDRESS = "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04"
SUBNET_ID = 1
PROFILE = "default"

# Node configurations for Subnet1 (Image Generation)
NODES_CONFIG = {
    "validators": [
        {
            "key_index": 1,
            "name": "image_validator_1",
            "profile": "default",  # Already registered - will skip
            "hex_name": "696d6167655f76616c696461746f725f31",  # "image_validator_1" in hex
            "stake": 50000000,
            "validator_bond": 10000000,  # 0.1 APT bond
            "wallet_hex": "696d6167655f76616c696461746f725f315f77616c6c6574",  # "image_validator_1_wallet" in hex
            "endpoint_hex": "687474703a2f2f696d6167652d76616c696461746f72312e6578616d706c652e636f6d"  # "http://image-validator1.example.com" in hex
        },
        {
            "key_index": 3,
            "name": "image_validator_2", 
            "profile": "validator2",  # Using Key 3
            "hex_name": "696d6167655f76616c696461746f725f32",  # "image_validator_2" in hex
            "stake": 50000000,
            "validator_bond": 10000000,  # 0.1 APT bond
            "wallet_hex": "696d6167655f76616c696461746f725f325f77616c6c6574",  # "image_validator_2_wallet" in hex
            "endpoint_hex": "687474703a2f2f696d6167652d76616c696461746f72322e6578616d706c652e636f6d"  # "http://image-validator2.example.com" in hex
        },
        {
            "key_index": 4,
            "name": "image_validator_3",
            "profile": "validator3",  # Using Key 4
            "hex_name": "696d6167655f76616c696461746f725f33",  # "image_validator_3" in hex
            "stake": 50000000,
            "validator_bond": 10000000,  # 0.1 APT bond
            "wallet_hex": "696d6167655f76616c696461746f725f335f77616c6c6574",  # "image_validator_3_wallet" in hex
            "endpoint_hex": "687474703a2f2f696d6167652d76616c696461746f72332e6578616d706c652e636f6d"  # "http://image-validator3.example.com" in hex
        }
    ],
    "miners": [
        {
            "key_index": 2,
            "name": "image_generator_1",
            "profile": "miner1",  # Using Key 2
            "hex_name": "696d6167655f67656e657261746f725f31",  # "image_generator_1" in hex
            "stake": 10000000,
            "wallet_hex": "696d6167655f67656e657261746f725f315f77616c6c6574",  # "image_generator_1_wallet" in hex
            "endpoint_hex": "687474703a2f2f696d6167652d67656e657261746f72312e6578616d706c652e636f6d"  # "http://image-generator1.example.com" in hex
        },
        {
            "key_index": 5,
            "name": "image_generator_2",
            "profile": "miner2",  # Using Key 5
            "hex_name": "696d6167655f67656e657261746f725f32",  # "image_generator_2" in hex
            "stake": 10000000,
            "wallet_hex": "696d6167655f67656e657261746f725f325f77616c6c6574",  # "image_generator_2_wallet" in hex
            "endpoint_hex": "687474703a2f2f696d6167652d67656e657261746f72322e6578616d706c652e636f6d"  # "http://image-generator2.example.com" in hex
        }
    ]
}

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {text}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def run_cmd(cmd, description=""):
    """Run a command and show the result"""
    if description:
        print(f"🔄 {description}")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Failed!")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_contract_deployment():
    """Check if contract is deployed and accessible"""
    print_step(1, "Checking contract deployment")
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_network_stats"
    if not run_cmd(cmd, "Verifying contract deployment"):
        print("❌ Contract not deployed or not responding")
        print("💡 Please ensure the contract is deployed first")
        return False
    return True

def get_network_info():
    """Get current network information"""
    print_step(2, "Getting network information")
    
    # Get network stats
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_network_stats"
    run_cmd(cmd, "Getting network statistics")
    
    # Get all validators
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_all_validators"
    run_cmd(cmd, "Getting validator list")
    
    # Get all miners
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_all_miners"
    run_cmd(cmd, "Getting miner list")

def register_validators():
    """Register all validators"""
    print_step(3, "Registering validators")
    
    success_count = 0
    for validator in NODES_CONFIG["validators"]:
        print(f"\n📋 Registering {validator['name']} (Key {validator['key_index']})")
        
        # Skip already registered validator
        if validator['profile'] == 'default':
            print(f"⏭️  Skipping {validator['name']} - already registered")
            success_count += 1
            continue
        
        cmd = f"""aptos move run --profile {validator['profile']} --assume-yes \\
            --function-id {CONTRACT_ADDRESS}::moderntensor::register_validator \\
            --args hex:"{validator['hex_name']}" \\
            --args u64:{SUBNET_ID} \\
            --args u64:{validator['stake']} \\
            --args u64:{validator['validator_bond']} \\
            --args hex:"{validator['wallet_hex']}" \\
            --args hex:"{validator['endpoint_hex']}" """
        
        if run_cmd(cmd, f"Registering {validator['name']}"):
            success_count += 1
            print(f"✅ {validator['name']} registered successfully!")
            time.sleep(3)  # Wait for transaction confirmation
        else:
            print(f"❌ Failed to register {validator['name']}")
    
    print(f"\n📊 Validators registered: {success_count}/{len(NODES_CONFIG['validators'])}")
    return success_count

def register_miners():
    """Register all miners"""
    print_step(4, "Registering miners")
    
    success_count = 0
    for miner in NODES_CONFIG["miners"]:
        print(f"\n📋 Registering {miner['name']} (Key {miner['key_index']})")
        
        cmd = f"""aptos move run --profile {miner['profile']} --assume-yes \\
            --function-id {CONTRACT_ADDRESS}::moderntensor::register_miner \\
            --args hex:"{miner['hex_name']}" \\
            --args u64:{SUBNET_ID} \\
            --args u64:{miner['stake']} \\
            --args hex:"{miner['wallet_hex']}" \\
            --args hex:"{miner['endpoint_hex']}" """
        
        if run_cmd(cmd, f"Registering {miner['name']}"):
            success_count += 1
            print(f"✅ {miner['name']} registered successfully!")
            time.sleep(3)  # Wait for transaction confirmation
        else:
            print(f"❌ Failed to register {miner['name']}")
    
    print(f"\n📊 Miners registered: {success_count}/{len(NODES_CONFIG['miners'])}")
    return success_count

def verify_registrations():
    """Verify all registrations were successful"""
    print_step(5, "Verifying registrations")
    
    # Get updated network stats
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_network_stats"
    run_cmd(cmd, "Getting updated network statistics")
    
    # Get all validators
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_all_validators"
    run_cmd(cmd, "Getting all validators")
    
    # Get all miners
    cmd = f"aptos move view --profile {PROFILE} --function-id {CONTRACT_ADDRESS}::moderntensor::get_all_miners"
    run_cmd(cmd, "Getting all miners")

def main():
    """Main registration function"""
    print_header("MODERNTENSOR SUBNET1 REGISTRATION - IMAGE GENERATION")
    
    print("This script will register all nodes for subnet1 (Image Generation):")
    print("📋 Image Validators:")
    for validator in NODES_CONFIG["validators"]:
        print(f"  • {validator['name']} (Key {validator['key_index']})")
    
    print("\n📋 Image Generators:")
    for miner in NODES_CONFIG["miners"]:
        print(f"  • {miner['name']} (Key {miner['key_index']})")
    
    print(f"\n🎯 Target subnet: {SUBNET_ID} (Image Generation - No Permits Required)")
    print(f"📧 Contract: {CONTRACT_ADDRESS}")
    
    input("\nPress Enter to continue...")
    
    # Step 1: Check contract deployment
    if not check_contract_deployment():
        sys.exit(1)
    
    # Step 2: Get network information
    get_network_info()
    
    # Step 3: Register validators
    validator_count = register_validators()
    
    # Step 4: Register miners
    miner_count = register_miners()
    
    # Step 5: Verify registrations
    verify_registrations()
    
    # Summary
    print_header("REGISTRATION COMPLETED!")
    
    total_validators = len(NODES_CONFIG["validators"])
    total_miners = len(NODES_CONFIG["miners"])
    
    print("🎉 Registration Summary:")
    print(f"  ✅ Validators: {validator_count}/{total_validators}")
    print(f"  ✅ Miners: {miner_count}/{total_miners}")
    print(f"  🎯 Total nodes: {validator_count + miner_count}/{total_validators + total_miners}")
    
    if validator_count == total_validators and miner_count == total_miners:
        print("\n🎊 All registrations successful!")
    else:
        print("\n⚠️  Some registrations failed. Please check the logs above.")
    
    print("\n🚀 Next Steps:")
    print("  1. Start consensus testing")
    print("  2. Monitor node performance")
    print("  3. Test validator permits")
    print("  4. Check staking rewards")
    print("  5. Run metagraph updates")
    
    print("\n💡 Useful Commands:")
    print("  • Check balance: aptos account list --profile default")
    print("  • View subnet: aptos move view --function-id <addr>::moderntensor::get_subnet_info --args u64:1")
    print("  • Network stats: aptos move view --function-id <addr>::moderntensor::get_enhanced_network_stats")
    
    print("\n" + "="*60)
    print("✨ Subnet1 is ready for operation! ✨")
    print("="*60)

if __name__ == "__main__":
    main() 