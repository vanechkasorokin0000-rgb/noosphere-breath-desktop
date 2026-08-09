#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Noosphere Breath - Breathing Practices Application
Entry point for the Tkinter version
"""

import sys
import os

# Добавляем корневую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.tkinter import TkinterApp
from ui.tkinter.pages import *


def main():
    app = TkinterApp()
    
    # Регистрация всех страниц
    app.register_page("StartPage", StartPage)
    app.register_page("SurveyStartPage", SurveyStartPage)
    app.register_page("SurveyResultPage", SurveyResultPage)
    app.register_page("CompanyPage", CompanyPage)
    app.register_page("BreathingTechniquesPage", BreathingTechniquesPage)
    app.register_page("BreathingTechniquesBeginnerPage", BreathingTechniquesBeginnerPage)
    app.register_page("BreathingTechniquesAdvancedPage", BreathingTechniquesAdvancedPage)
    
    # Wim Hof страницы
    app.register_page("WimHofBeginnerPage", BeginnerWimHofPage)
    app.register_page("WimHofBeginnerDescriptionPage", WimHofBeginnerDescriptionPage)
    app.register_page("WimHofBeginnerTimer", WimHofBeginnerTimer)
    app.register_page("WimHofAdvancedPage", AdvancedWimHofPage)
    app.register_page("WimHofAdvancedDescriptionPage", WimHofAdvancedDescriptionPage)
    app.register_page("WimHofAdvancedTimer", WimHofAdvancedTimer)
    
    # Pranayama страницы
    app.register_page("PranasBeginnerPage", BeginnerPranasPage)
    app.register_page("PranasBeginnerDescriptionPage", PranasBeginnerDescriptionPage)
    app.register_page("PranasAdvancedPage", AdvancedPranasPage)
    app.register_page("PranasAdvancedDescriptionPage", PranasAdvancedDescriptionPage)
    
    app.register_page("Prana1BeginnerPage", BeginnerPrana1Page)
    app.register_page("Prana1BeginnerDescriptionPage", Prana1BeginnerDescriptionPage)
    app.register_page("Prana1BeginnerTimer", Prana1BeginnerTimer)
    app.register_page("Prana1AdvancedPage", AdvancedPrana1Page)
    app.register_page("Prana1AdvancedDescriptionPage", Prana1AdvancedDescriptionPage)
    app.register_page("Prana1AdvancedTimer", Prana1AdvancedTimer)
    
    app.register_page("Prana2BeginnerPage", BeginnerPrana2Page)
    app.register_page("Prana2BeginnerDescriptionPage", Prana2BeginnerDescriptionPage)
    app.register_page("Prana2BeginnerTimer", Prana2BeginnerTimer)
    app.register_page("Prana2AdvancedPage", AdvancedPrana2Page)
    app.register_page("Prana2AdvancedDescriptionPage", Prana2AdvancedDescriptionPage)
    app.register_page("Prana2AdvancedTimer", Prana2AdvancedTimer)
    
    app.register_page("Prana3BeginnerPage", BeginnerPrana3Page)
    app.register_page("Prana3BeginnerDescriptionPage", Prana3BeginnerDescriptionPage)
    app.register_page("Prana3BeginnerTimer", Prana3BeginnerTimer)
    app.register_page("Prana3AdvancedPage", AdvancedPrana3Page)
    app.register_page("Prana3AdvancedDescriptionPage", Prana3AdvancedDescriptionPage)
    app.register_page("Prana3AdvancedTimer", Prana3AdvancedTimer)
    
    # Другие техники
    app.register_page("OtherTechniquesMainPage", OtherTechniquesMainPage)
    app.register_page("AddictionBattleTechniquePage", AddictionBattleTechniquePage)
    app.register_page("AddictionBattleDescriptionPage", AddictionBattleDescriptionPage)
    app.register_page("AddictionBattleTimerApp", AddictionBattleTimerApp)
    
    # Дневник
    app.register_page("DiaryStartPage", DiaryStartPage)
    app.register_page("DiaryViewPage", DiaryViewPage)
    app.register_page("DiaryAddPage", DiaryAddPage)
    app.register_page("DiaryEditPage", DiaryEditPage)
    app.register_page("DiaryStatisticsPage", DiaryStatisticsPage)
    
    # ==================== ДИНАМИЧЕСКИЕ СТРАНИЦЫ ОПРОСНИКА ====================
    # Используем lambda со значением по умолчанию для захвата индекса
    total_questions = app.controller.get_survey_questions_count()
    
    for i in range(total_questions):
        page_name = f"SurveyQuestion_{i+1}"
        
        # Способ 1: Используем lambda с параметром по умолчанию
        # Создаем класс с помощью type() и передаем индекс через замыкание
        DynamicClass = type(
            f"DynamicSurveyQuestionPage_{i}",
            (SurveyQuestionPage,),
            {
                '__init__': lambda self, parent, controller, bg_image, idx=i: 
                    SurveyQuestionPage.__init__(self, parent, controller, bg_image, idx)
            }
        )
        app.register_page(page_name, DynamicClass)
    
    # Запуск приложения
    app.run()


if __name__ == "__main__":
    main()
