"""
Skills Extractor — извлечение навыков, проектов, опыта из текста
"""

import re
from typing import List, Dict, Any
from datetime import datetime


class SkillsExtractor:
    """Извлекает структурированные данные из текста резюме"""

    SKILLS_DB = {
        "python": ["python", "питон"],
        "machine learning": ["machine learning", "ml", "машинное обучение", "нейросети", "нейронные сети",
                             "data science"],
        "llm": ["llm", "large language model", "языковые модели", "gpt", "chatgpt", "claude"],
        "ai": ["ai", "ии", "искусственный интеллект"],
        "rag": ["rag", "retrieval"],
        "langchain": ["langchain"],
        "pytorch": ["pytorch", "torch"],
        "tensorflow": ["tensorflow", "tf"],
        "sql": ["sql", "базы данных", "postgresql", "mysql"],
        "docker": ["docker"],
        "kubernetes": ["kubernetes", "k8s"],
        "react": ["react", "react.js"],
        "javascript": ["javascript", "js"],
        "html": ["html", "css"],
        "api": ["api", "rest api"],
        "fastapi": ["fastapi"],
        "django": ["django"],
        "flask": ["flask"],
        "vibecoding": ["vibecode", "vibe coding", "vibe"],
        "cursor": ["cursor"],
        "copilot": ["copilot", "github copilot"],
        "ai_agent": ["ai-агент", "ai agent", "мульти-агент", "multi-agent"],
        "prompt_engineering": ["промпт", "prompt engineering", "промпт-инжиниринг"],
        "fullstack": ["fullstack", "full-stack", "full stack"],
        "devops": ["devops", "ci/cd", "деплой"],
        "business": ["бизнес", "воронки", "конверсии", "продукт", "управление", "ип"],
        "yolo": ["yolo", "fasterrcnn", "resnet"],
        "ar_vr": ["ar", "vr", "augmented reality", "virtual reality", "unity", "unreal"],
    }

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()

        skills = set()
        for skill, keywords in self.SKILLS_DB.items():
            for kw in keywords:
                if kw in text_lower:
                    skills.add(skill)
                    break

        experience = self._extract_experience(text)
        education = self._extract_education(text)
        projects = self._extract_projects(text)
        positions = self._extract_positions(text)
        name = self._extract_name(text)

        return {
            "name": name,
            "skills": list(skills),
            "experience_years": experience,
            "education": education,
            "projects": projects,
            "positions": positions,
            "raw_text": text[:2000]
        }

    def _extract_experience(self, text: str) -> float:
        patterns = [
            r'(\d+)\+?\s*лет',
            r'(\d+)\+?\s*года',
            r'опыт\s+работы\s*[:]*\s*(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return float(match.group(1))

        years_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|present|н\.в\.|настоящее время)'
        dates = re.findall(years_pattern, text.lower())
        if dates:
            total_years = 0
            for start, end in dates:
                start_year = int(start)
                end_year = datetime.now().year if end in ('present', 'н.в.', 'настоящее время') else int(end)
                total_years += end_year - start_year
            return total_years
        return 2.5

    def _extract_education(self, text: str) -> str:
        universities = ["вшэ", "мгу", "мфти", "спбгу", "итмо", "баумана", "сибирский федеральный", "terra ai"]
        for uni in universities:
            if uni in text.lower():
                return f"{uni.upper()}"
        return "Не указано"

    def _extract_projects(self, text: str) -> List[str]:
        lines = text.split('\n')
        projects = []
        for line in lines:
            line = line.strip()
            if re.match(r'(проект|project|разработал|создал|реализовал|внедрение|стажировка)', line, re.I):
                if len(line) > 10 and len(line) < 200:
                    projects.append(line[:100])
        return projects[:5]

    def _extract_positions(self, text: str) -> List[str]:
        positions = []
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(
                    r'(инженер|developer|аналитик|менеджер|manager|engineer|analyst|lead|senior|junior|разработчик)',
                    line, re.I):
                positions.append(line[:50])
        return positions[:3]

    def _extract_name(self, text: str) -> str:
        lines = text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 2 and len(line) < 50:
                if ' ' in line and not any(x in line.lower() for x in ['опыт', 'навыки', 'образование', 'работа']):
                    return line
        return "Кандидат"