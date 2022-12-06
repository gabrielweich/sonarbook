import axios from "axios";
import { parseCookies, setCookie } from "nookies";
import { refreshAccessToken } from "./users";
import jwt_decode from "jwt-decode";

export function getAPIClient(ctx?: any) {
  const baseClientParams = {
    baseURL: process.env.NEXT_PUBLIC_API_URL,
  };
  const api = axios.create(baseClientParams);
  const authApi = axios.create(baseClientParams);

  api.interceptors.request.use(async (config) => {
    let { "sonarauth.accesstoken": accessToken } = parseCookies(ctx);
    const { "sonarauth.refreshtoken": refreshToken } = parseCookies(ctx);

    if (!accessToken) return config;

    const decodedAccessToken: { exp: number } = jwt_decode(accessToken);
    const expirationDate = new Date(decodedAccessToken.exp * 1000);
    const now = new Date();

    if (expirationDate <= now) {
      accessToken = await refreshAccessToken(refreshToken);
      api.defaults.headers["Authorization"] = `Bearer ${accessToken}`;
      setCookie(ctx, "sonarauth.accesstoken", accessToken);
    }

    config = {
      ...config,
      headers: {
        ...config.headers,
        Authorization: `Bearer ${accessToken}`,
      },
    };

    return config;
  });

  api.interceptors.response.use(
    (response) => {
      return response;
    },
    async function (error) {
      const originalRequest = error.config;
      const { "sonarauth.refreshtoken": refreshToken } = parseCookies(ctx);

      if (
        error.response?.status === 401 &&
        refreshToken &&
        !originalRequest._retry
      ) {
        originalRequest._retry = true;

        const accessToken = await refreshAccessToken(refreshToken);
        api.defaults.headers["Authorization"] = `Bearer ${accessToken}`;
        setCookie(ctx, "sonarauth.accesstoken", accessToken);

        return api(originalRequest);
      }
      return Promise.reject(error);
    }
  );

  return { api, authApi };
}
