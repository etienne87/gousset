"""
Basic usage example for gousset timing profiler.

Run this to see gousset in action!
"""

import gousset
import sys
import os

# Add the tests directory to the path so we can import test modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tests"))

import module_a
import module_b


def main():
    """Demonstrate gousset's capabilities"""
    print("🕰️  Gousset - Your Pocket Profiler Demo")
    print("=" * 50)

    # Instrument both modules
    print("\n📦 Instrumenting modules...")
    gousset.instrument(module_a)
    gousset.instrument(module_b)

    # Use module_a functions
    print("\n⚡ Running module_a functions...")
    print("  - slow_function() calls fast_function() internally")
    print("  - Notice how both get timed!")

    for i in range(8):
        result = module_a.slow_function()  # Nested calls!

    for i in range(3):
        result = module_a.fast_function()  # Direct calls

    for i in range(5):
        result = module_a.medium_function()

    # Use module_b functions
    print("\n🔢 Running module_b functions...")
    print("  - factorial() is recursive - each call creates more calls!")
    print("  - fibo() processes large lists")

    data = list(range(1, 2000))
    for i in range(4):
        result = module_b.fibo(data)

    for i in range(2):
        result = module_b.factorial(50)  # Creates 50 calls each time!

    for i in range(6):
        result = module_b.sum_squares(5000)

    print("\n✅ Done! Check the timing statistics below:")
    print("   (Statistics automatically print when the program exits)")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
