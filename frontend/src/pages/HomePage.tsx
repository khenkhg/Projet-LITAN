import { useTranslation } from 'react-i18next'

export default function HomePage() {
  const { t } = useTranslation()
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      {/* Hero */}
      <section className="text-center mb-16">
        <h1 className="text-4xl font-bold text-primary-700 mb-4">{t('home.title')}</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">{t('home.subtitle')}</p>
      </section>
      {/* Latest news placeholder */}
      <section className="mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-semibold text-gray-900">{t('home.latestNews')}</h2>
          <a href="/actualites" className="text-primary-600 hover:underline text-sm">{t('home.viewAll')}</a>
        </div>
        <p className="text-gray-500 italic">{t('common.loading')}</p>
      </section>
      {/* Latest publications placeholder */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-semibold text-gray-900">{t('home.latestPublications')}</h2>
          <a href="/publications" className="text-primary-600 hover:underline text-sm">{t('home.viewAll')}</a>
        </div>
        <p className="text-gray-500 italic">{t('common.loading')}</p>
      </section>
    </div>
  )
}
