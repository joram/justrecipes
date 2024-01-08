import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import {jwtDecode} from "jwt-decode";
import {setJWT} from "../utils/api";

function SignIn() {
    // This function will be called upon a successful login
    const handleSuccess = (credentialResponse) => {
        const jwt = jwtDecode(credentialResponse.credential)
        setJWT(credentialResponse.credential)
    };

    const handleError = (errorResponse) => {
        console.error('Google login failed', errorResponse);
    };

    return (
        <div>
            <GoogleLogin
                onSuccess={handleSuccess}
                onError={handleError}
                useOneTap
                flow="auth-code"
            />
        </div>
    );
}

export default SignIn;