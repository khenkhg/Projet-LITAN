import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

export default function PendingApprovalPage() {
  const { t } = useTranslation()
  const { logout, isLoggingOut } = useAuth()

  return (
    <div className="max-w-lg mx-auto px-4 py-24 text-center">
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-8 shadow-sm">
        <div className="text-5xl mb-4">⏳</div>
        <h1 className="text-2xl font-semibold text-yellow-800 mb-3">{t('auth.pendingTitle')}</h1>
        <p className="text-yellow-700 mb-6 leading-relaxed">{t('auth.pendingMessage')}</p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            to="/"
            className="w-full sm:w-auto px-4 py-2 border border-yellow-300 text-yellow-800 rounded-lg hover:bg-yellow-100 transition-colors text-sm font-medium"
          >
            {t('common.back')}
          </Link>
          <button
            type="button"
            onClick={() => logout()}
            disabled={isLoggingOut}
            className="w-full sm:w-auto px-4 py-2 bg-yellow-700 text-white rounded-lg hover:bg-yellow-800 transition-colors text-sm font-medium disabled:opacity-50"
          >
            {t('nav.logout')}
          </button>
        </div>
      </div>
    </div>
  )
}
