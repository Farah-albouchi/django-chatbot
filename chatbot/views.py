from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json
import requests
import threading
import time

# Hugging Face API integration
def get_chat_response(user_input):
    api_url = "https://chatgpt-api8.p.rapidapi.com/"

    payload = [
	{
		"content": "Hello! I'm an AI assistant bot based on ChatGPT 3. How may I help you?",
		"role": "system"
	},
	{
		"content": user_input,
		"role": "user"
	}
    ]
    headers = {
	"x-rapidapi-key": "6d1066720amsh569ceb4550b9323p1721b3jsnd3a80581d893",
	"x-rapidapi-host": "chatgpt-api8.p.rapidapi.com",
	"Content-Type": "application/json"
    }   

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
        print(response_data);
        if response.status_code == 200:
            return response_data['text']
        else:
            return "Service is at capacity. Please try again shortly."
    
    except Exception as e:
        print(f"Error calling Hugging Face API: {str(e)}")
        return "An error occurred. Please try again."

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message', '').strip()

            if not user_input:
                return JsonResponse({'error': 'Please enter a message'}, status=400)

            response = get_chat_response(user_input)
            
            return JsonResponse({'response': response})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request format'}, status=400)
        except Exception as e:
            print(f"Error in chat view: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def index(request):
    return render(request, 'chat.html')
