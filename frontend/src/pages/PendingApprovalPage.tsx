import { useTranslation } from 'react-i18next'

export default function PendingApprovalPage() {
  const { t } = useTranslation()
  return (
    <div className="max-w-lg mx-auto px-4 py-24 text-center">
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-8">
        <div className="text-5xl mb-4">⏳</div>
        <h1 className="text-2xl font-semibold text-yellow-800 mb-3">{t('auth.pendingTitle')}</h1>
        <p className="text-yellow-700">{t('auth.pendingMessage')}</p>
      </div>
    </div>
  )
}
