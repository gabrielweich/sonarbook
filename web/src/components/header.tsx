import React, { FC, useContext } from "react";
import Link from "next/link";
import { destroyCookie } from "nookies";
import { AuthContext } from "../contexts/AuthContext";
import { useRouter } from "next/router";

type Props = {};

const Header: FC<Props> = () => {
  const { isAuthenticated } = useContext(AuthContext);
  const router = useRouter();

  const onLogout = () => {
    destroyCookie(null, "sonarauth.accesstoken");
    destroyCookie(null, "sonarauth.refreshtoken");
    router.push("/login");
  };

  const authMenus = () => {
    if (isAuthenticated)
      return (
        <button
          onClick={onLogout}
          className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900"
        >
          Sign out
        </button>
      );
    return (
      <>
        <Link
          href="/login"
          className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900"
        >
          Sign in
        </Link>
        <Link
          href="/register"
          className="ml-8 inline-flex items-center justify-center whitespace-nowrap rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-indigo-700"
        >
          Sign up
        </Link>
      </>
    );
  };

  const MenuLink = ({
    children,
    href,
  }: {
    children: React.ReactNode;
    href: string;
  }) => {
    const activeClassName = router.pathname == href ? "text-gray-800" : "";
    return (
      <Link
        href={href}
        className={`text-base font-medium text-gray-500 hover:text-gray-800 ${activeClassName}`}
      >
        {children}
      </Link>
    );
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6">
      <div className="flex items-center justify-between border-b-2 border-gray-100 py-6 relative">
        <div className="flex justify-start lg:w-0">
          <a className="flex items-center" href="#">
            <img
              className="h-8 w-auto sm:h-10"
              src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
            />
            <h1 className="ml-2 text-lg">Sonarbook</h1>
          </a>
        </div>

        <nav className="left-[50%] top-[50%] absolute -translate-y-[50%] -translate-x-[50%] flex space-x-6">
          <MenuLink href="/">Home</MenuLink>
          <MenuLink href="/dashboard">Dashboard</MenuLink>
        </nav>

        <div className="items-center justify-end flex lg:w-0">
          {authMenus()}
        </div>
      </div>
    </div>
  );
};

export default Header;
