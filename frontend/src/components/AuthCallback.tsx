import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function AuthCallback() {
    let code = window.location.href.split("code=")[1];

    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://localhost:8004/users/auth/callback?code="+code, {
            method: "GET",
            headers: {
                "accept": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            document.cookie = "token="+data.access_token;
            navigate("/");
        })
        .catch(error => {
            console.log("ERROR: ", error);
        })
    }, [])

    return (
        <div>
            <h1>Waiting...</h1>
        </div>
    )
}