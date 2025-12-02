import os
import subprocess
import sys
from pathlib import Path
import pyperclip
from typing import Callable

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Header, Footer, RichLog, LoadingIndicator, ContentSwitcher
from textual.containers import Horizontal, Vertical
from textual.notifications import Notification
from textual.message import Message
from textual import work


class AdventDirectoryTree(DirectoryTree):

    def filter_paths(self, paths):
        for path in paths:
            if path.is_dir() and path.name.isdigit() and len(path.name) == 4:
                yield path
            elif path.is_file() and (path.name.startswith("day") and (path.suffix == ".py" or path.suffix == ".go")):
                yield path


class ScriptResultMessage(Message):
    """Message sent when a script finishes running."""
    def __init__(self, sender, result: tuple[str, str]) -> None:
        self.result = result
        super().__init__(sender)


class AdventOfCodeApp(App):
    """A Textual app to browse and run Advent of Code solutions."""

    CSS_PATH = "main.css"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if running in dev/debug mode via command line flag: --debug or -D
        # Note: --debug is removed from sys.argv before app creation, so this will be False
        # It will be set to True in main() after app creation if needed
        self._is_dev_mode = False
    

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "copy", "Copy Output"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with Horizontal():
            yield AdventDirectoryTree(".", id="tree")

            with Vertical():
                with ContentSwitcher(initial="log", id="content-switcher"):
                    yield LoadingIndicator(id="loading")
                    yield RichLog(id="log", wrap=True, highlight=True, auto_scroll=True)
                
                # Debug panel that's only visible in dev mode
                # Note: We'll check again in on_mount since _is_dev_mode might not be set yet
                debug_log = RichLog(id="debug-log", wrap=True, classes="debug-panel")
                debug_log.border_title = "Debug Log"
                yield debug_log

        yield Footer()

    def action_copy(self) -> None:
        """Copy the content of the RichLog to the clipboard."""
        log = self.query_one("#log")
        log_content = "\n".join(line.text for line in log.lines)

        if log_content:
            pyperclip.copy(log_content)
            self.notify("Output copied to clipboard!", title="Copied", severity="information")
        else:
            self.notify("No output to copy.", title="Copy Failed", severity="warning")

    def action_copy_debug(self) -> None:
        """Copy the content of the Debug Log to the clipboard (only available in dev mode)."""
        if not getattr(self, '_is_dev_mode', False):
            self.notify("Debug mode not enabled. Run with --debug flag.", title="Debug Mode Required", severity="warning")
            return
        try:
            debug_log = self.query_one("#debug-log")
            debug_content = "\n".join(line.text for line in debug_log.lines)

            if debug_content:
                pyperclip.copy(debug_content)
                self.notify("Debug log copied to clipboard!", title="Copied", severity="information")
            else:
                self.notify("No debug log to copy.", title="Copy Failed", severity="warning")
            
            # Refresh footer to show the binding (in case it wasn't visible before)
            try:
                footer = self.query_one("Footer")
                footer.refresh()
            except:
                pass
        except:
            self.notify("Debug log not available.", title="Copy Failed", severity="warning")

    def _debug_log(self, message: str) -> None:
        """Log to both the main log and the debug log (if in dev mode)."""
        if self._is_dev_mode:
            try:
                debug_log = self.query_one("#debug-log", RichLog)
                debug_log.write(f"[DEBUG] {message}")
            except:
                pass  # Debug log might not exist if not in dev mode
        self.log(message)
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Ensure _is_dev_mode is set (it should be set in main before app.run())
        # But check it here to be safe
        if not hasattr(self, '_is_dev_mode'):
            self._is_dev_mode = False
        
        self._debug_log("=== TROUBLESHOOTING: on_mount called ===")
        self._debug_log(f"DEBUG: _is_dev_mode in on_mount = {self._is_dev_mode}")
        
        self._debug_log(f"DEBUG: _is_dev_mode = {self._is_dev_mode}")
        self._debug_log(f"DEBUG: sys.argv = {sys.argv}")
        
        # Show/hide debug log based on dev mode
        try:
            debug_log = self.query_one("#debug-log", RichLog)
            self._debug_log(f"DEBUG: Found debug-log widget")
            if not self._is_dev_mode:
                debug_log.display = False
                self._debug_log(f"DEBUG: Hiding debug log")
            else:
                debug_log.display = True
                self._debug_log(f"DEBUG: Showing debug log")
        except Exception as e:
            self._debug_log(f"DEBUG: Error accessing debug-log: {e}")
        
        self.query_one("#tree").focus()
        switcher = self.query_one("#content-switcher")
        self._debug_log(f"ContentSwitcher initial state: {switcher.current}")
        self._debug_log(f"Available ContentSwitcher IDs: {[child.id for child in switcher.children]}")
        
        # Add debug log copy binding if in dev mode
        # The binding should already be in BINDINGS (added before app creation)
        # but we also call bind() to ensure it's registered
        if self._is_dev_mode:
            try:
                # Register the binding
                result = self.bind("d", "copy_debug")
                self._debug_log(f"Debug log binding registered via bind(), result: {result}")
            except Exception as e:
                self._debug_log(f"bind() failed: {e}")
                import traceback
                self._debug_log(traceback.format_exc())
        else:
            self._debug_log("Debug log binding NOT added (not in dev mode)")
        
        self._debug_log("=== TROUBLESHOOTING: App mounted ===")
        self._debug_log(f"ContentSwitcher initial state: {switcher.current}")
        self._debug_log(f"Available ContentSwitcher IDs: {[child.id for child in switcher.children]}")
        if self._is_dev_mode:
            self._debug_log("Dev mode: ENABLED")
        else:
            self._debug_log("Dev mode: DISABLED")

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when a file is selected in the directory tree."""
        self._debug_log("=== TROUBLESHOOTING: on_directory_tree_file_selected CALLED ===")
        self._debug_log(f"File selected: {event.path}")
        event.stop()

        self._debug_log("=== TROUBLESHOOTING: File selected event received ===")
        self._debug_log(f"File selected: {event.path}")
        
        try:
            log = self.query_one("#log")
            self._debug_log("✓ Found #log widget")
            log.clear()
            self._debug_log("✓ Cleared log widget")
        except Exception as e:
            self._debug_log(f"✗ Error accessing #log: {e}")
            import traceback
            self._debug_log(traceback.format_exc())
            self._debug_log(f"✗ Error accessing #log: {e}")
            self._debug_log(traceback.format_exc())
            return

        try:
            switcher = self.query_one("#content-switcher")
            self._debug_log(f"✓ Found #content-switcher widget")
            self._debug_log(f"  Current state before switch: {switcher.current}")
            self._debug_log(f"  Available children: {[child.id for child in switcher.children]}")
            self._debug_log(f"✓ Found #content-switcher widget")
            self._debug_log(f"  Current state before switch: {switcher.current}")
            self._debug_log(f"  Available children: {[child.id for child in switcher.children]}")
            
            switcher.current = "loading"
            self._debug_log(f"✓ Switched to 'loading'")
            self._debug_log(f"  Current state after switch: {switcher.current}")
            self._debug_log(f"✓ Switched to 'loading'")
            self._debug_log(f"  Current state after switch: {switcher.current}")
        except Exception as e:
            self._debug_log(f"✗ Error switching to loading: {e}")
            import traceback
            self._debug_log(traceback.format_exc())
            self._debug_log(f"✗ Error switching to loading: {e}")
            self._debug_log(traceback.format_exc())
            return

        file_path = event.path

        try:
            self._debug_log("=== TROUBLESHOOTING: Starting worker ===")
            self._debug_log(f"  File path: {file_path}")
            self._debug_log(f"  Worker callback: {self.on_script_done}")
            self._debug_log(f"  Callback type: {type(self.on_script_done)}")
            
            # Store file_path for debugging
            self._current_file_path = file_path
            
            # Try using @work decorator approach as alternative
            # But first, let's try the direct callback with better error handling
            def worker_func():
                try:
                    # Note: Can't use _debug_log in worker thread (UI updates must be on main thread)
                    # They were only for troubleshooting anyway
                    result = self.run_script(file_path)
                    
                    # Use call_from_thread to safely update UI from worker thread
                    try:
                        # Try using call_from_thread if it exists
                        if hasattr(self, 'call_from_thread'):
                            self.call_from_thread(self.on_script_done, result)
                        else:
                            # Fallback: post message
                            self.post_message(ScriptResultMessage(self, result))
                    except Exception as msg_error:
                        # Error updating UI - will be handled by callback
                        pass
                    
                    return result
                except Exception as e:
                    import traceback
                    error_trace = traceback.format_exc()
                    # Post error message
                    error_result = (f"Error in worker: {e}", error_trace)
                    try:
                        self.post_message(ScriptResultMessage(self, error_result))
                    except:
                        pass
                    return error_result
            
            # Store callback reference for debugging
            callback_ref = self.on_script_done
            self._debug_log(f"  About to call run_worker with callback: {callback_ref}")
            self._debug_log(f"  Callback is callable: {hasattr(callback_ref, '__call__')}")
            
            # Set a timeout to switch back if worker doesn't complete
            def timeout_fallback():
                # Check if we're still on loading
                try:
                    switcher = self.query_one("#content-switcher")
                    if switcher.current == "loading":
                        self._debug_log("⚠ Timeout: Still on loading after 10 seconds, switching back")
                        switcher.current = "log"
                        log = self.query_one("#log")
                        log.write("⚠ Script execution timed out or callback failed to fire.\n")
                        log.write("Check terminal output (where you ran 'textual run') for worker thread messages.\n")
                except Exception as e:
                    self._debug_log(f"✗ Error in timeout_fallback: {e}")
            
            # Schedule timeout check
            self.set_timer(10.0, timeout_fallback)
            
            try:
                worker_handle = self.run_worker(
                    worker_func, 
                    callback_ref,
                    thread=True
                )
                self._debug_log(f"  run_worker() call completed without exception")
                self._debug_log(f"  Worker handle: {worker_handle}")
            except Exception as e:
                self._debug_log(f"  ✗ Exception calling run_worker: {e}")
                import traceback
                self._debug_log(traceback.format_exc())
                raise
            self._debug_log("✓ Worker started successfully")
            self._debug_log("✓ Worker started successfully")
            self._debug_log("  ⚠ IMPORTANT: Check terminal output for worker thread messages!")
        except Exception as e:
            self._debug_log(f"✗ Error starting worker: {e}")
            import traceback
            self._debug_log(traceback.format_exc())
            self._debug_log(f"✗ Error starting worker: {e}")
            self._debug_log(traceback.format_exc())

    def run_script(self, file_path: Path) -> tuple[str, str]:
        """Run a script and return its output."""
        # Note: Can't use _debug_log in worker thread (UI updates must be on main thread)

        try:
            if file_path.suffix == ".py":
                result = self._run_python(file_path)
                return result
            elif file_path.suffix == ".go":
                result = self._run_go(file_path)
                return result
            else:
                error_msg = f"Unsupported file type: {file_path.suffix}"
                pass  # Error message returned in result
                return error_msg, ""
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            return f"Error running {file_path}: {e}", ""

    def on_script_result_message(self, message: ScriptResultMessage) -> None:
        """Handle script result message posted from worker thread."""
        self._debug_log("=== TROUBLESHOOTING: on_script_result_message called ===")
        self.on_script_done(message.result)
    
    def on_script_result_message(self, message: ScriptResultMessage) -> None:
        """Handle script result message posted from worker thread."""
        self._debug_log("=== TROUBLESHOOTING: on_script_result_message called ===")
        self.on_script_done(message.result)
    
    def on_script_done(self, result: tuple[str, str]) -> None:
        """Called when the script finishes running."""
        self._debug_log("=== TROUBLESHOOTING: on_script_done CALLED ===")
        self._debug_log(f"  Result type: {type(result)}, length: {len(result) if result else 'None'}")
        self._debug_log("=== TROUBLESHOOTING: Worker finished, running on_script_done ===")
        if result:
            self._debug_log(f"  Result received: tuple with {len(result)} elements")
        else:
            self._debug_log("  WARNING: Result is None or empty!")
        
        try:
            log = self.query_one("#log")
            self._debug_log("✓ Found #log widget in on_script_done")
            self._debug_log("✓ Found #log widget in on_script_done")
        except Exception as e:
            self._debug_log(f"✗ Error accessing #log in on_script_done: {e}")
            import traceback
            self._debug_log(traceback.format_exc())
            self._debug_log(f"✗ Error accessing #log in on_script_done: {e}")
            self._debug_log(traceback.format_exc())
            return

        stdout, stderr = result
        self._debug_log(f"  Result: stdout length={len(stdout)}, stderr length={len(stderr)}")
        self._debug_log(f"  Result: stdout length={len(stdout)}, stderr length={len(stderr)}")

        try:
            if stdout:
                log.write(stdout)
                self._debug_log("✓ Wrote stdout to log")
                self._debug_log("✓ Wrote stdout to log")
            else:
                self._debug_log("  No stdout to write")
                self._debug_log("  No stdout to write")

            if stderr:
                log.write(stderr)
                self._debug_log("✓ Wrote stderr to log")
                self._debug_log("✓ Wrote stderr to log")
            else:
                self._debug_log("  No stderr to write")
                self._debug_log("  No stderr to write")
        except Exception as e:
            self._debug_log(f"✗ Error writing to log: {e}")
            import traceback
            self._debug_log(traceback.format_exc())
            self._debug_log(f"✗ Error writing to log: {e}")
            self._debug_log(traceback.format_exc())

        try:
            switcher = self.query_one("#content-switcher")
            self._debug_log(f"✓ Found #content-switcher in on_script_done")
            self._debug_log(f"  Current state before switch: {switcher.current}")
            self._debug_log(f"✓ Found #content-switcher in on_script_done")
            self._debug_log(f"  Current state before switch: {switcher.current}")
            switcher.current = "log"
            self._debug_log(f"✓ Switched to 'log'")
            self._debug_log(f"  Current state after switch: {switcher.current}")
            self._debug_log(f"✓ Switched to 'log'")
            self._debug_log(f"  Current state after switch: {switcher.current}")
        except Exception as e:
            self._debug_log(f"✗ Error switching to log view: {e}")
            import traceback
            self._debug_log(traceback.format_exc())
            self._debug_log(f"✗ Error switching to log view: {e}")
            self._debug_log(traceback.format_exc())

    def _run_python(self, file_path: Path) -> tuple[str, str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()

        # Note: Can't use _debug_log in worker thread (UI updates must be on main thread)
        process = subprocess.Popen(
            [sys.executable, str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )

        # Note: Can't use _debug_log in worker thread (UI updates must be on main thread)
        try:
            stdout, stderr = process.communicate(timeout=30)  # 30 second timeout
            # Note: Can't use _debug_log in worker thread (UI updates must be on main thread)
            return stdout, stderr
        except subprocess.TimeoutExpired:
            # Note: Can't use _debug_log in worker thread (UI updates must be on main thread)
            process.kill()
            stdout, stderr = process.communicate()
            return f"Error: Script timed out after 30 seconds", stderr or "No stderr output"

    def _run_go(self, file_path: Path) -> tuple[str, str]:
        # We need to also include the utils.go file if it exists
        go_files = [str(file_path)]

        utils_go = file_path.parent / "utils.go"
        if utils_go.exists():
            go_files.append(str(utils_go))

        # Special case for 2020 where there is a main.go and utils are in parent dir
        if "2020" in str(file_path):
            # The go files in 2020 dir don't have a main function
            # we need to use the main.go in that directory to run the correct day
            day = file_path.stem
            main_go = file_path.parent / "main.go"

            if main_go.exists():
                command = ["go", "run", str(main_go), day]
            else:
                return "main.go not found for 2020 solutions", ""
        else:
            command = ["go", "run"] + go_files

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=file_path.parent,
        )

        stdout, stderr = process.communicate()
        return stdout, stderr


if __name__ == "__main__":
    # Check for debug flag BEFORE creating app
    is_debug = "--debug" in sys.argv or "-D" in sys.argv
    
    # Add debug binding to BINDINGS if in debug mode (before app is created)
    if is_debug:
        # Convert to list, add binding
        bindings_list = list(AdventOfCodeApp.BINDINGS)
        if not any(b[0] == "d" for b in bindings_list):
            bindings_list.append(("d", "copy_debug", "Copy Debug Log"))
            AdventOfCodeApp.BINDINGS = bindings_list
    
    # Remove --debug/-D from sys.argv if present so Textual doesn't see it
    if "--debug" in sys.argv:
        sys.argv.remove("--debug")
    if "-D" in sys.argv:
        sys.argv.remove("-D")
    
    app = AdventOfCodeApp()
    # Pass debug mode to app if needed
    if is_debug:
        app._is_dev_mode = True
    app.run()
