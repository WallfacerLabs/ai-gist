#!/usr/bin/env python3

"""
Main test runner for Python tests
Runs all Python tests to verify documentation examples and commands
"""

import subprocess
import sys
import os
from pathlib import Path


def run_test_file(test_file):
    """Run a specific test file and return success status"""
    print(f"\n🏃 Running {test_file}...")
    
    try:
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {test_file} passed")
            print(result.stdout)
            return True
        else:
            print(f"❌ {test_file} failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    dependencies = ['vaultsfyi', 'pytest']
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} is available")
        except ImportError:
            print(f"❌ {dep} is missing")
            missing.append(dep)
    
    return missing


def main():
    """Main test runner"""
    print("🚀 Running Python Tests for vaults.fyi Documentation\n")
    
    # Check if we're in a virtual environment
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if in_venv:
        print("✅ Running in a virtual environment (recommended)")
    else:
        print("⚠️  Not running in a virtual environment")
        print("   Recommendation: Create and activate a virtual environment:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print()
    
    # Check dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please install them with:")
        print("pip install " + " ".join(missing_deps))
        print("Or: pip install -r requirements.txt")
        return False
    
    print()
    
    # List of test files to run
    tests = [
        ('Virtual Environment Setup', 'test_venv_setup.py'),
        ('SDK Imports and Examples', 'test_imports.py'),
        ('Parameter Coverage Tests', 'test_parameters.py')
    ]
    
    print("📋 Test Plan:")
    for i, (name, file) in enumerate(tests, 1):
        print(f"   {i}. {name} ({file})")
    print()
    
    # Run all tests
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_file in tests:
        if run_test_file(test_file):
            passed_tests += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 Final Results: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("🎉 All Python tests passed!")
        print("✅ All documentation examples and commands are working correctly.")
        return True
    else:
        print("💥 Some tests failed.")
        print("❌ Documentation examples or commands may need to be updated.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)