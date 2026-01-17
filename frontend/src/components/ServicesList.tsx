import { Haircut } from '../types';

interface ServicesListProps {
  haircuts: Haircut[];
  onEditPrice: (id: string, currentPrice: number) => void;
}

export function ServicesList({ haircuts, onEditPrice }: ServicesListProps) {
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

  const servicesMap = haircuts.reduce((acc, haircut) => {
    const existing = acc.find(s => s.name.toLowerCase() === haircut.name.toLowerCase());
    if (existing) {
      existing.count += 1;
    } else {
      acc.push({ ...haircut, count: 1 });
    }
    return acc;
  }, [] as (Haircut & { count: number })[]);

  const uniqueServices = servicesMap;

  if (uniqueServices.length === 0) {
    return <div className="no-data">No hay servicios registrados</div>;
  }

  return (
    <div className="table-responsive">
      <table className="data-table">
        <thead>
          <tr>
            <th>Servicio</th>
            <th>Precio</th>
            <th>Hoy</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {uniqueServices.map((service) => (
            <tr key={service.id}>
              <td>
                <span className="badge">{service.name}</span>
              </td>
              <td className="price">{formatCurrency(service.price)}</td>
              <td>{service.count}</td>
              <td className="actions">
                <button
                  onClick={() => onEditPrice(service.id, service.price)}
                  className="edit-btn"
                >
                  ✏️
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
