import { useEffect, useState } from "react"
import Cookies from 'js-cookie';

export function HomePage() {
    let [nickname, setNickname] = useState("");

    useEffect(() => {
        const token = Cookies.get("access_token")
        const url = `http://localhost:8004/users/me?token=${encodeURIComponent(token)}`;
        fetch(url, {
            method: "GET",
            headers: {
                "accept": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
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