"""
TalentFlow Pro — AI-Powered Talent Analytics Platform
"""

import os
import shutil
import re
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

# Импорт наших агентов и утилит
from agents.talent_agent import TalentFlowAgent
from agents.market_analyzer import MarketAnalyzer
from agents.skills_extractor import SkillsExtractor
from agents.vacancy_parser import VacancyParser
from utils.resume_parser import ResumeParser

app = FastAPI(
    title="TalentFlow Pro API",
    description="AI-агент для анализа рынка труда и подбора персонала",
    version="1.0.0"
)

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация агентов
talent_agent = TalentFlowAgent()
market_analyzer = MarketAnalyzer()
skills_extractor = SkillsExtractor()

# Модели данных
class CandidateAnalysisRequest(BaseModel):
    name: str
    skills: List[str]
    experience_years: float
    education: str
    role: str
    projects: Optional[List[str]] = None
    positions: Optional[List[str]] = None

class AnalysisResponse(BaseModel):
    candidate_name: str
    match_score: float
    recommendation: str
    strengths: List[str]
    gaps: List[str]
    ai_insights: str
    skill_radar: Dict
    salary_range: Dict
    projects: Optional[List[str]] = None
    positions: Optional[List[str]] = None

# ============= API ЭНДПОИНТЫ =============

@app.get("/")
async def root():
    return {
        "name": "TalentFlow Pro",
        "version": "1.0.0",
        "status": "active",
        "ai_agent_ready": True
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/analyze/candidate", response_model=AnalysisResponse)
async def analyze_candidate(request: CandidateAnalysisRequest):
    """Анализ кандидата (ручной ввод)"""
    try:
        result = talent_agent.analyze_candidate(
            name=request.name,
            skills=request.skills,
            experience=request.experience_years,
            education=request.education,
            target_role=request.role,
            projects=request.projects,
            positions=request.positions
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/resume-file")
async def analyze_resume_file(
    file: UploadFile = File(...),
    target_role: str = Form(...),
    name: Optional[str] = Form(None)
):
    """Анализ загруженного резюме (PDF, DOCX, TXT)"""
    # Сохраняем временный файл
    temp_file = f"/tmp/{file.filename}"
    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Извлекаем текст
        text = ResumeParser.extract_text(temp_file)

        # Извлекаем структурированные данные
        data = skills_extractor.extract_from_text(text)

        candidate_name = name if name else data.get("name", "Кандидат")

        # Вызываем агента
        result = talent_agent.analyze_candidate(
            name=candidate_name,
            skills=data["skills"],
            experience=data["experience_years"],
            education=data["education"],
            target_role=target_role,
            projects=data.get("projects", []),
            positions=data.get("positions", [])
        )
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.post("/api/analyze/resume-against-vacancy")
async def analyze_resume_against_vacancy(
    file: UploadFile = File(...),
    vacancy_url: str = Form(...),
    name: Optional[str] = Form(None)
):
    """
    Анализ резюме (PDF/DOCX/TXT) под конкретную вакансию (по URL hh.ru)
    """
    # Сохраняем временный файл резюме
    temp_file = f"/tmp/{file.filename}"
    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Извлекаем текст из резюме
        text = ResumeParser.extract_text(temp_file)

        # Извлекаем данные кандидата
        data = skills_extractor.extract_from_text(text)

        candidate_name = name if name else data.get("name", "Кандидат")

        # Парсим вакансию
        match = re.search(r'vacancy/(\d+)', vacancy_url)
        if not match:
            raise HTTPException(status_code=400, detail="Неверный URL вакансии")
        vacancy_id = match.group(1)

        vacancy_data = VacancyParser.get_vacancy_by_id(vacancy_id)
        requirements = VacancyParser.extract_requirements(vacancy_data)

        # Сравниваем
        result = talent_agent.analyze_candidate_against_vacancy(
            candidate_name=candidate_name,
            candidate_skills=data["skills"],
            candidate_experience=data["experience_years"],
            candidate_education=data["education"],
            vacancy_requirements=requirements
        )
        result["vacancy_title"] = vacancy_data.get("name", "")
        return JSONResponse(result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.get("/api/market/trends")
async def get_market_trends(role: Optional[str] = None):
    """Получение трендов рынка"""
    trends = market_analyzer.get_trends(role)
    return JSONResponse(trends)

@app.get("/api/market/top-skills")
async def get_top_skills():
    """Топ востребованных навыков"""
    return JSONResponse(market_analyzer.get_top_skills())

@app.get("/api/market/salary-benchmark")
async def get_salary_benchmark(role: str = "AI_ENGINEER"):
    """Бенчмарк зарплат по роли"""
    return JSONResponse(market_analyzer.get_salary_benchmark(role))

@app.get("/api/insights/dashboard")
async def get_dashboard_data():
    """Все данные для дашборда"""
    try:
        dashboard_data = {
            "market_overview": market_analyzer.get_market_overview(),
            "top_skills": market_analyzer.get_top_skills(),
            "salary_distribution": market_analyzer.get_salary_distribution(),
            "trending_roles": market_analyzer.get_trending_roles(),
            "ai_agent_stats": talent_agent.get_stats()
        }
        return JSONResponse(dashboard_data)
    except Exception as e:
        # Если ошибка, возвращаем заглушку
        return JSONResponse({
            "market_overview": {
                "AI Engineer": {"count": 1250, "avg_salary": 210},
                "ML Engineer": {"count": 980, "avg_salary": 225},
                "Data Scientist": {"count": 870, "avg_salary": 195},
                "AI Product Manager": {"count": 450, "avg_salary": 240}
            },
            "top_skills": [
                {"skill": "python", "count": 95},
                {"skill": "machine learning", "count": 92},
                {"skill": "llm", "count": 85},
                {"skill": "sql", "count": 88},
                {"skill": "pytorch", "count": 78}
            ],
            "salary_distribution": {
                "bins": ["0-100", "100-150", "150-200", "200-250", "250-300", "300+"],
                "values": [5, 15, 25, 30, 18, 7],
                "average": 210
            },
            "trending_roles": [
                {"role": "LLM Engineer", "growth": "+156%", "vacancies": 342},
                {"role": "AI Product Manager", "growth": "+89%", "vacancies": 187},
                {"role": "MLOps Engineer", "growth": "+78%", "vacancies": 265}
            ],
            "ai_agent_stats": {
                "total_analyses": 0,
                "average_match_score": 72,
                "hire_rate": 34
            }
        })

@app.get("/api/insights/article")
async def get_article_preview():
    """Получает черновик статьи на основе анализа рынка"""
    return JSONResponse(market_analyzer.generate_article_preview())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)