import { Routes, Route } from 'react-router-dom'
import AppShell from '@/components/layout/AppShell'
import HomePage from '@/pages/HomePage'
import LaboratoryPage from '@/pages/LaboratoryPage'
import TeamsPage from '@/pages/TeamsPage'
import MembersPage from '@/pages/MembersPage'
import PublicationsPage from '@/pages/PublicationsPage'
import EquipmentPage from '@/pages/EquipmentPage'
import OffersPage from '@/pages/OffersPage'
import LinksPage from '@/pages/LinksPage'
import ContactPage from '@/pages/ContactPage'
import NotFoundPage from '@/pages/NotFoundPage'
import PendingApprovalPage from '@/pages/PendingApprovalPage'

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/laboratoire" element={<LaboratoryPage />} />
        <Route path="/equipes" element={<TeamsPage />} />
        <Route path="/membres" element={<MembersPage />} />
        <Route path="/publications" element={<PublicationsPage />} />
        <Route path="/equipements" element={<EquipmentPage />} />
        <Route path="/offres" element={<OffersPage />} />
        <Route path="/liens" element={<LinksPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/en-attente" element={<PendingApprovalPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AppShell>
  )
}
