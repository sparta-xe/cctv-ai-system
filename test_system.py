"""
Test script for CCTV AI System
Run this to verify all components are working
"""

import os
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import cv2
        print("✅ OpenCV installed")
    except ImportError:
        print("❌ OpenCV not installed. Run: pip install opencv-python")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics installed")
    except ImportError:
        print("❌ Ultralytics not installed. Run: pip install ultralytics")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence Transformers installed")
    except ImportError:
        print("❌ Sentence Transformers not installed. Run: pip install sentence-transformers")
        return False
    
    try:
        import faiss
        print("✅ FAISS installed")
    except ImportError:
        print("❌ FAISS not installed. Run: pip install faiss-cpu")
        return False
    
    try:
        from fastapi import FastAPI
        print("✅ FastAPI installed")
    except ImportError:
        print("❌ FastAPI not installed. Run: pip install fastapi")
        return False
    
    return True

def test_modules():
    """Test if all custom modules can be imported"""
    print("\nTesting custom modules...")
    try:
        import detector
        print("✅ detector.py loaded")
    except Exception as e:
        print(f"❌ detector.py failed: {e}")
        return False
    
    try:
        import embedder
        print("✅ embedder.py loaded")
    except Exception as e:
        print(f"❌ embedder.py failed: {e}")
        return False
    
    try:
        import tracker
        print("✅ tracker.py loaded")
    except Exception as e:
        print(f"❌ tracker.py failed: {e}")
        return False
    
    try:
        import database
        print("✅ database.py loaded")
    except Exception as e:
        print(f"❌ database.py failed: {e}")
        return False
    
    try:
        import auth
        print("✅ auth.py loaded")
    except Exception as e:
        print(f"❌ auth.py failed: {e}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    dirs = ["storage", "storage/frames", "templates"]
    
    for d in dirs:
        if os.path.exists(d):
            print(f"✅ {d} exists")
        else:
            print(f"⚠️  {d} not found, creating...")
            os.makedirs(d, exist_ok=True)
    
    return True

def test_auth():
    """Test authentication system"""
    print("\nTesting authentication...")
    from auth import login
    
    # Test valid login
    role = login("admin", "admin123")
    if role == "admin":
        print("✅ Admin login works")
    else:
        print("❌ Admin login failed")
        return False
    
    # Test invalid login
    role = login("admin", "wrongpassword")
    if role is None:
        print("✅ Invalid login rejected")
    else:
        print("❌ Invalid login accepted (security issue!)")
        return False
    
    return True

def test_embedder():
    """Test embedding system"""
    print("\nTesting embedder...")
    from embedder import add, search, get_index_size
    
    # Add test data
    add("person walking", {"test": "data1"})
    add("car driving", {"test": "data2"})
    
    size = get_index_size()
    if size >= 2:
        print(f"✅ Embedder can add data (size: {size})")
    else:
        print("❌ Embedder failed to add data")
        return False
    
    # Test search
    results = search("person")
    if len(results) > 0:
        print(f"✅ Embedder can search (found {len(results)} results)")
    else:
        print("❌ Embedder search failed")
        return False
    
    return True

def main():
    print("=" * 50)
    print("CCTV AI System - Component Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Custom Modules", test_modules),
        ("Directories", test_directories),
        ("Authentication", test_auth),
        ("Embedder", test_embedder),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("Run: python main.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
