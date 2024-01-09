import { Login } from './Login';
import { HomePage } from './HomePage';
import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';

export function Home() {

    const [nickname, setNickname] = useState('');


    useEffect(() => {
        const url = '/api/v1/users/me';
        fetch(url, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                credentials: 'include',
            },
        })
            .then(async (response) => {
                if (response.status === 200) {
                    setNickname((await response.json()).nickname);
                }
            })
            .catch((error) => {
                console.log('ERROR: ', error);
            });
    }, []);

    return (
        <div>
            {nickname.length > 0 ? <HomePage nickname={nickname} /> : <Login />}
        </div>
    );
}