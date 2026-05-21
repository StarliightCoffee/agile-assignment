import React, { useEffect, useState } from 'react'
import { useUser } from '@/context/user-context'


import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarHeader,
    SidebarInset,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    useSidebar,
} from './ui/sidebar';

import { CalendarClockIcon, CarFrontIcon, HouseIcon, IdCardIcon, LogOutIcon, MoonIcon, Settings2Icon, ShieldCheckIcon, SunIcon, MenuIcon } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button'

type SidebarWrapperProps = {
  title?: string
  children?: React.ReactNode
}

const navigationItems = [
  { title: 'Home', href: '/home', icon: HouseIcon },
  { title: 'Membership', href: '/membership', icon: IdCardIcon },
  { title: 'Parking', href: '/parking', icon: CarFrontIcon },
  { title: 'Sessions', href: '/sessions', icon: CalendarClockIcon },
  { title: 'Account Options', href: '/account-options', icon: Settings2Icon },
  { title: 'Log Out', href: '/', icon: LogOutIcon },
]

export const SidebarWrapper: React.FC<SidebarWrapperProps> = ({
  title = 'Home',
  children,
}) => {
  const location = useLocation()
  const { toggleSidebar, open } = useSidebar()
  const { userId, clearUserId } = useUser()
  const [isDark, setIsDark] = useState(false)
  const [userName, setUserName] = useState('...')

  useEffect(() => {
    if (!userId) return
    fetch(`/api/db-api/get-user/${userId}`)
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(data => setUserName(data.name))
      .catch(() => setUserName('Unknown'))
  }, [userId])

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const shouldUseDark = savedTheme ? savedTheme === 'dark' : prefersDark

    document.documentElement.classList.toggle('dark', shouldUseDark)
    setIsDark(shouldUseDark)
  }, [])

  const toggleTheme = () => {
    setIsDark((currentValue) => {
      const nextValue = !currentValue
      document.documentElement.classList.toggle('dark', nextValue)
      localStorage.setItem('theme', nextValue ? 'dark' : 'light')
      return nextValue
    })
  }

  return (
        <div className="flex flex-row w-full">
          <Sidebar variant="floating" collapsible="icon" className="border-r border-sidebar-border h-screen">
            <SidebarHeader className="px-4 py-5 flex items-center justify-between">
              {open && (
                <div className="flex items-center gap-3">
                  <div className="flex size-9 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                    <ShieldCheckIcon className="size-5" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold tracking-tight">Agile Club</p>
                    <p className="text-xs text-sidebar-foreground/70">Member Portal</p>
                  </div>
                </div>
              )}
              <Button
                size="icon"
                variant="ghost"
                onClick={toggleSidebar}
                className="shrink-0"
                aria-label="Toggle sidebar"
              >
                <MenuIcon className="size-5" />
              </Button>
            </SidebarHeader>

            <SidebarContent>
              <SidebarGroup className="px-3 py-2">
                <SidebarMenu>
                  {navigationItems.map((item) => (
                    <SidebarMenuItem key={item.title}>
                      <SidebarMenuButton
                        render={<Link to={item.href} onClick={item.title === 'Log Out' ? clearUserId : undefined} />}
                        isActive={location.pathname === item.href}
                      >
                        <item.icon />
                        <span>{item.title}</span>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroup>
            </SidebarContent>

            <SidebarFooter className="border-t border-sidebar-border p-4">
              {open && (
                <div className="flex items-center gap-2">
                  <div className="flex-1 rounded-md bg-sidebar-accent/60 px-3 py-2">
                    <p className="text-xs text-sidebar-foreground/70">Signed in as</p>
                    <p className="text-sm font-medium">{userName}</p>
                  </div>
                  <Button
                    size="icon"
                    variant="outline"
                    aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
                    onClick={toggleTheme}
                    className="shrink-0 hover:cursor-pointer"
                  >
                    {isDark ? <SunIcon /> : <MoonIcon />}
                  </Button>
                </div>
              )}
            </SidebarFooter>
          </Sidebar>

          <SidebarInset className="min-h-svh w-full bg-background">
            <div className="flex min-h-svh flex-col w-full h-screen overflow-x-hidden">
              <header className="border-b border-border px-6 py-5">
                <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
              </header>
              <main className="min-h-0 flex-1 overflow-auto px-6 py-6">
                {children ?? (
                  <div className="rounded-xl border border-dashed border-border bg-muted/40 p-8 text-sm text-muted-foreground">
                    Main dashboard content goes here.
                  </div>
                )}
              </main>
            </div>
          </SidebarInset>
        </div>
      )
    }