---
name: dsp-builder
description: Compiles Visual Studio DSP project files. When compiling is needed, pass in a local path, automatically find DSP files and execute compilation. Defaults to Win32 - Debug mode.
---

# DSP Project Compilation Tool

## Overview

This skill is used to compile Visual Studio DSP project files. When compilation is needed, pass in a local path, automatically find DSP project files in that path, extract project names and compilation modes, then directly execute msdev.exe compilation commands via command line, and determine whether compilation is successful. Defaults to using Win32 - Debug mode for compilation.

## Features

- Automatically finds DSP files in the specified path
- Extracts project name and compilation mode information from project files
- Directly executes msdev.exe compilation commands via command line (using /OUT parameter to output compilation results)
- Supports GBK encoding processing to resolve Chinese path and resource file issues
- Waits for command execution to complete and output files to be generated before obtaining compilation results
- Outputs compilation results and determines whether compilation is successful
- Supports batch processing of multiple DSP project files
- Defaults to using Win32 - Debug mode for compilation

## Trigger Conditions

Use this skill when you need to compile Visual Studio DSP project files. Simply pass in the project path, and the skill will automatically handle the compilation process.

## Usage

### Basic Usage

1. When calling this skill, pass in the local path as a parameter
2. The skill will automatically find all files with .dsp extension in that path
3. For each DSP file, extract the project name and compilation mode
4. Directly execute msdev.exe compilation command via command line (using GBK encoding and /OUT parameter)
5. Wait for command execution to complete and output files to be generated, then obtain and analyze compilation results
6. Output compilation results and success status

### Parameter Description

- **local_path**£ºLocal path used to find DSP project files
- **compile_mode**£ºOptional, specifies the compilation mode, such as "Win32 Debug", "Win32 Release", etc., defaults to "Win32 Debug"
- **project_name**£ºOptional, specifies the project name, used to filter specific projects
- **encoding**£ºOptional, specifies the encoding, defaults to "GBK", used to handle Chinese paths and resource files

### Output Results

- **success**£ºWhether compilation is successful (true/false)
- **output**£ºCompilation output information
- **error**£ºError information (if any)
- **projects**£ºList of processed projects, including project name, compilation mode, and compilation status

## Implementation Principle

1. **File Search**£ºUses glob pattern to find DSP files in the specified path
2. **Project Information Extraction**£ºParses DSP file content to extract project name and compilation mode
3. **Compilation Execution**£ºSets GBK encoding, builds msdev.exe command line (including /OUT parameter), directly executes compilation operation via command line and waits for completion
4. **Result Obtaining**£ºWaits for output file generation (maximum 60 seconds), reads and analyzes compilation results
5. **Success Judgment**£ºDetermines whether compilation is successful based on compilation output

## Examples

### Example 1: Basic Compilation (using default Win32 - Debug mode)

```
/dsp-builder "C:\Projects\MyProject"
```

### Example 2: Specifying Compilation Mode

```
/dsp-builder "C:\Projects\MyProject" "Win32 Release"
```

### Example 3: Specifying Project Name

```
/dsp-builder "C:\Projects\MyProject" "Win32 Debug" "SCManager"
```

## Dependencies

- **msdev.exe**£ºVisual Studio 6.0 or earlier development environment, needs to be in system PATH or specified in configuration
- **Windows Operating System**£ºSince msdev.exe is a Windows-specific tool
- **Permissions**£ºNeeds permission to execute msdev.exe and access project files

## Notes

1. This skill only supports Visual Studio 6.0 and earlier DSP project files
2. Ensure msdev.exe is in system PATH or specify its path in skill configuration
3. Compilation process may be time-consuming, depending on project size and complexity
4. For projects with Chinese paths or resource files, it is recommended to use GBK encoding
5. Compilation result judgment is based on output information, which may be affected by different versions of msdev.exe output formats
6. The skill waits for command execution to complete and output files to be generated before obtaining results, ensuring complete compilation output capture
7. The skill waits up to 60 seconds to obtain compilation output files, after which it returns an error message if timed out
8. Defaults to using Win32 - Debug mode for compilation, no need to specify manually

## Error Handling

- **No DSP files found**£ºReturns error message indicating no DSP files found in the specified path
- **msdev.exe not found**£ºReturns error message indicating msdev.exe not found in the system
- **Compilation failed**£ºReturns error message containing details of compilation errors
- **Insufficient permissions**£ºReturns error message indicating inability to access files or execute commands
- **Encoding issues**£ºIf encountering Chinese path or resource file issues, try using GBK encoding
- **Output file generation timeout**£ºIf output file not generated within 60 seconds, returns timeout error

## Configuration Instructions

### msdev.exe Path Configuration

If msdev.exe is not in system PATH, you can specify its path in the skill configuration:

```python
# msdev.exe path
MSDEV_PATH = "C:\Program Files (x86)\Microsoft Visual Studio\Common\MSDev98\Bin\MSDEV.EXE"
```

### Encoding Configuration

Default uses GBK encoding to handle Chinese paths and resource files, ensuring no encoding errors during compilation.

### Compilation Command Configuration

The skill uses the following command format to execute compilation:

```
chcp 936 && "msdev.exe path" "dsp file path" /MAKE "project name - compilation mode" /OUT "compile_output.txt"
```

This ensures:
1. Uses GBK encoding to handle Chinese
2. Redirects compilation output to file
3. Waits for command execution to complete before obtaining results

### Output File Waiting Configuration

The skill waits for compilation output file generation, maximum 60 seconds:

```python
# Wait for output file generation, maximum 60 seconds
max_wait_time = 60
start_time = time.time()
while not os.path.exists(output_file) and (time.time() - start_time) < max_wait_time:
    print(f"Waiting for output file to be generated... ({int(time.time() - start_time)}s)")
    time.sleep(1)
```

### Default Compilation Mode Configuration

The skill defaults to using Win32 - Debug mode for compilation, no need to specify manually:

```python
# Select compilation mode
target_mode = compile_mode if compile_mode else "Win32 Debug"
```

## Summary

This skill provides an automated method for compiling Visual Studio DSP project files. When compilation is needed, through simple parameter input, it can complete the entire process from finding files to executing compilation, and return compilation results. It supports GBK encoding processing, resolving Chinese path and resource file issues. The skill waits for command execution to complete and output files to be generated before»ñÈ¡ results, ensuring complete compilation output capture. It defaults to using Win32 - Debug mode for compilation, simplifying user operations. This is very useful for scenarios that require batch compilation of multiple DSP projects, greatly improving development efficiency.