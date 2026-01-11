# Requirements Document

## Introduction

The Career Referee is an AI-powered career comparison tool that helps users make informed decisions between two career options. The system provides objective, neutral analysis using multiple AI providers (OpenAI, Ollama, or mock data) with cost-efficient prompting and standardized salary formatting.

## Glossary

- **Career_Referee**: The main application system that orchestrates career comparisons
- **AI_Provider**: External AI service (OpenAI, Ollama, or mock data) that generates career analysis
- **Career_Info**: Data structure containing overview, skills, salary, timeline, pros, and cons for a single career
- **Comparison_Result**: Complete comparison data containing two CareerInfo objects and decision guidance
- **Salary_Standardizer**: Component that converts various salary formats to low/medium/high categories
- **UI_Component**: Streamlit-based user interface elements for input and display

## Requirements

### Requirement 1: User Input Collection

**User Story:** As a user, I want to input my name and two career options, so that I can receive a personalized career comparison.

#### Acceptance Criteria

1. WHEN a user accesses the application, THE Career_Referee SHALL display an input form with fields for name and two career options
2. WHEN a user submits the form with valid inputs, THE Career_Referee SHALL store the inputs and proceed to analysis
3. WHEN a user submits empty or invalid inputs, THE Career_Referee SHALL display validation errors and prevent submission
4. WHEN a user enters identical career options, THE Career_Referee SHALL reject the input and request different careers
5. THE Career_Referee SHALL limit career input to 100 characters maximum
6. THE Career_Referee SHALL limit user name input to 50 characters maximum

### Requirement 2: AI-Powered Career Analysis

**User Story:** As a user, I want the system to analyze my career options using AI, so that I receive comprehensive and objective career information.

#### Acceptance Criteria

1. WHEN career analysis is requested, THE AI_Provider SHALL generate structured career data including overview, skills, salary, timeline, pros, and cons
2. WHEN multiple AI providers are available, THE Career_Referee SHALL try providers in order: Ollama, OpenAI, then mock data
3. WHEN an AI provider fails, THE Career_Referee SHALL automatically fallback to the next available provider
4. WHEN all AI providers fail, THE Career_Referee SHALL return mock comparison data
5. THE AI_Provider SHALL return exactly 3 pros and 3 cons for each career
6. THE AI_Provider SHALL provide decision guidance with at least 2 recommendation statements

### Requirement 3: Salary Standardization

**User Story:** As a user, I want salary information presented in a consistent format, so that I can easily compare compensation across different careers.

#### Acceptance Criteria

1. WHEN AI returns salary data in any format, THE Salary_Standardizer SHALL convert it to low/medium/high categories
2. WHEN salary contains numeric ranges under $60k, THE Salary_Standardizer SHALL categorize as "low"
3. WHEN salary contains numeric ranges $60k-$99k, THE Salary_Standardizer SHALL categorize as "medium"  
4. WHEN salary contains numeric ranges $100k+, THE Salary_Standardizer SHALL categorize as "high"
5. WHEN salary contains descriptive terms like "entry" or "junior", THE Salary_Standardizer SHALL categorize as "low"
6. WHEN salary data is unclear or missing, THE Salary_Standardizer SHALL default to "medium"

### Requirement 4: Career Comparison Display

**User Story:** As a user, I want to see my career options compared side-by-side, so that I can easily evaluate the differences and make an informed decision.

#### Acceptance Criteria

1. WHEN comparison data is available, THE UI_Component SHALL display careers in side-by-side cards
2. WHEN displaying career information, THE UI_Component SHALL show overview, skills, salary, timeline, pros, and cons
3. WHEN displaying salary, THE UI_Component SHALL show standardized format with appropriate emoji (💰)
4. WHEN displaying timeline, THE UI_Component SHALL show time-to-enter information with clock emoji (⏱️)
5. WHEN displaying pros, THE UI_Component SHALL prefix each item with checkmark emoji (✅)
6. WHEN displaying cons, THE UI_Component SHALL prefix each item with warning emoji (⚠️)

### Requirement 5: Decision Guidance

**User Story:** As a user, I want personalized guidance on choosing between careers, so that I can understand which option aligns better with my priorities.

#### Acceptance Criteria

1. WHEN comparison is complete, THE Career_Referee SHALL display decision guidance section
2. WHEN showing guidance, THE UI_Component SHALL present recommendations with clear visual indicators (🅰️, 🅱️)
3. WHEN guidance contains multiple items, THE UI_Component SHALL display each with appropriate formatting
4. THE Career_Referee SHALL personalize guidance using the user's provided name
5. THE Career_Referee SHALL ensure guidance remains neutral and objective

### Requirement 6: Multi-Provider AI Integration

**User Story:** As a system administrator, I want the application to support multiple AI providers with automatic fallback, so that users receive analysis even when preferred providers are unavailable.

#### Acceptance Criteria

1. WHEN Ollama is available locally, THE Career_Referee SHALL use it as the primary AI provider
2. WHEN Ollama is unavailable and OpenAI API key exists, THE Career_Referee SHALL use OpenAI as secondary provider
3. WHEN both AI providers fail, THE Career_Referee SHALL use mock data as final fallback
4. WHEN using OpenAI, THE Career_Referee SHALL implement retry logic with exponential backoff
5. WHEN using Ollama, THE Career_Referee SHALL try multiple models in preference order
6. THE Career_Referee SHALL optimize prompts to minimize token usage for cost efficiency

### Requirement 7: Data Validation and Error Handling

**User Story:** As a user, I want the system to handle errors gracefully, so that I receive meaningful feedback when something goes wrong.

#### Acceptance Criteria

1. WHEN AI returns invalid JSON, THE Career_Referee SHALL parse and clean the response before processing
2. WHEN AI response is missing required fields, THE Career_Referee SHALL return validation errors
3. WHEN AI response contains invalid salary formats, THE Career_Referee SHALL apply standardization
4. WHEN pros or cons lists don't contain exactly 3 items, THE Career_Referee SHALL reject the response
5. WHEN decision guide contains fewer than 2 items, THE Career_Referee SHALL reject the response
6. WHEN any validation fails, THE Career_Referee SHALL provide fallback data with error messaging

### Requirement 8: Navigation and Session Management

**User Story:** As a user, I want to navigate between input and comparison pages seamlessly, so that I can easily compare different career combinations.

#### Acceptance Criteria

1. WHEN starting the application, THE Career_Referee SHALL display the input page
2. WHEN valid comparison is submitted, THE Career_Referee SHALL navigate to comparison page
3. WHEN on comparison page, THE Career_Referee SHALL provide option to return to input page
4. WHEN returning to input page, THE Career_Referee SHALL clear previous session data
5. WHEN session data is missing, THE Career_Referee SHALL redirect to input page
6. THE Career_Referee SHALL maintain session state throughout the comparison process