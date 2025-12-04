"""
Reusable helper functions for notebook automation.
"""

import sys
import os
import subprocess
import shutil
import shlex
import time
import webbrowser
from typing import List, Optional
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def start_in_new_terminal(cmd: List[str], title: Optional[str] = None, log_file: Optional[str] = None, cwd: Optional[str] = None):
    """Start the given command in a new terminal window if possible.
    
    Args:
        cmd: Command to run as a list of strings.
        title: Title for the terminal window.
        log_file: Optional file to redirect stdout/stderr.
        cwd: Working directory to start the terminal in.
    
    If `cwd` is provided, attempt to make the new terminal start there.
    """
    if title is None:
        title = 'Process'
    
    # Windows: create a new console window
    if os.name == 'nt':
        from subprocess import Popen, CREATE_NEW_CONSOLE
        try:
            Popen(cmd, creationflags=CREATE_NEW_CONSOLE, cwd=cwd)
            print(f'Started in new Windows console: {cmd} (cwd={cwd})')
            return
        except Exception as e:
            print('Windows new console failed:', e)
    
    # Unix-like: try common terminal emulators
    terminals = [('gnome-terminal', ['--']), ('konsole', ['-e']), ('xterm', ['-e']), ('alacritty', ['-e'])]
    for term, arg_prefix in terminals:
        if shutil.which(term):
            try:
                # Handle working directory where supported
                if cwd:
                    if term == 'gnome-terminal':
                        full_cmd = [term, '--working-directory', cwd, '--'] + cmd
                    elif term == 'konsole':
                        full_cmd = [term, '--workdir', cwd, '-e'] + cmd
                    elif term == 'alacritty':
                        full_cmd = [term, '--working-directory', cwd, '-e'] + cmd
                    else:
                        # xterm: ask the shell to cd then exec the command
                        shell_cmd = ['bash', '-lc', f'cd {shlex.quote(cwd)} && exec {shlex.join(cmd)}']
                        full_cmd = [term, '-e'] + shell_cmd
                else:
                    full_cmd = [term] + arg_prefix + cmd

                subprocess.Popen(full_cmd)
                print(f'Started in new terminal using: {term} (cwd={cwd})')
                return
            except Exception as e:
                print(f'Failed to start with {term}:', e)
    
    # macOS: try Terminal.app via AppleScript
    if sys.platform == 'darwin':
        try:
            if cwd:
                apple_cmd = f'tell application "Terminal" to do script "cd {shlex.quote(cwd)} && {shlex.join(cmd)}"'
            else:
                apple_cmd = f'tell application "Terminal" to do script "{shlex.join(cmd)}"'
            subprocess.Popen(['osascript', '-e', apple_cmd])
            print('Started in new Terminal.app window (macOS).')
            return
        except Exception as e:
            print('Failed to start macOS Terminal:', e)
    
    # Fallback: run in background, optionally redirecting output to a log file
    try:
        kwargs = {}
        if log_file:
            f = open(log_file, 'a')
            kwargs['stdout'] = f
            kwargs['stderr'] = f
        preexec = os.setsid if hasattr(os, 'setsid') else None
        p = subprocess.Popen(cmd, preexec_fn=preexec, cwd=cwd, **kwargs)
        print(f'Started in background (PID {p.pid}), logs -> {log_file or "console"} (cwd={cwd})')
    except Exception as e:
        print('Failed to start background process:', e)


def open_url_when_ready(url: str, timeout: float = 30.0, poll_interval: float = 0.5, new: int = 2) -> bool:
    """Poll `url` until it responds (status 200) or timeout is reached.
    
    Args:
        url: URL to poll and open.
        timeout: Maximum time to wait in seconds.
        poll_interval: Time to wait between retries in seconds.
        new: Browser window behavior (0=current, 1=new, 2=new tab).
    
    If available, opens it in the default browser. Returns True if opened, False otherwise.
    """
    start = time.time()
    while True:
        try:
            with urlopen(url, timeout=1) as resp:
                status = getattr(resp, 'status', None) or getattr(resp, 'code', None)
                if status == 200:
                    print(f'URL {url} is available (status=200)')
                    break
        except Exception:
            # ignore and retry until timeout
            pass
        if time.time() - start > timeout:
            print(f'URL {url} not available after {timeout}s')
            return False
        time.sleep(poll_interval)
    webbrowser.open(url, new=new)
    return True
