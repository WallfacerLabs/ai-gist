#!/usr/bin/env python3

"""
Test virtual environment setup commands from documentation
Validates that the virtual environment workflow from claude.md works correctly
"""

import unittest
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path


class TestVirtualEnvironmentSetup(unittest.TestCase):
    """Test virtual environment setup commands from documentation"""
    
    def setUp(self):
        """Set up temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_venv_creation_command(self):
        """Test 'python -m venv venv' command from documentation"""
        # This is the exact command from documentation
        result = subprocess.run([
            sys.executable, '-m', 'venv', 'venv'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"venv creation failed: {result.stderr}")
        
        # Check that venv directory was created
        venv_path = Path('venv')
        self.assertTrue(venv_path.exists(), "venv directory should be created")
        self.assertTrue(venv_path.is_dir(), "venv should be a directory")
        
        # Check for expected venv structure
        if sys.platform == 'win32':
            python_exe = venv_path / 'Scripts' / 'python.exe'
            pip_exe = venv_path / 'Scripts' / 'pip.exe'
        else:
            python_exe = venv_path / 'bin' / 'python'
            pip_exe = venv_path / 'bin' / 'pip'
        
        self.assertTrue(python_exe.exists(), f"Python executable should exist at {python_exe}")
        self.assertTrue(pip_exe.exists(), f"Pip executable should exist at {pip_exe}")
    
    def test_venv_activation_script_exists(self):
        """Test that activation script exists (referenced in documentation)"""
        # Create venv first
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        venv_path = Path('venv')
        
        if sys.platform == 'win32':
            # Windows activation script
            activate_script = venv_path / 'Scripts' / 'activate.bat'
        else:
            # Unix/macOS activation script (from documentation)
            activate_script = venv_path / 'bin' / 'activate'
        
        self.assertTrue(
            activate_script.exists(),
            f"Activation script should exist at {activate_script}"
        )
    
    def test_pip_install_in_venv(self):
        """Test pip install commands work in virtual environment"""
        # Create venv
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        venv_path = Path('venv')
        
        if sys.platform == 'win32':
            python_exe = venv_path / 'Scripts' / 'python.exe'
            pip_exe = venv_path / 'Scripts' / 'pip.exe'
        else:
            python_exe = venv_path / 'bin' / 'python'
            pip_exe = venv_path / 'bin' / 'pip'
        
        # Test pip install command (install a simple package for testing)
        result = subprocess.run([
            str(pip_exe), 'install', 'requests'
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"pip install failed: {result.stderr}")
        
        # Test that package is available in venv
        test_import = subprocess.run([
            str(python_exe), '-c', 'import requests; print("success")'
        ], capture_output=True, text=True)
        
        self.assertEqual(test_import.returncode, 0, "Package should be importable in venv")
        self.assertIn("success", test_import.stdout)
    
    def test_requirements_txt_creation(self):
        """Test requirements.txt creation mentioned in documentation"""
        # Create venv
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        venv_path = Path('venv')
        
        if sys.platform == 'win32':
            pip_exe = venv_path / 'Scripts' / 'pip.exe'
        else:
            pip_exe = venv_path / 'bin' / 'pip'
        
        # Install a package
        subprocess.run([str(pip_exe), 'install', 'requests'], check=True)
        
        # Test pip freeze > requirements.txt (from documentation)
        with open('requirements.txt', 'w') as f:
            result = subprocess.run([
                str(pip_exe), 'freeze'
            ], stdout=f, capture_output=False, text=True)
        
        # Check that requirements.txt was created and has content
        requirements_file = Path('requirements.txt')
        self.assertTrue(requirements_file.exists(), "requirements.txt should be created")
        
        content = requirements_file.read_text()
        self.assertIn('requests', content, "requirements.txt should contain installed packages")
    
    def test_gitignore_patterns(self):
        """Test .gitignore patterns mentioned in documentation"""
        # These are the exact patterns from documentation
        gitignore_content = """venv/
*.pyc
__pycache__/
.env"""
        
        # Create .gitignore
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        
        # Create some files that should be ignored
        os.makedirs('venv', exist_ok=True)
        os.makedirs('__pycache__', exist_ok=True)
        
        Path('test.pyc').touch()
        Path('.env').touch()
        Path('__pycache__/test.pyc').touch()
        
        # Test git status (if git is available)
        try:
            # Initialize git repo
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            subprocess.run(['git', 'add', '.gitignore'], check=True, capture_output=True)
            
            # Check git status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            # Files in .gitignore should not appear in git status
            status_output = result.stdout
            self.assertNotIn('venv/', status_output, "venv/ should be ignored")
            self.assertNotIn('.pyc', status_output, ".pyc files should be ignored")
            self.assertNotIn('.env', status_output, ".env should be ignored")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Git not available, skip this part
            self.skipTest("Git not available for testing .gitignore patterns")


class TestProjectStructure(unittest.TestCase):
    """Test recommended project structure from documentation"""
    
    def setUp(self):
        """Set up temporary directory"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_recommended_project_structure(self):
        """Test creating recommended project structure from documentation"""
        # This is the exact structure from documentation
        structure = [
            'venv/',
            'src/',
            'src/main.py',
            'src/utils.py',
            'tests/',
            'tests/test_main.py',
            'requirements.txt',
            '.gitignore',
            'README.md'
        ]
        
        # Create the structure
        for item in structure:
            path = Path(item)
            if item.endswith('/'):
                # Directory
                path.mkdir(parents=True, exist_ok=True)
            else:
                # File
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
        
        # Verify structure exists
        for item in structure:
            path = Path(item.rstrip('/'))
            self.assertTrue(path.exists(), f"{item} should exist in project structure")


if __name__ == '__main__':
    print("🧪 Testing Virtual Environment Setup Commands...\n")
    
    # Check if we're already in a venv
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if in_venv:
        print("✅ Currently running in a virtual environment")
    else:
        print("⚠️  Not running in a virtual environment")
        print("   (This is expected when testing venv creation)")
    
    print()
    
    unittest.main(verbosity=2)