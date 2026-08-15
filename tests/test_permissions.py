import sys
import os
import unittest

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tars.tools.permissions import PermissionCategory, PermissionManager, PermissionDeniedError

class TestPermissions(unittest.TestCase):
    def test_permission_ordering(self):
        self.assertTrue(PermissionCategory.READ_ONLY < PermissionCategory.SAFE_ACTION)
        self.assertTrue(PermissionCategory.SAFE_ACTION < PermissionCategory.SENSITIVE)
        self.assertTrue(PermissionCategory.SENSITIVE < PermissionCategory.DANGEROUS)
        
    def test_permission_manager_allow(self):
        manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
        
        # Read-only is allowed
        self.assertTrue(manager.is_allowed(PermissionCategory.READ_ONLY))
        # Safe action is allowed
        self.assertTrue(manager.is_allowed(PermissionCategory.SAFE_ACTION))
        
    def test_permission_manager_deny(self):
        manager = PermissionManager(max_allowed=PermissionCategory.SAFE_ACTION)
        
        # Sensitive is denied
        self.assertFalse(manager.is_allowed(PermissionCategory.SENSITIVE))
        
        with self.assertRaises(PermissionDeniedError):
            manager.enforce(PermissionCategory.SENSITIVE, "some_sensitive_tool")

if __name__ == '__main__':
    unittest.main()
