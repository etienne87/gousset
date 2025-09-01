"""
Core functionality for gousset timing profiler.
"""

import time
import atexit
import statistics
from functools import wraps
from collections import defaultdict
from typing import Any, Callable, Dict, List
import inspect

# Module-level variables
_timings: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
_instrumented_modules = set()
_original_functions = {}  # Store original functions for potential restoration
_registered_exit = False


def _register_exit_handler() -> None:
    """Register exit handler only once"""
    global _registered_exit
    if not _registered_exit:
        atexit.register(_print_all_statistics)
        _registered_exit = True


def _print_all_statistics() -> None:
    """Print timing statistics for all instrumented modules"""
    if not _timings:
        return

    for module_name, functions in _timings.items():
        if not functions:
            continue

        print(f"\n=== Gousset Timing Statistics for Module: {module_name} ===")
        print("-" * 70)

        for func_name, times in functions.items():
            if not times:
                continue

            total_time = sum(times)
            avg_time = statistics.mean(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0.0
            min_time = min(times)
            max_time = max(times)
            count = len(times)

            print(f"Function: {func_name}")
            print(f"  Calls:   {count:>8}")
            print(f"  Sum:     {total_time:>8.6f}s")
            print(f"  Average: {avg_time:>8.6f}s")
            print(f"  Std Dev: {std_time:>8.6f}s")
            print(f"  Min:     {min_time:>8.6f}s")
            print(f"  Max:     {max_time:>8.6f}s")
            print()


def _create_timed_function(
    original_func: Callable, func_name: str, module_name: str
) -> Callable:
    """Create a timed version of a function"""

    @wraps(original_func)
    def timed_wrapper(*args: Any, **kwargs: Any) -> Any:
        ts = time.time()
        result = original_func(*args, **kwargs)
        te = time.time()
        dt = te - ts

        # Store timing
        _timings[module_name][func_name].append(dt)
        return result

    return timed_wrapper


def instrument(module, only=None, exclude=None, **kwargs):
    """
    Instrument functions in a module to be timed automatically

    Args:
        module: The Python module to instrument
        only: Optional string or list of function names to instrument exclusively
        exclude: Optional string or list of function names to exclude
        **kwargs: Additional arguments (e.g., custom measure_func)

    Examples:
        # Instrument entire module
        gousset.instrument(my_module)

        # Instrument single function
        gousset.instrument(my_module, only='slow_function')

        # Instrument multiple specific functions
        gousset.instrument(my_module, only=['func1', 'func2'])

        # Instrument all except some functions
        gousset.instrument(my_module, exclude=['_private', 'test_func'])
    """
    _register_exit_handler()

    if not inspect.ismodule(module):
        raise ValueError(
            f"First argument must be a module, got {type(module).__name__}"
        )

    # Normalize only/exclude to sets
    if only is not None:
        if isinstance(only, str):
            only = {only}
        else:
            only = set(only)

    if exclude is not None:
        if isinstance(exclude, str):
            exclude = {exclude}
        else:
            exclude = set(exclude)

    _instrument_module(module, only=only, exclude=exclude, **kwargs)


def _instrument_single_function(func, **kwargs):
    """
    Instrument a single function
    Returns the timed wrapper function that should replace the original
    """
    func_name = getattr(func, "__name__", "unknown_function")
    module_name = getattr(func, "__module__", "unknown_module")

    key = f"{module_name}.{func_name}"
    if key in _original_functions:
        # Already instrumented, return existing wrapper
        # Find and return the existing timed function
        pass

    # Store original
    _original_functions[key] = func

    # Create timed version
    timed_func = _create_timed_function(func, func_name, module_name, **kwargs)

    # Try to replace in module automatically (best effort)
    import sys

    if module_name in sys.modules:
        module = sys.modules[module_name]
        if hasattr(module, func_name):
            setattr(module, func_name, timed_func)

    # Return the timed function for manual replacement
    return timed_func


def _instrument_module(module, only=None, exclude=None, **kwargs):
    """Instrument functions in a module with optional filtering"""
    module_name = getattr(module, "__name__", "unknown_module")

    if module_name in _instrumented_modules:
        return  # Already instrumented

    _instrumented_modules.add(module_name)

    # Get all functions in the module and instrument them
    for name in dir(module):
        # Skip private functions by default
        if name.startswith("_"):
            continue

        # Apply only filter
        if only is not None and name not in only:
            continue

        # Apply exclude filter
        if exclude is not None and name in exclude:
            continue

        obj = getattr(module, name)
        # Check for any callable that's not a class and not private
        if callable(obj) and not inspect.isclass(obj) and not inspect.ismodule(obj):

            # Store original for potential restoration
            _original_functions[f"{module_name}.{name}"] = obj

            # Create timed version
            timed_func = _create_timed_function(obj, name, module_name, **kwargs)

            # Replace in module
            setattr(module, name, timed_func)


def restore_all():
    """
    Restore all instrumented functions to their original state
    This completely undoes all instrumentation
    """
    global _timings, _instrumented_modules, _original_functions, _registered_exit

    # Restore all original functions
    for key, original_func in _original_functions.items():
        try:
            module_name, func_name = key.rsplit(".", 1)
            print(f"DEBUG: Restoring {module_name}.{func_name}")

            import sys

            if module_name in sys.modules:
                module = sys.modules[module_name]
                if hasattr(module, func_name):
                    setattr(module, func_name, original_func)
                    print(f"DEBUG: Successfully restored {func_name}")
                else:
                    print(f"DEBUG: Function {func_name} not found in module")
            else:
                print(f"DEBUG: Module {module_name} not in sys.modules")
        except Exception as e:
            print(f"DEBUG: Error restoring {key}: {e}")

    # Clear all state
    _timings = defaultdict(lambda: defaultdict(list))
    _instrumented_modules = set()
    _original_functions = {}
    _registered_exit = False
    print("DEBUG: All state cleared")
