#!/usr/bin/env python3
"""
patchtree.py - Patch management module for OpenKomodoIDE build system

This module handles applying patches to the Mozilla source tree.
"""

import os
import sys
import logging
import shutil
import subprocess
from os.path import join, exists, basename, dirname

# Setup logging
log = logging.getLogger("patchtree")


def log_setLevel(level):
    """Set logging level for patchtree module"""
    log.setLevel(level)


def patch(patches_dirs, src_dir, config=None, dryRun=0, logDir=None, patchExe="patch", logFilename=None):
    """
    Apply patches from patches_dirs to src_dir
    
    Args:
        patches_dirs: List of directories containing patches
        src_dir: Target directory to apply patches to
        config: Configuration object
        dryRun: If True, don't actually apply patches
        logDir: Directory for patch logs
        patchExe: Path to patch executable
        logFilename: Name for patch log file
    """
    log.info("Starting patch process")
    log.info("Source directory: %s", src_dir)
    log.info("Patch directories: %s", patches_dirs)
    
    # Ensure source directory exists
    if not exists(src_dir):
        raise Exception(f"Source directory does not exist: {src_dir}")
    
    # Create log directory if specified
    if logDir and not exists(logDir):
        os.makedirs(logDir)
        log.info("Created log directory: %s", logDir)
    
    # Setup patch log file
    patch_log = None
    if logDir and logFilename:
        patch_log_path = join(logDir, logFilename)
        patch_log = open(patch_log_path, 'w')
        log.info("Patch log: %s", patch_log_path)
    
    # Find and apply patches
    patches_applied = 0
    patches_skipped = 0
    
    for patches_dir in patches_dirs:
        if not exists(patches_dir):
            log.warning("Patch directory not found: %s", patches_dir)
            continue
            
        log.info("Processing patch directory: %s", patches_dir)
        
        # Find all patch files in this directory
        for root, dirs, files in os.walk(patches_dir):
            for file in files:
                if file.endswith('.patch') or file.endswith('.diff'):
                    patch_file = join(root, file)
                    relative_path = os.path.relpath(patch_file, patches_dir)
                    
                    log.info("Found patch: %s", relative_path)
                    
                    # Determine target path in source directory
                    # Remove the patches directory prefix and apply to src_dir
                    target_rel_path = os.path.dirname(relative_path)
                    target_dir = join(src_dir, target_rel_path) if target_rel_path != '.' else src_dir
                    
                    # Create target directory if it doesn't exist
                    if not exists(target_dir):
                        os.makedirs(target_dir, exist_ok=True)
                    
                    # Apply the patch
                    try:
                        if dryRun:
                            log.info("DRY RUN: Would apply %s to %s", patch_file, target_dir)
                            patches_skipped += 1
                        else:
                            # Use patch command to apply the patch
                            cmd = [patchExe, '-p0', '--input', patch_file]
                            log.info("Applying patch: %s", ' '.join(cmd))
                            
                            result = subprocess.run(
                                cmd,
                                cwd=target_dir,
                                capture_output=True,
                                text=True
                            )
                            
                            if result.returncode == 0:
                                log.info("Successfully applied: %s", relative_path)
                                patches_applied += 1
                                if patch_log:
                                    patch_log.write(f"# Successfully applied: {relative_path}\n")
                                    patch_log.write(f"# Target: {target_dir}\n")
                            else:
                                log.warning("Failed to apply %s: %s", relative_path, result.stderr)
                                if patch_log:
                                    patch_log.write(f"# Failed to apply: {relative_path}\n")
                                    patch_log.write(f"# Error: {result.stderr}\n")
                                    
                    except Exception as e:
                        log.error("Error applying patch %s: %s", relative_path, str(e))
                        if patch_log:
                            patch_log.write(f"# Error applying: {relative_path}\n")
                            patch_log.write(f"# Exception: {str(e)}\n")
    
    # Close patch log if it was opened
    if patch_log:
        patch_log.close()
    
    log.info("Patch process completed")
    log.info("Patches applied: %d", patches_applied)
    log.info("Patches skipped (dry run): %d", patches_skipped)
    
    return patches_applied


# Module-level log access is already available via the global log variable
