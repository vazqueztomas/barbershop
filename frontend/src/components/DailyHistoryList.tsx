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
              <td className="total">${total.toLocaleString('es-AR', { minimumFractionDigits: 2 })}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
