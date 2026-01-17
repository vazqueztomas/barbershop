import React from 'react';
import { Haircut } from '../types';

interface HaircutListProps {
  haircuts: Haircut[];
  onEdit: (haircut: Haircut) => void;
  onDelete: (id: string) => void;
  onEditPrice: (id: string, currentPrice: number) => void;
}

export function HaircutList({ haircuts, onEdit, onDelete, onEditPrice }: HaircutListProps) {
  if (haircuts.length === 0) {
    return <p className="no-data">No hay cortes registrados.</p>;
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

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('es-AR');
  };

  return (
    <div className="haircut-list">
      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Corte</th>
            <th>Precio</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {haircuts.map((haircut) => (
            <tr key={haircut.id}>
              <td>{formatDate(haircut.date)}</td>
              <td>{haircut.name}</td>
              <td className="price-cell">
                <span className="price">{formatCurrency(haircut.price)}</span>
                <button
                  onClick={() => onEditPrice(haircut.id, haircut.price)}
                  className="price-btn"
                  title="Cambiar precio"
                >
                  ✏️
                </button>
              </td>
              <td className="actions">
                <button onClick={() => onEdit(haircut)} className="edit-btn">
                  Editar
                </button>
                <button
                  onClick={() => onDelete(haircut.id)}
                  className="delete-btn"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
