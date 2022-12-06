import React, { createContext, useEffect, useState } from "react";
import { setCookie, parseCookies } from "nookies";
import Router from "next/router";

import { recoverUserInformation, signInRequest } from "../services/users";
import { api } from "../services/api";

type User = {
  username: string;
};

type SignInData = {
  username: string;
  password: string;
};

type AuthContextType = {
  isAuthenticated: boolean;
  user: User | null;
  signIn: (data: SignInData) => Promise<void>;
};

export const AuthContext = createContext({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const isAuthenticated = !!user;

  useEffect(() => {
    const { "sonarauth.accesstoken": token } = parseCookies();

    if (token) {
      recoverUserInformation().then((response) => {
        setUser(response);
      });
    }
  }, []);

  async function signIn({ username, password }: SignInData) {
    const { refreshToken, accessToken } = await signInRequest({
      username,
      password,
    });

    setCookie(null, "sonarauth.refreshtoken", refreshToken);
    setCookie(null, "sonarauth.accesstoken", accessToken);

    api.defaults.headers["Authorization"] = `Bearer ${accessToken}`;

    setUser({ username });

    Router.push("/");
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, signIn }}>
      {children}
    </AuthContext.Provider>
  );
}
