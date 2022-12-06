import { useRouter } from "next/router";
import { ArrowLeftIcon, HandThumbUpIcon } from "@heroicons/react/24/outline";
import { useEffect, useState } from "react";
import {
  getPostDetails,
  IPostDetail,
  registerActivity,
  ActivityTypesEnum,
} from "../../services/posts";

export default function PostDetail() {
  const router = useRouter();
  const { postId } = router.query;
  const [post, setPost] = useState<IPostDetail | null>(null);
  const [likeLoading, setLikeLoading] = useState(false);

  const loadPost = async () => {
    const data = await getPostDetails(postId as string);
    setPost(data);
  };

  const likePost = async () => {
    setLikeLoading(true);
    await registerActivity(postId as string, ActivityTypesEnum.like);
    await loadPost();
    setLikeLoading(false);
  };

  useEffect(() => {
    registerActivity(postId as string, ActivityTypesEnum.view);
    loadPost();
  }, []);

  return (
    <div>
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex items-center justify-between border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
          <a
            href="#"
            onClick={() => router.back()}
            className="flex justify-start items-center lg:w-0 lg:flex-1"
          >
            <ArrowLeftIcon className="w-8 text-gray-700" />
            <p className="ml-2 text-xl inline text-gray-700">Back</p>
          </a>
        </div>
      </div>
      <div className="max-w-7xl my-0 mx-auto">
        {post && (
          <div className="p-10">
            <h1 className="text-2xl font-semibold text-gray-900 text-center">
              {post.title}
            </h1>
            <img className="max-w-[80vh] mx-auto my-10" src={post.image_src} />
            <p className="text-lg">{post.description}</p>
            <p className="font-semibold text-lg text-indigo-500">
              Likes: {post.likes_count}
            </p>
            <button
              className="max-w-xs group relative w-full flex justify-center items-center py-2 px-4 text-base rounded-md text-white bg-indigo-600 hover:bg-indigo-700 mx-auto my-6 disabled:bg-gray-400"
              onClick={likePost}
              disabled={likeLoading || post.user_liked}
            >
              Like
              <span className="inset-y-0 flex items-center pl-2">
                <HandThumbUpIcon
                  className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400 group-disabled:text-white"
                  aria-hidden="true"
                />
              </span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
