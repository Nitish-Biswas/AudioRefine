
import requests

class correcting:
    def correct_transcription(word_timings):

        segments = []
        current_segment = []
        current_timing = {'start': None, 'end': None}
            
        for i, word_info in enumerate(word_timings):
            if current_segment == []:
                current_timing['start'] = word_info['start_time']
                current_segment.append(word_info['word'])
            else:
                    # Check if there's a significant pause
                time_gap = word_info['start_time'] - word_timings[i-1]['end_time']
                if time_gap > 0.35:  # 350ms threshold for natural pauses
                    current_timing['end'] = word_timings[i-1]['end_time']
                    segments.append({
                        'text': ' '.join(current_segment),
                        'timing': current_timing.copy()
                    })
                    current_segment = [word_info['word']]
                    current_timing['start'] = word_info['start_time']
                else:
                    current_segment.append(word_info['word'])
        if current_segment:
            current_timing['end'] = word_timings[-1]['end_time']
            segments.append({
                'text': ' '.join(current_segment),
                'timing': current_timing.copy()
            })

        
        azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc" 
        azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"  
        
        # Check if both the key and endpoint are provided
        if azure_openai_key and azure_openai_endpoint:
            try:
                
                headers = {
                    "Content-Type": "application/json",
                    "api-key": azure_openai_key
                }
                enhanced_segments=[]
                
                for segment in segments:
                    data = {
                        "messages":[
                            {"role": "system", "content": "Correct grammar and remove filler words while keeping the same general length and meaning. Preserve key timing and pacing."},
                            {"role": "user", "content": segment['text']}
                        ],
                        "max_tokens": 150
                    }
                    response = requests.post(azure_openai_endpoint, headers=headers, json=data)
                    if response.status_code == 200:
                        result = response.json()
                        enhanced_segments.append({
                            'text': result["choices"][0]["message"]["content"],
                            'timing': segment['timing']
                        })
                return [True,enhanced_segments]
                
            except Exception as e:
                return [False,e]
        else:
            return [False, "Please enter all the required details."]
        