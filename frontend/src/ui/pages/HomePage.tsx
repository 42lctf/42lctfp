import { useEffect, useState } from "react"
import Cookies from 'js-cookie';

export function HomePage() {
    const [nickname, setNickname] = useState("");

    useEffect(() => {
        const token = Cookies.get("refresh_token")
        if (!token) {
            return
        }
        const url = `/api/v1/users/me`;
        fetch(url, {
            method: "GET",
            headers: {
                "accept": "application/json",
                "token": token,
                credentials: 'include'
            }
        })
        .then(response => response.json())
        .then(data => {
            setNickname(data.nickname);
        })
        .catch(error => {
            console.log("ERROR: ", error);
        })
    }, [])

    return (
        <div>
            <h1>Welcome {nickname}</h1>
        </div>
    )
}