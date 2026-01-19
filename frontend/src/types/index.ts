export interface Haircut {
  id: string;
  clientName: string;
  serviceName: string;
  price: number;
  date: string;
  time?: string;
}

export interface HaircutCreate {
  clientName: string;
  serviceName: string;
  price: number;
  date: string;
  time?: string;
}

export interface DailySummary {
  date: string;
  count: number;
  total: number;
}

export interface DailyHistoryItem {
  date: string;
  total: number;
  count: number;
  clients: string[];
}

export type DailyHistory = DailyHistoryItem[];

export interface ApiResponse<T> {
  data: T;
  status: number;
}

export interface ErrorResponse {
  detail: string;
}

export interface DateRange {
  startDate: string;
  endDate: string;
  label: string;
}

export interface SearchSuggestion {
  text: string;
  dateRange: DateRange;
  description: string;
}

export interface DateSearchResult {
  data: DailyHistory;
  dateRange: DateRange;
  totalCount: number;
  totalAmount: number;
}
