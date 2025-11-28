#!/usr/bin/env python3
"""
F1 Telegram Bot Deployment Validation Script
This script validates the deployment configuration for Leapcell.
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class DeploymentValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_structure(self):
        """Validate project structure"""
        required_files = [
            'leapcell_f1_bot.py',
            'leapcell.yaml',
            'Dockerfile',
            'requirements.txt',
            'optimized_scraper.py',
            'final_working_scraper.py',
            'streams.txt',
            'user_streams.json'
        ]
        
        missing_files = []
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.errors.append(f"Missing required files: {', '.join(missing_files)}")
        else:
            self.info.append("All required files present")
    
    def validate_dockerfile(self):
        """Validate Dockerfile configuration"""
        try:
            with open('Dockerfile', 'r') as f:
                dockerfile_content = f.read()
            
            # Check for critical components
            checks = {
                'FROM python:3.11': 'Base image',
                'WORKDIR /app': 'Working directory',
                'pip install': 'Python dependencies',
                'playwright install': 'Playwright browsers',
                'USER app': 'Non-root user',
                'EXPOSE 8080': 'Port exposure',
                'gunicorn': 'WSGI server'
            }
            
            for check, description in checks.items():
                if check not in dockerfile_content:
                    self.warnings.append(f"Missing in Dockerfile: {description}")
                else:
                    self.info.append(f"Dockerfile: {description}")
                    
        except Exception as e:
            self.errors.append(f"Dockerfile validation error: {e}")
    
    def validate_leapcell_config(self):
        """Validate leapcell.yaml configuration"""
        try:
            with open('leapcell.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            # Check critical sections
            required_sections = ['ports', 'env', 'image', 'healthCheck']
            for section in required_sections:
                if section not in config.get('spec', {}):
                    self.errors.append(f"Missing leapcell.yaml section: {section}")
                else:
                    self.info.append(f"leapcell.yaml: {section}")
            
            # Check environment variables
            env_vars = [env['name'] for env in config['spec'].get('env', [])]
            required_env = ['TELEGRAM_BOT_TOKEN', 'PORT']
            for var in required_env:
                if var not in env_vars:
                    self.errors.append(f"Missing environment variable: {var}")
                else:
                    self.info.append(f"Environment variable: {var}")
                    
        except Exception as e:
            self.errors.append(f"leapcell.yaml validation error: {e}")
    
    def validate_requirements(self):
        """Validate Python requirements"""
        try:
            with open('requirements.txt', 'r') as f:
                requirements = f.read()
            
            required_packages = [
                'python-telegram-bot',
                'flask',
                'gunicorn',
                'requests',
                'playwright'
            ]
            
            for package in required_packages:
                if package not in requirements:
                    self.warnings.append(f"Missing package: {package}")
                else:
                    self.info.append(f"Requirement: {package}")
                    
        except Exception as e:
            self.errors.append(f"requirements.txt validation error: {e}")
    
    def validate_python_syntax(self):
        """Validate Python files syntax"""
        python_files = [
            'leapcell_f1_bot.py',
            'optimized_scraper.py',
            'final_working_scraper.py'
        ]
        
        for file in python_files:
            try:
                # Try to read with utf-8 first, fallback to latin-1 if needed
                content = None
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(file, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    self.errors.append(f"Could not read {file} with any encoding")
                    continue
                
                compile(content, file, 'exec')
                self.info.append(f"Syntax OK: {file}")
                
            except SyntaxError as e:
                self.errors.append(f"Syntax error in {file}: {e}")
            except Exception as e:
                self.errors.append(f"Error validating {file}: {e}")
    
    def validate_environment(self):
        """Check environment setup"""
        # Check if required environment variables are set
        required_env_vars = ['TELEGRAM_BOT_TOKEN']
        for var in required_env_vars:
            if os.getenv(var):
                self.info.append(f"Environment variable set: {var}")
            else:
                self.warnings.append(f"Environment variable not set: {var} (required for testing)")
    
    def check_docker_build(self):
        """Check if Docker build would succeed"""
        try:
            result = subprocess.run([
                'docker', 'build', '-t', 'f1-bot-test', '.'
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.info.append("Docker build successful")
                # Clean up
                subprocess.run(['docker', 'rmi', 'f1-bot-test'], capture_output=True)
            else:
                self.errors.append(f"Docker build failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.warnings.append("Docker build timeout (might be slow network)")
        except FileNotFoundError:
            self.warnings.append("Docker not installed (skipping build test)")
        except Exception as e:
            self.warnings.append(f"Docker test error: {e}")
    
    def validate_telegram_token(self):
        """Validate Telegram bot token format"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if token:
            if len(token) > 10 and ':' in token:
                self.info.append("Telegram token format appears valid")
            else:
                self.warnings.append("Telegram token format might be invalid")
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*60)
        print("F1 TELEGRAM BOT DEPLOYMENT VALIDATION REPORT")
        print("="*60)
        
        # Summary
        print(f"\nSUMMARY:")
        print(f"Info: {len(self.info)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")
        
        # Info messages
        if self.info:
            print(f"\nINFO:")
            for msg in self.info:
                print(f"  {msg}")
        
        # Warnings
        if self.warnings:
            print(f"\nWARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        # Errors
        if self.errors:
            print(f"\nERRORS:")
            for msg in self.errors:
                print(f"  {msg}")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        if self.errors:
            print("  1. Fix all errors before deployment")
            print("  2. Address warnings for optimal performance")
        elif self.warnings:
            print("  1. Address warnings for optimal performance")
            print("  2. All critical components are configured")
        else:
            print("  1. All validations passed!")
            print("  2. Ready for deployment")
        
        print(f"\nNEXT STEPS:")
        print("  1. Set TELEGRAM_BOT_TOKEN environment variable")
        print("  2. Push code to GitHub")
        print("  3. Follow DEPLOYMENT_GUIDE.md")
        print("  4. Deploy on Leapcell")
        
        # Return success status
        return len(self.errors) == 0
    
    def run_all_validations(self):
        """Run all validation checks"""
        print("Running deployment validation checks...")
        
        self.validate_structure()
        self.validate_dockerfile()
        self.validate_leapcell_config()
        self.validate_requirements()
        self.validate_python_syntax()
        self.validate_environment()
        self.validate_telegram_token()
        
        # Only run Docker test if not in CI/CD
        if not os.getenv('CI'):
            self.check_docker_build()
        
        return self.generate_report()

def main():
    """Main validation function"""
    validator = DeploymentValidator()
    success = validator.run_all_validations()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()