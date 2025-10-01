# test_bedrock_direct.py
import boto3
import json

print("Testing Bedrock access...")

# Create bedrock-runtime client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

try:
    # Try to call Claude directly
    response = bedrock_runtime.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": "Say 'hello' if you can hear me"}]
            }
        ]
    )
    
    print("✓ SUCCESS! Bedrock is working!")
    print(f"Response: {response['output']['message']['content'][0]['text']}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nThis means your AWS credentials don't have Bedrock permissions")
