import { useState } from 'react';
import { Haircut, HaircutCreate } from '../types';
import { HaircutForm } from './HaircutForm';
import { HaircutList } from './HaircutList';
import { DailyHistoryList } from './DailyHistoryList';
import { PriceEditor } from './PriceEditor';
import { ServicesList } from './ServicesList';
import { Statistics } from './Statistics';
import { ExcelImporter } from './ExcelImporter';
import { useHaircuts, useDailySummary } from '../hooks/useHaircuts';
import { haircutService } from '../services/haircutService';

export type TabType = 'sales' | 'history' | 'services' | 'import' | 'stats';

export function Dashboard() {
  const { haircuts, loading, error, addHaircut, updateHaircut, updatePrice, deleteHaircut, refetch } =
    useHaircuts();
  const { summary, history, refetch: refetchSummary } = useDailySummary();
  const [editingHaircut, setEditingHaircut] = useState<Haircut | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingPrice, setEditingPrice] = useState<string | null>(null);
  const [newPrice, setNewPrice] = useState<string>('');
  const [activeTab, setActiveTab] = useState<TabType>('sales');

  const handleCreate = () => {
    setEditingHaircut(null);
    setShowForm(true);
  };

  const handleEdit = (haircut: Haircut) => {
    setEditingHaircut(haircut);
    setShowForm(true);
  };

  const handleSubmit = async (haircutData: HaircutCreate) => {
    try {
      if (editingHaircut) {
        await updateHaircut({ ...haircutData, id: editingHaircut.id });
      } else {
        await addHaircut(haircutData);
      }
      setShowForm(false);
      setEditingHaircut(null);
      refetchSummary();
    } catch (err) {
      console.error('Error saving haircut:', err);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteHaircut(id);
      refetchSummary();
    } catch (err) {
      console.error('Error deleting haircut:', err);
    }
  };

  const handlePriceEdit = (id: string, currentPrice: number) => {
    setEditingPrice(id);
    setNewPrice(currentPrice.toString());
  };

  const handlePriceSave = async (id: string) => {
    const price = parseFloat(newPrice);
    if (isNaN(price) || price < 0) {
      return;
    }
    try {
      await updatePrice(id, price);
      setEditingPrice(null);
      setNewPrice('');
      refetchSummary();
    } catch (err) {
      console.error('Error updating price:', err);
    }
  };

  const handleCancelPriceEdit = () => {
    setEditingPrice(null);
    setNewPrice('');
  };

  const handleDeleteToday = async () => {
    if (!summary) return;
    if (!confirm(`¿Eliminar los ${summary.count} cortes de hoy?`)) {
      return;
    }
    try {
      await haircutService.deleteByDate(summary.date);
      refetchSummary();
      refetch();
    } catch (err) {
      console.error('Error deleting today\'s haircuts:', err);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingHaircut(null);
  };

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

  const avgTicket = summary?.count && summary.count > 0 
    ? summary.total / summary.count 
    : 0;

  if (loading) {
    return (
      <div className="dashboard">
        <div className="header">
          <h1>Barbershop</h1>
        </div>
        <div className="empty-state">
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="header">
        <h1>Barbershop</h1>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="summary-cards">
        <div className="summary-card today">
          <h3>Hoy</h3>
          <p className="count">{summary?.count || 0}</p>
          <p className="label">cortes</p>
        </div>
        <div className="summary-card stats">
          <h3>Recaudado</h3>
          <p className="total">{formatCurrency(summary?.total || 0)}</p>
          <p className="label">promedio: {formatCurrency(avgTicket)}</p>
        </div>
        <div className="summary-card quick">
          <h3>Acciones</h3>
          <div className="quick-actions">
            <button onClick={handleCreate} className="action-btn create">
              + Corte
            </button>
            {summary && summary.count > 0 && (
              <button onClick={handleDeleteToday} className="action-btn delete-all">
                Limpiar
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="section-card">
        <div className="section-header">
          <div className="tabs">
            <button
              className={`badge ${activeTab === 'sales' ? 'badge-success' : ''}`}
              onClick={() => setActiveTab('sales')}
            >
              Ventas
            </button>
            <button
              className={`badge ${activeTab === 'history' ? 'badge-success' : ''}`}
              onClick={() => setActiveTab('history')}
            >
              Historial
            </button>
            <button
              className={`badge ${activeTab === 'services' ? 'badge-success' : ''}`}
              onClick={() => setActiveTab('services')}
            >
              Servicios
            </button>
            <button
              className={`badge ${activeTab === 'import' ? 'badge-success' : ''}`}
              onClick={() => setActiveTab('import')}
            >
              Importar Excel
            </button>
            <button
              className={`badge ${activeTab === 'stats' ? 'badge-success' : ''}`}
              onClick={() => setActiveTab('stats')}
            >
              Estadisticas
            </button>
          </div>
          {activeTab === 'sales' && (
            <button onClick={handleCreate} className="add-btn">
              + Nuevo
            </button>
          )}
        </div>

        {showForm && (
          <div className="form-container">
            <div className="form-header">
              <h2>{editingHaircut ? 'Editar Corte' : 'Nuevo Corte'}</h2>
              <button onClick={handleCancel} className="icon-btn">✕</button>
            </div>
            <HaircutForm
              onSubmit={handleSubmit}
              initialData={editingHaircut || undefined}
              onCancel={handleCancel}
            />
          </div>
        )}

        {activeTab === 'sales' && (
          <div className="table-responsive">
            {haircuts.length === 0 ? (
              <div className="empty-state">
                <p>Sin cortes hoy</p>
                <button onClick={handleCreate} className="add-btn">
                  + Agregar
                </button>
              </div>
            ) : (
              <HaircutList
                haircuts={haircuts}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onEditPrice={handlePriceEdit}
              />
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <DailyHistoryList history={history} />
        )}

        {activeTab === 'services' && (
          <ServicesList
            haircuts={haircuts}
            onEditPrice={handlePriceEdit}
          />
        )}

        {activeTab === 'import' && (
          <ExcelImporter onImportComplete={refetchSummary} />
        )}

        {activeTab === 'stats' && (
          <Statistics haircuts={haircuts} />
        )}
      </div>

      {editingPrice && (
        <PriceEditor
          currentPrice={parseFloat(newPrice)}
          newPrice={newPrice}
          onNewPriceChange={setNewPrice}
          onSave={() => handlePriceSave(editingPrice)}
          onCancel={handleCancelPriceEdit}
        />
      )}
    </div>
  );
}
