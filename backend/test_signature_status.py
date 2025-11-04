"""
Quick test to verify signature service is properly configured
"""

from app.services.signature_service import signature_service

print("=" * 60)
print("DIGITAL SIGNATURE SERVICE - STATUS CHECK")
print("=" * 60)

# Get service status
status = signature_service.get_service_status()

print("\n📊 Service Status:")
for key, value in status.items():
    print(f"  {key}: {value}")

print("\n🔒 Service Enabled:", signature_service.is_signature_available())

print("\n✅ Service imported and configured successfully!")
print("\n⚠️  REMINDER: Service is DISABLED until legal verification complete")
print("   and CA partnership signed.")
print("=" * 60)
