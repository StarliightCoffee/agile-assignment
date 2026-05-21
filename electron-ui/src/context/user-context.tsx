import React, { createContext, useContext, useState } from 'react'

type UserContextType = {
    userId: number | null
    setUserId: (id: number) => void
    clearUserId: () => void
}

const UserContext = createContext<UserContextType>({
    userId: null,
    setUserId: () => {},
    clearUserId: () => {},
})

export function UserProvider({ children }: { children: React.ReactNode }) {
    const [userId, setUserIdState] = useState<number | null>(() => {
        const stored = localStorage.getItem('userId')
        return stored ? Number(stored) : null
    })

    const setUserId = (id: number) => {
        localStorage.setItem('userId', String(id))
        setUserIdState(id)
    }

    const clearUserId = () => {
        localStorage.removeItem('userId')
        setUserIdState(null)
    }

    return (
        <UserContext.Provider value={{ userId, setUserId, clearUserId }}>
            {children}
        </UserContext.Provider>
    )
}

export const useUser = () => useContext(UserContext)
