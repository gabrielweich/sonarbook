import { useContext, useEffect, useState } from "react";
import Head from "next/head";

import { AuthContext } from "../contexts/AuthContext";
import { getPosts, IPost } from "../services/posts";
import Link from "next/link";
import { useRouter } from "next/router";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "@components/post";
import Header from "@components/header";

export default function Dashboard() {
  const { user, isAuthenticated } = useContext(AuthContext);
  const router = useRouter();

  const [posts, setPosts] = useState<IPost[]>([]);
  const [hasMore, setHasMore] = useState(true);
  const [nextPage, setNextPage] = useState(1);

  const fetchPosts = async () => {
    const result = await getPosts({ page: nextPage });
    setPosts([...posts, ...result.items]);
    setHasMore(result.current_page < result.total_pages);
    setNextPage(result.current_page + 1);
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const onClickPost = (postId: string) => {
    if (user) router.push(`/posts/${postId}`);
    else router.push("/login");
  };

  return (
    <div className="relative bg-white">
      <Head>
        <title>Home</title>
      </Head>
      <Header />
      <InfiniteScroll
        dataLength={posts.length}
        next={fetchPosts}
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
      >
        <div className="flex flex-col items-center">
          {posts.map((post) => (
            <div className="p-12" key={post.id}>
              <Post
                onClick={() => onClickPost(post.id)}
                title={post.title}
                imageSrc={post.image_src}
              />
            </div>
          ))}
        </div>
      </InfiniteScroll>
    </div>
  );
}
