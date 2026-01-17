import { DailyHistory } from '../types';

interface DailyHistoryProps {
  history: DailyHistory;
}

export function DailyHistoryList({ history }: DailyHistoryProps) {
  const entries = Object.entries(history).sort((a, b) => b[0].localeCompare(a[0]));

  if (entries.length === 0) {
    return <div className="no-data">Sin historial aún</div>;
  }

  const formatCurrency = (amount: number) => {
    if (isNaN(amount) || amount === null || amount === undefined) {
      return '$0';
    }
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Hoy';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Ayer';
    }
    return date.toLocaleDateString('es-AR', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
    });
  };

  return (
    <div className="table-responsive">
      <table className="data-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {entries.map(([date, total]) => (
            <tr key={date}>
              <td>{formatDate(date)}</td>
              <td className="price">{formatCurrency(total)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
