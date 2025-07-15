#!/usr/bin/env python3
"""
Request Validator Permits for Subnet1
=====================================

This script requests validator permits for all validators in subnet1.
"""

import subprocess
import sys
import time

# Configuration
CONTRACT_ADDRESS = "0x9ba2d796ed64ea00a4f7690be844174820e0729de9f37fcaae429bc15ac37c04"
SUBNET_ID = 1

# Validators that need permits
VALIDATORS = [
    {"name": "image_validator_1", "profile": "validator_1", "key_index": 1},
    {"name": "image_validator_2", "profile": "validator_2", "key_index": 3},
    {"name": "image_validator_3", "profile": "validator_3", "key_index": 4}
]

def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔐 {text}")
    print(f"{'='*60}")

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

def request_validator_permits():
    """Request validator permits for all validators"""
    print_header("REQUESTING VALIDATOR PERMITS")
    
    success_count = 0
    for validator in VALIDATORS:
        print(f"\n📋 Requesting permit for {validator['name']} (Key {validator['key_index']})")
        
        cmd = f"""aptos move run --profile {validator['profile']} --assume-yes \\
            --function-id {CONTRACT_ADDRESS}::moderntensor::request_validator_permit \\
            --args u64:{SUBNET_ID}"""
        
        if run_cmd(cmd, f"Requesting permit for {validator['name']}"):
            success_count += 1
            print(f"✅ Permit requested for {validator['name']}!")
            time.sleep(3)  # Wait for transaction confirmation
        else:
            print(f"❌ Failed to request permit for {validator['name']}")
    
    print(f"\n📊 Permits requested: {success_count}/{len(VALIDATORS)}")
    return success_count

def main():
    """Main function"""
    print_header("VALIDATOR PERMIT REQUEST")
    
    print("This script will request validator permits for:")
    for validator in VALIDATORS:
        print(f"  • {validator['name']} (Key {validator['key_index']})")
    
    print(f"\n🎯 Target subnet: {SUBNET_ID} (Image Generation)")
    print(f"📧 Contract: {CONTRACT_ADDRESS}")
    
    input("\nPress Enter to continue...")
    
    # Request permits
    success_count = request_validator_permits()
    
    # Summary
    print_header("PERMIT REQUEST COMPLETED!")
    
    total_validators = len(VALIDATORS)
    
    print("🎉 Permit Request Summary:")
    print(f"  ✅ Permits requested: {success_count}/{total_validators}")
    
    if success_count == total_validators:
        print("\n🎊 All permits requested successfully!")
        print("\n🚀 Next Steps:")
        print("  1. Wait for permits to be approved (may take time)")
        print("  2. Run register_all_nodes.py to register nodes")
        print("  3. Check permit status if needed")
    else:
        print("\n⚠️  Some permits failed. Please check the logs above.")
    
    print("\n💡 Note:")
    print("  • Permits may need manual approval")
    print("  • Check validator permit status before registering")
    print("  • Some subnets may have automatic permit approval")
    
    print("\n" + "="*60)
    print("✨ Permit requests completed! ✨")
    print("="*60)

if __name__ == "__main__":
    main() 