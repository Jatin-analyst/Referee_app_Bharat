"""
AI Agent for Career Comparison
Handles AI interaction and prompt optimization for career analysis.
Supports both OpenAI and open source APIs for cost efficiency.
"""

from typing import Dict, List
import json
import os
import time
import random
import re
from models import CareerInfo, ComparisonResult

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def run_referee(career_a: str, career_b: str) -> ComparisonResult:
    """
    Main comparison function that generates career analysis using AI.
    Supports OpenAI, Ollama, and other open source APIs.
    
    Args:
        career_a: First career option
        career_b: Second career option
        
    Returns:
        ComparisonResult object containing career comparison data
    """
    # Try different AI providers in order of preference
    providers = [
        ("ollama", _call_ollama_api),
        ("openai", _call_openai_api),
        ("mock", _get_mock_comparison)
    ]
    
    for provider_name, provider_func in providers:
        try:
            if provider_name == "ollama" and _is_ollama_available():
                print(f"Using {provider_name} for AI analysis...")
                result = provider_func(career_a, career_b)
                return _standardize_salary_format(result)
            elif provider_name == "openai" and OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                print(f"Using {provider_name} for AI analysis...")
                result = provider_func(career_a, career_b)
                return _standardize_salary_format(result)
            elif provider_name == "mock":
                print("Using mock data for analysis...")
                result = provider_func(career_a, career_b)
                return _standardize_salary_format(result)
        except Exception as e:
            print(f"Failed to use {provider_name}: {e}")
            continue
    
    # Final fallback
    return _get_mock_comparison(career_a, career_b)


def _is_ollama_available() -> bool:
    """Check if Ollama is running locally."""
    if not REQUESTS_AVAILABLE:
        return False
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def _call_ollama_api(career_a: str, career_b: str) -> ComparisonResult:
    """Call Ollama API for career comparison."""
    if not REQUESTS_AVAILABLE:
        raise Exception("requests library not available")
    
    prompt = _build_optimized_prompt(career_a, career_b)
    
    # Try different models in order of preference
    models = ["llama3.1:8b", "llama3:8b", "llama2:7b", "mistral:7b"]
    
    for model in models:
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 800
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get("response", "")
                return _parse_ai_response(ai_response)
                
        except Exception as e:
            print(f"Failed with model {model}: {e}")
            continue
    
    raise Exception("All Ollama models failed")


def _call_openai_api(career_a: str, career_b: str) -> ComparisonResult:
    """Call OpenAI API with retry logic."""
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            prompt = _build_optimized_prompt(career_a, career_b)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a neutral career referee. Provide objective career comparisons in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3,
                timeout=30,
            )
            
            ai_response = response.choices[0].message.content
            return _parse_ai_response(ai_response)
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
    
    raise Exception("OpenAI API failed after retries")


def _get_mock_comparison(career_a: str, career_b: str) -> ComparisonResult:
    """
    Returns a mock comparison for testing when AI is not available.
    """
    career_a_info = CareerInfo(
        overview=f"{career_a} involves specialized skills and offers various career paths. This field typically requires dedicated learning and practice.",
        skills=f"Core skills for {career_a} include problem-solving, communication, and domain-specific technical abilities.",
        salary="medium",
        time_to_enter="2-4 years",
        pros=["Growing field", "Good opportunities", "Skill development"],
        cons=["Learning curve", "Competition", "Constant updates"]
    )
    
    career_b_info = CareerInfo(
        overview=f"{career_b} offers unique opportunities and challenges. This career path has its own requirements and growth potential.",
        skills=f"Essential skills for {career_b} include analytical thinking, creativity, and relevant technical knowledge.",
        salary="medium",
        time_to_enter="2-4 years",
        pros=["Diverse opportunities", "Creative work", "Professional growth"],
        cons=["Market variability", "Skill requirements", "Time investment"]
    )
    
    return ComparisonResult(
        career_a=career_a_info,
        career_b=career_b_info,
        decision_guide=[
            f"Choose {career_a} if you prefer structured problem-solving and technical challenges",
            f"Choose {career_b} if you value creativity and diverse project opportunities"
        ]
    )


def _build_optimized_prompt(career_a: str, career_b: str) -> str:
    """
    Creates token-efficient prompt for AI analysis.
    
    This prompt is optimized to minimize token usage while ensuring comprehensive
    career comparison data. Target: 25-35 credits per comparison.
    """
    return f"""Compare careers: {career_a} vs {career_b}

Rules: Neutral comparison, no recommendations, simple language
Output JSON format:
{{
  "career_a": {{
    "overview": "2-line summary",
    "skills": "required skills",
    "salary": "low/medium/high",
    "time_to_enter": "time needed",
    "pros": ["advantage1", "advantage2", "advantage3"],
    "cons": ["disadvantage1", "disadvantage2", "disadvantage3"]
  }},
  "career_b": {{
    "overview": "2-line summary", 
    "skills": "required skills",
    "salary": "low/medium/high",
    "time_to_enter": "time needed",
    "pros": ["advantage1", "advantage2", "advantage3"],
    "cons": ["disadvantage1", "disadvantage2", "disadvantage3"]
  }},
  "decision_guide": [
    "Choose {career_a} if...",
    "Choose {career_b} if..."
  ]
}}

Focus on trade-offs, not superiority. Be concise."""


def _parse_ai_response(response: str) -> ComparisonResult:
    """
    Validates and parses JSON response from AI.
    
    Args:
        response: Raw AI response string
        
    Returns:
        ComparisonResult object with validated data
        
    Raises:
        ValueError: If response cannot be parsed or validated
    """
    if not response or not response.strip():
        raise ValueError("Empty or null response from AI")
    
    try:
        # Clean the response - remove any markdown formatting
        cleaned_response = response.strip()
        
        # Handle common markdown code block formats
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
            
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
            
        cleaned_response = cleaned_response.strip()
        
        # Parse JSON
        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        
        # Validate data is a dictionary
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data)}")
        
        # Validate required top-level fields exist
        required_fields = ["career_a", "career_b", "decision_guide"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Validate career data structure
        for career_key in ["career_a", "career_b"]:
            career_data = data[career_key]
            
            if not isinstance(career_data, dict):
                raise ValueError(f"{career_key} must be an object, got {type(career_data)}")
            
            required_career_fields = ["overview", "skills", "salary", "time_to_enter", "pros", "cons"]
            missing_career_fields = [field for field in required_career_fields if field not in career_data]
            if missing_career_fields:
                raise ValueError(f"Missing fields in {career_key}: {missing_career_fields}")
            
            # Validate salary format
            salary = career_data.get("salary", "").lower()
            if salary not in ["low", "medium", "high"]:
                raise ValueError(f"Invalid salary format in {career_key}: {salary}. Must be low/medium/high")
            
            # Validate pros and cons are lists
            for list_field in ["pros", "cons"]:
                field_value = career_data.get(list_field)
                if not isinstance(field_value, list):
                    raise ValueError(f"{list_field} in {career_key} must be a list, got {type(field_value)}")
                if len(field_value) != 3:
                    raise ValueError(f"{list_field} in {career_key} must have exactly 3 items, got {len(field_value)}")
        
        # Validate decision guide
        decision_guide = data.get("decision_guide")
        if not isinstance(decision_guide, list):
            raise ValueError(f"decision_guide must be a list, got {type(decision_guide)}")
        if len(decision_guide) < 2:
            raise ValueError(f"decision_guide must have at least 2 items, got {len(decision_guide)}")
        
        # Create and return ComparisonResult
        return ComparisonResult.from_dict(data)
        
    except ValueError:
        # Re-raise ValueError as-is (these are validation errors we want to propagate)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise ValueError(f"Unexpected error parsing response: {e}")


def _standardize_salary_format(result: ComparisonResult) -> ComparisonResult:
    """
    Standardizes salary format to ensure only 'low', 'medium', 'high' values.
    
    Args:
        result: ComparisonResult with potentially non-standard salary formats
        
    Returns:
        ComparisonResult with standardized salary formats
    """
    def standardize_salary(salary_str: str) -> str:
        """Convert various salary formats to standard low/medium/high."""
        if not salary_str:
            return "medium"
        
        salary_lower = salary_str.lower().strip()
        
        # Direct matches
        if salary_lower in ["low", "medium", "high"]:
            return salary_lower
        
        # Pattern matching for various formats
        low_patterns = [
            r'\b(low|poor|minimal|entry|junior|starting|below|under)\b',
            r'\$?[0-9,]+\s*-?\s*\$?[0-5][0-9],?000',  # Under 60k
            r'\b[0-5][0-9]k?\b'  # Under 60k
        ]
        
        high_patterns = [
            r'\b(high|excellent|premium|senior|executive|above|over|top)\b',
            r'\$?[1-9][0-9][0-9],?000',  # 100k+
            r'\b[1-9][0-9][0-9]k?\b',  # 100k+
            r'[8-9][0-9],?000',  # 80k-99k (upper medium to high)
            r'\b[8-9][0-9]k\b'  # 80k-99k
        ]
        
        medium_patterns = [
            r'\b(medium|average|moderate|mid|middle|fair|decent|competitive)\b',
            r'\$?[6-9][0-9],?000',  # 60k-99k
            r'\b[6-9][0-9]k?\b'  # 60k-99k
        ]
        
        # Check patterns
        for pattern in low_patterns:
            if re.search(pattern, salary_lower):
                return "low"
        
        for pattern in high_patterns:
            if re.search(pattern, salary_lower):
                return "high"
        
        for pattern in medium_patterns:
            if re.search(pattern, salary_lower):
                return "medium"
        
        # Default fallback
        return "medium"
    
    # Standardize both careers
    standardized_career_a = CareerInfo(
        overview=result.career_a.overview,
        skills=result.career_a.skills,
        salary=standardize_salary(result.career_a.salary),
        time_to_enter=result.career_a.time_to_enter,
        pros=result.career_a.pros,
        cons=result.career_a.cons
    )
    
    standardized_career_b = CareerInfo(
        overview=result.career_b.overview,
        skills=result.career_b.skills,
        salary=standardize_salary(result.career_b.salary),
        time_to_enter=result.career_b.time_to_enter,
        pros=result.career_b.pros,
        cons=result.career_b.cons
    )
    
    return ComparisonResult(
        career_a=standardized_career_a,
        career_b=standardized_career_b,
        decision_guide=result.decision_guide
    )
    """
    Returns a fallback result when AI response parsing fails.
    
    Args:
        error_message: Custom error message to display
    """
    career_a_info = CareerInfo(
        overview=f"Unable to analyze career: {error_message}. Please try again with different inputs.",
        skills="Analysis unavailable",
        salary="medium",
        time_to_enter="Unknown",
        pros=["Please", "try", "again"],
        cons=["Analysis", "error", "occurred"]
    )
    
    career_b_info = CareerInfo(
        overview=f"Unable to analyze career: {error_message}. Please try again with different inputs.",
        skills="Analysis unavailable",
        salary="medium",
        time_to_enter="Unknown",
        pros=["Please", "try", "again"],
        cons=["Analysis", "error", "occurred"]
    )
    
    return ComparisonResult(
        career_a=career_a_info,
        career_b=career_b_info,
        decision_guide=[
            f"Analysis failed: {error_message}",
            "Please check your inputs and try again"
        ]
    )


def _get_error_fallback_result(error_message: str = "Analysis error occurred") -> ComparisonResult:
    """
    Returns a fallback result when AI response parsing fails.
    
    Args:
        error_message: Custom error message to display
    """
    career_a_info = CareerInfo(
        overview=f"Unable to analyze career: {error_message}. Please try again with different inputs.",
        skills="Analysis unavailable",
        salary="medium",
        time_to_enter="Unknown",
        pros=["Please", "try", "again"],
        cons=["Analysis", "error", "occurred"]
    )
    
    career_b_info = CareerInfo(
        overview=f"Unable to analyze career: {error_message}. Please try again with different inputs.",
        skills="Analysis unavailable",
        salary="medium",
        time_to_enter="Unknown",
        pros=["Please", "try", "again"],
        cons=["Analysis", "error", "occurred"]
    )
    
    return ComparisonResult(
        career_a=career_a_info,
        career_b=career_b_info,
        decision_guide=[
            f"Analysis failed: {error_message}",
            "Please check your inputs and try again"
        ]
    )