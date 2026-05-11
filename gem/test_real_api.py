#!/usr/bin/env python3
"""
Real Gemini API test - tests actual API call without mocks
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv('/home/joona/ai-assistant-app/.env')

def test_gemini_api():
    """Test actual Gemini API call"""
    
    # Get credentials
    api_key = os.environ.get('GEMINI_API_KEY')
    model = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')
    system_prompt = os.environ.get('GEMINI_SYSTEM_PROMPT', 'You are a helpful assistant.')
    
    if not api_key:
        print("✗ GEMINI_API_KEY not set")
        return False
    
    print(f"✓ API Key: {api_key[:20]}...")
    print(f"✓ Model: {model}")
    
    # Prepare API request
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": "Tervehdys! Kuka sinä olet? (Respond in 1-2 sentences)"
            }]
        }],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 150
        }
    }
    
    print(f"\nℹ Calling {model}...")
    
    try:
        response = requests.post(
            url,
            headers=headers,
            params={"key": api_key},
            json=payload,
            timeout=10
        )
        
        print(f"✓ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and data['candidates']:
                text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"✓ Response:\n  {text}\n")
                return True
            else:
                print(f"✗ No candidates in response: {data}")
                return False
        else:
            print(f"✗ API Error: {response.status_code}")
            print(f"  {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_gemini_api()
    exit(0 if success else 1)
