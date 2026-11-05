import type { ReactNode } from 'react'
import Header from './Header'
import Footer from './Footer'

interface AppShellProps {
  children: ReactNode
}

/**
 * AppShell wraps every page with the persistent Header and Footer.
 * The main element grows to fill remaining vertical space (flex-col min-h-screen).
 */
export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Accessibility: skip navigation for keyboard users */}
      <a href="#main-content" className="skip-link">
        Aller au contenu principal
      </a>
      <Header />
      <main id="main-content" className="flex-1">
        {children}
      </main>
      <Footer />
    </div>
  )
}
