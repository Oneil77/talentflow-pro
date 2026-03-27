"""
Vacancy Parser — упрощённый парсинг вакансий
"""

import requests
import re
from typing import Dict, List


class VacancyParser:

    @staticmethod
    def get_vacancy_by_id(vacancy_id: str) -> Dict:
        """Получить вакансию по ID с hh.ru"""
        url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def clean_html(text: str) -> str:
        """Очищает HTML-теги из текста"""
        if not text:
            return ""
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean)
        return clean.lower()

    @staticmethod
    def extract_requirements(vacancy: Dict) -> Dict:
        """Извлекает требования из вакансии"""

        # Собираем весь текст
        description = vacancy.get("description", "")
        requirement_snippet = vacancy.get("snippet", {}).get("requirement", "")
        full_text = VacancyParser.clean_html(description + " " + requirement_snippet)

        # Список навыков для поиска (ключевые слова)
        skill_keywords = {
            "python": ["python"],
            "machine learning": ["machine learning", "машинное обучение", "ml", "нейросети", "нейронные сети"],
            "llm": ["llm", "large language model", "языковые модели", "gpt", "chatgpt", "claude"],
            "ai": ["ai", "ии", "искусственный интеллект"],
            "rag": ["rag", "retrieval"],
            "langchain": ["langchain"],
            "pytorch": ["pytorch", "torch"],
            "tensorflow": ["tensorflow", "tf"],
            "sql": ["sql", "базы данных"],
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "react": ["react"],
            "javascript": ["javascript", "js"],
            "html": ["html", "css"],
            "api": ["api", "rest api"],
            "fastapi": ["fastapi"],
            "django": ["django"],
            "flask": ["flask"],
            "vibecoding": ["vibecode", "vibe coding"],
            "cursor": ["cursor"],
            "copilot": ["copilot"],
            "ai_agent": ["ai-агент", "ai agent", "агентная система"],
            "prompt_engineering": ["промпт", "prompt engineering"],
            "fullstack": ["fullstack", "full-stack", "full stack"],
            "devops": ["devops", "ci/cd"],
            "business": ["бизнес", "воронки", "конверсии", "продукт"],
        }

        # Ищем навыки
        found_skills = []
        for skill, keywords in skill_keywords.items():
            for keyword in keywords:
                if keyword in full_text:
                    found_skills.append(skill)
                    break

        # Извлекаем опыт
        experience = 0
        exp_patterns = [
            r'опыт работы от (\d+) лет',
            r'опыт (\d+)[+\-]?\s*лет',
            r'от (\d+) лет',
            r'(\d+)\+ лет',
        ]
        for pattern in exp_patterns:
            match = re.search(pattern, full_text)
            if match:
                experience = int(match.group(1))
                break

        print(f"[DEBUG] Найдено навыков в вакансии: {found_skills}")  # для отладки
        print(f"[DEBUG] Найден опыт: {experience} лет")

        return {
            "skills": found_skills,
            "min_experience": experience,
        }