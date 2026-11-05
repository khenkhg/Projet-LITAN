import { useTranslation } from 'react-i18next'

export default function EquipmentPage() {
  const { t } = useTranslation()
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">{t('equipment.title')}</h1>
      <p className="text-gray-500 italic">{t('common.loading')}</p>
    </div>
  )
}
