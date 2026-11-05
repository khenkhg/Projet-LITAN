import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  const { t } = useTranslation()
  return (
    <div className="max-w-lg mx-auto px-4 py-24 text-center">
      <h1 className="text-6xl font-bold text-primary-700 mb-4">404</h1>
      <p className="text-xl text-gray-600 mb-8">{t('common.notFound')}</p>
      <Link
        to="/"
        className="px-6 py-3 bg-primary-600 text-white rounded hover:bg-primary-700 transition-colors"
      >
        {t('nav.home')}
      </Link>
    </div>
  )
}
