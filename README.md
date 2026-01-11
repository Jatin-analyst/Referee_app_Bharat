# Career Referee ⚖️

A neutral career comparison tool that helps users make informed decisions between two career options using AI-powered analysis. Supports both OpenAI and open source AI models for cost efficiency.

## Features

- **Multiple AI Providers**: Supports OpenAI, Ollama (local), and other open source models
- **Cost Efficient**: Prioritizes free/low-cost AI options, optimized prompts
- **Neutral Comparisons**: Objective career analysis without bias
- **Modern UI**: Clean, responsive Streamlit interface
- **Salary Standardization**: Automatically standardizes salary formats to low/medium/high
- **Comprehensive Analysis**: Covers skills, salary, timeline, pros, and cons
- **Decision Guidance**: Personalized guidance based on your priorities

## AI Provider Options (in order of preference)

1. **Ollama (Free, Local)** - Install Ollama locally for free AI analysis
2. **OpenAI (Paid)** - Requires API key, optimized for 25-35 credits per comparison
3. **Mock Data** - Fallback for testing without AI

## Quick Start

### Option 1: Free with Ollama (Recommended)

1. **Install Ollama**
   ```bash
   # Install Ollama from https://ollama.ai
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model (choose one)
   ollama pull llama3.1:8b    # Best quality
   ollama pull llama3:8b      # Good balance
   ollama pull mistral:7b     # Fastest
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

### Option 2: With OpenAI

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set OpenAI API Key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your name for personalization
2. Input two career options you're considering
3. Click "Compare Careers" to get AI-powered analysis
4. Review the side-by-side comparison with standardized salary ranges
5. Use the decision guide to understand which career aligns with your priorities

## Architecture

- **app.py**: Main Streamlit application with routing
- **models.py**: Data models, validation, and salary standardization
- **referee_agent.py**: Multi-provider AI integration with optimized prompts
- **ui.py**: UI components and styling
- **styles.css**: Custom CSS for modern design

## Deployment

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Add `OPENAI_API_KEY` to secrets (optional - will use mock data if not provided)
4. Deploy!

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Option 1: Use Ollama (free)
ollama pull llama3.1:8b
streamlit run app.py

# Option 2: Use OpenAI (paid)
export OPENAI_API_KEY="your-key"
streamlit run app.py
```

## Cost Efficiency Features

- **Free AI Option**: Ollama runs locally without API costs
- **Optimized Prompts**: Minimal token usage for OpenAI (25-35 credits)
- **Smart Fallbacks**: Graceful degradation to mock data
- **Salary Standardization**: Reduces AI processing complexity

## Requirements

- Python 3.8+
- Internet connection (for OpenAI) OR Ollama installed locally
- Optional: OpenAI API key for premium analysis

## License

MIT License - feel free to use and modify!