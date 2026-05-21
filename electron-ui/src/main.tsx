import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter, Route, Routes } from 'react-router-dom'
import Home from '../src/pages/Home.tsx';
import './index.css'
import { SidebarProvider } from './components/ui/sidebar.tsx'
import Authenticate from './App.tsx'
import AccountOptions from './pages/AccountOptions.tsx'
import Sessions from './pages/Sessions.tsx'
import Membership from './pages/Membership.tsx';
import Parking from './pages/Parking.tsx';
import { UserProvider } from './context/user-context.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <UserProvider>
      <HashRouter>
        <SidebarProvider>
          <Routes>
            <Route path="/" element={<Authenticate />} />
            <Route path="/membership" element={<Membership />} />
            <Route path="/home" element={<Home />} />
            <Route path="/parking" element={<Parking />} />
            <Route path="/sessions" element={<Sessions />} />
            <Route path="/account-options" element={<AccountOptions />} />
          </Routes>
        </SidebarProvider>
      </HashRouter>
    </UserProvider>
  </React.StrictMode>,
)

// Only available when running inside Electron with preload bridge.
window.ipcRenderer?.on('main-process-message', (_event, message) => {
  console.log(message)
})
