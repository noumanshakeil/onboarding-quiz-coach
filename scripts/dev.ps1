# Dev server for onboarding-quiz-coach
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
