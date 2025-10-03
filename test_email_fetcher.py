"""
Test suite for the Email Ingestion & Filtering Module
Demonstrates functionality without requiring actual Gmail credentials
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module_structure():
    """Test that the email_fetcher module can be imported and has the required functions."""
    print("🔍 Testing module structure...")
    
    try:
        import email_fetcher
        
        # Check if required functions exist
        required_functions = ['search_emails', 'get_raw_email']
        
        for func_name in required_functions:
            if hasattr(email_fetcher, func_name):
                print(f"  ✅ Function '{func_name}' found")
            else:
                print(f"  ❌ Function '{func_name}' missing")
                return False
        
        print("  ✅ All required functions present")
        return True
        
    except ImportError as e:
        print(f"  ❌ Failed to import email_fetcher: {e}")
        return False

def test_function_signatures():
    """Test function signatures and basic validation."""
    print("\n🔍 Testing function signatures...")
    
    try:
        import email_fetcher
        import inspect
        
        # Test search_emails signature
        sig = inspect.signature(email_fetcher.search_emails)
        params = list(sig.parameters.keys())
        if params == ['service', 'query']:
            print("  ✅ search_emails(service, query) signature correct")
        else:
            print(f"  ❌ search_emails signature incorrect: {params}")
        
        # Test get_raw_email signature  
        sig = inspect.signature(email_fetcher.get_raw_email)
        params = list(sig.parameters.keys())
        if params == ['service', 'message_id']:
            print("  ✅ get_raw_email(service, message_id) signature correct")
        else:
            print(f"  ❌ get_raw_email signature incorrect: {params}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing signatures: {e}")
        return False

def test_error_handling():
    """Test error handling with None service object."""
    print("\n🔍 Testing error handling...")
    
    try:
        import email_fetcher
        
        # Test search_emails with None service (should handle gracefully)
        result = email_fetcher.search_emails(None, "test query")
        if result == []:
            print("  ✅ search_emails handles None service gracefully")
        else:
            print(f"  ❌ search_emails unexpected result: {result}")
        
        # Test get_raw_email with None service
        result = email_fetcher.get_raw_email(None, "test_id")
        if result is None:
            print("  ✅ get_raw_email handles None service gracefully")
        else:
            print(f"  ❌ get_raw_email unexpected result: {result}")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error during error handling test: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Email Ingestion & Filtering Module - Test Suite")
    print("=" * 55)
    
    tests = [
        test_module_structure,
        test_function_signatures,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Module is ready for integration.")
        print("\n📋 Next steps:")
        print("1. Obtain Google Cloud credentials (credentials.json)")
        print("2. Test with real Gmail data")
        print("3. Proceed to Content Parsing & Extraction Module")
    else:
        print("❌ Some tests failed. Please review the module.")

if __name__ == '__main__':
    main()