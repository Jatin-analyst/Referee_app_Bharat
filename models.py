"""
Data Models for Career Referee Application
Defines the core data structures for career information and comparison results.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CareerInfo:
    """
    Data structure for individual career information.
    
    Attributes:
        overview: 2-line career summary
        skills: Required skills description
        salary: Salary range (low/medium/high)
        time_to_enter: Time to become job-ready
        pros: List of 3 advantages
        cons: List of 3 disadvantages
    """
    overview: str
    skills: str
    salary: str
    time_to_enter: str
    pros: List[str]
    cons: List[str]
    
    def __post_init__(self):
        """Validate data after initialization."""
        # Note: Salary validation is handled by standardization process
        # to allow for various input formats before standardization
        
        # Ensure pros and cons are lists with exactly 3 items
        if not isinstance(self.pros, list) or len(self.pros) != 3:
            raise ValueError("Pros must be a list with exactly 3 items")
        if not isinstance(self.cons, list) or len(self.cons) != 3:
            raise ValueError("Cons must be a list with exactly 3 items")


@dataclass
class ComparisonResult:
    """
    Data structure for complete career comparison results.
    
    Attributes:
        career_a: CareerInfo object for first career
        career_b: CareerInfo object for second career
        decision_guide: List of guidance statements
    """
    career_a: CareerInfo
    career_b: CareerInfo
    decision_guide: List[str]
    
    def __post_init__(self):
        """Validate data after initialization."""
        # Ensure decision_guide has at least 2 items (one for each career)
        if not isinstance(self.decision_guide, list) or len(self.decision_guide) < 2:
            raise ValueError("Decision guide must be a list with at least 2 guidance statements")
    
    def to_dict(self) -> Dict:
        """Convert ComparisonResult to dictionary format for JSON serialization."""
        return {
            "career_a": {
                "overview": self.career_a.overview,
                "skills": self.career_a.skills,
                "salary": self.career_a.salary,
                "time_to_enter": self.career_a.time_to_enter,
                "pros": self.career_a.pros,
                "cons": self.career_a.cons
            },
            "career_b": {
                "overview": self.career_b.overview,
                "skills": self.career_b.skills,
                "salary": self.career_b.salary,
                "time_to_enter": self.career_b.time_to_enter,
                "pros": self.career_b.pros,
                "cons": self.career_b.cons
            },
            "decision_guide": self.decision_guide
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ComparisonResult':
        """Create ComparisonResult from dictionary data."""
        career_a = CareerInfo(**data["career_a"])
        career_b = CareerInfo(**data["career_b"])
        return cls(
            career_a=career_a,
            career_b=career_b,
            decision_guide=data["decision_guide"]
        )


def validate_career_input(career_input: str) -> bool:
    """
    Validates career input for non-empty string validation.
    
    Args:
        career_input: The career string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(career_input, str):
        return False
    
    # Check if string is empty or contains only whitespace
    if not career_input or career_input.strip() == "":
        return False
    
    # Check length limits (max 100 characters as per design)
    if len(career_input.strip()) > 100:
        return False
    
    return True


def validate_user_name(name: str) -> bool:
    """
    Validates user name input.
    
    Args:
        name: The user name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(name, str):
        return False
    
    # Check if string is empty or contains only whitespace
    if not name or name.strip() == "":
        return False
    
    # Check reasonable length limits
    if len(name.strip()) > 50:
        return False
    
    return True


def validate_standardized_salary(salary: str) -> bool:
    """
    Validates that salary is in standardized format.
    
    Args:
        salary: The salary string to validate
        
    Returns:
        bool: True if salary is 'low', 'medium', or 'high'
    """
    return salary.lower() in {"low", "medium", "high"}


def create_standardized_career_info(overview: str, skills: str, salary: str, 
                                  time_to_enter: str, pros: List[str], cons: List[str]) -> CareerInfo:
    """
    Creates a CareerInfo with validated standardized salary.
    
    Args:
        overview: Career overview
        skills: Required skills
        salary: Salary in standardized format (low/medium/high)
        time_to_enter: Time to enter field
        pros: List of advantages
        cons: List of disadvantages
        
    Returns:
        CareerInfo object with validated salary
        
    Raises:
        ValueError: If salary is not in standardized format
    """
    if not validate_standardized_salary(salary):
        raise ValueError(f"Salary must be 'low', 'medium', or 'high', got: {salary}")
    
    return CareerInfo(
        overview=overview,
        skills=skills,
        salary=salary.lower(),
        time_to_enter=time_to_enter,
        pros=pros,
        cons=cons
    )