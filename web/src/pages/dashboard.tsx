import Head from "next/head";
import Header from "@components/header";
import { useEffect, useState } from "react";
import { getPosts, IPost } from "../services/posts";
import { getUsersStats, IUserStats } from "../services/users";
import { EyeIcon, HandThumbUpIcon } from "@heroicons/react/24/outline";

export default function Dashboard() {
  const [topLikesPost, setTopLikesPost] = useState<IPost[]>([]);
  const [topViewsPost, setTopViewsPost] = useState<IPost[]>([]);
  const [userStats, setUserStats] = useState<IUserStats>();

  const postsToLoad = 5;

  const fetchTopLikePosts = async () => {
    const result = await getPosts({
      page: 1,
      page_size: postsToLoad,
      order: "desc",
      order_by: "likes_count",
    });
    setTopLikesPost(result.items);
  };

  const fetchTopViewsPosts = async () => {
    const result = await getPosts({
      page: 1,
      page_size: postsToLoad,
      order: "desc",
      order_by: "views_count",
    });
    setTopViewsPost(result.items);
  };

  const fetchUsersStats = async () => {
    const result = await getUsersStats();
    setUserStats(result);
  };

  useEffect(() => {
    fetchTopLikePosts();
    fetchTopViewsPosts();
    fetchUsersStats();
  }, []);

  const Post = ({ image_src, likes_count, views_count, title }: IPost) => (
    <div className="w-40 max-w-sm overflow-hidden rounded-xl shadow-md mr-6 mb-6 relative">
      <img className="h-20 w-full object-cover" src={image_src} />
      <h1 className="text-base p-2 text-gray-900">{title}</h1>
      <div className="h-10">
        <div className="flex absolute bottom-0 justify-between w-full left-0 p-2 items-center">
          <div className="inline-flex items-center">
            <EyeIcon className="h-4 text-gray-500 mr-2" />
            <p>{views_count}</p>
          </div>
          <div className="inline-flex items-center">
            <HandThumbUpIcon className="h-4 text-gray-500 mr-2" />
            <p>{likes_count}</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div>
      <Head>
        <title>Dashboard</title>
      </Head>
      <Header />
      <div className="p-6">
        <h1 className="text-xl my-8">
          Registered users:{" "}
          <span className="font-semibold">{userStats?.count ?? ""}</span>
        </h1>
        <h1 className="text-xl my-8">Top views posts</h1>
        <div className="flex flex-wrap">
          {topViewsPost.map((post) => (
            <Post {...post} key={post.id} />
          ))}
        </div>
        <h1 className="text-xl my-8">Top likes posts</h1>
        <div className="flex flex-wrap">
          {topLikesPost.map((post) => (
            <Post {...post} key={post.id} />
          ))}
        </div>
      </div>
    </div>
  );
}
