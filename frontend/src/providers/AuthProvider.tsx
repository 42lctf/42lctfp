import { dispatchLogin, dispatchLogout, registerCustomEvent, removeCustomEvent } from "@/technical/events"
import { isDef } from "@/technical/isDef"
import { ReactNode, createContext, useCallback, useContext, useEffect, useMemo, useState } from "react"

type User = {
    id: number,
    name: string,
}

type AuthContextValue = {
    user?: User | null
    logout: () => void
    login: (user: string) => void
    isLogged: boolean
}

const AuthContext = createContext<AuthContextValue>(Object.create(null))

export const useAuth = () => useContext(AuthContext);

export const AuthProvider: React.FC<{ children?: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);

    const handleLogout = useCallback(() => {
        setUser(null);
    }, [])

    const handleLogin = useCallback(() => {
        console.log("AuthProvider - handleLogin")
    }, [])

    useEffect(() => {
        registerCustomEvent("logout", handleLogout);
        registerCustomEvent("login", handleLogin);

        return () => {
            removeCustomEvent("logout", handleLogout);
            removeCustomEvent("login", handleLogin)
        }
    }, [handleLogin, handleLogout])

    useEffect(() => {
        
    }, [])

    const contextValue: AuthContextValue = useMemo(() => ({
        user: user,
        login: () => dispatchLogin(),
        logout: () => dispatchLogout(),
        isLogged: isDef(user)
    }), [user])

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    )
}