"""Configuration for pytest."""

import sys
from pathlib import Path

# Add the package to the path (at the beginning to override other sage packages)
package_root = Path(__file__).parent.parent
sys.path.insert(0, str(package_root))

# Remove any existing sage.libs from sys.modules to avoid conflicts
modules_to_remove = [key for key in sys.modules if key.startswith('sage.libs') and 'amms' not in key]
for mod in modules_to_remove:
    sys.modules.pop(mod, None)
