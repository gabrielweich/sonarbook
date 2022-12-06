import { FC } from "react";

type Props = {
  title: string;
  imageSrc: string;
  onClick: () => void;
};

const Post: FC<Props> = ({ title, imageSrc, onClick }) => {
  return (
    <div className="max-w-sm overflow-hidden rounded-xl bg-white shadow-md duration-200 hover:scale-105 hover:shadow-xl">
      <img src={imageSrc} alt={title} className="h-auto w-full" />
      <div className="p-5">
        <p className="text-xl font-semibold mb-5 text-gray-700">{title}</p>
        <button
          onClick={onClick}
          className="w-full rounded-md bg-indigo-600  py-2 text-indigo-100 hover:bg-indigo-500 hover:shadow-md duration-75"
        >
          See More
        </button>
      </div>
    </div>
  );
};

export default Post;
