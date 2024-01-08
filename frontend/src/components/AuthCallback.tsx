import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

export function AuthCallback() {
    const code = window.location.href.split("code=")[1];
    const renderAfterCalled = useRef(false);

    const navigate = useNavigate();

    useEffect(() => {
        if (!renderAfterCalled.current) {
            fetch(`/api/v1/users/auth/callback?code=${code}`, {
                method: "GET",
                headers: {
                    "accept": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                // TODO fix this shit if the response is not 200;
                Cookies.set("access_token", data.access_token);
                Cookies.set("refresh_token", data.refresh_token);
                navigate("/");
            })
            .catch(error => {
                console.log("ERROR: ", error);
            })
        }

        renderAfterCalled.current = true;
    }, [code, navigate])

    return (
        <div>
            <h1>Waiting...</h1>
        </div>
    )
}