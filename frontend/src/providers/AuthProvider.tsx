import { axiosClient } from '@/services/axiosInstance';
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

    const handleLogin = useCallback(async () => {
        const { data }: { data: User } = await axiosClient.get('/users/me');
        setUser(data);
        redirect('/');
    }, []);

    useEffect(() => {
        registerCustomEvent('logout', handleLogout);
        registerCustomEvent('login', handleLogin);

        return () => {
            removeCustomEvent('logout', handleLogout);
            removeCustomEvent('login', handleLogin);
        };
    }, [handleLogin, handleLogout]);

    useEffect(() => {
        //onEntry -> authorize ? -> handleLogin
        dispatchLogin();
    }, []);

    const contextValue: AuthContextValue = useMemo(() => ({
        user: user,
        login: () => dispatchLogin(),
        logout: () => dispatchLogout(),
        isLogged: isDef(user),
    }), [user]);

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};