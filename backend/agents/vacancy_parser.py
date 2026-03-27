"""
Vacancy Parser — умный парсинг вакансий с hh.ru
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
        return clean.strip()

    @staticmethod
    def extract_requirements(vacancy: Dict) -> Dict:
        """
        Умное извлечение требований из вакансии
        """
        # Собираем весь текст
        description = vacancy.get("description", "")
        requirement_snippet = vacancy.get("snippet", {}).get("requirement", "")
        full_text = VacancyParser.clean_html(description + " " + requirement_snippet).lower()

        # ========== ИЗВЛЕЧЕНИЕ НАВЫКОВ ==========
        # Все возможные навыки (большой словарь)
        all_skills = {
            "python": ["python", "питон", "django", "flask"],
            "javascript": ["javascript", "js", "node.js", "react", "vue", "angular"],
            "typescript": ["typescript", "ts"],
            "java": ["java", "spring"],
            "c++": ["c++", "cpp"],
            "c#": ["c#", "c sharp"],
            "go": ["go", "golang"],
            "rust": ["rust"],
            "php": ["php"],
            "sql": ["sql", "postgresql", "mysql", "oracle"],
            "machine learning": ["machine learning", "ml", "машинное обучение", "нейросети", "нейронные сети",
                                 "data science"],
            "llm": ["llm", "large language model", "языковые модели", "gpt", "chatgpt", "claude", "bert"],
            "rag": ["rag", "retrieval augmented"],
            "langchain": ["langchain", "lang chain"],
            "pytorch": ["pytorch", "torch"],
            "tensorflow": ["tensorflow", "tf"],
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "aws": ["aws", "amazon web services", "ec2", "s3"],
            "gcp": ["gcp", "google cloud"],
            "azure": ["azure"],
            "react": ["react", "react.js"],
            "vue": ["vue", "vue.js"],
            "angular": ["angular"],
            "html": ["html", "css"],
            "fastapi": ["fastapi"],
            "django": ["django"],
            "flask": ["flask"],
            "api": ["api", "rest api", "graphql"],
            "product management": ["product management", "продукт", "pm"],
            "agile": ["agile", "scrum", "kanban"],
            "devops": ["devops", "ci/cd", "jenkins"],
            "cursor": ["cursor"],
            "claude": ["claude", "claude code"],
            "copilot": ["copilot", "github copilot"],
            "vibecoding": ["vibecode", "vibe coding"],
            "ai_agent": ["ai agent", "ai-агент", "multi-agent"],
            "prompt_engineering": ["prompt engineering", "промпт-инжиниринг"],
            "vibecoding": ["vibecode", "vibe coding", "vibe"],
            "cursor": ["cursor"],
            "claude": ["claude", "claude code"],
            "copilot": ["copilot", "github copilot"],
            "ai_agent": ["ai-агент", "ai agent", "мульти-агент", "multi-agent", "агентная система"],
            "prompt_engineering": ["промпт", "prompt engineering", "промпт-инжиниринг"],
            "langchain": ["langchain", "lang chain"],
            "rag": ["rag", "retrieval augmented"],
            "product_management": ["product management", "продукт", "pm", "управление продуктом"],
            "business_thinking": ["бизнес-мышление", "business thinking", "бизнес-процессы"],
            "fullstack": ["fullstack", "full-stack", "full stack"],
            "fastapi": ["fastapi"],
            "sql": ["sql", "базы данных"],
            "api": ["api", "rest api"],
            "business_thinking": ["бизнес-мышление", "business thinking", "бизнес-процессы", "воронки", "конверсии"],
            "self_management": ["самостоятельность", "сам декомпозируешь", "без промежуточных менеджеров"],
            "devops": ["devops", "ci/cd", "деплой"],
        }

        found_skills = set()
        for skill, keywords in all_skills.items():
            for kw in keywords:
                if kw in full_text:
                    found_skills.add(skill)
                    break

        # Специальные проверки
        if "ai" in full_text or "ии" in full_text or "искусственный интеллект" in full_text:
            found_skills.add("ai")
        if "нейросет" in full_text:
            found_skills.add("machine learning")

        # ========== ИЗВЛЕЧЕНИЕ ОПЫТА ==========
        experience = 0
        exp_patterns = [
            r'опыт работы от (\d+) лет',
            r'опыт (\d+)[+\-]?\s*лет',
            r'experience (\d+)\+?\s*years',
            r'требуемый опыт (\d+)',
            r'от (\d+) лет',
            r'(\d+)\+ лет',
        ]
        for pattern in exp_patterns:
            match = re.search(pattern, full_text)
            if match:
                experience = int(match.group(1))
                break

        # Проверка на диапазон
        range_match = re.search(r'(\d+)\s*[-–]\s*(\d+)\s*лет', full_text)
        if range_match and experience == 0:
            experience = int(range_match.group(1))

        return {
            "skills": list(found_skills),
            "min_experience": experience,
            "raw_text": full_text[:1000]
        }
