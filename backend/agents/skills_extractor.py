"""
Skills Extractor — умное извлечение навыков, проектов, опыта из текста
"""

import re
from typing import List, Dict, Any
from datetime import datetime


class SkillsExtractor:
    """Извлекает структурированные данные из текста резюме"""

    # Расширенный словарь навыков (можно добавлять)
    SKILLS_DB = {
        # Языки программирования
        "python": ["python", "питон", "django", "flask"],
        "java": ["java", "spring", "kotlin"],
        "javascript": ["javascript", "js", "node.js", "nodejs", "react", "vue", "angular"],
        "typescript": ["typescript", "ts"],
        "c++": ["c++", "cpp", "c plus plus"],
        "c#": ["c#", "c sharp"],
        "go": ["go", "golang"],
        "rust": ["rust"],
        "php": ["php"],
        "ruby": ["ruby", "rails"],
        "sql": ["sql", "postgresql", "mysql", "oracle", "базы данных"],

        # ML/AI
        "machine learning": ["machine learning", "ml", "машинное обучение", "нейросети", "нейронные сети"],
        "deep learning": ["deep learning", "dl", "глубокое обучение"],
        "llm": ["llm", "large language model", "языковые модели", "gpt", "chatgpt", "claude", "bert"],
        "rag": ["rag", "retrieval augmented"],
        "langchain": ["langchain", "lang chain"],
        "pytorch": ["pytorch", "torch"],
        "tensorflow": ["tensorflow", "tf"],
        "keras": ["keras"],
        "scikit-learn": ["scikit-learn", "sklearn"],
        "transformers": ["transformers", "huggingface"],
        "computer vision": ["computer vision", "cv", "компьютерное зрение"],
        "nlp": ["nlp", "natural language processing", "обработка текста"],

        # Data
        "pandas": ["pandas"],
        "numpy": ["numpy"],
        "spark": ["spark", "pyspark"],
        "airflow": ["airflow"],
        "tableau": ["tableau"],
        "power bi": ["power bi"],

        # DevOps/Cloud
        "docker": ["docker"],
        "kubernetes": ["kubernetes", "k8s"],
        "aws": ["aws", "amazon web services"],
        "gcp": ["gcp", "google cloud"],
        "azure": ["azure"],
        "terraform": ["terraform"],
        "ci/cd": ["ci/cd", "jenkins", "gitlab ci", "github actions"],

        # Frontend
        "react": ["react", "react.js"],
        "vue": ["vue", "vue.js"],
        "angular": ["angular"],
        "html": ["html", "css"],

        # Backend
        "fastapi": ["fastapi"],
        "flask": ["flask"],
        "django": ["django"],
        "api": ["api", "rest api", "graphql"],

        # Business
        "product management": ["product management", "продукт", "pm"],
        "agile": ["agile", "scrum", "kanban"],
        "project management": ["project management", "управление проектами"],
        "risk management": ["risk management", "управление рисками"],
        "financial modeling": ["financial modeling", "финансовое моделирование"],

        # AI Tools
        "cursor": ["cursor"],
        "claude": ["claude", "claude code"],
        "copilot": ["copilot", "github copilot"],
        "vibecoding": ["vibecode", "vibe coding"],
        "ai agent": ["ai agent", "ai-агент", "multi-agent"],
        "prompt engineering": ["prompt engineering", "промпт-инжиниринг"],

        # Soft Skills
        "teamwork": ["teamwork", "работа в команде"],
        "leadership": ["leadership", "лидерство"],
        "communication": ["communication", "коммуникация"],
        "problem solving": ["problem solving", "решение проблем"],
<<<<<<< HEAD

=======
        
>>>>>>> 34e7c326be1c27cf8154ffefdbe92240341e847c
        # Доп
        "vibecoding": ["vibecode", "vibe coding", "vibe"],
        "cursor": ["cursor"],
        "claude": ["claude", "claude code", "chatgpt"],
        "copilot": ["copilot", "github copilot"],
        "ai_agent": ["ai-агент", "ai agent", "мульти-агент", "multi-agent"],
        "prompt_engineering": ["промпт", "prompt engineering"],
        "langchain": ["langchain", "lang chain"],
        "rag": ["rag", "retrieval augmented"],
        "genetic_algorithms": ["genetic algorithms", "генетические алгоритмы"],
        "unity": ["unity", "unreal engine"],
        "yolo": ["yolo", "yolov8", "fasterrcnn", "resnet"],
        "ar_vr": ["ar", "vr", "augmented reality", "virtual reality"],
        "business_management": ["ип", "предприниматель", "бизнес-процессы", "управление"],
        "neural_networks": ["нейронные сети", "neural networks", "нейросети"],
    }

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """Извлекает все навыки из текста"""
        text_lower = text.lower()

        # Извлекаем навыки
        skills = set()
        for skill, keywords in self.SKILLS_DB.items():
            for kw in keywords:
                if kw in text_lower:
                    skills.add(skill)
                    break

        # Опыт
        experience = self._extract_experience(text)

        # Образование
        education = self._extract_education(text)

        # Проекты
        projects = self._extract_projects(text)

        # Должности
        positions = self._extract_positions(text)

        # Имя
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
        """Извлекает опыт работы в годах"""
        patterns = [
            r'(\d+)\+?\s*лет',
            r'(\d+)\+?\s*года',
            r'опыт\s+работы\s*[:]*\s*(\d+)',
            r'experience\s*[:]*\s*(\d+)\+?\s*years',
            r'общий стаж\s*[:]*\s*(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return float(match.group(1))

        # Поиск по датам
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
        """Извлекает образование"""
        universities = ["вшэ", "мгу", "мфти", "спбгу", "итмо", "баумана", "мифи", "сибирский федеральный"]
        for uni in universities:
            if uni in text.lower():
                return f"{uni.upper()}"
        return "Не указано"

    def _extract_projects(self, text: str) -> List[str]:
        """Извлекает проекты"""
        lines = text.split('\n')
        projects = []
        for line in lines:
            line = line.strip()
            if re.match(r'(проект|project|разработал|создал|реализовал|внедрение|стажировка)', line, re.I):
                if len(line) > 10 and len(line) < 200:
                    projects.append(line[:100])
        return projects[:5]

    def _extract_positions(self, text: str) -> List[str]:
        """Извлекает должности"""
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
        """Извлекает имя (упрощённо)"""
        lines = text.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 2 and len(line) < 50:
                if ' ' in line and not any(x in line.lower() for x in ['опыт', 'навыки', 'образование', 'работа']):
                    return line
        return "Кандидат"
