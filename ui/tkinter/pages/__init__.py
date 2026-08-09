"""
Pages package - все страницы приложения
"""

from .start_page import StartPage
from .survey_pages import SurveyStartPage, SurveyQuestionPage, SurveyResultPage
from .company_page import CompanyPage
from .breathing_pages import (
    BreathingTechniquesPage, 
    BreathingTechniquesBeginnerPage, 
    BreathingTechniquesAdvancedPage
)
from .wim_hof_pages import (
    BeginnerWimHofPage, 
    WimHofBeginnerDescriptionPage, 
    WimHofBeginnerTimer,
    AdvancedWimHofPage, 
    WimHofAdvancedDescriptionPage, 
    WimHofAdvancedTimer
)
from .pranayama_pages import (
    BeginnerPranasPage, 
    PranasBeginnerDescriptionPage,
    AdvancedPranasPage, 
    PranasAdvancedDescriptionPage,
    BeginnerPrana1Page, 
    Prana1BeginnerDescriptionPage, 
    Prana1BeginnerTimer,
    AdvancedPrana1Page, 
    Prana1AdvancedDescriptionPage, 
    Prana1AdvancedTimer,
    BeginnerPrana2Page, 
    Prana2BeginnerDescriptionPage, 
    Prana2BeginnerTimer,
    AdvancedPrana2Page, 
    Prana2AdvancedDescriptionPage, 
    Prana2AdvancedTimer,
    BeginnerPrana3Page, 
    Prana3BeginnerDescriptionPage, 
    Prana3BeginnerTimer,
    AdvancedPrana3Page, 
    Prana3AdvancedDescriptionPage, 
    Prana3AdvancedTimer
)
from .other_techniques_pages import (
    OtherTechniquesMainPage,
    AddictionBattleTechniquePage, 
    AddictionBattleDescriptionPage, 
    AddictionBattleTimerApp
)
from .diary_pages import (
    DiaryStartPage, 
    DiaryViewPage, 
    DiaryAddPage, 
    DiaryEditPage, 
    DiaryStatisticsPage
)

__all__ = [
    'StartPage',
    'SurveyStartPage', 'SurveyQuestionPage', 'SurveyResultPage',
    'CompanyPage',
    'BreathingTechniquesPage', 'BreathingTechniquesBeginnerPage', 'BreathingTechniquesAdvancedPage',
    'BeginnerWimHofPage', 'WimHofBeginnerDescriptionPage', 'WimHofBeginnerTimer',
    'AdvancedWimHofPage', 'WimHofAdvancedDescriptionPage', 'WimHofAdvancedTimer',
    'BeginnerPranasPage', 'PranasBeginnerDescriptionPage',
    'AdvancedPranasPage', 'PranasAdvancedDescriptionPage',
    'BeginnerPrana1Page', 'Prana1BeginnerDescriptionPage', 'Prana1BeginnerTimer',
    'AdvancedPrana1Page', 'Prana1AdvancedDescriptionPage', 'Prana1AdvancedTimer',
    'BeginnerPrana2Page', 'Prana2BeginnerDescriptionPage', 'Prana2BeginnerTimer',
    'AdvancedPrana2Page', 'Prana2AdvancedDescriptionPage', 'Prana2AdvancedTimer',
    'BeginnerPrana3Page', 'Prana3BeginnerDescriptionPage', 'Prana3BeginnerTimer',
    'AdvancedPrana3Page', 'Prana3AdvancedDescriptionPage', 'Prana3AdvancedTimer',
    'OtherTechniquesMainPage',
    'AddictionBattleTechniquePage', 'AddictionBattleDescriptionPage', 'AddictionBattleTimerApp',
    'DiaryStartPage', 'DiaryViewPage', 'DiaryAddPage', 'DiaryEditPage', 'DiaryStatisticsPage'
]
