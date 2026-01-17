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
      return '$0';
    }
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatTime = (dateStr: string) => {
    return new Date(dateStr).toLocaleTimeString('es-AR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="table-responsive">
      <table className="data-table">
        <thead>
          <tr>
            <th>Hora</th>
            <th>Servicio</th>
            <th>Precio</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {haircuts.map((haircut) => (
            <tr key={haircut.id}>
              <td>{formatTime(haircut.date)}</td>
              <td>
                <span className="badge">{haircut.name}</span>
              </td>
              <td className="price">{formatCurrency(haircut.price)}</td>
              <td className="actions">
                <button
                  onClick={() => onEditPrice(haircut.id, haircut.price)}
                  className="icon-btn"
                  title="Cambiar precio"
                >
                  ✏️
                </button>
                <button onClick={() => onEdit(haircut)} className="edit-btn">
                  Editar
                </button>
                <button
                  onClick={() => onDelete(haircut.id)}
                  className="delete-btn"
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
