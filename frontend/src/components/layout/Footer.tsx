import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'

export default function Footer() {
  const { t } = useTranslation()
  const year = new Date().getFullYear()

  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Lab identity */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 bg-primary-500 rounded flex items-center justify-center">
                <span className="text-white font-bold text-sm">L</span>
              </div>
              <span className="text-white font-semibold">Laboratoire LITAN</span>
            </div>
            <p className="text-sm">{t('footer.address')}</p>
          </div>

          {/* Quick links */}
          <div>
            <h3 className="text-white font-medium mb-3 text-sm uppercase tracking-wider">
              Navigation rapide
            </h3>
            <ul className="space-y-1 text-sm">
              {[
                { label: t('nav.laboratory'), path: '/laboratoire' },
                { label: t('nav.teams'), path: '/equipes' },
                { label: t('nav.publications'), path: '/publications' },
                { label: t('nav.offers'), path: '/offres' },
                { label: t('nav.contact'), path: '/contact' },
              ].map(({ label, path }) => (
                <li key={path}>
                  <Link to={path} className="hover:text-white transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-medium mb-3 text-sm uppercase tracking-wider">
              {t('contact.title')}
            </h3>
            <address className="not-italic text-sm space-y-1">
              <p>ESTIN, Béjaïa 06000, Algérie</p>
              <p>
                <a href="mailto:litan@estin.dz" className="hover:text-white transition-colors">
                  litan@estin.dz
                </a>
              </p>
            </address>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-6 text-xs text-gray-500 text-center">
          {t('footer.rights', { year })}
        </div>
      </div>
    </footer>
  )
}
