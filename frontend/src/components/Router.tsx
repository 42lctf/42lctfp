import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Boilerplate } from "../ui/templates/Boilerplate";
import { Home } from "../ui/pages/Home";
import { Paths } from "../services/Paths";
import { AuthCallback } from "./AuthCallback";

export function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<Boilerplate />}>
                    <Route path={Paths.Home} element={<Home />} />
                    <Route path={Paths.AuthCallback} element={<AuthCallback/>} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}