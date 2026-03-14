#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern remotely run Komodo builds (and other tasks) using Python 3.

This script presumes that you have password-less SSH authentication setup 
to each machine (i.e. the current box has to have an SSH agent running).

The exit value is the number of task failures.

Examples:
  rrun_modern.py ping              # ping all machines
  rrun_modern.py -m linux koide    # build Komodo IDE on Linux boxes
  rrun_modern.py -m gila kodev     # build Komodo dev tree on the machine 'gila'

komodo build tasks:
  ko                    Full Komodo IDE build
  ok                    Full Komodo Edit build

  kodev                 sync and build in komodo build tree
  kodev-configure       sync and configure (default config) in komodo
  kodev-reconfigure     sync and re-configure in the komodo build tree
  kodev-test            sync and run modern test suite in komodo build tree
  kodev-clean           sync and run modern clean in komodo build tree

  okdev, okdev-configure, okdev-reconfigure, okdev-test, okdev-clean
                        ditto for openkomodo build tree (Komodo Edit trunk)

secondary tasks:
  mozpy                 build the siloed Python into mozilla/prebuilt/pythonX.Y
  xdebug                update xdebug builds with latest from Xdebug CVS
  koup-nightly          update to the latest Komodo IDE and Edit nightlies
  koup-releasetest      update to the latest Komodo IDE and Edit release
                        and on release channel
  admin                 Run some administrative tasks on the build machines.
                        E.g. monitor disk usages (komodo builds suck *huge*
                        amounts of space).
  svncleanup

diagnostic tasks:
  hupbb                 hup the Komodo buildbot slave on this machine
  ping                  just check to see if machines are awake
  plat                  dump platform info (as per platform.py)
  slow                  echo begin, sleep, echo done
  error                 check error handling by running a command that fails
"""

__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))

import os
import sys
import re
import glob
import traceback
import logging
import argparse
import copy
import threading
import queue
import socket
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from build_config import BuildConfig


class Error(Exception):
    pass


log = logging.getLogger("rrun_modern")


#---- machines
# Modern machine configuration - update with current build machines
g_machines = [
    {
        "hostname": "localhost",
        "platform": "modern-linux-x86_64",
        "tmp-dir": "~/tmp",
        "var-dir": "~/var",
        "build-dir": str(PROJECT_ROOT),
        "tags": ["official", "modern", "localhost"]
    },
    # Add other modern build machines here as needed
    # {
    #     "hostname": "modern-build-server",
    #     "login": "builduser@modern-build-server",
    #     "platform": "modern-linux-x86_64",
    #     "tmp-dir": "/home/builduser/tmp",
    #     "var-dir": "/home/builduser/var",
    #     "build-dir": "/home/builduser/komodo",
    #     "tags": ["official", "modern", "remote"]
    # }
]


def _add_this_machine():
    """Add the current machine to the list if not already present"""
    hostname = socket.gethostname().split('.')[0]
    for m in g_machines:
        if m["hostname"] == hostname:
            break
    else:
        # Not already in the list. Add it.
        g_machines.append(
            {
                "hostname": hostname,
                "platform": f"modern-{sys.platform}-{sys.maxsize.bit_length()}",
                "tmp-dir": "~/tmp",
                "var-dir": "~/var",
                "build-dir": str(PROJECT_ROOT),
                "tags": ["localhost", "modern"]
            }
        )


def _get_machines_for_tags(tags):
    """Get list of machines that match the given tags"""
    if not tags:
        return g_machines
    
    machines = []
    for machine in g_machines:
        if any(tag in machine["tags"] for tag in tags):
            machines.append(machine)
    
    return machines


def _run_command_on_machine(machine, command, timeout=None):
    """Run a command on a specific machine"""
    log.info(f"Running on {machine['hostname']}: {command}")
    
    if machine["hostname"] == "localhost" or machine["hostname"] == socket.gethostname().split('.')[0]:
        # Local execution
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=machine["build-dir"],
                capture_output=True, 
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    else:
        # Remote execution via SSH
        ssh_command = f"ssh {machine.get('login', machine['hostname'])} \"cd {machine['build-dir']} && {command}\""
        try:
            result = subprocess.run(
                ssh_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "SSH command timed out"
        except Exception as e:
            return False, "", str(e)


def _run_task_on_machine(machine, task_name, task_args):
    """Run a specific task on a machine"""
    log.info(f"Running task '{task_name}' on {machine['hostname']}")
    
    # Modern task mapping
    task_commands = {
        # Build tasks
        'ko': 'python3 mozilla/build.py all',
        'ok': 'python3 mozilla/build.py all --product=edit',
        'kodev': 'python3 mozilla/build.py configure && python3 mozilla/build.py all',
        'kodev-configure': 'python3 mozilla/build.py configure',
        'kodev-reconfigure': 'python3 mozilla/build.py configure --reconfigure',
        'kodev-test': 'python3 mozilla/build.py test',
        'kodev-clean': 'python3 mozilla/build.py clean',
        
        # Modern equivalents for legacy tasks
        'okdev': 'python3 mozilla/build.py configure --product=edit && python3 mozilla/build.py all',
        'okdev-configure': 'python3 mozilla/build.py configure --product=edit',
        'okdev-reconfigure': 'python3 mozilla/build.py configure --product=edit --reconfigure',
        'okdev-test': 'python3 mozilla/build.py test --product=edit',
        'okdev-clean': 'python3 mozilla/build.py clean --product=edit',
        
        # Diagnostic tasks
        'ping': 'echo "pong from $(hostname)"',
        'plat': 'python3 -c "import platform; print(platform.platform())"',
        'slow': 'echo begin && sleep 5 && echo done',
        'error': 'exit 1',
        
        # Modern build tasks
        'mozpy': 'python3 mozilla/build.py mozilla-python',
        'xdebug': 'echo "xdebug task - update with modern implementation"',
        'koup-nightly': 'python3 util/mknightly.py',
        'koup-releasetest': 'python3 util/mknightly.py --release',
        'admin': 'df -h && free -m',
        'svncleanup': 'echo "svn cleanup - update with modern VCS cleanup"',
        'hupbb': 'echo "buildbot hup - update with modern CI integration"'
    }
    
    if task_name not in task_commands:
        log.error(f"Unknown task: {task_name}")
        return False, f"Unknown task: {task_name}", ""
    
    # Get the base command
    command = task_commands[task_name]
    
    # Add any task-specific arguments
    if task_args:
        command += " " + " ".join(task_args)
    
    # Run the command
    success, stdout, stderr = _run_command_on_machine(machine, command)
    
    if success:
        log.info(f"Task '{task_name}' completed successfully on {machine['hostname']}")
    else:
        log.error(f"Task '{task_name}' failed on {machine['hostname']}: {stderr}")
    
    return success, stdout, stderr


def run_tasks(machines, tasks):
    """Run tasks on specified machines"""
    failures = 0
    
    for machine in machines:
        log.info(f"Processing machine: {machine['hostname']}")
        
        for task in tasks:
            task_name, *task_args = task.split()
            success, stdout, stderr = _run_task_on_machine(machine, task_name, task_args)
            
            if not success:
                failures += 1
                log.error(f"Task failed: {task_name} on {machine['hostname']}")
                if stderr:
                    log.error(f"Error: {stderr}")
            else:
                if stdout:
                    log.info(f"Output: {stdout.strip()}")
    
    return failures


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Modern Komodo Remote Build Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true',
        help='verbose output'
    )
    parser.add_argument(
        '-m', '--machines',
        help='comma-separated list of machine tags or hostnames'
    )
    parser.add_argument(
        '-l', '--list-machines',
        action='store_true',
        help='list available machines and exit'
    )
    parser.add_argument(
        'tasks',
        nargs='*',
        help='tasks to run'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add this machine to the list
    _add_this_machine()
    
    if args.list_machines:
        print("Available machines:")
        for machine in g_machines:
            tags_str = ", ".join(machine["tags"])
            print(f"  {machine['hostname']:20} ({machine['platform']}) - {tags_str}")
        return 0
    
    # Check if tasks are provided when not listing machines
    if not args.tasks and not args.list_machines:
        parser.print_help()
        return 1
    
    # Determine which machines to use
    if args.machines:
        machine_tags = [tag.strip() for tag in args.machines.split(',')]
        machines = _get_machines_for_tags(machine_tags)
    else:
        machines = g_machines
    
    if not machines:
        log.error("No machines selected")
        return 1
    
    log.info(f"Running tasks on {len(machines)} machines: {[m['hostname'] for m in machines]}")
    
    # Run the tasks
    failures = run_tasks(machines, args.tasks)
    
    if failures > 0:
        log.error(f"Completed with {failures} failures")
        return failures
    else:
        log.info("All tasks completed successfully")
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        log.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)