import { Header } from '@/components/Header';
import { Outlet } from 'react-router';

export function Boilerplate() {
    return (
        <div>
            <div>
                <Header />
            </div>
            <Outlet />
        </div>
    );
}