#!/usr/bin/env python3
# -*- coding: gbk -*-
"""
DSP Project Compilation Tool
Compile projects directly through command line execution of msdev.exe and output compilation results
"""

import os
import sys
import time
import glob
import re

# msdev.exe path, can be modified according to actual situation
MSDEV_PATH = "C:\Program Files (x86)\Microsoft Visual Studio\Common\MSDev98\Bin\MSDEV.EXE"

# Default compilation mode
DEFAULT_COMPILE_MODE = "Win32 Debug"

# Maximum waiting time (seconds)
MAX_WAIT_TIME = 60

def find_dsp_files(local_path):
    """Find DSP files in the specified path"""
    dsp_files = []
    
    # Find DSP files in the root directory
    root_pattern = os.path.join(local_path, "*.dsp")
    for dsp_file in glob.glob(root_pattern):
        dsp_files.append(dsp_file)

    return dsp_files

def extract_project_info(dsp_file):
    """Extract project name from DSP file"""
    try:
        with open(dsp_file, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()
        # Find project name
        match = re.search(r'Project\s*=\s*"([^"]+)"', content)
        if match:
            project_name = match.group(1)
            return project_name
        return os.path.splitext(os.path.basename(dsp_file))[0]
    except Exception as e:
        print(f"Failed to extract project info: {e}")
        return os.path.splitext(os.path.basename(dsp_file))[0]

def build_compile_command(dsp_file, project_name, compile_mode):
    """Build compilation command"""
    # Ensure msdev.exe path exists
    if not os.path.exists(MSDEV_PATH):
        raise Exception(f"msdev.exe not found at {MSDEV_PATH}")
    
    # Build command
    command = f"chcp 936 && \"{MSDEV_PATH}\" \"{dsp_file}\" /MAKE \"{project_name} - {compile_mode}\" /OUT \"compile_output.txt\""
    return command

def execute_command(command, cwd=None):
    """Execute command and return result"""
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='gbk'
        )
        return result
    except Exception as e:
        print(f"Failed to execute command: {e}")
        return None

def wait_for_output_file(output_file):
    """Wait for output file to be generated"""
    start_time = time.time()
    while not os.path.exists(output_file) and (time.time() - start_time) < MAX_WAIT_TIME:
        print(f"Waiting for output file to be generated... ({int(time.time() - start_time)}s)")
        time.sleep(1)
    
    if not os.path.exists(output_file):
        raise Exception(f"Output file generation timeout, exceeding {MAX_WAIT_TIME} seconds")
    
    # Wait for file content to be written completely
    time.sleep(2)

def analyze_compile_result(output_file):
    """Analyze compilation result"""
    try:
        with open(output_file, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()
        
        # Determine if compilation is successful
        if "error(s), 0 warning(s)" in content:
            success = True
            error = ""
        else:
            success = False
            # Extract error information
            error_match = re.search(r'error.*', content, re.DOTALL)
            if error_match:
                error = error_match.group(0)
            else:
                error = content
        
        return success, content, error
    except Exception as e:
        print(f"Failed to analyze compilation result: {e}")
        return False, "", str(e)

def compile_dsp(local_path, compile_mode=None, project_name=None):
    """Compile DSP project"""
    # Find DSP files
    dsp_files = find_dsp_files(local_path)
    if not dsp_files:
        print("Error: No DSP files found")
        return False, "", "No DSP files found", []
    
    # Filter projects
    if project_name:
        filtered_files = []
        for dsp_file in dsp_files:
            extracted_name = extract_project_info(dsp_file)
            if extracted_name == project_name:
                filtered_files.append(dsp_file)
        dsp_files = filtered_files
        if not dsp_files:
            print(f"Error: No DSP files found for project name {project_name}")
            return False, "", f"No DSP files found for project name {project_name}", []
    
    # Use default compilation mode
    if not compile_mode:
        compile_mode = DEFAULT_COMPILE_MODE
    
    results = []
    all_success = True
    all_output = ""
    all_error = ""
    
    # Compile each DSP file
    for dsp_file in dsp_files:
        print(f"\nCompiling project: {dsp_file}")
        
        # Extract project name
        extracted_project_name = extract_project_info(dsp_file)
        print(f"Project name: {extracted_project_name}")
        print(f"Compile mode: {compile_mode}")
        
        # Build compilation command
        try:
            command = build_compile_command(dsp_file, extracted_project_name, compile_mode)
            print(f"Executing command: {command}")
            
            # Execute command
            result = execute_command(command, cwd=os.path.dirname(dsp_file))
            if result is None:
                success = False
                output = ""
                error = "Failed to execute command"
            else:
                # Wait for output file to be generated
                output_file = os.path.join(os.path.dirname(dsp_file), "compile_output.txt")
                try:
                    wait_for_output_file(output_file)
                    # Analyze compilation result
                    success, output, error = analyze_compile_result(output_file)
                except Exception as e:
                    success = False
                    output = ""
                    error = str(e)
            
            # Record result
            results.append({
                "project_name": extracted_project_name,
                "compile_mode": compile_mode,
                "status": success
            })
            
            # Update overall result
            all_success = all_success and success
            all_output += f"\n=== Compiling {extracted_project_name} ===\n{output}\n"
            if error:
                all_error += f"\n=== {extracted_project_name} Error ===\n{error}\n"
            
            # Output compilation status
            if success:
                print("Compilation successful!")
            else:
                print("Compilation failed!")
                if error:
                    print(f"Error message: {error}")
                    
        except Exception as e:
            print(f"Error during compilation: {e}")
            results.append({
                "project_name": extracted_project_name,
                "compile_mode": compile_mode,
                "status": False
            })
            all_success = False
            all_error += f"\n=== {extracted_project_name} Error ===\n{str(e)}\n"
    
    return all_success, all_output, all_error, results

def main():
    """Main function"""
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python run.py <local_path> [compile_mode] [project_name]")
        print(f"Example: python run.py \"C:\\Projects\\MyProject\" \"Win32 Debug\" \"SCManager\"")
        return
    
    local_path = sys.argv[1]
    compile_mode = sys.argv[2] if len(sys.argv) > 2 else None
    project_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Validate path
    if not os.path.exists(local_path):
        print(f"Error: Path does not exist: {local_path}")
        return
    
    # Execute compilation
    success, output, error, projects = compile_dsp(local_path, compile_mode, project_name)
    
    # Output result
    print("\n" + "="*60)
    print("Compilation Result Summary")
    print("="*60)
    print(f"Overall status: {'Success' if success else 'Failed'}")
    print(f"Number of projects processed: {len(projects)}")
    
    print("\nProject details:")
    for project in projects:
        status = "Success" if project["status"] else "Failed"
        print(f"- {project['project_name']} ({project['compile_mode']}): {status}")
    
    if error:
        print("\nError information:")
        print(error)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
