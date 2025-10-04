# ARCHITECTURE GUIDE FOR RCM_RECIPE

## Project Overview

RCM_RECIPE is an AI-powered Recipe Generation System that creates personalized recipes based on trending topics and user segmentation.

## Project Structure

```
RCM_RECIPE/
├── app/                    # FastAPI application layer
│   ├── main.py            # Application entry point
│   └── routers/           # API route handlers
│       ├── recipes.py     # Recipe generation endpoints
│       ├── trends.py      # Trend analysis endpoints
│       ├── segments.py    # User segmentation endpoints
│       └── health.py      # Health check endpoints
│
├── domain/                # Business logic (core domain)
│   ├── entities/          # Business entities
│   │   ├── recipe.py      # Recipe entity
│   │   ├── user_segment.py # User segment entity
│   │   ├── trend.py       # Trend entity
│   │   └── ingredient.py  # Ingredient entity
│   ├── value_objects/     # Immutable value objects
│   │   ├── recipe_metadata.py # Recipe metadata
│   │   ├── trend_score.py     # Trend scoring
│   │   └── user_preferences.py # User preferences
│   └── services/          # Domain services
│       ├── recipe_generation_service.py # Core recipe logic
│       ├── trend_analysis_service.py    # Trend analysis
│       ├── user_segmentation_service.py # User segmentation
│       └── content_optimization_service.py # Content optimization
│
├── application/           # Application logic layer
│   ├── commands/          # Command objects (CQRS)
│   │   ├── generate_recipe_command.py
│   │   ├── analyze_trends_command.py
│   │   └── segment_users_command.py
│   └── use_cases/         # Use case implementations
│       ├── generate_personalized_recipe_use_case.py
│       ├── collect_trending_topics_use_case.py
│       ├── optimize_content_for_platform_use_case.py
│       └── analyze_recipe_performance_use_case.py
│
├── infrastructure/        # External concerns
│   ├── ai/               # AI model integrations
│   │   ├── gemini_client.py      # Google Gemini API
│   │   ├── t5_model_handler.py   # Hugging Face T5 model
│   │   └── model_factory.py      # AI model factory
│   ├── data_sources/     # External data sources
│   │   ├── google_trends_client.py
│   │   ├── news_api_client.py
│   │   ├── youtube_api_client.py
│   │   └── social_media_scraper.py
│   ├── db/               # Database implementations
│   │   ├── models.py     # SQLAlchemy models
│   │   └── repositories.py # Data access layer
│   ├── cache/            # Caching layer
│   │   └── redis_cache.py
│   └── schedulers/       # Background tasks
│       ├── trend_collector_scheduler.py
│       └── recipe_performance_analyzer.py
│
├── data/                 # Data storage
│   ├── trends/           # Trend data
│   ├── recipes/          # Generated recipes
│   ├── user_segments/    # User segmentation data
│   └── performance/      # Recipe performance metrics
│
├── configs/              # Configuration files
│   └── settings.py       # Application settings
│
├── .claude/              # Claude AI agents
│   └── agents/           # Specialized AI agents
│       ├── agent-expert.md
│       ├── prompt-engineer.md
│       ├── ml-engineer.md
│       ├── data-scientist.md
│       └── code-reviewer.md
│
├── output/               # Generated content
├── logs/                 # Application logs
├── cache/                # Cached data
├── notebooks/            # Data analysis notebooks
├── tests/                # Test files
└── docs/                 # Documentation
```

## Core Domain Concepts

### 1. Recipe Generation System

```python
# Domain Entity Example
class Recipe:
    def __init__(self, title: str, ingredients: List[Ingredient],
                 instructions: List[str], metadata: RecipeMetadata):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.metadata = metadata
        self.trend_alignment_score = 0.0
        self.user_segment_match = []
```

### 2. User Segmentation

- **Gen Z (10-25)**: Viral trends, aesthetic focus
- **Millennials (26-40)**: Quality, artisan preferences
- **Health Conscious**: Low sugar, organic ingredients
- **Kids (3-12)**: Colorful, fun presentations
- **Elderly (65+)**: Traditional, nutritious recipes

### 3. Trend Analysis Pipeline

```python
# Trend Collection Flow
Trend Sources → Data Aggregation → Scoring → Segmentation → Recipe Influence
     ↓              ↓              ↓           ↓              ↓
Google Trends   Normalize Data   Trend Score  User Mapping   Generation Input
News API        Remove Noise     Relevance    Demographics   Content Optimization
YouTube API     Deduplicate      Popularity   Preferences    Multi-language
Social Media    Categorize       Longevity    Behavior       Platform Adaptation
```

## Layer Responsibilities

### 1. Domain Layer (`domain/`)

- **Purpose:** Core recipe generation business logic
- **Rules:**
  - No external AI model dependencies
  - Pure business logic for recipes and trends
  - Framework agnostic entities and services
- **Components:**
  - Recipe entity with validation rules
  - Trend scoring algorithms
  - User preference matching logic

### 2. Application Layer (`application/`)

- **Purpose:** Orchestrates recipe generation workflows
- **Rules:**
  - Uses domain layer services
  - No direct AI API calls
  - Contains use cases for complex workflows
- **Components:**
  - Generate recipe use case
  - Trend analysis workflows
  - User segmentation logic

### 3. Infrastructure Layer (`infrastructure/`)

- **Purpose:** AI models and external data integrations
- **Rules:**
  - Implements domain interfaces
  - Contains all AI model interactions
  - Manages external API connections
- **Components:**
  - Gemini API client for content generation
  - T5 model handler for recipe creation
  - Trend data collectors (Google, News, YouTube)

### 4. App Layer (`app/`)

- **Purpose:** REST API endpoints for recipe system
- **Rules:**
  - FastAPI specific implementations
  - HTTP request/response handling
  - Authentication and rate limiting

## AI Integration Architecture

### 1. Multi-Model Strategy

```python
class AIModelFactory:
    def get_recipe_generator(self, model_type: str):
        if model_type == "gemini":
            return GeminiRecipeGenerator()
        elif model_type == "t5":
            return T5RecipeGenerator()
        else:
            return DefaultRecipeGenerator()
```

### 2. Prompt Engineering Pipeline

```python
class PromptBuilder:
    def build_recipe_prompt(self, user_segment: UserSegment,
                           trends: List[Trend]) -> str:
        base_prompt = self.get_segment_prompt(user_segment)
        trend_context = self.inject_trend_context(trends)
        return self.optimize_for_model(base_prompt + trend_context)
```

### 3. Quality Assurance Layer

- Content validation rules
- Recipe feasibility checks
- Trend relevance scoring
- Multi-language consistency

## Data Flow Architecture

### Recipe Generation Flow:

1. **Request** → App Layer (recipe generation endpoint)
2. **User Segmentation** → Application Layer (segment identification)
3. **Trend Analysis** → Domain Layer (trend scoring and selection)
4. **AI Generation** → Infrastructure Layer (Gemini/T5 API calls)
5. **Content Optimization** → Domain Layer (segment-specific optimization)
6. **Quality Validation** → Application Layer (feasibility and quality checks)
7. **Response** → App Layer (formatted recipe output)

### Trend Collection Flow:

1. **Scheduled Task** → Infrastructure Layer (trend collectors)
2. **Data Aggregation** → Domain Layer (trend analysis service)
3. **Scoring & Categorization** → Domain Layer (trend scoring algorithms)
4. **Storage** → Infrastructure Layer (database persistence)
5. **Cache Update** → Infrastructure Layer (Redis cache refresh)

## Technology Stack

### Core Technologies

- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **Redis**: Caching and session storage
- **Celery**: Background task processing

### AI/ML Stack

- **Google Gemini API**: Primary content generation
- **Hugging Face Transformers**: T5 model for recipes
- **NLTK/spaCy**: Natural language processing
- **scikit-learn**: User segmentation and trend analysis

### External APIs

- **Google Trends API**: Trend data collection
- **News API**: Current event trends
- **YouTube Data API**: Video trend analysis
- **Social Media APIs**: Trend discovery

## Performance Considerations

### 1. Caching Strategy

```python
# Multi-level caching
Level 1: In-memory (frequently used recipes)
Level 2: Redis (trend data, user segments)
Level 3: Database (persistent storage)
```

### 2. AI Model Optimization

- Model response caching
- Batch processing for bulk generation
- Fallback model strategy
- Response time monitoring

### 3. Scalability Patterns

- Horizontal scaling for API layer
- Async processing for AI calls
- Queue management for trend collection
- Database read replicas

## Security & Compliance

### 1. API Security

- Rate limiting per user segment
- API key rotation and management
- Input validation and sanitization
- Response filtering

### 2. Data Privacy

- User preference anonymization
- Trend data aggregation
- Recipe attribution handling
- GDPR compliance for EU users

## Monitoring & Analytics

### 1. Recipe Performance Metrics

- Generation success rate
- User engagement with recipes
- Trend prediction accuracy
- Model response times

### 2. Business Intelligence

- Popular ingredient trends
- Seasonal recipe patterns
- User segment preferences
- Content optimization effectiveness

This architecture supports the RCM_RECIPE system's core mission: generating personalized, trend-aware recipes through AI while maintaining clean separation of concerns and scalable design patterns.
