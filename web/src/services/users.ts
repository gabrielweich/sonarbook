import { api, authApi } from "./api";

interface SignInRequestData {
  username: string;
  password: string;
}

interface RegisterRequestData {
  username: string;
  password: string;
}

export interface IUserStats {
  count: number;
}

export async function signInRequest(data: SignInRequestData) {
  const form = new FormData();
  form.append("username", data.username);
  form.append("password", data.password);

  const response = await authApi.post("/api/users/token", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return {
    accessToken: response.data["access_token"],
    refreshToken: response.data["refresh_token"],
  };
}

export async function registerRequest(data: RegisterRequestData) {
  const response = await authApi.post("/api/users", data);
  return response;
}

export async function refreshAccessToken(refreshToken: string) {
  const form = new FormData();
  form.append("refresh_token", refreshToken);
  const response = await authApi.post("/api/users/refresh", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data["access_token"];
}

export async function recoverUserInformation() {
  const response = await api.get("/api/users/me");

  return {
    id: response.data["id"],
    username: response.data["username"],
  };
}

export async function getUsersStats(): Promise<IUserStats> {
  const response = await api.get("/api/users/stats");

  return {
    count: response.data["count"],
  };
}
