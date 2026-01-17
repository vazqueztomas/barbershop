import React from 'react';
import { DailyHistory } from '../types';

interface DailyHistoryProps {
  history: DailyHistory;
}

export function DailyHistoryList({ history }: DailyHistoryProps) {
  const entries = Object.entries(history).sort((a, b) => b[0].localeCompare(a[0]));

  if (entries.length === 0) {
    return <div className="history-list empty">No hay historial disponible</div>;
  }

  const formatCurrency = (amount: number) => {
    if (isNaN(amount) || amount === null || amount === undefined) {
      return '$0,00';
    }
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
    }).format(amount);
  };

  return (
    <div className="history-list">
      <h3>Historial de Ventas</h3>
      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Total (ARS)</th>
          </tr>
        </thead>
        <tbody>
          {entries.map(([date, total]) => (
            <tr key={date}>
              <td>{new Date(date).toLocaleDateString('es-AR')}</td>
              <td className="total">{formatCurrency(total)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
