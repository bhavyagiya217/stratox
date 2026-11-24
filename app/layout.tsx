import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Stratox | Infrastructure Intelligence',
  description: 'Enterprise Cloud FinOps, DevSecOps, and Architecture Engine.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-[#0e0e11] text-[#ededed] antialiased">
        {children}
      </body>
    </html>
  )
}
