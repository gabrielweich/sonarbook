import { api } from "./api";
import { PaginateRequest, PaginateResponse } from "./types";

export interface IPost {
  id: string;
  title: string;
  image_src: string;
  likes_count: number;
  views_count: number;
}

export interface IPostDetail extends IPost {
  user_liked: boolean;
  description: string;
}

export enum ActivityTypesEnum {
  like = "like",
  view = "view",
}

export async function getPosts(
  params: PaginateRequest
): Promise<PaginateResponse<IPost>> {
  const res = await api.get("/api/posts", { params });
  return res.data;
}

export async function getPostDetails(postId: string): Promise<IPostDetail> {
  const res = await api.get(`/api/posts/${postId}`);
  return res.data;
}

export async function registerActivity(
  postId: string,
  activityType: ActivityTypesEnum
) {
  const data = {
    post_id: postId,
    interaction_type: activityType,
  };
  const res = await api.post("/api/activity-logs", data);
  return res.data;
}
