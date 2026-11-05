/**
 * i18n configuration for LITAN.
 * - French is the active language for Phase 1.
 * - English locale file exists but is empty; add translations when Phase 2 begins.
 * - i18next-browser-languagedetector is wired up but will always fall back to 'fr'
 *   until English translations are populated.
 */
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

import frTranslation from './locales/fr/translation.json'
import enTranslation from './locales/en/translation.json'

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      fr: { translation: frTranslation },
      en: { translation: enTranslation },
    },
    fallbackLng: 'fr',
    lng: 'fr', // Phase 1: force French
    interpolation: {
      escapeValue: false, // React already escapes
    },
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
    },
  })

export default i18n
