# app/services/gemini_service.py
import google.generativeai as genai
from typing import Dict, List, Optional
import asyncio

class GeminiContentGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.flash_model = genai.GenerativeModel('gemini-1.5-flash')
        self.pro_model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_text_summary(self, text: str, target_language: str, 
                                   source_language: str = "auto",
                                   level: str = "intermediate") -> Dict[str, str]:
        """Generate text summary in target language for language learners"""
        
        prompt = f"""
        Create a learning-focused summary of this text in {target_language}.
        
        Source language: {source_language}
        Target language: {target_language}
        Learner level: {level}
        
        Requirements:
        1. Create a summary that captures the main points
        2. Use vocabulary appropriate for {level} learners
        
        Text to summarize:
        {text}
        
        Format your response as:
        SUMMARY:
        [Summary in {target_language}]
        
        """

        print(prompt)
        
        try:
            response = await self.flash_model.generate_content_async(prompt)
            return self._parse_summary_response(response.text)
        except Exception as e:
            return {"error": f"Summary generation failed: {str(e)}"}
    
    def _parse_summary_response(self, response_text: str) -> Dict[str, str]:
        """Parse the formatted response into structured data"""
        sections = {
            "summary": "",
            "vocabulary": [],
            "phrases": []
        }
        
        lines = response_text.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                current_section = "summary"
            elif line.startswith("KEY VOCABULARY:"):
                current_section = "vocabulary"
            elif line.startswith("USEFUL PHRASES:"):
                current_section = "phrases"
            elif line and current_section:
                if current_section == "summary":
                    sections["summary"] += line + " "
                elif line.startswith("-"):
                    if current_section == "vocabulary":
                        sections["vocabulary"].append(line[1:].strip())
                    elif current_section == "phrases":
                        sections["phrases"].append(line[1:].strip())
        
        return sections
    

    async def generate_conversation(self, scenario: str, target_language: str, 
                                source_language: str = "English",
                                level: str = "intermediate", 
                                num_exchanges: int = 6) -> Dict[str, any]:
        """Generate realistic conversations for language practice"""
        
        prompt = f"""
        Create a natural conversation in {target_language} between two people.
        
        Scenario: {scenario}
        Target language: {target_language}
        Learner level: {level}
        Number of exchanges: {num_exchanges}
        
        Requirements:
        1. Make the conversation realistic and practical
        2. Use {level}-appropriate vocabulary and grammar
        3. Include common expressions and cultural elements
        4. Each person should speak {num_exchanges} times
        
        Format:
        CONVERSATION:
        Person A: [dialogue]
        Person B: [dialogue]
        
        """
        
        try:
            # Use Pro model for better conversation quality
            response = await self.pro_model.generate_content_async(prompt)
            return self._parse_conversation_response(response.text, scenario, target_language, level)
        except Exception as e:
            return {"error": f"Conversation generation failed: {str(e)}"}

    def _parse_conversation_response(self, response_text: str, scenario: str, 
                                language: str, level: str) -> Dict[str, any]:
        """Parse conversation response into structured format"""
        result = {
            "scenario": scenario,
            "language": language,
            "level": level,
            "conversation": []
        }
        
        lines = response_text.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("CONVERSATION:"):
                current_section = "conversation"
            elif current_section:
                if current_section == "conversation":
                    if line.startswith("Person A:"):
                        result["conversation"].append({
                            "speaker": "A",
                            "text": line[9:].strip()
                        })
                    elif line.startswith("Person B:"):
                        result["conversation"].append({
                            "speaker": "B",
                            "text": line[9:].strip()
                        })
        
        return result

    async def generate_audio_summary(self, transcription: str, target_language: str,
                                source_language: str = "auto") -> Dict[str, str]:
        """Generate summary from audio transcription"""
        
        prompt = f"""
        This is a transcription from an audio file in {source_language}.
        Create a comprehensive summary in {target_language} for language learners.
        
        Include:
        1. Main topic and key points
        2. Important vocabulary used
        3. Any cultural context mentioned
        4. Suggested follow-up activities
        
        Transcription:
        {transcription}
        
        Format:
        TOPIC: [main topic]
        
        KEY POINTS:
        - [point 1]
        - [point 2]
        
        IMPORTANT VOCABULARY:
        - [word]: [meaning/context]
        
        CULTURAL CONTEXT:
        [if any]
        
        SUGGESTED ACTIVITIES:
        - [activity 1]
        - [activity 2]
        """
        
        try:
            response = await self.flash_model.generate_content_async(prompt)
            return self._parse_audio_summary(response.text)
        except Exception as e:
            return {"error": f"Audio summary generation failed: {str(e)}"}