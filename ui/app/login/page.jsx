"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Styles from './page.module.css';
import TextField from '@mui/material/TextField';
import { Button } from '@mui/material';
import { call } from '../utility/api'; 

export default function Login() {
    const [creds, setCreds] = useState({ username: "", password: "" });
    const router = useRouter();

    async function validate_and_navigate() {
        let result = await call("POST", "http://localhost:8000/auth/token", {}, { username: creds.username, password: creds.password });
        if (result["statusCode"] === 200) {
            localStorage.setItem('access_token', result["data"]["access_token"]);
            router.push("/todo");
        } else {
            alert("Invalid Credentials");
        }
    }

    return (
        <div className={`${Styles.mainContainer}`}>
            <div className={`${Styles.pageContainer}`}>
                <div className={`${Styles.imageContainer}`} />
                <div className={`${Styles.loginContainer}`}>
                    <div className={`${Styles.heading}`}>Task Management Portal</div>
                    <div className={`${Styles.creds}`}>
                        <div>
                            <TextField
                                className={`${Styles.extend}`}
                                label="Email"
                                variant='outlined'
                                value={creds.username}
                                onChange={(e) => { setCreds({ ...creds, username: e.target.value }) }}
                            />
                        </div>
                        <div>
                            <TextField
                                className={`${Styles.extend}`}
                                type='password'
                                label="Password"
                                value={creds.password}
                                variant='outlined'
                                onChange={(e) => { setCreds({ ...creds, password: e.target.value }) }}
                            />
                        </div>
                        <div>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={validate_and_navigate}
                                className={`${Styles.loginButton}`}>
                                Login
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
