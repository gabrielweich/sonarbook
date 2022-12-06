export type PaginateRequest = {
  page?: number;
  page_size?: number;
  order_by?: string;
  order?: "asc" | "desc";
};

export type PaginateResponse<T> = {
  total_items: number;
  total_pages: number;
  current_page: number;
  items: T[];
};
