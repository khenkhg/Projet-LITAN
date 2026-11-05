import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/hooks/useAuth'

/** Navigation items rendered both in the desktop bar and mobile drawer. */
const NAV_ITEMS = [
  { key: 'nav.home', path: '/' },
  { key: 'nav.laboratory', path: '/laboratoire' },
  { key: 'nav.teams', path: '/equipes' },
  { key: 'nav.members', path: '/membres' },
  { key: 'nav.publications', path: '/publications' },
  { key: 'nav.equipment', path: '/equipements' },
  { key: 'nav.offers', path: '/offres' },
  { key: 'nav.links', path: '/liens' },
  { key: 'nav.contact', path: '/contact' },
] as const

export default function Header() {
  const { t } = useTranslation()
  const { user, isAuthenticated, isPending, logout, isLoggingOut } = useAuth()
  const [mobileOpen, setMobileOpen] = useState(false)

  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded text-sm font-medium transition-colors ${
      isActive
        ? 'bg-primary-700 text-white'
        : 'text-gray-700 hover:bg-primary-50 hover:text-primary-700'
    }`

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & lab name */}
          <Link to="/" className="flex items-center gap-3 shrink-0">
            <div className="w-9 h-9 bg-primary-700 rounded flex items-center justify-center">
              <span className="text-white font-bold text-sm">L</span>
            </div>
            <span className="font-semibold text-gray-900 hidden sm:block">
              Laboratoire LITAN
            </span>
          </Link>

          {/* Desktop navigation */}
          <nav
            aria-label="Navigation principale"
            className="hidden lg:flex items-center gap-1 overflow-x-auto"
          >
            {NAV_ITEMS.map(({ key, path }) => (
              <NavLink key={path} to={path} className={navLinkClass} end={path === '/'}>
                {t(key)}
              </NavLink>
            ))}
          </nav>

          {/* Auth controls */}
          <div className="hidden lg:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                {isPending ? (
                  <Link
                    to="/en-attente"
                    className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 hover:bg-yellow-200 transition-colors"
                  >
                    ⏳ {t('auth.pendingBadge')}
                  </Link>
                ) : (
                  <span className="text-sm font-medium text-gray-700 truncate max-w-[150px]">
                    {user.first_name || user.email}
                  </span>
                )}
                <button
                  type="button"
                  onClick={() => logout()}
                  disabled={isLoggingOut}
                  className="px-3 py-1.5 border border-gray-300 text-gray-700 text-xs font-medium rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  {t('nav.logout')}
                </button>
              </div>
            ) : (
              <a
                href="/accounts/google/login/"
                className="px-4 py-2 bg-primary-600 text-white text-sm font-medium rounded hover:bg-primary-700 transition-colors flex items-center gap-2"
              >
                <span>{t('auth.loginWithGoogle')}</span>
              </a>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            type="button"
            aria-label={mobileOpen ? t('nav.closeMenu') : t('nav.openMenu')}
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
            onClick={() => setMobileOpen(!mobileOpen)}
            className="lg:hidden p-2 rounded text-gray-600 hover:bg-gray-100"
          >
            {mobileOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <nav
          id="mobile-menu"
          aria-label="Navigation mobile"
          className="lg:hidden border-t border-gray-200 bg-white"
        >
          <div className="px-4 py-3 flex flex-col gap-1">
            {NAV_ITEMS.map(({ key, path }) => (
              <NavLink
                key={path}
                to={path}
                className={navLinkClass}
                end={path === '/'}
                onClick={() => setMobileOpen(false)}
              >
                {t(key)}
              </NavLink>
            ))}
            <div className="pt-3 border-t border-gray-100 mt-2">
              {isAuthenticated ? (
                <div className="flex flex-col gap-2">
                  <div className="text-sm font-medium text-gray-700 px-3">
                    {user.full_name || user.email}
                    {isPending && (
                      <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs bg-yellow-100 text-yellow-800">
                        {t('auth.pendingBadge')}
                      </span>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setMobileOpen(false)
                      logout()
                    }}
                    className="w-full text-left px-3 py-2 text-sm text-red-600 font-medium hover:bg-red-50 rounded"
                  >
                    {t('nav.logout')}
                  </button>
                </div>
              ) : (
                <a
                  href="/accounts/google/login/"
                  className="block px-3 py-2 bg-primary-600 text-white text-sm font-medium rounded text-center"
                >
                  {t('auth.loginWithGoogle')}
                </a>
              )}
            </div>
          </div>
        </nav>
      )}
    </header>
  )
}
