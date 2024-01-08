import { axiosClient } from '@/services/axiosInstance';
import { Paths } from '@/technical/Paths';
import { dispatchLogin, dispatchLogout, registerCustomEvent, removeCustomEvent } from '@/technical/events';
import { isDef } from '@/technical/isDef';
import { ReactNode, createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { redirect } from 'react-router';

type User = {
    id: string,
    nickname: string,
}

type AuthContextValue = {
    user?: User | null
    logout: () => void
    login: () => void
    isLogged: boolean
}

const AuthContext = createContext<AuthContextValue>(Object.create(null));

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children?: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    const handleLogout = useCallback(() => {
        setUser(null);
    }, []);

    const handleLogin = useCallback(() => {
        axiosClient.get('/users/me')
            .then(({ data }) => {
                setUser(data);
                dispatchLogin();
                redirect('/');
            })
            .catch(() => redirect(Paths.AuthCallback));
    }, []);

    useEffect(() => {
        registerCustomEvent('logout', handleLogout);

        return () => removeCustomEvent('logout', handleLogout);
    }, [handleLogin, handleLogout]);

    useEffect(() => {
        handleLogin();
    }, [handleLogin]);

    const contextValue: AuthContextValue = useMemo(() => ({
        user: user,
        login: () => handleLogin(),
        logout: () => dispatchLogout(),
        isLogged: isDef(user),
    }), [handleLogin, user]);

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};