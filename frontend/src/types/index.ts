export interface Haircut {
  id: string;
  name: string;
  price: number;
  date: string;
}

export interface HaircutCreate {
  name: string;
  price: number;
  date: string;
}

export interface DailySummary {
  date: string;
  count: number;
  total: number;
}

export interface DailyHistory {
  [date: string]: number;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
}

export interface ErrorResponse {
  detail: string;
}
