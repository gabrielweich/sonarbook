export const errorCode = (error: any): string | null => {
  const code: string | null = error?.response?.data?.error?.code ?? null;
  if (code !== null) return code;
  return null;
};
