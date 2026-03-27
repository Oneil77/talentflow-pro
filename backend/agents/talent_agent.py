"""
TalentFlow AI Agent — расширенная аналитика
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

class TalentFlowAgent:
    def __init__(self):
        self.analyses_history = []

    def analyze_candidate(self,
                          name: str,
                          skills: List[str],
                          experience: float,
                          education: str,
                          target_role: str,
                          projects: Optional[List[str]] = None,
                          positions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Анализирует кандидата, используя все доступные данные
        """
        skills_lower = [s.lower() for s in skills]

        # Требования к ролям
        requirements = {
            "AI_ENGINEER": {
                "core": ["python", "machine learning", "pytorch", "tensorflow"],
                "nice": ["llm", "rag", "langchain", "docker", "kubernetes"],
                "weight_projects": 0.1,
                "weight_positions": 0.05,
                "min_experience": 2.0
            },
            "FINTECH_MANAGER": {
                "core": ["financial modeling", "risk management", "sql"],
                "nice": ["python", "machine learning", "product management"],
                "weight_projects": 0.15,
                "weight_positions": 0.1,
                "min_experience": 2.5
            },
            "PRODUCT_MANAGER": {
                "core": ["product management", "agile", "analytics"],
                "nice": ["sql", "python", "user research"],
                "weight_projects": 0.2,
                "weight_positions": 0.15,
                "min_experience": 2.0
            }
        }

        role_key = target_role.upper()
        req = requirements.get(role_key, requirements["AI_ENGINEER"])

        # Базовый скор по навыкам
        core_matched = sum(1 for s in req["core"] if s in skills_lower)
        core_score = (core_matched / len(req["core"])) * 100 if req["core"] else 0

        nice_matched = sum(1 for s in req["nice"] if s in skills_lower)
        nice_score = (nice_matched / len(req["nice"])) * 100 if req["nice"] else 0

        skill_score = (core_score * 0.7) + (nice_score * 0.3)

        # Опыт
        exp_factor = min(1.0, experience / req["min_experience"])
        # Проекты
        project_score = 0
        if projects:
            relevant_projects = sum(1 for p in projects if any(skill in p.lower() for skill in skills_lower))
            project_score = min(1.0, relevant_projects / max(1, len(projects))) * 100

        # Должности
        position_score = 0
        if positions:
            role_keywords = role_key.lower().replace('_', ' ')
            if any(role_keywords in pos.lower() for pos in positions):
                position_score = 80
            elif any(word in pos.lower() for word in ['engineer', 'developer', 'analyst'] for pos in positions):
                position_score = 50

        # Итоговый скор
        final_score = (skill_score * 0.6 +
                       exp_factor * 100 * 0.2 +
                       project_score * 0.15 +
                       position_score * 0.05)

        # Сильные стороны
        strengths = []
        for s in req["core"]:
            if s in skills_lower:
                strengths.append(f"Экспертный уровень в {s.title()}")
        if project_score > 70:
            strengths.append("Участвовал в релевантных проектах")
        if position_score > 70:
            strengths.append("Опыт работы на схожей позиции")

        # Gaps
        gaps = []
        for s in req["core"]:
            if s not in skills_lower:
                gaps.append(f"Критический gap: {s.title()}")
        for s in req["nice"][:2]:
            if s not in skills_lower:
                gaps.append(f"Желательно изучить: {s.title()}")
        if experience < req["min_experience"]:
            gaps.append(f"Недостаточно опыта (нужно {req['min_experience']} лет)")

        # Рекомендация
        if final_score >= 70:
            recommendation = "✅ Рекомендуется к найму (HIRE)"
        elif final_score >= 50:
            recommendation = "📋 Рекомендуется собеседование (INTERVIEW)"
        elif final_score >= 35:
            recommendation = "📚 Рассмотреть на junior позицию с обучением"
        else:
            recommendation = "⏸️ Не соответствует требованиям (REJECT)"

        # Инсайты
        insights = []
        if projects:
            insights.append("Проекты: " + "; ".join(projects[:2]))
        if "llm" in skills_lower:
            insights.append("Владение LLM — ключевой тренд 2026 года.")
        if position_score > 70:
            insights.append("Опыт работы на схожей позиции — большой плюс.")
        if not insights:
            insights.append("Кандидат имеет потенциал для развития в выбранной роли.")

        # Радар
        radar = self._generate_radar_data(skills_lower, role_key)

        # Зарплата
        salary = self._estimate_salary(target_role, experience, final_score)

        result = {
            "candidate_name": name,
            "match_score": round(final_score, 1),
            "recommendation": recommendation,
            "strengths": strengths[:4],
            "gaps": gaps[:4],
            "ai_insights": " ".join(insights),
            "skill_radar": radar,
            "salary_range": salary,
            "experience_years": experience,
            "education": education,
            "target_role": target_role,
            "analysis_timestamp": datetime.now().isoformat(),
            "projects": projects[:3] if projects else [],
            "positions": positions[:2] if positions else []
        }

        self.analyses_history.append(result)
        return result

    def analyze_candidate_against_vacancy(self,
                                          candidate_name: str,
                                          candidate_skills: List[str],
                                          candidate_experience: float,
                                          candidate_education: str,
                                          vacancy_requirements: Dict) -> Dict:
        """
        Анализирует кандидата относительно требований вакансии
        """
        required_skills = vacancy_requirements.get("skills", [])
        min_exp = vacancy_requirements.get("min_experience", 0)

        # Сравниваем навыки (регистронезависимо)
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]

        matched = sum(1 for s in required_skills_lower if s in candidate_skills_lower)
        skill_score = (matched / max(1, len(required_skills))) * 100

        # Опыт
        if min_exp > 0:
            exp_score = min(100, (candidate_experience / min_exp) * 100)
        else:
            exp_score = 70  # если не указан опыт

        final_score = (skill_score * 0.7) + (exp_score * 0.3)

        strengths = []
        gaps = []
        for skill in required_skills:
            if skill.lower() in candidate_skills_lower:
                strengths.append(f"Владение {skill}")
            else:
                gaps.append(f"Требуется {skill}")

        if candidate_experience < min_exp and min_exp > 0:
            gaps.append(f"Недостаточно опыта (нужно {min_exp} лет)")

        if final_score >= 70:
            recommendation = "✅ Рекомендуется к найму (HIRE)"
        elif final_score >= 50:
            recommendation = "📋 Рекомендуется собеседование (INTERVIEW)"
        elif final_score >= 35:
            recommendation = "📚 Рассмотреть на junior позицию с обучением"
        else:
            recommendation = "⏸️ Не соответствует требованиям (REJECT)"

        ai_insights = f"Найдено {matched} из {len(required_skills)} требуемых навыков. Требуемый опыт: {min_exp} лет."

        return {
            "candidate_name": candidate_name,
            "match_score": round(final_score, 1),
            "recommendation": recommendation,
            "strengths": strengths[:5],
            "gaps": gaps[:5],
            "ai_insights": ai_insights,
            "skill_radar": self._generate_radar_data(candidate_skills, "CUSTOM"),
            "salary_range": self._estimate_salary("CUSTOM", candidate_experience, final_score),
            "vacancy_requirements": vacancy_requirements
        }

    def _generate_radar_data(self, skills: List[str], role: str) -> Dict:
        """Генерирует данные для radar chart"""
        tech_skills = ["python", "docker", "kubernetes", "java", "c++"]
        business_skills = ["product management", "agile", "scrum"]
        ai_skills = ["machine learning", "llm", "pytorch", "tensorflow", "nlp"]
        data_skills = ["sql", "pandas", "spark", "tableau"]

        technical_score = min(100, sum(20 for s in skills if s in tech_skills))
        business_score = min(100, sum(25 for s in skills if s in business_skills))
        ai_ml_score = min(100, sum(20 for s in skills if s in ai_skills))
        data_score = min(100, sum(20 for s in skills if s in data_skills))

        return {
            "categories": ["Technical", "Business", "AI/ML", "Data", "Soft Skills"],
            "values": [technical_score, business_score, ai_ml_score, data_score, 70]
        }

    def _estimate_salary(self, role: str, experience: float, match_score: float) -> Dict:
        """Оценивает зарплатную вилку"""
        base_salaries = {
            "AI_ENGINEER": (120, 250),
            "FINTECH_MANAGER": (150, 280),
            "PRODUCT_MANAGER": (130, 260),
            "CUSTOM": (100, 200)
        }
        min_salary, max_salary = base_salaries.get(role, (100, 200))
        exp_factor = min(1.2, 0.8 + experience / 10)
        score_factor = 0.7 + (match_score / 100) * 0.6
        adjusted_min = int(min_salary * exp_factor * score_factor)
        adjusted_max = int(max_salary * exp_factor * score_factor)
        return {"min": adjusted_min, "max": adjusted_max, "currency": "тыс. руб./год", "percentile_50": (adjusted_min + adjusted_max) // 2}

    def get_stats(self) -> Dict:
        if not self.analyses_history:
            return {"total_analyses": 0}
        scores = [a["match_score"] for a in self.analyses_history]
        return {
            "total_analyses": len(self.analyses_history),
            "average_match_score": round(sum(scores) / len(scores), 1),
            "hire_rate": round(sum(1 for a in self.analyses_history if "HIRE" in a["recommendation"]) / len(self.analyses_history) * 100, 1)
        }